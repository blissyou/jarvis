from __future__ import annotations

import os
import tempfile
from functools import lru_cache
from pathlib import Path

from starlette.background import BackgroundTask
from fastapi import APIRouter, File, HTTPException, Query, UploadFile
from fastapi.responses import FileResponse, StreamingResponse
from pydantic import BaseModel

router = APIRouter(prefix="/voice", tags=["voice"])


class TranscriptionOut(BaseModel):
    text: str
    language: str | None = None
    duration_seconds: float | None = None


class TtsRequest(BaseModel):
    text: str
    voice: str | None = None
    rate: str | None = None
    pitch: str | None = None


def _tts_settings(payload: TtsRequest | None = None) -> tuple[str, str, str]:
    return (
        payload.voice if payload and payload.voice else os.getenv("JARVIS_TTS_VOICE", "ko-KR-HyunsuNeural"),
        payload.rate if payload and payload.rate else os.getenv("JARVIS_TTS_RATE", "-4%"),
        payload.pitch if payload and payload.pitch else os.getenv("JARVIS_TTS_PITCH", "-6Hz"),
    )


def _ensure_edge_tts():
    provider = os.getenv("JARVIS_TTS_PROVIDER", "edge")
    if provider != "edge":
        raise HTTPException(status_code=503, detail=f"Unsupported TTS provider: {provider}")
    try:
        import edge_tts
    except ImportError as exc:  # pragma: no cover - dependency diagnostic
        raise HTTPException(status_code=503, detail="edge-tts is not installed. Run pip install -r api/requirements.txt.") from exc
    return edge_tts


@lru_cache(maxsize=1)
def _load_model():
    try:
        from faster_whisper import WhisperModel
    except ImportError as exc:  # pragma: no cover - dependency diagnostic
        raise RuntimeError("faster-whisper is not installed. Run pip install -r api/requirements.txt.") from exc

    model_name = os.getenv("JARVIS_STT_MODEL", "tiny")
    device = os.getenv("JARVIS_STT_DEVICE", "cpu")
    compute_type = os.getenv("JARVIS_STT_COMPUTE_TYPE", "int8")
    return WhisperModel(model_name, device=device, compute_type=compute_type)


def preload_stt_model() -> None:
    try:
        _load_model()
    except Exception:
        return


@router.get("/stt/health")
def stt_health() -> dict[str, object]:
    return {
        "status": "configured",
        "provider": "faster-whisper",
        "model": os.getenv("JARVIS_STT_MODEL", "tiny"),
        "device": os.getenv("JARVIS_STT_DEVICE", "cpu"),
        "compute_type": os.getenv("JARVIS_STT_COMPUTE_TYPE", "int8"),
    }


@router.get("/tts/health")
def tts_health() -> dict[str, object]:
    return {
        "status": "configured",
        "provider": os.getenv("JARVIS_TTS_PROVIDER", "edge"),
        "voice": os.getenv("JARVIS_TTS_VOICE", "ko-KR-HyunsuNeural"),
        "rate": os.getenv("JARVIS_TTS_RATE", "-4%"),
        "pitch": os.getenv("JARVIS_TTS_PITCH", "-6Hz"),
    }


@router.post("/transcribe", response_model=TranscriptionOut)
async def transcribe(audio: UploadFile = File(...)) -> TranscriptionOut:
    suffix = Path(audio.filename or "audio.webm").suffix or ".webm"
    data = await audio.read()
    if not data:
        raise HTTPException(status_code=400, detail="Empty audio upload.")

    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp:
        temp.write(data)
        temp_path = temp.name

    try:
        model = _load_model()
        segments, info = model.transcribe(
            temp_path,
            language="ko",
            vad_filter=True,
            beam_size=1,
            best_of=1,
            temperature=0.0,
        )
        text = " ".join(segment.text.strip() for segment in segments).strip()
        return TranscriptionOut(
            text=text,
            language=getattr(info, "language", None),
            duration_seconds=getattr(info, "duration", None),
        )
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    finally:
        Path(temp_path).unlink(missing_ok=True)


@router.post("/speak")
async def speak(payload: TtsRequest) -> FileResponse:
    text = payload.text.strip()
    if not text:
        raise HTTPException(status_code=400, detail="Text is required.")

    edge_tts = _ensure_edge_tts()
    voice, rate, pitch = _tts_settings(payload)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp:
        temp_path = temp.name

    try:
        communicate = edge_tts.Communicate(text, voice=voice, rate=rate, pitch=pitch)
        await communicate.save(temp_path)
    except Exception as exc:  # noqa: BLE001
        Path(temp_path).unlink(missing_ok=True)
        raise HTTPException(status_code=503, detail=f"TTS generation failed: {exc}") from exc

    return FileResponse(
        temp_path,
        media_type="audio/mpeg",
        filename="jarvis-response.mp3",
        background=BackgroundTask(lambda: Path(temp_path).unlink(missing_ok=True)),
    )


@router.get("/speak/stream")
async def speak_stream(
    text: str = Query(..., min_length=1),
    voice: str | None = None,
    rate: str | None = None,
    pitch: str | None = None,
) -> StreamingResponse:
    clean_text = text.strip()
    if not clean_text:
        raise HTTPException(status_code=400, detail="Text is required.")

    edge_tts = _ensure_edge_tts()
    payload = TtsRequest(text=clean_text, voice=voice, rate=rate, pitch=pitch)
    selected_voice, selected_rate, selected_pitch = _tts_settings(payload)

    async def audio_chunks():
        communicate = edge_tts.Communicate(
            clean_text,
            voice=selected_voice,
            rate=selected_rate,
            pitch=selected_pitch,
        )
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                yield chunk["data"]

    return StreamingResponse(audio_chunks(), media_type="audio/mpeg")
