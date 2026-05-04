from __future__ import annotations

import os
from pathlib import Path

from api.app.schemas.contracts import RiskClass

SENSITIVE_SEGMENTS = {
    "windows",
    "program files",
    "program files (x86)",
    ".ssh",
    "appdata",
    "microsoft\\credentials",
}


def default_workspace() -> str:
    return os.getenv("JARVIS_WORKSPACE_ROOT", str(Path.cwd()))


def normalize_path(path: str) -> str:
    return str(Path(path).expanduser().resolve())


def is_inside_workspace(path: str, workspace_root: str | None = None) -> bool:
    root = normalize_path(workspace_root or default_workspace()).lower()
    target = normalize_path(path).lower()
    return target == root or target.startswith(root.rstrip("\\/") + os.sep.lower())


def contains_sensitive_segment(path: str) -> bool:
    lowered = normalize_path(path).lower()
    return any(segment in lowered for segment in SENSITIVE_SEGMENTS)


def requires_approval(risk_class: RiskClass, path: str | None = None, workspace_root: str | None = None) -> bool:
    if risk_class in {RiskClass.network_write, RiskClass.system_admin, RiskClass.write_outside_workspace}:
        return True
    if risk_class == RiskClass.write_workspace:
        return True
    if risk_class == RiskClass.network_read:
        return os.getenv("JARVIS_NETWORK_READ_AUTO", "true").lower() != "true"
    if path and contains_sensitive_segment(path):
        return True
    if path and not is_inside_workspace(path, workspace_root):
        return True
    return False


def risk_level_for(risk_class: RiskClass) -> str:
    if risk_class in {RiskClass.read_local, RiskClass.network_read}:
        return "low"
    if risk_class in {RiskClass.write_workspace, RiskClass.network_write}:
        return "medium"
    return "high"
