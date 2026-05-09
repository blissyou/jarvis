# OpenClaw Gateway Voice Adapter
#openclaw #gateway #voice-layer #electron #fastapi #adapter

## Status
Active design target. Implementation pending.

## Purpose
Define how JARVIS Voice Layer sends recognized speech to OpenClaw and receives assistant responses without using the legacy JARVIS model router.

This document is the bridge between:
- [[JARVIS_Voice_Layer_Strategy]]
- [[Voice_STT_Accuracy_Latency_Plan]]
- [[Voice_Runtime_Design]]
- OpenClaw Gateway runtime behavior

## Design Principle
JARVIS should treat OpenClaw as the source of truth for assistant turns.

JARVIS may own voice capture, STT, transcript display, TTS, and HUD state, but it must not independently decide tool execution, approvals, memory, or model routing when OpenClaw can do so.

## Target Flow
```text
1. User presses MIC in Electron HUD
2. Electron records audio
3. JARVIS Voice Layer API transcribes audio
4. HUD displays transcript
5. User confirms transcript if needed
6. JARVIS sends transcript to OpenClaw Gateway session
7. OpenClaw processes the turn
8. JARVIS receives final assistant text and/or approval-pending state
9. HUD displays response, tool state, and approval cards
10. JARVIS streams TTS only for safe visible assistant text
```

## Component Responsibilities
| Component | Responsibility |
|---|---|
| Electron renderer | microphone UX, transcript display, approval cards, TTS toggle |
| Electron main/preload | safe bridge for local desktop capabilities |
| JARVIS Voice Layer API | STT, TTS, transcript shaping, optional localhost-only aggregation |
| OpenClaw Gateway | sessions, assistant turn execution, tools, approvals, memory, channels |
| OpenClaw workspace | behavior rules, skills, memory, project context |

## Required Configuration
The adapter should read these values from environment/config:

| Name | Required | Purpose |
|---|---|---|
| `OPENCLAW_GATEWAY_URL` | yes | Gateway websocket/http base URL, usually local |
| `OPENCLAW_GATEWAY_TOKEN` | yes when auth enabled | Gateway auth token |
| `JARVIS_OPENCLAW_SESSION_TARGET` | no | Existing session key or routing target |
| `JARVIS_VOICE_CONFIRM_RISKY_TRANSCRIPTS` | no | Whether risky transcripts require user confirmation before dispatch |
| `JARVIS_TTS_ON_APPROVAL_PENDING` | no | Should default to short pending notice only |

Secrets must not be exposed to the renderer. Tokens should stay in the backend or secure preload/main process boundary.

## Message Contract
The adapter should produce a normalized request object before sending to OpenClaw:

```json
{
  "source": "jarvis_voice_layer",
  "inputMode": "voice",
  "transcript": "자비스 깃 상태 확인해줘",
  "transcriptMeta": {
    "sttProvider": "faster-whisper",
    "profile": "balanced",
    "model": "small",
    "language": "ko",
    "durationSeconds": 3.2,
    "latencyMs": 1240
  },
  "safety": {
    "confirmedByUser": true,
    "riskyTranscript": false
  },
  "ui": {
    "wantsTts": true,
    "surface": "desktop_hud"
  }
}
```

OpenClaw-facing text should include the transcript as the user message. Metadata can be attached through the adapter layer or maintained locally for telemetry if Gateway support is not available.

## Response Contract
JARVIS HUD needs a normalized response shape:

```json
{
  "status": "completed | awaiting_approval | failed | blocked",
  "visibleText": "응답 텍스트",
  "speakableText": "음성 출력용 정리 텍스트",
  "approval": {
    "required": false,
    "id": null,
    "summary": null
  },
  "toolActivity": [],
  "error": null
}
```

Rules:
- `visibleText` is what the user sees.
- `speakableText` must remove markdown, code fences, large tables, and internal metadata.
- If `status` is `awaiting_approval`, TTS must say only that approval is needed, not that the action completed.
- If OpenClaw returns an error, the HUD should show it plainly and TTS should use a short safe summary.

## Transcript Risk Gate
Before dispatching a transcript to OpenClaw, JARVIS should classify whether user confirmation is needed.

Require confirmation if transcript includes:
- delete/remove/overwrite semantics
- shell or script execution
- file write/move/rename
- email/message/send/post actions
- calendar/reminder creation
- credentials, tokens, or secrets
- payments, transfers, orders, trades, or financial execution terms
- low-confidence or malformed STT output

For financial transaction requests, JARVIS should preserve the transcript and let OpenClaw policy block or refuse. It must not rephrase into an executable instruction.

## Implementation Decision
Use **Option A - Backend Adapter** for the first implementation.

Reason:
- it keeps Gateway tokens out of the browser renderer
- it centralizes transcript safety gates and benchmark telemetry
- it lets Electron remain a focused HUD rather than a Gateway protocol client

The Electron main-process adapter can be revisited only after the backend adapter is stable and measured.

## Implementation Options
### Option A - Backend Adapter
Electron sends transcript to JARVIS FastAPI. FastAPI talks to OpenClaw Gateway.

Pros:
- Gateway token stays out of renderer.
- Easier telemetry and transcript safety gates.
- Simple to add benchmark metadata.

Cons:
- Keeps FastAPI in the path.

Recommended for first implementation.

### Option B - Electron Main Process Adapter
Electron main/preload talks to OpenClaw Gateway directly.

Pros:
- Lower latency.
- Less backend surface.

Cons:
- More care needed around token storage and IPC boundaries.

Good future option after the backend adapter is stable.

## Session Policy
Default to one persistent desktop voice session target, configured by `JARVIS_OPENCLAW_SESSION_TARGET`.

Rationale:
- preserves conversational continuity across voice turns
- makes HUD history easier to reason about
- avoids fragmenting memory/session context per utterance

If no explicit session target is configured, the adapter should use the current OpenClaw default session behavior and log which session was used.

## Minimal MVP Endpoint Shape
If using FastAPI as backend adapter, add:

```text
POST /openclaw/voice-turn
```

Request:
```json
{
  "transcript": "...",
  "transcript_meta": {},
  "confirmed_by_user": true,
  "wants_tts": true
}
```

Response:
```json
{
  "status": "completed",
  "visible_text": "...",
  "speakable_text": "...",
  "approval": null,
  "error": null
}
```

## Acceptance Criteria
- A typed or spoken Korean prompt from the HUD reaches an OpenClaw session.
- Ollama is not required for the turn to complete.
- OpenClaw approval-pending state appears as a HUD approval card.
- TTS never announces an approval-required action as completed.
- Transcript metadata is recorded locally for STT benchmark and debugging.
- Gateway token is not exposed in browser renderer state.
- Failure modes are visible and recoverable from the HUD.

## Test Cases
| Case | Expected Result |
|---|---|
| "엘리스 지금 상태 알려줘" | transcript sent to OpenClaw, normal response spoken |
| "이 파일 삭제해줘" | transcript confirmation and/or OpenClaw approval required |
| "이 내용 이메일로 보내" | approval-pending state shown, no completion TTS before approval |
| "엔비디아 십 주 매수해줘" | financial execution blocked/refused, not approval-gated as executable |
| Gateway unavailable | HUD shows reconnect/error state, no fake completion |
| STT malformed transcript | ask user to repeat or confirm before dispatch |

## Implementation Discovery Step
Before coding the adapter, verify the current OpenClaw Gateway client surface against the installed OpenClaw docs/source.

Record the chosen method in this document or a follow-up implementation note:
- websocket/RPC session send
- HTTP/session API
- local CLI bridge for an initial proof
- future dedicated SDK if available

Do not guess protocol details in code. The adapter contract in this document is JARVIS-side; the OpenClaw-facing transport must be confirmed against the installed version.

## Remaining Open Question
- Should approval cards deep-link to OpenClaw Control UI, support inline HUD approval, or both?

## Related Documents
- [[JARVIS_Voice_Layer_Strategy]]
- [[Voice_STT_Accuracy_Latency_Plan]]
- [[Voice_Runtime_Design]]
- [[OpenClaw_Migration_Plan]]
- [[Voice_Layer_Implementation_Readiness]]
- [[Desktop_UI_Spec]]
