from __future__ import annotations

import os
from pathlib import Path
from typing import Any

from api.app.schemas.contracts import RiskClass, ToolManifest, ToolResult
from api.app.security.policy import is_inside_workspace, normalize_path

TOOL_MANIFESTS: dict[str, ToolManifest] = {
    "filesystem.read_text": ToolManifest(
        tool_name="filesystem.read_text",
        risk_class=RiskClass.read_local,
        description="Read a text file inside the approved workspace.",
        input_schema={"type": "object", "required": ["path"], "properties": {"path": {"type": "string"}, "max_bytes": {"type": "integer", "default": 200000}}},
        requires_approval=False,
        idempotent=True,
    ),
    "git.status_summary": ToolManifest(
        tool_name="git.status_summary",
        risk_class=RiskClass.read_local,
        description="Return a lightweight git status summary for a repository.",
        input_schema={"type": "object", "required": ["repo_path"], "properties": {"repo_path": {"type": "string"}}},
        requires_approval=False,
        idempotent=True,
    ),
    "news.search_headlines": ToolManifest(
        tool_name="news.search_headlines",
        risk_class=RiskClass.network_read,
        description="Mock news headline search for MVP wiring.",
        input_schema={"type": "object", "required": ["query"], "properties": {"query": {"type": "string"}, "limit": {"type": "integer", "default": 5}}},
        requires_approval=False,
        idempotent=True,
    ),
    "stocks.get_quote": ToolManifest(
        tool_name="stocks.get_quote",
        risk_class=RiskClass.network_read,
        description="Mock stock quote lookup for MVP wiring.",
        input_schema={"type": "object", "required": ["symbol"], "properties": {"symbol": {"type": "string"}, "market": {"type": "string", "default": "US"}}},
        requires_approval=False,
        idempotent=True,
    ),
    "gmail.create_draft": ToolManifest(
        tool_name="gmail.create_draft",
        risk_class=RiskClass.network_write,
        description="Create a Gmail draft after explicit approval. Stubbed in MVP.",
        input_schema={"type": "object", "required": ["to", "subject", "body"], "properties": {"to": {"type": "array", "items": {"type": "string"}}, "subject": {"type": "string"}, "body": {"type": "string"}}},
        requires_approval=True,
        idempotent=False,
    ),
}


def list_tools() -> list[ToolManifest]:
    return list(TOOL_MANIFESTS.values())


def get_tool(tool_name: str) -> ToolManifest | None:
    return TOOL_MANIFESTS.get(tool_name)


def choose_tool(text: str, workspace_root: str | None = None, selected_files: list[str] | None = None) -> tuple[str | None, dict[str, Any]]:
    lowered = text.lower()
    if "email" in lowered or "gmail" in lowered or "메일" in text:
        return "gmail.create_draft", {"to": ["min@example.com"], "subject": "Draft from JARVIS", "body": text}
    if "stock" in lowered or "주식" in text or "quote" in lowered:
        symbol = "NVDA" if "nvda" in lowered else "AAPL"
        return "stocks.get_quote", {"symbol": symbol, "market": "US"}
    if "news" in lowered or "뉴스" in text:
        return "news.search_headlines", {"query": text, "limit": 5}
    if "git" in lowered:
        return "git.status_summary", {"repo_path": workspace_root or os.getenv("JARVIS_WORKSPACE_ROOT", ".")}
    if selected_files:
        return "filesystem.read_text", {"path": selected_files[0], "max_bytes": 200000}
    if "file" in lowered or "log" in lowered or "파일" in text or "로그" in text:
        return "filesystem.read_text", {"path": str(Path(workspace_root or ".") / "README_IMPLEMENTATION.md"), "max_bytes": 200000}
    return None, {}


def invoke_tool(tool_name: str, arguments: dict[str, Any], workspace_root: str | None = None) -> ToolResult:
    if tool_name == "filesystem.read_text":
        path = normalize_path(str(arguments["path"]))
        if not is_inside_workspace(path, workspace_root):
            return ToolResult(tool_name=tool_name, status="blocked", changed_state=False, summary="Path is outside the approved workspace.")
        max_bytes = int(arguments.get("max_bytes", 200000))
        content = Path(path).read_text(encoding="utf-8", errors="replace")[:max_bytes]
        return ToolResult(tool_name=tool_name, status="succeeded", changed_state=False, summary=f"Read {len(content)} characters from {path}.", raw={"path": path, "content_preview": content[:2000]})

    if tool_name == "git.status_summary":
        repo = normalize_path(str(arguments["repo_path"]))
        return ToolResult(tool_name=tool_name, status="succeeded", changed_state=False, summary=f"Git status requested for {repo}. Shell execution is not enabled in this MVP tool yet.", raw={"repo_path": repo})

    if tool_name == "news.search_headlines":
        query = str(arguments.get("query", "AI"))
        return ToolResult(tool_name=tool_name, status="succeeded", changed_state=False, summary=f"Mocked news search for '{query}'. Replace with RSS/API adapter next.", raw={"items": [{"title": "MVP news adapter placeholder", "source": "local mock"}]})

    if tool_name == "stocks.get_quote":
        symbol = str(arguments.get("symbol", "AAPL")).upper()
        return ToolResult(tool_name=tool_name, status="succeeded", changed_state=False, summary=f"Mock quote for {symbol}: price data adapter not configured yet.", raw={"symbol": symbol, "price": None, "source": "local mock"})

    if tool_name == "gmail.create_draft":
        return ToolResult(tool_name=tool_name, status="blocked", changed_state=False, summary="Gmail draft creation is stubbed until OAuth is configured.", raw={"arguments": arguments})

    return ToolResult(tool_name=tool_name, status="failed", changed_state=False, summary="Unknown tool.")
