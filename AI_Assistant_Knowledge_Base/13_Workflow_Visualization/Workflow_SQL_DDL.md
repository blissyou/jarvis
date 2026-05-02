# Workflow SQL DDL
#voice-ai #agent #architecture #mvp #security #automation

## 목적
`workflow_events`를 PostgreSQL에 실제로 생성하기 위한 SQL DDL과 인덱스, 제약 조건, 조회 최적화 전략을 정의한다.

## 핵심 요약
- `workflow_events`는 workflow 시각화 전용 타임라인 테이블이다.
- `audit_logs`와 분리하여 UI 복원, Mermaid 생성, 세션 타임라인 조회를 빠르게 처리한다.
- `session_id + created_at`, `tool_call_id`, `approval_id`, `node_id`를 중심으로 인덱스를 설계한다.

## 상세 내용
### 설계 원칙
- PostgreSQL 기준
- UUID 또는 text 기반 PK 모두 가능하지만, 여기서는 `uuid`를 기준 예시로 작성
- 상태와 이벤트 타입은 `CHECK` 또는 enum으로 제한
- `node_id`는 세션 내 unique를 권장
- `payload_json`은 시각화에 필요한 최소한의 구조화 정보를 담는다

### 권장 Enum 정의
```sql
CREATE TYPE workflow_event_type AS ENUM (
  'user_message_received',
  'stt_completed',
  'intent_parsed',
  'tool_plan_created',
  'approval_requested',
  'approval_approved',
  'approval_rejected',
  'tool_execution_started',
  'tool_execution_completed',
  'tool_execution_failed',
  'assistant_response_created',
  'tts_completed'
);

CREATE TYPE workflow_status AS ENUM (
  'received',
  'parsed',
  'planned',
  'pending_approval',
  'approved',
  'executing',
  'completed',
  'rejected',
  'failed',
  'cancelled'
);
```

### `workflow_events` DDL
```sql
CREATE TABLE workflow_events (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  session_id uuid NOT NULL REFERENCES voice_sessions(id) ON DELETE CASCADE,
  user_id uuid NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  conversation_id uuid NULL REFERENCES conversations(id) ON DELETE SET NULL,
  tool_call_id uuid NULL REFERENCES tool_calls(id) ON DELETE SET NULL,
  approval_id uuid NULL REFERENCES approvals(id) ON DELETE SET NULL,
  event_type workflow_event_type NOT NULL,
  status workflow_status NOT NULL,
  node_id text NOT NULL,
  parent_node_id text NULL,
  label text NOT NULL,
  payload_json jsonb NOT NULL DEFAULT '{}'::jsonb,
  created_at timestamptz NOT NULL DEFAULT now(),

  CONSTRAINT workflow_events_node_id_not_blank
    CHECK (char_length(trim(node_id)) > 0),

  CONSTRAINT workflow_events_label_not_blank
    CHECK (char_length(trim(label)) > 0)
);
```

### 유니크 및 인덱스
```sql
CREATE UNIQUE INDEX uq_workflow_events_session_node
  ON workflow_events (session_id, node_id);

CREATE INDEX idx_workflow_events_session_created_at
  ON workflow_events (session_id, created_at);

CREATE INDEX idx_workflow_events_user_created_at
  ON workflow_events (user_id, created_at DESC);

CREATE INDEX idx_workflow_events_tool_call_id
  ON workflow_events (tool_call_id)
  WHERE tool_call_id IS NOT NULL;

CREATE INDEX idx_workflow_events_approval_id
  ON workflow_events (approval_id)
  WHERE approval_id IS NOT NULL;

CREATE INDEX idx_workflow_events_event_type
  ON workflow_events (event_type);

CREATE INDEX idx_workflow_events_status
  ON workflow_events (status);

CREATE INDEX idx_workflow_events_payload_json_gin
  ON workflow_events
  USING GIN (payload_json);
```

### parent-child 참조 무결성 주의
`parent_node_id`는 같은 테이블의 다른 row를 가리키지만, FK로 강제하면 삽입 순서 제약이 커진다. 따라서 초기 구현에서는 FK를 두지 않고, 서비스 레이어에서 `session_id` 내 유효성 검사를 수행하는 것이 현실적이다.

### 조회 예시
#### 세션 타임라인 복원
```sql
SELECT
  id,
  session_id,
  conversation_id,
  tool_call_id,
  approval_id,
  event_type,
  status,
  node_id,
  parent_node_id,
  label,
  payload_json,
  created_at
FROM workflow_events
WHERE session_id = $1
ORDER BY created_at ASC, id ASC;
```

#### 최근 workflow 세션 조회
```sql
SELECT
  session_id,
  max(created_at) AS last_event_at,
  (
    SELECT we2.status
    FROM workflow_events we2
    WHERE we2.session_id = we.session_id
    ORDER BY we2.created_at DESC, we2.id DESC
    LIMIT 1
  ) AS latest_status,
  (
    SELECT we3.event_type
    FROM workflow_events we3
    WHERE we3.session_id = we.session_id
    ORDER BY we3.created_at DESC, we3.id DESC
    LIMIT 1
  ) AS latest_event_type
FROM workflow_events we
GROUP BY session_id
ORDER BY last_event_at DESC
LIMIT 20;
```

### Alembic 마이그레이션 메모
- `gen_random_uuid()`를 쓰려면 `pgcrypto` extension이 필요하다.
- migration 시작 시 아래를 보장한다.

```sql
CREATE EXTENSION IF NOT EXISTS pgcrypto;
```

### audit_logs와의 차이
| 항목 | workflow_events | audit_logs |
|---|---|---|
| 목적 | 시각화/복원 | 보안/감사 |
| 단위 | workflow stage | 보안 이벤트 |
| UI 사용 | 높음 | 중간 |
| Mermaid 생성 | 직접 사용 | 보조 사용 |
| payload | 노드/엣지 복원 중심 | 감사 근거 중심 |

## 관련 문서
- [[Database_Schema]]
- [[Workflow_Log_Format]]
- [[Workflow_Service_Layer]]
- [[Workflow_API_Design]]
- [[Workflow_Pydantic_Models]]

## 참고 자료
- [[References]]
> [!warning] Deprecated  
> Superseded by: [[Layered_Runtime_and_Data_Flow]]
