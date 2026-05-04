# Setup and Deployment
#setup #deployment #docker #desktop #local-first

## Purpose
Define the development and local deployment shape for JARVIS so implementation can start from a reproducible baseline.

## Development Components
| Component | Command Shape |
|---|---|
| FastAPI API | `uvicorn api.app.main:app --reload` |
| Electron desktop | `npm run dev` from `desktop/` |
| Local model provider | LM Studio or Ollama running locally |
| SQLite database | local file under `runtime/` |
| Docker sandbox | Docker Desktop or Docker Engine |
| Optional Redis | Docker compose service |

## Environment Variables
| Variable | Purpose |
|---|---|
| `JARVIS_DATA_DIR` | Runtime database, logs, artifacts |
| `JARVIS_WORKSPACE_ROOT` | Default approved workspace |
| `JARVIS_PROVIDER_MODE` | `local_strict`, `balanced`, `hybrid` |
| `OPENAI_API_KEY` | Optional cloud fallback |
| `OLLAMA_BASE_URL` | Local Ollama endpoint |
| `LMSTUDIO_BASE_URL` | Local LM Studio endpoint |
| `JARVIS_BUDGET_MONTHLY_KRW` | Monthly budget guardrail |

## Local Directory Layout
```text
runtime/
  logs/
  artifacts/
  sessions/
  db/
  cache/
```

## MVP Startup Order
1. Start local model provider.
2. Start FastAPI backend.
3. Run database migrations.
4. Start Electron UI.
5. Verify model router health.
6. Verify tool registry load.
7. Verify sandbox profile availability.

## Health Checks
| Check | Expected |
|---|---|
| `/health` | API is running |
| `/models/health` | At least one local provider available |
| `/tools` | First-party tools registered |
| `/budgets/current` | Budget counters initialized |
| Sandbox smoke test | Can run read-only command in isolated profile |

## Packaging Rule
For packaged desktop builds, secrets and writable runtime files must live outside the app installation directory. The app bundle should be replaceable without deleting user data.

## Interaction Points
- Project structure: [[Project_Structure]]
- Persistence: [[Persistence_and_Data_Model]]
- Windows policy: [[Windows_Host_Policy]]
- Docker isolation: [[Docker_Isolation_Strategy]]
