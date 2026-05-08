from __future__ import annotations

import os
import shutil
import socket
import subprocess
import threading
from typing import Iterable

from fastapi import APIRouter, HTTPException, Request

from api.app.schemas.contracts import (
    RuntimeServiceStatus,
    RuntimeShutdownOut,
    RuntimeShutdownRequest,
    RuntimeShutdownResult,
    RuntimeStatusOut,
)

router = APIRouter(prefix="/runtime", tags=["runtime"])


LOCAL_HOSTS = {"127.0.0.1", "::1", "localhost"}


def _ensure_local_request(request: Request) -> None:
    host = request.client.host if request.client else None
    if host not in LOCAL_HOSTS:
        raise HTTPException(status_code=403, detail="Runtime control is only available from localhost.")


def _run(command: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, capture_output=True, text=True, timeout=10, check=False)


def _port_open(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(0.35)
        return sock.connect_ex(("127.0.0.1", port)) == 0


def _powershell(script: str) -> subprocess.CompletedProcess[str]:
    return _run(["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", script])


def _pids_on_port(port: int) -> list[int]:
    result = _powershell(
        "$pids = Get-NetTCPConnection "
        f"-LocalPort {port} -State Listen -ErrorAction SilentlyContinue "
        "| Select-Object -ExpandProperty OwningProcess -Unique; "
        "$pids -join ','"
    )
    if result.returncode != 0 or not result.stdout.strip():
        return []
    pids: list[int] = []
    for item in result.stdout.strip().split(","):
        try:
            pids.append(int(item.strip()))
        except ValueError:
            continue
    return pids


def _stop_pids(pids: Iterable[int]) -> tuple[bool, str]:
    pid_list = [pid for pid in pids if pid > 0 and pid != os.getpid()]
    if not pid_list:
        return False, "No matching process was found."
    script = "; ".join(f"Stop-Process -Id {pid} -Force -ErrorAction Stop" for pid in pid_list)
    result = _powershell(script)
    if result.returncode == 0:
        return True, f"Stopped process id(s): {', '.join(str(pid) for pid in pid_list)}."
    return False, (result.stderr or result.stdout or "Failed to stop process.").strip()


def _process_running(image_name: str) -> bool:
    if os.name == "nt":
        result = _run(["tasklist", "/FI", f"IMAGENAME eq {image_name}"])
        return image_name.lower() in result.stdout.lower()
    result = _run(["pgrep", "-if", image_name])
    return result.returncode == 0 and bool(result.stdout.strip())


def _openclaw_status() -> RuntimeServiceStatus:
    configured_url = os.getenv("OPENCLAW_GATEWAY_URL")
    if configured_url:
        return RuntimeServiceStatus(
            name="openclaw",
            running=True,
            detail=f"Configured OpenClaw Gateway URL: {configured_url}.",
        )

    if shutil.which("openclaw"):
        result = _run(["openclaw", "gateway", "status"])
        running = result.returncode == 0 and "running" in (result.stdout + result.stderr).lower()
        detail = (result.stdout or result.stderr or "openclaw CLI found.").strip().splitlines()
        return RuntimeServiceStatus(
            name="openclaw",
            running=running,
            detail=detail[0] if detail else "OpenClaw CLI found.",
        )

    return RuntimeServiceStatus(
        name="openclaw",
        running=False,
        detail="Set OPENCLAW_GATEWAY_URL or install the openclaw CLI to report Gateway status.",
    )


def _stop_image(image_name: str) -> RuntimeShutdownResult:
    if not _process_running(image_name):
        return RuntimeShutdownResult(target=image_name, status="not_running", detail=f"{image_name} is not running.")
    if os.name == "nt":
        result = _run(["taskkill", "/IM", image_name, "/F"])
    else:
        result = _run(["pkill", "-if", image_name])
    if result.returncode == 0:
        return RuntimeShutdownResult(target=image_name, status="stopped", detail=(result.stdout or f"Stopped {image_name}.").strip())
    return RuntimeShutdownResult(target=image_name, status="failed", detail=(result.stderr or result.stdout).strip())


def _schedule_api_shutdown() -> None:
    def shutdown() -> None:
        os._exit(0)

    threading.Timer(0.8, shutdown).start()


@router.get("/status", response_model=RuntimeStatusOut)
def runtime_status(request: Request) -> RuntimeStatusOut:
    _ensure_local_request(request)
    ollama_running = _port_open(11434) or _process_running("ollama")
    services = [
        _openclaw_status(),
        RuntimeServiceStatus(name="voice_api", running=True, detail="JARVIS Voice Layer adapter is responding."),
        RuntimeServiceStatus(
            name="frontend",
            running=_port_open(5173),
            detail="Vite dev server on 127.0.0.1:5173." if _port_open(5173) else "No listener on 127.0.0.1:5173.",
        ),
        RuntimeServiceStatus(
            name="ollama",
            running=ollama_running,
            detail="Ollama API or process detected." if ollama_running else "Ollama is not detected.",
        ),
    ]
    return RuntimeStatusOut(services=services)


@router.post("/shutdown", response_model=RuntimeShutdownOut)
def runtime_shutdown(payload: RuntimeShutdownRequest, request: Request) -> RuntimeShutdownOut:
    _ensure_local_request(request)
    results: list[RuntimeShutdownResult] = []

    for target in payload.targets:
        if target == "frontend":
            stopped, detail = _stop_pids(_pids_on_port(5173))
            status = "stopped" if stopped else "not_running"
            results.append(RuntimeShutdownResult(target=target, status=status, detail=detail))
        elif target == "ollama":
            process_names = ["ollama.exe", "ollama app.exe"] if os.name == "nt" else ["ollama"]
            stop_results = [_stop_image(name) for name in process_names]
            status = "stopped" if any(item.status == "stopped" for item in stop_results) else "not_running"
            detail = " ".join(item.detail for item in stop_results).strip()
            results.append(RuntimeShutdownResult(target=target, status=status, detail=detail))
        elif target == "voice_api":
            _schedule_api_shutdown()
            results.append(RuntimeShutdownResult(target=target, status="scheduled", detail="Voice Layer API shutdown scheduled after response."))

    return RuntimeShutdownOut(results=results)
