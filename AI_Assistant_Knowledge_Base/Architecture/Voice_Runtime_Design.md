# Voice Runtime Design
#voice #stt #tts #latency #ux #openclaw

## Status
Active. Updated for the OpenClaw-first Voice Layer direction.

## Purpose
Define the practical voice pipeline for JARVIS after the runtime pivot.

JARVIS is now the voice interface. OpenClaw is the assistant runtime. Voice must improve accuracy and speed without bypassing OpenClaw safety, approvals, and session ownership.

## Voice Scope
Voice is an input and output layer. It must not bypass the same agent, policy, approval, and execution layers used by text requests.

The active voice path is:
```text
Microphone
-> push-to-talk / VAD
-> STT
-> transcript display and normalization
-> OpenClaw Gateway session message
-> OpenClaw response / approval state
-> TTS stream
-> Speaker and transcript UI
```

## Runtime Ownership
| Responsibility | Owner |
|---|---|
| Microphone recording | JARVIS |
| STT | JARVIS |
| Transcript display | JARVIS |
| Assistant turn | OpenClaw |
| Tool execution | OpenClaw |
| Approvals | OpenClaw |
| Sessions and memory | OpenClaw |
| TTS | JARVIS |
| Desktop HUD | JARVIS |

## Active Runtime Mode
| Mode | Stack | When To Use |
|---|---|---|
| OpenClaw-first voice | JARVIS STT/TTS + OpenClaw Gateway | Default and active MVP path |
| Accuracy benchmark | Multiple faster-whisper profiles + reports | STT tuning and regression testing |
| Legacy local model | JARVIS model router + Ollama | Historical fallback only, not active product direction |

## MVP Defaults
- Use push-to-talk before wake word detection.
- Show transcript before executing any confirm-required action.
- Send assistant turns to OpenClaw, not the legacy model router.
- Require explicit approval for commands inferred from noisy audio.
- Prefer text confirmation for email, calendar, file write, shell, and network write actions.
- Block financial transactions rather than approval-gating them.

## STT Profile Direction
Use configurable voice profiles:

| Profile | Model | Goal |
|---|---|---|
| fast | faster-whisper base int8 | quick commands |
| balanced | faster-whisper small int8 | likely default after benchmark |
| accurate | faster-whisper medium int8 | harder Korean phrases |

See [[Voice_STT_Accuracy_Latency_Plan]] for benchmark details.

## Latency Targets
| Stage | Target |
|---|---:|
| End-of-speech detection | Less than 800 ms |
| STT final transcript for short command | Less than 1.5 seconds |
| STT final transcript for medium utterance | Less than 3 seconds |
| OpenClaw response dispatch | Gateway-dependent; do not duplicate runtime |
| TTS start after final answer | Less than 1 second |

## Transcript Confidence Policy
| Condition | Behavior |
|---|---|
| Low STT confidence | Ask a clarification question |
| Contains recipient, amount, deletion, or command execution | Show transcript and require confirmation/approval |
| Background speech detected | Do not execute; ask user to repeat |
| Ambiguous entity match | Ask user to choose or type the value |
| Financial transaction request | Block according to MVP policy |

## Voice-Specific Failure Cases
| Failure | Mitigation |
|---|---|
| Misheard recipient | Confirm recipient in approval card |
| Misheard file path | Require file picker or typed path for writes |
| Long rambling input | Summarize inferred intent and ask for confirmation |
| Wake word false positive | MVP avoids wake word; push-to-talk only |
| OpenClaw approval pending | Speak as pending, not complete |

## Acceptance Criteria
- Voice input reaches OpenClaw as a session message rather than the legacy JARVIS model router.
- Risky or low-confidence transcripts require confirmation before dispatch or approval before execution.
- Approval-pending actions are displayed and spoken as pending, not completed.
- JARVIS can run the voice path without Ollama installed.
- STT profiles and latency targets are measurable through [[Voice_STT_Accuracy_Latency_Plan]].
- Gateway adapter behavior follows [[OpenClaw_Gateway_Voice_Adapter]].

## Related Documents
- Active strategy: [[JARVIS_Voice_Layer_Strategy]]
- STT benchmark: [[Voice_STT_Accuracy_Latency_Plan]]
- Gateway adapter: [[OpenClaw_Gateway_Voice_Adapter]]
- Runtime owner: [[OpenClaw_Runtime_Architecture]]
- Migration plan: [[OpenClaw_Migration_Plan]]
- Approval model: [[Permission_and_Approval_Model]]
- UI state: [[Voice_First_Minimal_UI]]
