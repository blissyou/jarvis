from __future__ import annotations

from enum import Enum
from typing import Any, Literal

from pydantic import BaseModel, Field


class RiskClass(str, Enum):
    read_local = "read_local"
    write_workspace = "write_workspace"
    write_outside_workspace = "write_outside_workspace"
    network_read = "network_read"
    network_write = "network_write"
    system_admin = "system_admin"


class TurnMode(str, Enum):
    text = "text"
    voice = "voice"


class SessionCreate(BaseModel):
    workspace_root: str | None = None


class SessionOut(BaseModel):
    id: str
    workspace_root: str | None
    status: str
    created_at: str


class UserInput(BaseModel):
    mode: TurnMode = TurnMode.text
    text: str
    transcript_confidence: float | None = Field(default=None, ge=0, le=1)


class WorkspaceContext(BaseModel):
    cwd: str | None = None
    selected_files: list[str] = Field(default_factory=list)


class PolicyContext(BaseModel):
    approval_mode: Literal["ask", "auto_readonly"] = "ask"
    cloud_allowed: bool = False
    network_allowed: Literal["deny", "ask", "allow"] = "ask"


class TurnCreate(BaseModel):
    input: UserInput
    workspace: WorkspaceContext = Field(default_factory=WorkspaceContext)
    policy: PolicyContext = Field(default_factory=PolicyContext)


class PlanStep(BaseModel):
    step_id: str
    kind: Literal["chat", "tool", "code_execution"]
    tool: str | None = None
    arguments: dict[str, Any] = Field(default_factory=dict)


class TurnOut(BaseModel):
    id: str
    session_id: str
    mode: str
    risk_level: str
    requires_approval: bool
    status: str
    plan: list[PlanStep]
    final_response: str | None = None
    approval_id: str | None = None


class ToolManifest(BaseModel):
    tool_name: str
    risk_class: RiskClass
    description: str
    input_schema: dict[str, Any]
    requires_approval: bool
    idempotent: bool = True


class ToolResult(BaseModel):
    tool_name: str
    status: Literal["succeeded", "failed", "blocked"]
    changed_state: bool
    summary: str
    artifacts: list[dict[str, Any]] = Field(default_factory=list)
    raw: Any | None = None


class ApprovalOut(BaseModel):
    id: str
    session_id: str
    turn_id: str | None
    risk_level: str
    action_summary: str
    status: str
    preview: dict[str, Any]
    created_at: str
    resolved_at: str | None = None


class ApprovalDecisionOut(BaseModel):
    approval: ApprovalOut
    turn: TurnOut | None = None


class EventOut(BaseModel):
    id: str
    session_id: str
    turn_id: str | None = None
    event_type: str
    risk_level: str | None = None
    payload: dict[str, Any]
    created_at: str


class BudgetOut(BaseModel):
    monthly_budget_krw: int
    estimated_cost_krw: float
    cloud_model_calls: int
    local_model_calls: int
    tool_calls: int
    approval_requests: int


class RuntimeServiceStatus(BaseModel):
    name: str
    running: bool
    detail: str


class RuntimeStatusOut(BaseModel):
    services: list[RuntimeServiceStatus]


class RuntimeShutdownRequest(BaseModel):
    targets: list[Literal["voice_api", "frontend", "ollama"]]


class RuntimeShutdownResult(BaseModel):
    target: str
    status: Literal["scheduled", "stopped", "not_running", "failed", "blocked"]
    detail: str


class RuntimeShutdownOut(BaseModel):
    results: list[RuntimeShutdownResult]
