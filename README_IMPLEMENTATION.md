# JARVIS MVP Scaffold

This repository contains the first implementation scaffold for the Obsidian architecture:

- `api/`: FastAPI orchestration backend
- `agent/`: model provider boundary placeholders
- `mcp/`: first-party tool registry and tools
- `desktop/`: Electron/React minimal voice-first UI scaffold
- `runtime/`: local logs, artifacts, sessions, and SQLite database

## Backend dev

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r api\requirements.txt
uvicorn api.app.main:app --reload
```

Open `http://127.0.0.1:8000/docs`.

## Frontend dev

```powershell
cd desktop
npm install
npm run dev
```

Open `http://127.0.0.1:5173`.

## Desktop app

Run the Electron desktop shell:

```powershell
.\scripts\start_desktop.ps1
```

Or manage the whole local runtime with one script:

```powershell
.\scripts\jarvis.ps1 start
.\scripts\jarvis.ps1 status
.\scripts\jarvis.ps1 restart
.\scripts\jarvis.ps1 stop
```

This starts or stops Ollama, the FastAPI backend, the Vite UI server, and the Electron desktop app. Logs and PID files are written under `runtime\logs` and `runtime\pids`.

For frontend-only development:

```powershell
cd desktop
npm run dev:electron
```

The desktop shell requests microphone permission for push-to-talk input. Spoken output uses the operating system/browser speech synthesis engine and can be toggled from `Voice output` in the session panel.

Current voice behavior:

- Chat automatically scrolls to the latest message.
- Chat opens in a separate popup so the main JARVIS shell does not scroll.
- `MIC` records audio through Electron, uploads it to `POST /voice/transcribe`, then submits the returned transcript as the user prompt.
- Local STT uses `faster-whisper`; the default speed profile uses `base` with CPU `int8`.
- Assistant replies are spoken through the streaming `GET /voice/speak/stream` endpoint when `Voice output` is on.
- Neural TTS uses `edge-tts` with `ko-KR-HyunsuNeural`, `-4%` rate, and `-6Hz` pitch by default.
- If streaming neural TTS fails, the desktop app falls back to the operating system `speechSynthesis` voice.

Current speed profile:

- Common Korean voice turns use an instant local intent path, then short unmatched turns route to `qwen2.5:1.5b`.
- Complex Korean analysis/debug/design turns route to `qwen3:8b`.
- Qwen thinking output is disabled for voice turns.

## Local model providers

JARVIS is configured for dual local routing:

- Ollama: fast local turns with `llama3.2`, reasoning turns with `qwen3:8b` by default
- LM Studio compatible API: optional complex reasoning provider when the local server is running
- local_echo: fallback when both local APIs are unavailable

Copy `.env.example` to `.env` and adjust:

```powershell
JARVIS_PROVIDER_MODE=local_dual
JARVIS_FAST_PROVIDER=ollama
JARVIS_REASONING_PROVIDER=ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.2
OLLAMA_FAST_MODEL=llama3.2
OLLAMA_REASONING_MODEL=qwen3:8b
JARVIS_STT_MODEL=tiny
LMSTUDIO_BASE_URL=http://localhost:1234
LMSTUDIO_MODEL=local-model
```

### Ollama

1. Start Ollama.
2. Pull the default models: `ollama pull llama3.2` and `ollama pull qwen3:8b`.
3. Confirm `http://localhost:11434/api/tags` responds.

### LM Studio

1. Open LM Studio.
2. Load a local model.
3. Start the local server with an OpenAI-compatible API.
4. Confirm `http://localhost:1234/v1/models` responds.
5. Set `LMSTUDIO_MODEL` to the loaded model ID if needed.

## Smoke test

```powershell
python scripts\smoke_api.py
```

## Useful endpoints

- UI: `http://127.0.0.1:5173`
- API docs: `http://127.0.0.1:8000/docs`
- API health: `http://127.0.0.1:8000/health`
- Model health: `http://127.0.0.1:8000/models/health`
- Runtime status: `http://127.0.0.1:8000/runtime/status`

## Runtime shutdown

Use the runtime script for local start/stop/status:

```powershell
.\scripts\jarvis.ps1 start
.\scripts\jarvis.ps1 stop
```

The development UI also includes a `RUNTIME CONTROL` section for local shutdown:

- `OLLAMA`: stops the Ollama Windows processes.
- `UI`: stops the Vite frontend dev server on port `5173`.
- `API`: schedules the FastAPI backend process to exit after the response.

The runtime control API only accepts localhost requests. Use it for development shutdown only, not as a production process manager.

