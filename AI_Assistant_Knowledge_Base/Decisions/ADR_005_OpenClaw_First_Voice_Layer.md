# ADR 005 - OpenClaw-First Voice Layer
#adr #openclaw #voice-layer #ollama #runtime

## Status
Accepted

## Purpose
Record the decision to make OpenClaw the only active assistant runtime for JARVIS and narrow JARVIS to a high-quality Voice Layer plus desktop HUD.

## Decision
JARVIS will use OpenClaw as the only active assistant runtime for the current direction. JARVIS will focus on becoming a high-quality voice layer and desktop HUD for OpenClaw.

Ollama and the custom JARVIS model router are no longer active MVP requirements. They may remain as legacy experiments or optional developer tools, but product architecture should not depend on them.

## Context
The previous architecture attempted to build a local-first desktop AI agent platform with:
- FastAPI orchestration
- custom model routing
- Ollama and LM Studio providers
- Open Interpreter execution
- MCP tool registry
- custom sessions, approvals, budgets, and tools

OpenClaw already provides many of these runtime surfaces. Maintaining a parallel JARVIS runtime increases complexity and slows the part the user actually wants improved: voice accuracy and speed.

The user direction is now:
- use OpenClaw only for assistant intelligence and execution
- stop relying on Ollama for the active product path
- invest in voice recognition accuracy, latency, and TTS experience
- preserve safety through OpenClaw approvals and transcript confirmation

## Consequences
### Positive
- Less duplicated runtime code.
- Faster path to a usable assistant.
- Better cost-performance by spending effort on STT/TTS rather than local LLM orchestration.
- OpenClaw remains the authority for approvals, sessions, tools, memory, channels, and background tasks.
- JARVIS can become a polished product shell instead of a fragile second runtime.

### Negative / Risks
- JARVIS becomes coupled to OpenClaw Gateway APIs and runtime behavior.
- Offline-only local LLM operation is no longer the default product promise.
- Existing Ollama/model-routing docs and code must be reclassified as legacy or optional.
- Voice accuracy becomes the main quality bottleneck.

## Implementation Rules
- New user-facing assistant turns should route to OpenClaw.
- FastAPI should only keep voice-specific or UI adapter endpoints unless a strong reason exists.
- The Electron HUD should display OpenClaw state and approval results.
- Voice transcripts are untrusted input and must preserve approval/confirmation gates.
- Documentation must list OpenClaw-first voice layer documents before older local-runtime documents.

## Supersedes / Changes
- Supersedes [[ADR_002_Model_Routing]] for the active MVP path.
- Narrows [[ADR_004_OpenClaw_Runtime_Adoption]] from proposed migration to active direction.
- Reclassifies Ollama/local model routing documents as legacy or optional.

## Acceptance Criteria
- Active JARVIS voice turns route to OpenClaw rather than the legacy model router.
- JARVIS can operate without Ollama installed.
- New documentation lists OpenClaw-first Voice Layer documents before custom-runtime documents.
- Legacy documents are preserved but clearly marked as non-active.
- Voice safety preserves transcript confirmation and OpenClaw approval boundaries.

## Related Documents
- [[JARVIS_Voice_Layer_Strategy]]
- [[Voice_STT_Accuracy_Latency_Plan]]
- [[OpenClaw_Gateway_Voice_Adapter]]
- [[OpenClaw_Migration_Plan]]
- [[OpenClaw_Runtime_Architecture]]
- [[Legacy_Documentation_Index]]
