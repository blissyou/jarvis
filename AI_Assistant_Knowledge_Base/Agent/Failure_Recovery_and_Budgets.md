# Failure Recovery and Budgets
#agent #recovery #budgets #reliability

## Purpose
Define how the agent stops, retries, asks for help, or falls back when planning, model calls, tools, or execution fail.

## Recovery Principle
The agent should fail closed for risky actions and fail helpfully for read-only actions. It should not keep retrying until cost or state becomes uncontrolled.

## Failure Classes
| Class | Example | Default Recovery |
|---|---|---|
| Model failure | timeout, invalid JSON, low confidence | Retry once with stricter schema, then ask user |
| Tool failure | API 401, rate limit, malformed result | Surface tool error and suggested fix |
| Execution failure | command non-zero exit | Stop and summarize stdout/stderr |
| Policy failure | denied permission | Explain blocked action and required approval |
| Budget failure | max steps or cost reached | Stop loop and summarize partial result |

## Agent Loop Limits
| Limit | Default |
|---|---:|
| Max planning attempts | 2 |
| Max execution attempts per step | 1 |
| Max total steps | 6 |
| Max cloud fallbacks | 1 |
| Max clarification questions | 2 |

## Retry Rules
- Retry read-only API calls at most twice.
- Do not retry `network_write`, file write, shell execution, or destructive actions without renewed approval.
- Do not change execution scope during retry.
- Do not broaden filesystem access automatically.

## Circuit Breakers
| Breaker | Trigger |
|---|---|
| Tool breaker | 3 failures for same tool in 5 minutes |
| Model breaker | 3 timeouts in 5 minutes |
| Execution breaker | 2 failed shell/code runs in same session |
| Cost breaker | 80% monthly soft budget reached |

## User-Facing Recovery Response
Every failed action should include:
- What was attempted
- Why it failed
- Whether anything changed
- What the safest next step is

## Structured Failure Envelope
```json
{
  "request_id": "req_01JARVIS",
  "failure_class": "tool_failure",
  "risk_level": "low",
  "changed_state": false,
  "retryable": true,
  "safe_next_action": "Reconnect the Gmail account and retry draft creation."
}
```

## Interaction Points
- Runtime owner: [[Agent_Runtime]]
- Cost policy: [[Cost_and_Budget_Model]]
- Evaluation: [[Evaluation_and_Acceptance]]
- Tool calls: [[Tool_Invocation_Model]]
