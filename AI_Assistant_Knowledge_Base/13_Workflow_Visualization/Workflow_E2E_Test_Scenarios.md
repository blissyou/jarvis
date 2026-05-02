# Workflow E2E Test Scenarios
#voice-ai #agent #architecture #mvp #security #automation

## 목적
workflow 시각화 기능이 실제 에이전트 실행 흐름과 일치하는지 검증하기 위한 end-to-end 테스트 시나리오를 정의한다.

## 핵심 요약
- E2E 테스트는 읽기 작업, 승인형 쓰기 작업, 승인 거절, 실행 실패, 재시도, 세션 취소를 모두 포함해야 한다.
- 각 시나리오는 API 응답뿐 아니라 `workflow_events`, `tool_calls`, `approvals`, `audit_logs`의 일관성을 함께 검증해야 한다.
- 최종 목표는 “사용자에게 보이는 workflow 상태와 실제 실행 상태가 항상 일치하는가”를 확인하는 것이다.

## 상세 내용
### 공통 검증 포인트
- `workflow_events`가 누락 없이 저장되는가
- `tool_calls.status`와 `workflow_events.status`가 일치하는가
- 승인 필요한 작업에서 `pending_approval`가 반드시 남는가
- `/workflow/{session_id}`의 `nodes`, `edges`, `timeline`, `mermaid`가 복원 가능한가

### 시나리오 1: 뉴스 스크럼 조회 성공
#### 입력
- 사용자: “오늘 개발 뉴스 요약해줘”

#### 기대 흐름
```text
received -> parsed -> planned -> executing -> completed
```

#### 기대 검증
- approval row 없음
- tool_calls.status = completed
- workflow_events.event_type 순서:
  - user_message_received
  - stt_completed
  - intent_parsed
  - tool_plan_created
  - tool_execution_started
  - tool_execution_completed
  - assistant_response_created
  - tts_completed

### 시나리오 2: 주식 브리핑 성공
#### 입력
- 사용자: “엔비디아랑 테슬라 오늘 어때?”

#### 기대 검증
- `tools/stocks/brief` 호출
- disclaimer 포함 응답
- workflow graph가 approval 없이 직선 흐름 생성

### 시나리오 3: 이메일 draft 생성 후 승인 발송 성공
#### 입력
- 사용자: “김철수에게 내일 회의 연기 메일 써줘”

#### 기대 흐름
```text
received -> parsed -> planned -> pending_approval -> approved -> executing -> completed
```

#### 기대 검증
- email_drafts row 생성
- approvals row 생성 및 decision=approved
- tool_calls.status 최종 completed
- workflow detail의 approvals 배열에 pending -> approved 반영

### 시나리오 4: 이메일 승인 거절
#### 입력
- 사용자: 이메일 초안 생성 후 거절

#### 기대 흐름
```text
received -> parsed -> planned -> pending_approval -> rejected
```

#### 기대 검증
- send 실행 없음
- tool_execution_started 이벤트 없음
- approvals.decision = rejected
- Mermaid graph에 `🚫` 상태 노드 포함

### 시나리오 5: 이메일 발송 실패 후 재시도
#### 입력
- 승인 후 provider API 실패

#### 기대 흐름
```text
received -> parsed -> planned -> pending_approval -> approved -> executing -> failed -> executing -> completed
```

#### 기대 검증
- tool_execution_failed 이벤트 존재
- 동일 tool_call_id 또는 retry tool_call trace 존재
- stateDiagram 상태 시퀀스 복원 가능

### 시나리오 6: 세션 중간 취소
#### 입력
- 승인 대기 중 사용자가 취소

#### 기대 흐름
```text
received -> parsed -> planned -> pending_approval -> cancelled
```

#### 기대 검증
- approvals는 pending 또는 cancelled 정책에 맞게 정리
- workflow latest status = cancelled

### 테스트 자동화 전략
#### API 레벨
- FastAPI TestClient 사용
- workflow API 응답 스냅샷 테스트

#### DB 레벨
- PostgreSQL test DB 또는 transaction rollback fixture
- workflow_events row count와 event_type 순서 검증

#### Mermaid 레벨
- Mermaid 문자열 snapshot 비교
- 최소한 `graph TD` 헤더, node label, edge 포함 여부 검증

### pytest 스타일 예시
```python
def test_news_scrum_workflow_e2e(client, db_session):
    session = client.post("/voice/session", json={
        "user_id": "user_123",
        "mode": "realtime",
        "language": "ko",
        "voice_output": True,
    }).json()

    client.post("/agent/message", json={
        "session_id": session["session_id"],
        "message": "오늘 개발 뉴스 요약해줘",
        "input_type": "text",
    })

    workflow = client.get(f"/workflow/{session['session_id']}").json()

    assert workflow["session_id"] == session["session_id"]
    assert len(workflow["nodes"]) >= 5
    assert "graph TD" in workflow["mermaid"]
    assert any(item["event_type"] == "tool_execution_completed" for item in workflow["timeline"])
```

## 관련 문서
- [[Workflow_API_Design]]
- [[Workflow_Service_Layer]]
- [[Workflow_SQL_DDL]]
- [[Task_State_Model]]
- [[Agent_Workflow]]

## 참고 자료
- [[References]]
> [!warning] Deprecated  
> Superseded by: [[Developer_Workflows]]
