# ADR 002 - Model Routing
#adr #models #ollama #openai

## Status
Legacy / Superseded for active MVP by [[ADR_005_OpenClaw_First_Voice_Layer]].

> Legacy note: This document is preserved for historical context. The active direction is [[JARVIS_Voice_Layer_Strategy]], where OpenClaw owns model execution and JARVIS focuses on STT/TTS/HUD.

## Decision
Historical decision: JARVIS defaults to local inference through Ollama and only escalates to OpenAI when policy, quality, or task complexity requires it.

Current active direction: JARVIS does not own model routing for the MVP. OpenClaw owns model execution and provider configuration.

## Context
The system is privacy-first and offline-first, but local models vary in quality. The design must preserve local execution for sensitive work while still enabling high-reasoning fallback.

## Consequences
- Every turn includes a routing decision
- Logs must record provider choice
- Cloud escalation must be policy-controlled

## Related Documents
- [[Model_Routing_Logic]]
- [[Security_Model]]
