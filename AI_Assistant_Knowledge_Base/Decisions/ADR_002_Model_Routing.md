# ADR 002 - Model Routing
#adr #models #ollama #openai

## Status
Accepted

## Decision
JARVIS defaults to local inference through Ollama and only escalates to OpenAI when policy, quality, or task complexity requires it.

## Context
The system is privacy-first and offline-first, but local models vary in quality. The design must preserve local execution for sensitive work while still enabling high-reasoning fallback.

## Consequences
- Every turn includes a routing decision
- Logs must record provider choice
- Cloud escalation must be policy-controlled

## Related Documents
- [[Model_Routing_Logic]]
- [[Security_Model]]
