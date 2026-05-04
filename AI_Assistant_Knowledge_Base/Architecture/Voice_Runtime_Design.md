# Voice Runtime Design
#voice #stt #tts #latency #ux

## Purpose
Define the practical voice pipeline for JARVIS, including local and cloud options, latency targets, fallback behavior, and MVP constraints.

## Voice Scope
Voice is an input and output layer. It must not bypass the same agent, policy, approval, and execution layers used by text requests.

## Pipeline
```text
Microphone
-> VAD / push-to-talk
-> STT
-> Transcript normalization
-> Agent Runtime
-> Tool or chat result
-> TTS
-> Speaker
```

## Runtime Modes
| Mode | Stack | When To Use |
|---|---|---|
| Local economy | whisper.cpp + Piper | KRW 5,000 budget, privacy-first, slower but cheap |
| Hybrid balanced | Local STT + cloud LLM + local/cloud TTS | Good default for desktop assistant |
| Cloud realtime | Realtime voice API | Best UX, highest cost risk |

## MVP Defaults
- Use push-to-talk before wake word detection.
- Show transcript before executing any confirm-required action.
- Require explicit approval for commands inferred from noisy audio.
- Prefer text confirmation for email, calendar, file write, shell, and network write actions.

## Latency Targets
| Stage | Target |
|---|---:|
| End-of-speech detection | Less than 800 ms |
| STT final transcript | Less than 2.5 seconds for short commands |
| Agent classification | Less than 1.5 seconds |
| Read-only tool response | Less than 8 seconds |
| TTS start after final answer | Less than 1 second |

## Transcript Confidence Policy
| Condition | Behavior |
|---|---|
| Low STT confidence | Ask a clarification question |
| Contains recipient, amount, deletion, or command execution | Show transcript and require confirmation |
| Background speech detected | Do not execute; ask user to repeat |
| Ambiguous entity match | Ask user to choose or type the value |

## Voice-Specific Failure Cases
| Failure | Mitigation |
|---|---|
| Misheard recipient | Confirm recipient in approval card |
| Misheard file path | Require file picker or typed path for writes |
| Long rambling input | Summarize inferred intent and ask for confirmation |
| Wake word false positive | MVP avoids wake word; push-to-talk only |

## Interaction Points
- Agent runtime: [[Agent_Runtime]]
- Approval model: [[Permission_and_Approval_Model]]
- Cost limits: [[Cost_and_Budget_Model]]
- UI state: [[Layered_Runtime_and_Data_Flow]]
