# Workflow API Design
#voice-ai #agent #architecture #mvp #security #automation

## 목적
프론트엔드 또는 Obsidian/Markdown에서 작업 흐름을 조회할 수 있도록 workflow 전용 API를 설계한다.

## 핵심 요약
- workflow API는 시각화에 필요한 `nodes`, `edges`, `timeline`, `approvals`, `mermaid`를 반환해야 한다.
- 원본 이벤트 조회, Mermaid 문자열 조회, 최근 세션 조회를 별도 엔드포인트로 분리한다.
- 세션 데이터는 민감할 수 있으므로 사용자 권한 검증이 필요하다.

## 상세 내용
### 1. `GET /workflow/{session_id}`
#### 목적
세션 기준 전체 workflow view를 반환한다.

#### Request
```http
GET /workflow/vs_001
Authorization: Bearer <token>
```

#### Response
```json
{
  "session_id": "vs_001",
  "nodes": [
    {"id": "n1", "label": "음성 입력", "status": "completed"},
    {"id": "n2", "label": "Intent 분석", "status": "completed"},
    {"id": "n3", "label": "승인 요청", "status": "pending_approval"}
  ],
  "edges": [
    {"from": "n1", "to": "n2"},
    {"from": "n2", "to": "n3"}
  ],
  "timeline": [
    {"event_type": "user_message_received", "created_at": "2026-04-27T09:58:00Z"},
    {"event_type": "approval_requested", "created_at": "2026-04-27T10:00:00Z"}
  ],
  "approvals": [
    {"approval_id": "appr_001", "status": "pending"}
  ],
  "mermaid": "graph TD\nn1[음성 입력] --> n2[Intent 분석] --> n3[승인 요청]"
}
```

#### 에러 응답
```json
{
  "error": "workflow_not_found",
  "message": "해당 session_id의 workflow를 찾을 수 없습니다."
}
```

#### 보안 고려사항
- session 소유자 또는 관리자만 조회 가능
- 민감 payload는 마스킹 가능
- 이메일 본문 전체를 기본 응답에 노출하지 않도록 주의

### 2. `GET /workflow/{session_id}/events`
#### 목적
원본 workflow event 목록을 반환한다.

#### Request
```http
GET /workflow/vs_001/events
```

#### Response
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

#### 에러 응답
```json
{
  "error": "events_not_found",
  "message": "workflow events가 없습니다."
}
```

#### 보안 고려사항
- debug용 상세 payload는 권한별로 제한
- 관리자 모드 외에는 일부 payload 생략 가능

### 3. `GET /workflow/{session_id}/mermaid`
#### 목적
Mermaid 문자열만 반환하여 Obsidian이나 웹 UI에서 직접 렌더링할 수 있게 한다.

#### Request
```http
GET /workflow/vs_001/mermaid
```

#### Response
```json
{
  "session_id": "vs_001",
  "diagram_type": "graph_td",
  "mermaid": "graph TD\nn1[음성 입력] --> n2[Plan] --> n3[Approval]"
}
```

#### 에러 응답
```json
{
  "error": "mermaid_generation_failed",
  "message": "Mermaid 문자열 생성에 실패했습니다."
}
```

#### 보안 고려사항
- Mermaid label에 민감 데이터를 그대로 노출하지 않기
- approval preview는 축약본으로 표시

### 4. `GET /workflow/latest`
#### 목적
최근 세션의 workflow 요약을 목록 형태로 반환한다.

#### Request
```http
GET /workflow/latest
```

#### Response
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

#### 에러 응답
```json
{
  "error": "no_recent_workflows",
  "message": "최근 workflow가 없습니다."
}
```

#### 보안 고려사항
- 사용자 본인의 최근 세션만 기본 제공
- 관리자용 전역 조회는 별도 권한 필요

## 관련 문서
- [[API_Spec]]
- [[Database_Schema]]
- [[Agent_Workflow]]
- [[Workflow_Log_Format]]
- [[Security_Model]]
- [[Mermaid_Generation_Strategy]]

## 참고 자료
- [[References]]
> [!warning] Deprecated  
> Superseded by: [[Layered_Runtime_and_Data_Flow]]
