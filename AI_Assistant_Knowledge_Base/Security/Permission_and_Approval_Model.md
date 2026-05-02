# Permission and Approval Model
#security #approval #permissions

## Purpose
Define the approval system for local actions, code execution, tool calls, and external side effects.

## Permission Classes
| Class | Examples | Default |
|---|---|---|
| `read_local` | read files, inspect logs, list directories | allow |
| `write_workspace` | modify files inside approved workspace | ask |
| `write_outside_workspace` | modify files elsewhere | deny unless explicit approval |
| `network_read` | external API fetch | ask or profile-based |
| `network_write` | upload/post/send | always ask |
| `system_admin` | install software, edit shell rc, change settings | always ask |

## Approval Envelope
```json
{
  "approval_id": "appr_01JARVIS",
  "risk_level": "high",
  "action_summary": "Run generated Python code in a Docker sandbox",
  "scope": {
    "workspace": "/Users/alex/project",
    "network": false,
    "writes": [
      "/Users/alex/project/tmp"
    ]
  }
}
```

## Approval Rules
- Read-only local analysis can auto-run
- Writes inside the chosen workspace require approval unless user profile explicitly relaxes it
- Host actions outside workspace always require approval
- External data exfiltration always requires approval

## Interaction Points
- Security overview: [[Security_Model]]
- Sandbox execution: [[Docker_Isolation_Strategy]]
- Agent risk classification: [[Agent_Runtime]]
