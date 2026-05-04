# Memory and Privacy Model
#memory #privacy #pgvector #personalization

## Purpose
Define what JARVIS may remember, how memory is stored, how it is retrieved, and how privacy risks are controlled.

## Memory Principle
Long-term memory must be user-confirmed, inspectable, editable, and deletable. The agent must not silently convert every conversation into permanent memory.

## Memory Types
| Type | Example | Default |
|---|---|---|
| Session memory | Current task state, selected files, last tool result | Auto-store, expires |
| Preference memory | "Use concise Korean summaries" | Ask before storing |
| Project memory | Repo conventions, command notes | Ask or workspace-scoped |
| Sensitive memory | Credentials, tokens, private identifiers | Do not store |
| Derived memory | Summaries of repeated behavior | Suggest before storing |

## Storage Layout
| Store | Data |
|---|---|
| SQLite/Postgres | Memory metadata, scope, consent, timestamps |
| pgvector or local vector DB | Embeddings for approved text memories |
| File vault | User-editable memory notes when appropriate |
| Audit log | Creation, update, retrieval, deletion events |

## Memory Record
```json
{
  "memory_id": "mem_01JARVIS",
  "scope": "user",
  "type": "preference",
  "content": "Prefer Korean technical reports with tables.",
  "source_request_id": "req_01JARVIS",
  "consent": "explicit",
  "sensitivity": "low",
  "expires_at": null
}
```

## Retrieval Rules
- Retrieve only memories scoped to the current user and workspace.
- Do not retrieve sensitive or expired memories.
- Inject at most 5 memory snippets into a normal turn.
- Show memory usage in the activity log for transparency.
- Prefer exact project notes over fuzzy personal memories.

## Privacy Controls
| Risk | Control |
|---|---|
| Sensitive data stored accidentally | Secret scanner before memory write |
| Wrong memory affects future actions | User can inspect and delete memory |
| Cloud leakage | Memory snippets follow model routing privacy policy |
| Over-personalization | Low confidence memories require confirmation |

## MVP Memory Scope
- Store session state automatically.
- Store user preferences only after explicit confirmation.
- Do not implement autonomous behavioral profiling in MVP.
- Do not store secrets, passwords, OAuth tokens, or raw email bodies as long-term memory.

## Interaction Points
- Model routing: [[Model_Routing_Logic]]
- Security: [[Security_Model]]
- Evaluation: [[Evaluation_and_Acceptance]]
- Data flow: [[Layered_Runtime_and_Data_Flow]]
