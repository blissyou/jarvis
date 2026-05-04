# Desktop UI Spec
#ui #electron #approval #activity-log #voice-first

## Purpose
Define the MVP desktop UI required for a safe local AI agent. The UI must make agent state, tool execution, approvals, and cost visible.

## UI Strategy
JARVIS is voice-first, so the desktop UI should stay intentionally small. The primary screen is not a complex dashboard. It is a command surface that shows voice state, transcript, chat fallback, approvals, and execution trace.

The detailed visual and layout direction lives in [[Voice_First_Minimal_UI]].

## Primary Views
| View | Purpose |
|---|---|
| Voice Core | Shows listening, thinking, speaking, tool-running, and approval-needed states |
| Chat Console | Development fallback for typed commands and transcript correction |
| Activity Log | Model calls, tool calls, approvals, execution events |
| Approval Panel | Preview and approve risky actions |
| Workspace Picker | Select explicit workspace root |
| Settings | Providers, budget, integrations, privacy |

## MVP Layout
```text
Top Bar
Central Voice Core
Transcript Strip
Bottom Chat Console + Right Activity/Approval Panel
```

## Visual Direction
- Dark technical HUD mood.
- Cyan and teal accents.
- Minimal gauges, no dense decorative dashboard.
- Central circular voice state indicator.
- Compact panels for chat and logs.
- Clear approval cards that interrupt risky execution.

## Conversation Requirements
- Show text input and optional push-to-talk button.
- Show normalized transcript before execution.
- Show provider route indicator for cloud fallback.
- Show tool result cards with source and timestamp.
- Show error recovery messages with changed-state status.

## Voice Core Requirements
- Show current state as readable text.
- Use a circular indicator for idle, listening, thinking, speaking, and error states.
- Show last transcript near the core.
- Show current provider route only as a small status label.
- Do not require the user to inspect logs for normal voice use.

## Approval Card Requirements
Every approval card must show:
- action summary
- tool or execution profile
- risk level
- exact target path, recipient, URL, or command
- expected state change
- approve, reject, and edit actions
- expiry timer for stale approvals

## Activity Log Event Types
| Event | Required Fields |
|---|---|
| `model_call` | provider, route reason, estimated cost |
| `tool_call` | tool name, risk class, latency, status |
| `approval_requested` | risk level, preview, expiry |
| `approval_resolved` | approved or rejected, actor, time |
| `execution_started` | profile, workspace, network policy |
| `execution_finished` | status, changed state, artifacts |

## MVP UI Non-Goals
- No always-listening wake word UI.
- No autonomous background agent panel until scheduler policy exists.
- No hidden execution mode.
- No raw command execution button outside approval flow.
- No dense always-on HUD widget collection in the MVP.

## Interaction Points
- Minimal visual design: [[Voice_First_Minimal_UI]]
- Runtime data flow: [[Layered_Runtime_and_Data_Flow]]
- Approval model: [[Permission_and_Approval_Model]]
- Voice: [[Voice_Runtime_Design]]
- Cost: [[Cost_and_Budget_Model]]
