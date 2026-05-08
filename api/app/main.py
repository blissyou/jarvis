"""FastAPI entrypoint for the JARVIS Voice Layer MVP adapter.

The latest architecture makes OpenClaw the agent/runtime owner. This API remains
as a thin local adapter for STT, TTS, HUD telemetry, and compatibility while the
Electron shell migrates toward OpenClaw Gateway as the execution substrate.
"""

import threading

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.app.persistence.db import init_db
from api.app.routers import approvals, budgets, health, runtime, sessions, tools, voice
from api.app.services.model_router import router as model_router

app = FastAPI(title="JARVIS Voice Layer API", version="0.2.0")
init_db()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(sessions.router)
app.include_router(tools.router)
app.include_router(approvals.router)
app.include_router(budgets.router)
app.include_router(runtime.router)
app.include_router(voice.router)


def _warm_runtime() -> None:
    voice.preload_stt_model()
    model_router.warmup()


@app.on_event("startup")
def warm_runtime() -> None:
    threading.Thread(target=_warm_runtime, daemon=True).start()
