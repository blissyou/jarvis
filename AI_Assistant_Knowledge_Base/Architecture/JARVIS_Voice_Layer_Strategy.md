# JARVIS Voice Layer Strategy
#jarvis #voice-layer #openclaw #stt #tts #latency #cost

## Status
Active direction as of 2026-05-09.

## Purpose
Define the new product direction: JARVIS is no longer a parallel local LLM runtime. JARVIS becomes a high-quality, low-latency voice interface for OpenClaw.

The goal is a high value personal assistant by combining:
- OpenClaw for intelligence, tools, approvals, sessions, channels, memory, and automation
- JARVIS for microphone capture, speech recognition, transcript UX, speech output, and a focused desktop HUD

## Strategic Decision
JARVIS should stop optimizing around Ollama/local model routing as the core product. OpenClaw is the runtime and model execution layer. JARVIS should optimize only the voice experience around that runtime.

In practice:
- Remove Ollama as a required JARVIS dependency.
- Retire the custom model router from the active architecture.
- Keep FastAPI only where it provides voice-specific value.
- Connect the Electron HUD to OpenClaw Gateway for actual assistant turns.
- Spend engineering effort on STT accuracy, response latency, TTS quality, and confirmation UX.

## Target Architecture
```text
User voice
-> JARVIS Electron HUD
-> Voice Layer API
   -> VAD / push-to-talk / recording lifecycle
   -> STT
   -> transcript normalization and confirmation policy
-> OpenClaw Gateway
   -> agent runtime
   -> tools
   -> approvals
   -> memory and sessions
   -> model providers
-> JARVIS Voice Layer API
   -> response text shaping for speech
   -> TTS stream
-> Speaker / transcript UI
```

## Responsibility Split
| Area | Owner | Notes |
|---|---|---|
| Agent reasoning | OpenClaw | JARVIS should not duplicate this. |
| Tool execution | OpenClaw | Includes approvals and safety gates. |
| Sessions/history | OpenClaw | JARVIS displays state but is not source of truth. |
| Background tasks | OpenClaw | Cron, heartbeat, taskflow-style work. |
| Messaging channels | OpenClaw | Telegram and future channels remain runtime concerns. |
| Microphone capture | JARVIS | Desktop product experience. |
| STT | JARVIS | Main optimization surface. |
| Transcript UX | JARVIS | Show what was heard before risky actions. |
| TTS | JARVIS | Voice persona and output quality. |
| HUD | JARVIS | Fast, focused, low-friction desktop interface. |

## Non-Goals
- JARVIS does not build a second OpenClaw.
- JARVIS does not maintain an independent long-term memory system.
- JARVIS does not require Ollama for MVP operation.
- JARVIS does not execute tools directly when OpenClaw can execute them with approvals.
- JARVIS does not execute financial transactions, payments, orders, trades, or transfers.

## Why This Improves Cost Performance
The expensive part of building a personal assistant is not only model inference. It is the runtime: sessions, tools, permissions, background tasks, recovery, channels, and safety. OpenClaw already provides those surfaces.

By narrowing JARVIS to voice quality:
- local compute is spent on STT/TTS rather than local LLM inference
- fewer duplicate services must be maintained
- model cost and quality are controlled by OpenClaw configuration
- the user gets a premium voice interface over a mature runtime

## Active Engineering Priorities
1. Improve Korean STT accuracy and measure latency.
2. Build a repeatable voice benchmark harness.
3. Keep TTS cheap and natural, using Edge TTS unless a better option is proven.
4. Replace FastAPI session/model-router assumptions with OpenClaw Gateway messaging.
5. Preserve transcript confirmation before risky or ambiguous actions.
6. Remove or mark legacy Ollama/local-routing documents as non-active.

## Acceptance Criteria
JARVIS Voice Layer is successful when:
- A Korean short command is transcribed accurately enough for safe routing.
- The user sees the transcript before risky action execution.
- The desktop HUD sends the transcript to OpenClaw, not to a custom local agent runtime.
- OpenClaw approval-required actions appear as pending, never as completed.
- TTS begins quickly after OpenClaw produces the final answer.
- JARVIS can run without Ollama installed.
- Implementation readiness passes [[Voice_Layer_Implementation_Readiness]].

## Definition Of Done
The Voice Layer MVP is not done until:
- STT profile config exists and can be changed without code edits.
- Benchmark output exists for `fast`, `balanced`, and `accurate` profiles.
- Gateway adapter sends at least one typed and one spoken Korean turn to OpenClaw.
- HUD shows completed, failed, blocked, and awaiting-approval states distinctly.
- High-risk transcript cases are covered by negative tests.
- README, [[Master_Index]], and [[Legacy_Documentation_Index]] still point users away from legacy runtime paths.

## Related Documents
- [[OpenClaw_Migration_Plan]]
- [[OpenClaw_Runtime_Architecture]]
- [[Voice_STT_Accuracy_Latency_Plan]]
- [[OpenClaw_Gateway_Voice_Adapter]]
- [[Voice_Runtime_Design]]
- [[Desktop_UI_Spec]]
- [[Voice_Layer_Implementation_Readiness]]
- [[Legacy_Documentation_Index]]
