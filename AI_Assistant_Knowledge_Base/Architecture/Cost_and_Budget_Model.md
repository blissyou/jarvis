# Cost and Budget Model
#cost #budget #models #voice #operations

## Purpose
Define how JARVIS controls monthly spend across local inference, cloud fallback, voice APIs, external tools, and long-running agent loops.

## Budget Principle
JARVIS must treat cost as a runtime policy, not as an after-the-fact billing surprise. Every model call, external API call, and agent loop consumes from a session budget and a monthly budget.

## Budget Tiers
| Monthly Budget | Default Runtime Profile | Expected Capability |
|---|---|---|
| KRW 5,000 or less | Local-first strict | Local chat, local STT/TTS, RSS summaries, limited cloud fallback |
| KRW 10,000 | Local-first balanced | Local default, cloud fallback for planning, email draft quality, error recovery |
| KRW 50,000 | Hybrid performance | Cloud model for complex tasks, better voice, frequent tool use, scheduled briefs |

## Cost Drivers
| Driver | Risk | Control |
|---|---|---|
| Multi-step agent loops | Repeated model calls can multiply token usage | Max steps per turn, planner budget, early stop |
| Realtime voice | Long sessions can cost more than text | Push-to-talk default, idle timeout, local STT option |
| Large document context | Long prompts increase input cost and latency | Chunking, retrieval, summaries, context caps |
| Tool retries | Failed APIs can trigger repeated calls | Retry limit, exponential backoff, circuit breaker |
| Scheduled automation | Daily jobs accumulate silently | Per-automation monthly cap |

## Runtime Budget Envelope
```json
{
  "budget_id": "budget_01JARVIS",
  "scope": "session",
  "max_model_calls": 8,
  "max_tool_calls": 12,
  "max_execution_seconds": 120,
  "max_cloud_tokens_input": 50000,
  "max_cloud_tokens_output": 10000,
  "max_estimated_cost_krw": 300
}
```

## Default Limits
| Limit | MVP Default |
|---|---|
| Model calls per user turn | 4 |
| Tool calls per user turn | 6 |
| Cloud fallback per turn | 1 |
| Agent loop depth | 3 |
| Realtime voice idle timeout | 20 seconds |
| Scheduled brief max runtime | 3 minutes |

## Model Routing Cost Rules
- Use local inference for file summaries, logs, private content, and low-risk Q&A.
- Use cloud fallback for ambiguous planning, failed local tool selection, or high-value generation such as email drafts.
- Never silently escalate private local content to cloud. Redact first or ask the user.
- Record provider, estimated tokens, and budget impact for every model call.

## Budget Failure Behavior
| Condition | Behavior |
|---|---|
| Session limit reached | Stop the agent loop and summarize partial progress |
| Monthly soft limit reached | Ask before cloud fallback |
| Monthly hard limit reached | Disable cloud calls except explicit override |
| Tool retry limit reached | Return a recoverable error with next action options |

## Implementation Notes
- Store budget counters in SQLite/Postgres and cache active counters in Redis.
- Estimate cost before a cloud call and reconcile after receiving usage metadata.
- Expose current session spend in the activity log.
- Treat scheduled automations as separate budget scopes.

## Interaction Points
- Model routing: [[Model_Routing_Logic]]
- Agent limits: [[Failure_Recovery_and_Budgets]]
- Runtime flow: [[Layered_Runtime_and_Data_Flow]]
- Evaluation: [[Evaluation_and_Acceptance]]
