# API and Tool Contracts
#api #tools #mcp #schemas #contracts

## Purpose
Define stable request, tool, approval, and result contracts used between the UI, FastAPI backend, agent runtime, MCP broker, and execution runtime.

## Contract Principle
The model may propose tool calls, but typed application code validates and executes them. Tool outputs must be normalized before returning to the agent.

## Request Envelope
```json
{
  "session_id": "sess_01JARVIS",
  "request_id": "req_01JARVIS",
  "input": {
    "mode": "voice",
    "text": "Draft an email to Min saying I will be late",
    "transcript_confidence": 0.91
  },
  "workspace": {
    "cwd": "C:/Users/PC/Desktop/project/jarvis",
    "selected_files": []
  },
  "policy": {
    "approval_mode": "ask",
    "cloud_allowed": true,
    "network_allowed": "ask"
  }
}
```

## Tool Manifest
```json
{
  "tool_name": "gmail.create_draft",
  "risk_class": "network_write",
  "description": "Create a Gmail draft without sending it.",
  "input_schema": {
    "to": "string",
    "subject": "string",
    "body": "string"
  },
  "requires_approval": true,
  "idempotent": false
}
```

## Tool Result Envelope
```json
{
  "tool_name": "gmail.create_draft",
  "status": "succeeded",
  "changed_state": true,
  "summary": "Created a draft email to Min.",
  "artifacts": [
    {
      "type": "external_reference",
      "label": "Gmail draft",
      "uri": "gmail://drafts/123"
    }
  ],
  "raw": null
}
```

## Approval Contract
```json
{
  "approval_id": "appr_01JARVIS",
  "request_id": "req_01JARVIS",
  "risk_level": "medium",
  "action_summary": "Create a Gmail draft to Min",
  "tool_name": "gmail.create_draft",
  "preview": {
    "to": "min@example.com",
    "subject": "Running late",
    "body_excerpt": "I will be about 10 minutes late."
  },
  "expires_in_seconds": 300
}
```

## Validation Rules
- Reject unknown tool names.
- Reject arguments not matching schema.
- Reject path arguments outside the approved workspace unless policy permits.
- Reject hidden state changes in tools marked read-only.
- Require approval for every non-idempotent external side effect.

## API Surface
| Endpoint | Purpose |
|---|---|
| `POST /sessions` | Create a new agent session |
| `POST /sessions/{id}/turns` | Submit text or transcript input |
| `GET /sessions/{id}/events` | Stream event log |
| `POST /approvals/{id}/approve` | Approve a pending action |
| `POST /approvals/{id}/reject` | Reject a pending action |
| `GET /tools` | List registered tools and risk classes |
| `GET /budgets/current` | Show current budget state |

## Interaction Points
- Tool registry: [[Tool_Registry_Design]]
- Tool invocation: [[Tool_Invocation_Model]]
- Approval model: [[Permission_and_Approval_Model]]
- Runtime flow: [[Layered_Runtime_and_Data_Flow]]
