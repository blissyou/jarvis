# Workflow Service Layer
#voice-ai #agent #architecture #mvp #security #automation

## 목적
workflow 조회와 생성, Mermaid 변환을 담당하는 서비스 레이어 함수 구조를 정의한다.

## 핵심 요약
- 서비스 레이어는 DB row를 읽고, timeline을 복원하고, node/edge를 만들고, Mermaid를 생성하는 책임을 가진다.
- 라우터는 thin하게 유지하고, 비즈니스 로직은 `workflow_service.py`로 집중시키는 것이 좋다.
- event 생성 로직과 조회 로직을 분리해야 테스트와 확장이 쉬워진다.

## 상세 내용
### 권장 파일 구조
```text
app/
  services/
    workflow_service.py
    workflow_event_service.py
    mermaid_service.py
  repositories/
    workflow_repository.py
```

### 핵심 함수 목록
#### 1. event 생성
```python
def create_workflow_event(
    db: Session,
    *,
    session_id: str,
    user_id: str,
    event_type: WorkflowEventType,
    status: WorkflowStatus,
    node_id: str,
    label: str,
    conversation_id: str | None = None,
    tool_call_id: str | None = None,
    approval_id: str | None = None,
    parent_node_id: str | None = None,
    payload: dict | None = None,
) -> WorkflowEvent:
    ...
```

역할:
- workflow_events row 저장
- payload 기본값 보정
- node_id 유효성 검증

#### 2. 세션 timeline 조회
```python
def get_workflow_timeline(
    db: Session,
    *,
    session_id: str,
) -> list[WorkflowEvent]:
    ...
```

역할:
- `session_id` 기준 정렬 조회
- timeline 원본 반환

#### 3. approval 요약 조회
```python
def get_workflow_approvals(
    db: Session,
    *,
    session_id: str,
) -> list[Approval]:
    ...
```

역할:
- 해당 세션과 관련된 approval 목록 반환

#### 4. node/edge 변환
```python
def build_workflow_graph(
    timeline: list[WorkflowEvent],
) -> tuple[list[WorkflowNode], list[WorkflowEdge]]:
    ...
```

역할:
- timeline -> nodes/edges 변환

#### 5. 전체 workflow 응답 조립
```python
def get_workflow_detail(
    db: Session,
    *,
    session_id: str,
) -> WorkflowDetailResponse:
    ...
```

역할:
- timeline 조회
- approvals 조회
- graph 변환
- Mermaid 생성
- 최종 response model 반환

#### 6. 최신 workflow 목록
```python
def get_latest_workflows(
    db: Session,
    *,
    user_id: str,
    limit: int = 20,
) -> WorkflowLatestResponse:
    ...
```

### 서비스 레이어 예시 코드
```python
def get_workflow_detail(db: Session, *, session_id: str) -> WorkflowDetailResponse:
    timeline_rows = get_workflow_timeline(db, session_id=session_id)
    approvals = get_workflow_approvals(db, session_id=session_id)

    timeline = [map_workflow_event_row_to_timeline_item(row) for row in timeline_rows]
    nodes, edges = build_workflow_graph(timeline_rows)
    mermaid_bundle = build_workflow_mermaid_bundle(
        [map_timeline_item_to_mermaid_item(item) for item in timeline]
    )

    return WorkflowDetailResponse(
        session_id=session_id,
        nodes=nodes,
        edges=edges,
        timeline=timeline,
        approvals=[map_approval_row_to_summary(a) for a in approvals],
        mermaid=mermaid_bundle["graph_td"],
    )
```

### 상태 일관성 검증 함수
```python
def validate_workflow_consistency(
    *,
    tool_call_status: str | None,
    approval_decision: str | None,
    latest_workflow_status: str,
) -> None:
    if latest_workflow_status == "pending_approval" and approval_decision == "approved":
        # 구현 정책에 따라 허용 또는 보정 필요
        return

    if latest_workflow_status == "completed" and tool_call_status == "failed":
        raise ValueError("workflow 상태와 tool 상태가 불일치합니다.")
```

### 권장 repository 함수
```python
def list_workflow_events_by_session(db: Session, session_id: str) -> list[WorkflowEvent]:
    ...


def list_approvals_by_session(db: Session, session_id: str) -> list[Approval]:
    ...


def list_latest_workflow_sessions(db: Session, user_id: str, limit: int) -> list[dict]:
    ...
```

### 구현 메모
- 라우터에서 직접 SQLAlchemy query를 작성하지 않는 것이 좋다.
- event 생성은 agent/tool/approval 서비스 어디서든 공통 호출 가능해야 한다.
- 실패한 tool 실행도 반드시 workflow event를 남겨야 Mermaid 복원이 가능하다.

## 관련 문서
- [[Workflow_SQL_DDL]]
- [[Workflow_Pydantic_Models]]
- [[Mermaid_Generator_Code]]
- [[Workflow_API_Design]]
- [[Task_State_Model]]

## 참고 자료
- [[References]]
> [!warning] Deprecated  
> Superseded by: [[Agent_Runtime]]
