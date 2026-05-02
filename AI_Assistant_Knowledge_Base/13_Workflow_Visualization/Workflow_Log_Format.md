# Workflow Log Format
#voice-ai #agent #architecture #mvp #security #automation

## 목적
작업 흐름 시각화를 만들기 위한 로그 데이터 구조와 event 복원 규칙을 정의한다.

## 핵심 요약
- workflow 시각화는 `workflow_event`를 중심으로 구성한다.
- `audit_logs`는 감사용, `workflow_events`는 시각화 복원용으로 역할을 분리한다.
- `session_id`를 기준으로 event timeline을 복원하고, `node_id`/`parent_node_id`로 graph를 생성한다.

## 상세 내용
### workflow_event의 개념
`workflow_event`는 에이전트가 사용자 요청을 처리하는 과정에서 생성되는 시각화 전용 이벤트다. 각 이벤트는 타임라인에 찍히며, 동시에 노드와 엣지 생성의 입력이 된다.

### event_type 목록
- `user_message_received`
- `stt_completed`
- `intent_parsed`
- `tool_plan_created`
- `approval_requested`
- `approval_approved`
- `approval_rejected`
- `tool_execution_started`
- `tool_execution_completed`
- `tool_execution_failed`
- `assistant_response_created`
- `tts_completed`

### workflow_events JSON 예시
```json
{
  "id": "we_001",
  "session_id": "vs_001",
  "user_id": "user_123",
  "conversation_id": "conv_001",
  "tool_call_id": "tc_001",
  "approval_id": null,
  "event_type": "tool_plan_created",
  "status": "planned",
  "node_id": "n_plan_001",
  "parent_node_id": "n_parse_001",
  "label": "뉴스 스크럼 계획 생성",
  "payload_json": {
    "tool_name": "news_scrum",
    "arguments": {
      "topics": ["AI", "Docker"]
    }
  },
  "created_at": "2026-04-27T10:00:02Z"
}
```

### audit_logs.payload_json 예시
```json
{
  "event_type": "tool_call",
  "tool_name": "email_send",
  "status": "completed",
  "provider_message_id": "msg_001",
  "trace_id": "trace_abc123"
}
```

### tool_calls.result_json 예시
```json
{
  "status": "completed",
  "result": {
    "message_id": "msg_001",
    "sent_at": "2026-04-27T10:05:00Z"
  }
}
```

### approvals.preview_json 예시
```json
{
  "tool_name": "email_send",
  "preview": {
    "to": "kim@example.com",
    "subject": "내일 회의 일정 조정",
    "body": "안녕하세요. 내일 회의 일정 조정 관련 메일입니다."
  }
}
```

### workflow node/edge 생성 규칙
- 각 `workflow_event`는 하나의 node 후보가 된다.
- `node_id`는 같은 세션 안에서 유일해야 한다.
- `parent_node_id`가 있으면 `parent -> child` edge를 생성한다.
- `approval_requested -> approval_approved/rejected`는 명시적 분기 edge로 생성한다.
- `tool_execution_failed`가 발생하면 동일한 `tool_call_id` 기준으로 retry edge를 연결할 수 있다.

### session_id 기준 timeline 복원 방법
1. `workflow_events`를 `session_id` + `created_at asc`로 조회
2. 타임라인 배열 생성
3. `node_id` 기준 노드 맵 생성
4. `parent_node_id` 기준 엣지 생성
5. `approvals`, `tool_calls`, `conversations`를 join해 보강
6. 최종적으로 `nodes`, `edges`, `timeline`, `mermaid`를 조합

## 관련 문서
- [[Database_Schema]]
- [[API_Spec]]
- [[Agent_Workflow]]
- [[Task_State_Model]]
- [[Workflow_API_Design]]

## 참고 자료
- [[References]]
> [!warning] Deprecated  
> Superseded by: [[Layered_Runtime_and_Data_Flow]]
