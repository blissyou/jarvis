# Database Schema
#voice-ai #agent #architecture #mvp #security #automation

## 목적
PostgreSQL 기준으로 JARVIS MVP와 확장 단계를 위한 데이터베이스 스키마를 정의한다.

## 핵심 요약
- 핵심 테이블은 사용자, 음성 세션, 대화, tool 호출, 승인, 이메일 draft, 뉴스 캐시, 관심 종목, 감사 로그다.
- 모든 쓰기 작업은 approval과 audit 로그를 통해 추적 가능해야 한다.
- 장기 메모리 확장 시 `pgvector` 기반 `memory_items` 테이블을 추가한다.

## 상세 내용
### 설계 원칙
- 모든 주요 엔터티는 `id`, `created_at`, `updated_at`를 갖는다.
- `user_id`, `session_id`, `conversation_id`, `tool_call_id` 연결을 유지한다.
- 상태값은 enum 또는 text + check constraint로 제한한다.
- 민감 데이터는 최소 저장 원칙을 따른다.

### 1. `users`
사용자 계정 및 환경 설정 저장

| 컬럼 | 타입 | 설명 |
|---|---|---|
| id | uuid / text | 사용자 PK |
| email | text | 로그인 이메일 |
| display_name | text | 표시 이름 |
| locale | text | 기본 언어 |
| timezone | text | 시간대 |
| created_at | timestamptz | 생성 시각 |
| updated_at | timestamptz | 수정 시각 |

### 2. `voice_sessions`
음성 세션 및 Realtime 세션 메타데이터 저장

| 컬럼 | 타입 | 설명 |
|---|---|---|
| id | uuid / text | 세션 PK |
| user_id | uuid / text | 사용자 FK |
| mode | text | realtime/transcription |
| language | text | 세션 언어 |
| status | text | ready/active/closed/error |
| started_at | timestamptz | 시작 시각 |
| ended_at | timestamptz | 종료 시각 |
| created_at | timestamptz | 생성 시각 |
| updated_at | timestamptz | 수정 시각 |

### 3. `conversations`
세션 내 사용자/assistant 메시지 저장

| 컬럼 | 타입 | 설명 |
|---|---|---|
| id | uuid / text | 대화 메시지 PK |
| session_id | uuid / text | voice_sessions FK |
| role | text | user/assistant/system/tool |
| content | text | 메시지 본문 |
| message_type | text | transcript/response/tool_result |
| created_at | timestamptz | 생성 시각 |
| updated_at | timestamptz | 수정 시각 |

### 4. `tool_calls`
모든 tool 호출 계획 및 실행 결과 저장

| 컬럼 | 타입 | 설명 |
|---|---|---|
| id | uuid / text | tool call PK |
| session_id | uuid / text | 세션 FK |
| conversation_id | uuid / text | 대화 FK |
| tool_name | text | 도구 이름 |
| arguments_json | jsonb | 호출 인자 |
| result_json | jsonb | 실행 결과 |
| status | text | planned/pending_approval/completed/failed/rejected |
| approval_required | boolean | 승인 필요 여부 |
| created_at | timestamptz | 생성 시각 |
| updated_at | timestamptz | 수정 시각 |

### 5. `approvals`
사용자 승인 요청과 결정 저장

| 컬럼 | 타입 | 설명 |
|---|---|---|
| id | uuid / text | approval PK |
| tool_call_id | uuid / text | tool_calls FK |
| user_id | uuid / text | 사용자 FK |
| decision | text | pending/approved/rejected/edited |
| preview_json | jsonb | 사용자에게 보여준 미리보기 |
| edited_arguments_json | jsonb | 사용자가 수정한 인자 |
| decided_at | timestamptz | 승인/거절 시각 |
| created_at | timestamptz | 생성 시각 |
| updated_at | timestamptz | 수정 시각 |

### 6. `email_drafts`
Gmail draft와 내부 draft 상태 관리

| 컬럼 | 타입 | 설명 |
|---|---|---|
| id | uuid / text | 내부 draft PK |
| user_id | uuid / text | 사용자 FK |
| tool_call_id | uuid / text | 생성한 tool call FK |
| provider_draft_id | text | Gmail draft ID |
| to_email | text | 수신자 |
| subject | text | 제목 |
| body_text | text | 본문 |
| status | text | draft_created/approved/sent/cancelled/failed |
| sent_message_id | text | 발송 후 provider message id |
| created_at | timestamptz | 생성 시각 |
| updated_at | timestamptz | 수정 시각 |

### 7. `news_items`
뉴스 수집 및 중복 제거용 캐시 테이블

| 컬럼 | 타입 | 설명 |
|---|---|---|
| id | uuid / text | 뉴스 PK |
| source | text | 출처 |
| topic | text | AI, Docker 등 분류 |
| title | text | 제목 |
| url | text | 기사 링크 |
| published_at | timestamptz | 발행 시각 |
| summary_ko | text | 한국어 요약 |
| raw_payload | jsonb | 원본 API 결과 |
| created_at | timestamptz | 생성 시각 |
| updated_at | timestamptz | 수정 시각 |

### 8. `stock_watchlist`
사용자 관심 종목 저장

| 컬럼 | 타입 | 설명 |
|---|---|---|
| id | uuid / text | watchlist PK |
| user_id | uuid / text | 사용자 FK |
| symbol | text | 종목 티커 |
| note | text | 사용자 메모 |
| created_at | timestamptz | 생성 시각 |
| updated_at | timestamptz | 수정 시각 |

### 9. `audit_logs`
보안 및 운영 감사 로그 저장

| 컬럼 | 타입 | 설명 |
|---|---|---|
| id | uuid / text | 로그 PK |
| user_id | uuid / text | 사용자 FK |
| session_id | uuid / text | 세션 FK |
| event_type | text | login/tool_call/approval/email_send/error |
| resource_type | text | email/news/stocks/session |
| resource_id | text | 관련 리소스 ID |
| payload_json | jsonb | 상세 이벤트 데이터 |
| created_at | timestamptz | 생성 시각 |

### 10. `memory_items` (`pgvector` 사용 시)
장기 메모리 및 검색용 임베딩 테이블

| 컬럼 | 타입 | 설명 |
|---|---|---|
| id | uuid / text | memory PK |
| user_id | uuid / text | 사용자 FK |
| source_type | text | conversation/news/document/preference |
| source_id | text | 원본 리소스 ID |
| content | text | 저장 텍스트 |
| embedding | vector(n) | pgvector 임베딩 |
| metadata_json | jsonb | 추가 메타데이터 |
| created_at | timestamptz | 생성 시각 |
| updated_at | timestamptz | 수정 시각 |

### 11. `user_api_keys`
사용자별 외부 provider API 키를 암호화 저장하는 테이블

| 컬럼 | 타입 | 설명 |
|---|---|---|
| id | uuid / text | API 키 PK |
| user_id | uuid / text | 사용자 FK |
| provider | text | openai, gnews, finnhub 등 |
| key_name | text | OPENAI_API_KEY, GNEWS_API_KEY 등 |
| encrypted_value | text | 암호화된 secret |
| masked_value | text | 마스킹된 표시용 값 |
| status | text | active, invalid, deleted, unchecked |
| last_checked_at | timestamptz | 마지막 검증 시각 |
| created_at | timestamptz | 생성 시각 |
| updated_at | timestamptz | 수정 시각 |

주의:
- `encrypted_value`만 저장하고 원본 값은 저장 후 반환하지 않는다.
- `masked_value`만 UI와 API 응답에 사용한다.

### 12. `workflow_events`
시각화 전용 event timeline 테이블

| 컬럼 | 타입 | 설명 |
|---|---|---|
| id | uuid / text | workflow event PK |
| session_id | uuid / text | voice_sessions FK |
| user_id | uuid / text | 사용자 FK |
| conversation_id | uuid / text | conversations FK |
| tool_call_id | uuid / text | tool_calls FK |
| approval_id | uuid / text | approvals FK |
| event_type | text | workflow 이벤트 유형 |
| status | text | received/planned/executing/completed 등 |
| node_id | text | 시각화 노드 ID |
| parent_node_id | text | 상위 노드 ID |
| label | text | 다이어그램 표시 라벨 |
| payload_json | jsonb | 시각화와 복원용 세부 정보 |
| created_at | timestamptz | 생성 시각 |

설명:
- `workflow_events`는 시각화 전용 event timeline이다.
- 기존 `audit_logs`는 보안/감사용이며, `workflow_events`는 UI/시각화 복원용이다.
- 같은 실행이라도 `audit_logs`는 누가 무엇을 했는지 추적하고, `workflow_events`는 어떤 순서와 상태로 흘렀는지 복원한다.

### 관계 요약
```text
users
  -> voice_sessions
  -> approvals
  -> email_drafts
  -> stock_watchlist
  -> audit_logs
  -> memory_items
  -> user_api_keys
  -> workflow_events

voice_sessions
  -> conversations
  -> tool_calls
  -> audit_logs
  -> workflow_events

tool_calls
  -> approvals
  -> email_drafts
  -> workflow_events

approvals
  -> workflow_events
```

### 구현 메모
- `tool_calls.arguments_json`와 `result_json`은 디버깅에 중요하다.
- `approvals.preview_json`는 UI와 감사 모두에 사용된다.
- `news_items.url`는 unique constraint를 고려한다.
- `stock_watchlist(user_id, symbol)`는 unique 구성 추천
- `memory_items.embedding`은 cosine similarity index 설계 필요
- `workflow_events(session_id, created_at)` 인덱스는 timeline 복원에 중요하다.
- `workflow_events.node_id`는 세션 내 unique 규칙을 추천한다.

## 관련 문서
- [[API_Spec]]
- [[System_Architecture]]
- [[Tool_Execution_Model]]
- [[Approval_System]]
- [[Security_Model]]
- [[PRD]]
- [[Agent_Workflow]]
- [[Task_State_Model]]
- [[Workflow_Log_Format]]
- [[Workflow_API_Design]]

## 참고 자료
- [[References]]
> [!warning] Deprecated  
> Superseded by: [[Layered_Runtime_and_Data_Flow]]
