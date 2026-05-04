# Persistence and Data Model
#database #sqlite #postgres #audit #sessions

## Purpose
Define the active persistence model for sessions, turns, approvals, tools, budgets, memory, and audit events.

## Storage Strategy
| Stage | Store | Reason |
|---|---|---|
| MVP local dev | SQLite | Simple setup, enough for one-user desktop |
| Advanced local | Postgres | Better concurrency and migration discipline |
| Memory search | pgvector or local vector DB | Semantic retrieval for approved memories |
| Runtime cache | Redis optional | Useful for queues and streaming state |

## Core Tables
| Table | Purpose |
|---|---|
| `sessions` | Top-level user interaction sessions |
| `turns` | User inputs and agent outputs |
| `events` | Structured lifecycle and audit records |
| `approvals` | Pending and resolved approval requests |
| `tool_invocations` | Tool call input, result, latency, risk |
| `model_calls` | Provider, route reason, tokens, estimated cost |
| `budgets` | Session and monthly counters |
| `memories` | User-approved memory metadata |
| `connected_accounts` | Non-secret account metadata |

## Minimal SQL Shape
```sql
create table sessions (
  id text primary key,
  created_at text not null,
  workspace_root text,
  status text not null
);

create table turns (
  id text primary key,
  session_id text not null references sessions(id),
  input_mode text not null,
  user_text text not null,
  final_response text,
  created_at text not null
);

create table approvals (
  id text primary key,
  session_id text not null references sessions(id),
  turn_id text references turns(id),
  risk_level text not null,
  action_summary text not null,
  status text not null,
  preview_json text not null,
  created_at text not null,
  resolved_at text
);

create table events (
  id text primary key,
  session_id text not null,
  turn_id text,
  event_type text not null,
  risk_level text,
  payload_json text not null,
  created_at text not null
);
```

## Audit Event Requirements
Every state-changing operation must record:
- request ID or turn ID
- risk class
- actor component
- approved or denied status
- changed state flag
- result summary

## Data Retention Defaults
| Data | Default Retention |
|---|---|
| Session transcripts | Keep until user deletes |
| Audit events | Keep for 90 days locally |
| Tool raw results | Keep only if needed for traceability |
| OAuth tokens | Until integration is disconnected |
| Session memory | Expire with session |
| User-approved memory | Keep until edited or deleted |

## Migration Rule
All schema changes must be migration-based once implementation starts. Do not mutate production SQLite/Postgres schemas manually.

## Interaction Points
- API contracts: [[API_and_Tool_Contracts]]
- Memory: [[Memory_and_Privacy_Model]]
- Cost: [[Cost_and_Budget_Model]]
- Evaluation: [[Evaluation_and_Acceptance]]
