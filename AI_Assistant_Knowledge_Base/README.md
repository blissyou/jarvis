# JARVIS Knowledge Base
#jarvis #openclaw #voice-layer #stt #tts #electron

## Status
Active vault entry point. Updated for the OpenClaw-first Voice Layer direction.

## Purpose
This vault is the system-of-record for JARVIS as an OpenClaw-first voice assistant product layer.

The active product direction is:

```text
JARVIS = high-quality Voice Layer + desktop HUD
OpenClaw = assistant runtime + model execution + tools + approvals + sessions + memory + automation
```

JARVIS should not duplicate OpenClaw runtime capabilities. It should make OpenClaw feel fast, natural, and safe through high-quality voice input/output and a focused desktop interface.

## Active Product Direction
- OpenClaw owns assistant reasoning, model providers, tools, approvals, sessions, memory, channels, and background tasks.
- JARVIS owns microphone capture, Korean STT accuracy, transcript UX, TTS quality, and the desktop HUD.
- JARVIS FastAPI remains only as a Voice Layer adapter where needed for STT, TTS, transcript shaping, and local UI convenience.
- Ollama, custom model routing, Open Interpreter, Docker execution, MCP registry design, and duplicated sessions/tools are legacy or optional research unless a new ADR reactivates them.

## Canonical Reading Order
1. [[Master_Index]]
2. [[JARVIS_Voice_Layer_Strategy]]
3. [[Voice_STT_Accuracy_Latency_Plan]]
4. [[OpenClaw_Gateway_Voice_Adapter]]
5. [[Figma_Architecture_Diagram_Brief]]
6. [[Voice_Layer_Implementation_Readiness]]
7. [[ADR_005_OpenClaw_First_Voice_Layer]]
8. [[OpenClaw_Runtime_Architecture]]
9. [[OpenClaw_Migration_Plan]]
10. [[OpenClaw_Architecture_Visual]]
11. [[OpenClaw_Workspace_Strategy]]
12. [[Voice_Runtime_Design]]
13. [[Voice_First_Minimal_UI]]
14. [[Desktop_UI_Spec]]
15. [[Evaluation_and_Acceptance]]
16. [[Test_Automation_Strategy]]
17. [[Security_Model]]
18. [[Permission_and_Approval_Model]]
19. [[Windows_Host_Policy]]
20. [[OAuth_and_Secrets_Model]]
21. [[Memory_and_Privacy_Model]]
22. [[Cost_and_Budget_Model]]
23. [[Legacy_Documentation_Index]]

## Current Architecture Summary
The overall architecture should be drawn in Figma using [[Figma_Architecture_Diagram_Brief]].

Figma source: `<FIGMA_LINK_HERE>`

Image export target:

```markdown
![JARVIS OpenClaw-first Voice Architecture](assets/jarvis-openclaw-voice-architecture.png)
```

```text
User voice
-> Electron HUD
-> JARVIS Voice Layer API
   -> record / trim / STT / transcript confirmation
-> OpenClaw Gateway
   -> session message / reasoning / tools / approvals / memory
-> JARVIS Voice Layer API
   -> response shaping / TTS stream
-> Speaker + transcript UI
```

Note: add the exported PNG/SVG from Figma under `AI_Assistant_Knowledge_Base/assets/` when available.

## Active Implementation Priorities
1. Improve Korean STT accuracy and latency with measurable benchmarks.
2. Add configurable STT profiles: `fast`, `balanced`, `accurate`.
3. Connect JARVIS transcript submission to OpenClaw Gateway.
4. Reflect OpenClaw approval state in the Electron HUD.
5. Keep TTS cheap, natural, and streaming-first.
6. Track implementation through [[Voice_Layer_Implementation_Readiness]].
7. Remove active-path assumptions that require Ollama or the legacy model router.

## Vault Structure
- `00_Index/`
  - active navigation, starting points, and legacy references
- `Architecture/`
  - active Voice Layer architecture, OpenClaw integration, STT/TTS, HUD, setup, privacy, and cost documents
- `OpenClaw/`
  - runtime architecture, migration plan, workspace strategy, and diagrams
- `Decisions/`
  - ADRs and architectural decisions
- `Security/`
  - approval, host, OAuth, privacy, and safety policies
- `Workflows/`
  - evaluation, testing, and developer workflows
- `Legacy/`
  - index for older documents that are preserved but not active
- `Agent/`, `Interpreter/`, `MCP/`, `Docker/`, numeric folders
  - mostly legacy or research material unless linked from an active document

## Documentation Quality Rules
- Every active document must state status, purpose, responsibility boundaries, flow, acceptance criteria or testability, and related documents.
- Active docs should be implementation-directing, not vague brainstorming.
- Legacy docs must not be treated as source of truth unless a new ADR reactivates them.
- Design claims should trace to OpenClaw behavior, project assumptions, benchmark results, or official docs.

## Legacy Policy
Older custom-runtime documents are preserved under [[Legacy_Documentation_Index]]. They are useful for context but should not guide new implementation unless explicitly promoted by a new ADR.

## Related Documents
- [[Master_Index]]
- [[JARVIS_Voice_Layer_Strategy]]
- [[Voice_STT_Accuracy_Latency_Plan]]
- [[OpenClaw_Gateway_Voice_Adapter]]
- [[Figma_Architecture_Diagram_Brief]]
- [[Voice_Layer_Implementation_Readiness]]
- [[ADR_005_OpenClaw_First_Voice_Layer]]
- [[Legacy_Documentation_Index]]
