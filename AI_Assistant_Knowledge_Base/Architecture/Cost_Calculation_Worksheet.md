# Cost Calculation Worksheet
#cost #pricing #worksheet #budget

## Purpose
Provide a concrete worksheet for estimating monthly operating cost from model tokens, voice minutes, tool API usage, and scheduled automations.

## Formula
```text
monthly_cost =
  model_input_tokens_m / 1,000,000 * input_price
+ model_output_tokens_m / 1,000,000 * output_price
+ voice_minutes * voice_price_per_minute
+ external_api_subscription
+ automation_runs * average_run_cost
```

## Required Inputs
| Input | Example |
|---|---:|
| User turns per day | 50 |
| Cloud fallback rate | 20% |
| Average input tokens per cloud turn | 3,000 |
| Average output tokens per cloud turn | 800 |
| Voice minutes per day | 10 |
| Scheduled runs per month | 30 |
| External paid APIs | KRW 0 to 50,000 |

## Scenario Worksheet
| Scenario | Turns/Day | Cloud Rate | Voice | Expected Tier |
|---|---:|---:|---:|---|
| Local text MVP | 30 | 5% | none | KRW 5,000 or less |
| Balanced assistant | 50 | 20% | local STT/TTS | Around KRW 10,000 |
| Voice-heavy hybrid | 80 | 40% | cloud realtime | Around KRW 50,000 or higher |

## Runtime Counters
The implementation should track these counters:
- `cloud_input_tokens`
- `cloud_output_tokens`
- `local_model_calls`
- `cloud_model_calls`
- `voice_input_seconds`
- `voice_output_seconds`
- `tool_calls_by_name`
- `automation_runs_by_id`
- `estimated_cost_krw`

## Budget Enforcement
| Threshold | Behavior |
|---|---|
| 50% monthly budget | Show passive warning in settings |
| 80% monthly budget | Ask before cloud fallback |
| 100% monthly budget | Disable automatic cloud fallback |
| Per-turn cap exceeded | Stop and summarize partial result |

## Implementation Note
Prices change. Store provider prices in a local config file and update them manually or through a trusted pricing sync task. Do not hard-code prices into the agent planner.

## Interaction Points
- Budget policy: [[Cost_and_Budget_Model]]
- Model router: [[Model_Router_Design]]
- Evaluation: [[Evaluation_and_Acceptance]]
