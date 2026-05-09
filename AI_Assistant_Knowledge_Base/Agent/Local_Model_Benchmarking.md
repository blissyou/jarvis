> Legacy note: This document is preserved for historical context. The active direction is [[JARVIS_Voice_Layer_Strategy]].

# Local Model Benchmarking
#models #benchmark #lmstudio #ollama #routing

## Purpose
Define how JARVIS evaluates local models before trusting them for routing, planning, tool selection, and summarization.

## Benchmark Principle
Local models should earn capabilities through measured behavior. A model that is good at chat is not automatically safe for tool planning.

## Capability Matrix
| Capability | Test |
|---|---|
| Korean instruction following | Korean command set with expected structured output |
| Tool selection | Choose correct tool from 5 similar tools |
| JSON schema adherence | Return valid JSON for 50 cases |
| Local file summarization | Summarize logs without leaking unrelated content |
| Risk classification | Mark write/network/admin actions correctly |
| Recovery quality | Explain failed tool calls without inventing success |

## Minimum Scores
| Capability | MVP Minimum |
|---|---:|
| Valid JSON output | 95% |
| Correct read-only tool selection | 90% |
| Correct approval-required classification | 100% |
| Korean command understanding | 85% |
| Hallucinated tool result rate | 0% accepted |

## Routing Use
| Model Result | Allowed Use |
|---|---|
| Passes summarization only | Chat and summarization |
| Passes tool selection | Read-only tool planning |
| Passes risk classification | Approval pre-classification |
| Fails approval classification | Never route risky actions to this model alone |

## Benchmark Record
```json
{
  "model": "local-model-name",
  "provider": "ollama",
  "date": "2026-05-03",
  "json_valid_rate": 0.96,
  "tool_selection_rate": 0.91,
  "approval_classification_rate": 1.0,
  "allowed_capabilities": ["chat", "summarization", "read_only_tools"]
}
```

## Interaction Points
- Model routing: [[Model_Routing_Logic]]
- Router design: [[Model_Router_Design]]
- Evaluation: [[Evaluation_and_Acceptance]]
- Failure budgets: [[Failure_Recovery_and_Budgets]]
