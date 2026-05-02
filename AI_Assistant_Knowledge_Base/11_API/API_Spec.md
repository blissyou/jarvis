# API Spec
#voice-ai #agent #architecture #mvp #security #automation

## 목적
FastAPI 기준으로 JARVIS MVP의 핵심 API 엔드포인트와 요청/응답 구조를 정의한다.

## 핵심 요약
- API는 음성 세션, 에이전트 메시지, 뉴스/주식 도구, 이메일 draft/send, 승인, 로그 조회로 구성한다.
- 초기 구현은 REST 중심으로 시작하되, 음성 스트리밍은 별도 Realtime 세션과 연결한다.
- 모든 쓰기 작업은 approval 상태와 함께 관리한다.

## 상세 내용
### 공통 원칙
- 인증은 사용자 세션 또는 Bearer token 기반
- 모든 응답은 `request_id` 또는 `trace_id` 포함 권장
- tool 실행은 `status`와 `approval_required`를 명시
- 고위험 작업은 바로 완료 상태를 반환하지 않음

### 1. `POST /voice/session`
음성 세션을 시작하거나 Realtime 연결에 필요한 메타데이터를 발급한다.

#### Request
```json
{
  "user_id": "user_123",
  "mode": "realtime",
  "language": "ko",
  "voice_output": true
}
```

#### Response
```json
{
  "session_id": "vs_001",
  "mode": "realtime",
  "language": "ko",
  "realtime": {
    "provider": "openai",
    "client_secret": "ephemeral_token_here"
  },
  "status": "ready"
}
```

### 2. `POST /agent/message`
텍스트 또는 음성 전사 결과를 에이전트에 전달해 intent 분석 및 tool planning을 수행한다.

#### Request
```json
{
  "session_id": "vs_001",
  "message": "엔비디아랑 테슬라 오늘 어때?",
  "input_type": "text"
}
```

#### Response
```json
{
  "session_id": "vs_001",
  "intent": "stocks_brief",
  "slots": {
    "symbols": ["NVDA", "TSLA"]
  },
  "tool_plan": [
    {
      "tool": "stocks_brief",
      "arguments": {
        "symbols": ["NVDA", "TSLA"]
      }
    }
  ],
  "approval_required": false,
  "assistant_text": "엔비디아와 테슬라의 현재가와 관련 뉴스를 확인할게요."
}
```

### 3. `POST /tools/news/scrum`
지정된 기술 카테고리 기준으로 뉴스 스크럼을 생성한다.

#### Request
```json
{
  "session_id": "vs_001",
  "topics": ["AI", "embedded", "web", "C#", "Docker", "Linux", "GitHub"],
  "language": "ko",
  "max_items": 10
}
```

#### Response
```json
{
  "status": "completed",
  "summary": "오늘은 AI 모델 업데이트와 GitHub 자동화 관련 소식이 중요합니다.",
  "items": [
    {
      "title": "Example article",
      "source": "Example Source",
      "url": "https://example.com/article",
      "summary_ko": "핵심 내용 요약"
    }
  ]
}
```

### 4. `POST /tools/stocks/brief`
관심 종목의 현재가, 변동률, 관련 뉴스를 요약한다.

#### Request
```json
{
  "session_id": "vs_001",
  "symbols": ["NVDA", "TSLA"],
  "include_news": true
}
```

#### Response
```json
{
  "status": "completed",
  "brief": [
    {
      "symbol": "NVDA",
      "price": 123.45,
      "change_percent": 2.31,
      "currency": "USD",
      "news": [
        {
          "title": "NVIDIA related article",
          "url": "https://example.com/nvda-news"
        }
      ]
    }
  ],
  "disclaimer": "투자 판단이 아닌 정보 제공용 요약입니다."
}
```

### 5. `POST /tools/email/draft`
이메일 초안을 생성한다.

#### Request
```json
{
  "session_id": "vs_001",
  "to": "kim@example.com",
  "subject": "내일 회의 일정 조정",
  "body_prompt": "내일 회의를 다음 주로 연기하고 싶다는 내용을 정중하게 써줘"
}
```

#### Response
```json
{
  "status": "draft_created",
  "approval_required": true,
  "draft_id": "draft_001",
  "preview": {
    "to": "kim@example.com",
    "subject": "내일 회의 일정 조정",
    "body": "안녕하세요. 내일 예정된 회의를 다음 주로 조정하고자 연락드립니다..."
  }
}
```

### 6. `POST /tools/email/send`
승인된 draft를 실제 발송한다.

#### Request
```json
{
  "session_id": "vs_001",
  "draft_id": "draft_001",
  "approval_id": "appr_001"
}
```

#### Response
```json
{
  "status": "sent",
  "message_id": "msg_001",
  "sent_at": "2026-04-27T10:00:00Z"
}
```

### 7. `GET /approvals`
현재 대기 중인 승인 요청 목록을 조회한다.

#### Response
```json
{
  "items": [
    {
      "approval_id": "appr_001",
      "tool_name": "email_send",
      "status": "pending",
      "resource_preview": {
        "to": "kim@example.com",
        "subject": "내일 회의 일정 조정"
      }
    }
  ]
}
```

### 8. `POST /approvals/{approval_id}`
승인 요청을 승인/거절/수정한다.

#### Request
```json
{
  "decision": "approve",
  "edited_arguments": null
}
```

#### Response
```json
{
  "approval_id": "appr_001",
  "status": "approved"
}
```

### 9. `GET /logs`
세션 또는 사용자 기준 실행 로그를 조회한다.

#### Query Params
- `session_id`
- `user_id`
- `limit`

#### Response
```json
{
  "items": [
    {
      "log_id": "log_001",
      "session_id": "vs_001",
      "event_type": "tool_call",
      "tool_name": "stocks_brief",
      "status": "completed",
      "created_at": "2026-04-27T09:58:00Z"
    }
  ]
}
```

### FastAPI 라우터 예시 구조
```text
app/
  api/
    routes/
      voice.py
      agent.py
      approvals.py
      logs.py
      tools/
        news.py
        stocks.py
        email.py
```

### 10. Workflow API
작업 흐름 시각화와 세션 추적을 위한 전용 조회 API다.

#### `GET /workflow/{session_id}`
세션 기준 전체 workflow를 반환한다.

##### Response
```json
{
  "session_id": "vs_001",
  "nodes": [
    {"id": "n1", "label": "user_message_received", "status": "completed"},
    {"id": "n2", "label": "tool_plan_created", "status": "completed"},
    {"id": "n3", "label": "approval_requested", "status": "pending_approval"}
  ],
  "edges": [
    {"from": "n1", "to": "n2"},
    {"from": "n2", "to": "n3"}
  ],
  "timeline": [
    {"event_type": "user_message_received", "created_at": "2026-04-27T09:58:00Z"},
    {"event_type": "tool_plan_created", "created_at": "2026-04-27T09:58:02Z"}
  ],
  "approvals": [
    {"approval_id": "appr_001", "status": "pending"}
  ],
  "mermaid": "graph TD\nn1[User Message] --> n2[Plan] --> n3[Approval]"
}
```

#### `GET /workflow/{session_id}/events`
workflow event 타임라인 원본을 반환한다.

##### Response
```json
{
  "session_id": "vs_001",
  "events": [
    {
      "event_type": "user_message_received",
      "status": "received",
      "node_id": "n1",
      "created_at": "2026-04-27T09:58:00Z"
    }
  ]
}
```

#### `GET /workflow/{session_id}/mermaid`
Mermaid 문자열만 반환한다.

##### Response
```json
{
  "session_id": "vs_001",
  "diagram_type": "graph_td",
  "mermaid": "graph TD\nn1[User Message] --> n2[Plan]"
}
```

#### `GET /workflow/latest`
최근 세션들의 workflow 요약을 반환한다.

##### Response
```json
{
  "items": [
    {
      "session_id": "vs_001",
      "latest_status": "pending_approval",
      "last_event_type": "approval_requested",
      "updated_at": "2026-04-27T10:01:00Z"
    }
  ]
}
```

### 11. Settings API
사용자 API 키를 안전하게 저장, 조회, 검증, 삭제하는 API다.

#### `POST /settings/api-keys`
```json
{
  "provider": "openai",
  "key_name": "OPENAI_API_KEY",
  "value": "sk-..."
}
```

```json
{
  "status": "saved",
  "provider": "openai",
  "key_name": "OPENAI_API_KEY",
  "masked_value": "sk-****abcd"
}
```

#### `GET /settings/api-keys`
```json
{
  "items": [
    {
      "id": "uuid",
      "provider": "openai",
      "key_name": "OPENAI_API_KEY",
      "masked_value": "sk-****abcd",
      "status": "active",
      "last_checked_at": null
    }
  ]
}
```

#### `POST /settings/api-keys/test`
```json
{
  "provider": "openai",
  "key_name": "OPENAI_API_KEY"
}
```

```json
{
  "status": "valid",
  "provider": "openai",
  "key_name": "OPENAI_API_KEY"
}
```

#### `DELETE /settings/api-keys/{key_id}`
```json
{
  "status": "deleted"
}
```

## 관련 문서
- [[System_Architecture]]
- [[Tool_Execution_Model]]
- [[Approval_System]]
- [[Security_Model]]
- [[PRD]]
- [[Database_Schema]]
- [[Agent_Workflow]]
- [[Workflow_Log_Format]]
- [[Workflow_API_Design]]

## 참고 자료
- [[References]]
> [!warning] Deprecated  
> Superseded by: [[Layered_Runtime_and_Data_Flow]]
