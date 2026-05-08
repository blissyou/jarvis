from __future__ import annotations

import asyncio
import os
import tempfile
from pathlib import Path

import edge_tts
from faster_whisper import WhisperModel

PHRASE = "자비스 음성 레이어 테스트입니다. 주식 브리핑은 가능하지만 매매는 실행하지 않습니다."
REQUIRED_KEYWORDS = ("자비스", "음성", "레이어", "테스트", "주식", "브리핑", "매매")


async def synthesize(path: Path) -> None:
    voice = os.getenv("JARVIS_TTS_VOICE", "ko-KR-HyunsuNeural")
    rate = os.getenv("JARVIS_TTS_RATE", "-4%")
    pitch = os.getenv("JARVIS_TTS_PITCH", "-6Hz")
    communicate = edge_tts.Communicate(PHRASE, voice=voice, rate=rate, pitch=pitch)
    await communicate.save(str(path))


def transcribe(path: Path) -> str:
    model_name = os.getenv("JARVIS_STT_MODEL", "base")
    device = os.getenv("JARVIS_STT_DEVICE", "cpu")
    compute_type = os.getenv("JARVIS_STT_COMPUTE_TYPE", "int8")
    model = WhisperModel(model_name, device=device, compute_type=compute_type)
    segments, info = model.transcribe(
        str(path),
        language="ko",
        vad_filter=False,
        beam_size=5,
        best_of=5,
        temperature=0.0,
    )
    text = " ".join(segment.text.strip() for segment in segments).strip()
    print(f"language={getattr(info, 'language', None)} duration={getattr(info, 'duration', None)}")
    return text


async def main() -> None:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp:
        audio_path = Path(temp.name)

    try:
        await synthesize(audio_path)
        print(f"tts_file={audio_path} bytes={audio_path.stat().st_size}")
        text = transcribe(audio_path)
        print(f"expected={PHRASE}")
        print(f"transcribed={text}")
        missing = [word for word in REQUIRED_KEYWORDS if word not in text]
        if missing:
            raise SystemExit(f"voice loopback failed; missing keywords: {missing}")
        print("voice loopback check passed")
    finally:
        audio_path.unlink(missing_ok=True)


if __name__ == "__main__":
    asyncio.run(main())
