# Workflow Pydantic Models
#voice-ai #agent #architecture #mvp #security #automation

## 목적
FastAPI에서 workflow 시각화 관련 request/response를 구현하기 위한 Pydantic 모델 구조를 정의한다.

## 핵심 요약
- workflow API는 `nodes`, `edges`, `timeline`, `approvals`, `mermaid`를 공통 응답 구조로 사용한다.
- 내부 DB row 모델과 외부 API 응답 모델을 분리한다.
- Pydantic v2 기준으로 작성하며, FastAPI response_model에 바로 적용 가능한 수준으로 설계한다.

## 상세 내용
### 설계 원칙
- DB row 직접 노출 금지
- enum을 적극 활용해 status/event_type 오타 방지
- event/timeline/node/edge를 별도 모델로 분리
- Mermaid 문자열은 최종 응답 필드로 포함

### Enum 정의 예시
```python
from enum import Enum


class WorkflowEventType(str, Enum):
    USER_MESSAGE_RECEIVED = "user_message_received"
    STT_COMPLETED = "stt_completed"
    INTENT_PARSED = "intent_parsed"
    TOOL_PLAN_CREATED = "tool_plan_created"
    APPROVAL_REQUESTED = "approval_requested"
    APPROVAL_APPROVED = "approval_approved"
    APPROVAL_REJECTED = "approval_rejected"
    TOOL_EXECUTION_STARTED = "tool_execution_started"
    TOOL_EXECUTION_COMPLETED = "tool_execution_completed"
    TOOL_EXECUTION_FAILED = "tool_execution_failed"
    ASSISTANT_RESPONSE_CREATED = "assistant_response_created"
    TTS_COMPLETED = "tts_completed"


class WorkflowStatus(str, Enum):
    RECEIVED = "received"
    PARSED = "parsed"
    PLANNED = "planned"
    PENDING_APPROVAL = "pending_approval"
    APPROVED = "approved"
    EXECUTING = "executing"
    COMPLETED = "completed"
    REJECTED = "rejected"
    FAILED = "failed"
    CANCELLED = "cancelled"
```

### Base 모델
```python
from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class WorkflowBaseModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class WorkflowNode(WorkflowBaseModel):
    id: str
    label: str
    status: WorkflowStatus
    event_type: WorkflowEventType | None = None
    tool_name: str | None = None
    created_at: datetime | None = None


class WorkflowEdge(WorkflowBaseModel):
    from_node: str = Field(alias="from")
    to_node: str = Field(alias="to")
    edge_type: str = "next"


class WorkflowTimelineItem(WorkflowBaseModel):
    event_id: str
    event_type: WorkflowEventType
    status: WorkflowStatus
    node_id: str
    parent_node_id: str | None = None
    label: str
    payload: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime


class WorkflowApprovalSummary(WorkflowBaseModel):
    approval_id: str
    tool_call_id: str | None = None
    decision: str
    preview: dict[str, Any] = Field(default_factory=dict)
    decided_at: datetime | None = None
```

### API 응답 모델
```python
class WorkflowDetailResponse(WorkflowBaseModel):
    session_id: str
    nodes: list[WorkflowNode]
    edges: list[WorkflowEdge]
    timeline: list[WorkflowTimelineItem]
    approvals: list[WorkflowApprovalSummary]
    mermaid: str


class WorkflowEventsResponse(WorkflowBaseModel):
    session_id: str
    events: list[WorkflowTimelineItem]


class WorkflowMermaidResponse(WorkflowBaseModel):
    session_id: str
    diagram_type: str
    mermaid: str


class WorkflowLatestItem(WorkflowBaseModel):
    session_id: str
    latest_status: WorkflowStatus
    last_event_type: WorkflowEventType
    updated_at: datetime


class WorkflowLatestResponse(WorkflowBaseModel):
    items: list[WorkflowLatestItem]
```

### 내부 서비스 입력 모델
```python
class WorkflowBuildRequest(WorkflowBaseModel):
    session_id: str
    include_mermaid: bool = True
    include_approvals: bool = True
    include_payloads: bool = True


class WorkflowEventCreate(WorkflowBaseModel):
    session_id: str
    user_id: str
    conversation_id: str | None = None
    tool_call_id: str | None = None
    approval_id: str | None = None
    event_type: WorkflowEventType
    status: WorkflowStatus
    node_id: str
    parent_node_id: str | None = None
    label: str
    payload: dict[str, Any] = Field(default_factory=dict)
```

### FastAPI 라우터 예시
```python
from fastapi import APIRouter

router = APIRouter(prefix="/workflow", tags=["workflow"])


@router.get("/{session_id}", response_model=WorkflowDetailResponse)
def get_workflow(session_id: str):
    ...


@router.get("/{session_id}/events", response_model=WorkflowEventsResponse)
def get_workflow_events(session_id: str):
    ...


@router.get("/{session_id}/mermaid", response_model=WorkflowMermaidResponse)
def get_workflow_mermaid(session_id: str):
    ...


@router.get("/latest", response_model=WorkflowLatestResponse)
def get_latest_workflows():
    ...
```

### 구현 메모
- `WorkflowEdge`는 `from`이 Python 예약어와 충돌할 수 있어 alias 사용
- Pydantic v2에서는 `ConfigDict(from_attributes=True)`로 ORM row 매핑
- payload는 API 응답에서 마스킹 옵션을 둘 수 있음

## 관련 문서
- [[API_Spec]]
- [[Workflow_API_Design]]
- [[Workflow_Service_Layer]]
- [[Workflow_SQL_DDL]]
- [[Database_Schema]]

## 참고 자료
- [[References]]
> [!warning] Deprecated  
> Superseded by: [[Layered_Runtime_and_Data_Flow]]
