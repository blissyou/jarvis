from __future__ import annotations

import os
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
    result = _run(["tasklist", "/FI", f"IMAGENAME eq {image_name}"])
    return image_name.lower() in result.stdout.lower()


def _stop_image(image_name: str) -> RuntimeShutdownResult:
    if not _process_running(image_name):
        return RuntimeShutdownResult(target=image_name, status="not_running", detail=f"{image_name} is not running.")
    result = _run(["taskkill", "/IM", image_name, "/F"])
    if result.returncode == 0:
        return RuntimeShutdownResult(target=image_name, status="stopped", detail=result.stdout.strip())
    return RuntimeShutdownResult(target=image_name, status="failed", detail=(result.stderr or result.stdout).strip())


def _schedule_api_shutdown() -> None:
    def shutdown() -> None:
        os._exit(0)

    threading.Timer(0.8, shutdown).start()


@router.get("/status", response_model=RuntimeStatusOut)
def runtime_status(request: Request) -> RuntimeStatusOut:
    _ensure_local_request(request)
    services = [
        RuntimeServiceStatus(name="api", running=True, detail="Current FastAPI process is responding."),
        RuntimeServiceStatus(
            name="frontend",
            running=_port_open(5173),
            detail="Vite dev server on 127.0.0.1:5173." if _port_open(5173) else "No listener on 127.0.0.1:5173.",
        ),
        RuntimeServiceStatus(
            name="ollama",
            running=_port_open(11434) or _process_running("ollama.exe"),
            detail="Ollama API or process detected." if (_port_open(11434) or _process_running("ollama.exe")) else "Ollama is not detected.",
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
            ollama_result = _stop_image("ollama.exe")
            app_result = _stop_image("ollama app.exe")
            status = "stopped" if "stopped" in {ollama_result.status, app_result.status} else "not_running"
            detail = f"{ollama_result.detail} {app_result.detail}".strip()
            results.append(RuntimeShutdownResult(target=target, status=status, detail=detail))
        elif target == "api":
            _schedule_api_shutdown()
            results.append(RuntimeShutdownResult(target=target, status="scheduled", detail="API shutdown scheduled after response."))

    return RuntimeShutdownOut(results=results)
