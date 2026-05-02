# Mermaid Generator Code
#voice-ai #agent #architecture #mvp #security #automation

## 목적
workflow 데이터를 Mermaid 문자열로 변환하는 Python 코드 초안을 제공한다.

## 핵심 요약
- workflow 시각화는 `graph TD`, `sequenceDiagram`, `stateDiagram-v2` 세 가지 생성기로 분리하는 것이 좋다.
- generator는 DB 접근을 직접 하지 않고, 정규화된 `nodes`, `edges`, `timeline` 입력을 받는 순수 함수 형태가 테스트에 유리하다.
- FastAPI에서는 서비스 레이어가 데이터를 구성하고, generator는 Mermaid 문자열만 책임진다.

## 상세 내용
### 입력 모델 가정
```python
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass
class MermaidNode:
    id: str
    label: str
    status: str
    event_type: str | None = None
    tool_name: str | None = None
    created_at: datetime | None = None


@dataclass
class MermaidEdge:
    from_node: str
    to_node: str
    edge_type: str = "next"


@dataclass
class MermaidTimelineItem:
    event_type: str
    status: str
    node_id: str
    parent_node_id: str | None
    label: str
    payload: dict[str, Any] = field(default_factory=dict)
    created_at: datetime | None = None
```

### 상태 아이콘 함수
```python
def status_icon(status: str) -> str:
    return {
        "completed": "✅",
        "pending_approval": "⏳",
        "failed": "❌",
        "executing": "🔄",
        "rejected": "🚫",
        "approved": "✅",
        "planned": "📝",
        "parsed": "🧠",
        "received": "🎤",
        "cancelled": "⛔",
    }.get(status, "")
```

### graph TD 생성기
```python
def build_graph_td(nodes: list[MermaidNode], edges: list[MermaidEdge]) -> str:
    lines = ["graph TD"]

    for node in nodes:
        icon = status_icon(node.status)
        label = f"{icon} {node.label}".strip()
        safe_label = label.replace('"', "'")
        lines.append(f'    {node.id}["{safe_label}"]')

    for edge in edges:
        lines.append(f"    {edge.from_node} --> {edge.to_node}")

    return "\n".join(lines)
```

### sequenceDiagram 생성기
```python
def build_sequence_diagram(timeline: list[MermaidTimelineItem]) -> str:
    lines = [
        "sequenceDiagram",
        "    participant U as User",
        "    participant V as Voice",
        "    participant A as Agent",
        "    participant P as Policy",
        "    participant T as Tool",
        "    participant D as DB",
    ]

    mapping = {
        "user_message_received": "U->>V: 사용자 음성 입력",
        "stt_completed": "V->>A: STT 완료",
        "intent_parsed": "A->>A: intent 분석",
        "tool_plan_created": "A->>P: tool 계획 점검",
        "approval_requested": "A-->>U: 승인 요청",
        "approval_approved": "U-->>A: 승인",
        "approval_rejected": "U-->>A: 거절",
        "tool_execution_started": "A->>T: tool 실행 시작",
        "tool_execution_completed": "T-->>A: 실행 완료",
        "tool_execution_failed": "T-->>A: 실행 실패",
        "assistant_response_created": "A->>D: 응답/로그 저장",
        "tts_completed": "A-->>U: 음성 응답 완료",
    }

    for item in timeline:
        line = mapping.get(item.event_type)
        if line:
            lines.append(f"    {line}")

    return "\n".join(lines)
```

### stateDiagram-v2 생성기
```python
def build_state_diagram(statuses: list[str]) -> str:
    lines = ["stateDiagram-v2"]
    if not statuses:
        lines.append("    [*] --> received")
        return "\n".join(lines)

    lines.append(f"    [*] --> {statuses[0]}")
    for current_status, next_status in zip(statuses, statuses[1:]):
        lines.append(f"    {current_status} --> {next_status}")

    return "\n".join(lines)
```

### workflow event에서 node/edge 생성
```python
def build_nodes_and_edges_from_timeline(
    timeline: list[MermaidTimelineItem],
) -> tuple[list[MermaidNode], list[MermaidEdge]]:
    nodes: list[MermaidNode] = []
    edges: list[MermaidEdge] = []

    for item in timeline:
        nodes.append(
            MermaidNode(
                id=item.node_id,
                label=item.label,
                status=item.status,
                event_type=item.event_type,
                created_at=item.created_at,
            )
        )
        if item.parent_node_id:
            edges.append(
                MermaidEdge(
                    from_node=item.parent_node_id,
                    to_node=item.node_id,
                )
            )

    return nodes, edges
```

### 통합 생성 함수
```python
def build_workflow_mermaid_bundle(
    timeline: list[MermaidTimelineItem],
) -> dict[str, str]:
    nodes, edges = build_nodes_and_edges_from_timeline(timeline)
    statuses = [item.status for item in timeline]

    return {
        "graph_td": build_graph_td(nodes, edges),
        "sequence": build_sequence_diagram(timeline),
        "state": build_state_diagram(statuses),
    }
```

### FastAPI 응답 예시
```python
from fastapi import APIRouter

router = APIRouter()


@router.get("/workflow/{session_id}/mermaid")
def get_workflow_mermaid(session_id: str):
    timeline = load_timeline_for_session(session_id)
    diagrams = build_workflow_mermaid_bundle(timeline)
    return {
        "session_id": session_id,
        "diagram_type": "graph_td",
        "mermaid": diagrams["graph_td"],
    }
```

### 구현 메모
- label은 Mermaid 파싱 에러를 줄이기 위해 큰따옴표 이스케이프 필요
- sequenceDiagram은 이벤트 타입 템플릿 기반으로 시작하고, 나중에 tool_name별 커스터마이징 가능
- stateDiagram은 task 단위 생성이 더 읽기 쉬움

## 관련 문서
- [[Mermaid_Generation_Strategy]]
- [[Workflow_Service_Layer]]
- [[Workflow_API_Design]]
- [[Workflow_Log_Format]]
- [[Task_State_Model]]

## 참고 자료
- [[References]]
> [!warning] Deprecated  
> Superseded by: [[Developer_Workflows]]
