# Voice Layer Implementation Readiness
#voice-layer #implementation #readiness #qa #openclaw

## Status
Active A+ readiness checklist for the OpenClaw-first Voice Layer implementation.

## Purpose
Convert the voice-layer architecture into an implementation-ready checklist with traceability from product goals to code changes, tests, and release gates.

This document should be used before starting implementation and again before marking the Voice Layer MVP complete.

## Readiness Standard
A document set is A+ only when a developer can answer these questions without asking for missing architecture context:

1. What is the active product direction?
2. Which runtime owns assistant turns?
3. Which files or components probably need implementation changes?
4. Which metrics determine whether STT/TTS is good enough?
5. Which safety cases block release?
6. Which legacy paths must not be used accidentally?
7. How is success verified?

## Traceability Matrix
| Goal | Source Document | Implementation Surface | Verification |
|---|---|---|---|
| OpenClaw owns assistant turns | [[ADR_005_OpenClaw_First_Voice_Layer]] | Electron/FastAPI adapter sends transcript to Gateway | voice turn reaches OpenClaw session |
| JARVIS owns STT/TTS/HUD | [[JARVIS_Voice_Layer_Strategy]] | `api/app/routers/voice.py`, Electron HUD | voice loopback and HUD smoke tests |
| STT is measurable | [[Voice_STT_Accuracy_Latency_Plan]] | `scripts/voice_stt_benchmark.py`, benchmark dataset | CSV/JSON benchmark report |
| Gateway integration is explicit | [[OpenClaw_Gateway_Voice_Adapter]] | `POST /openclaw/voice-turn` or Electron main adapter | typed and spoken prompts complete through OpenClaw |
| Risky transcript safety is preserved | [[Voice_Runtime_Design]] | transcript risk gate, approval card UI | destructive/send/financial tests do not execute silently |
| Legacy runtime is not active | [[Legacy_Documentation_Index]] | remove voice path dependency on model router/Ollama | run without Ollama installed |

## Implementation Work Breakdown
### 1. STT Profile Configuration
Likely files:
- `api/app/routers/voice.py`
- voice service module if introduced
- `.env.example` or setup docs

Required behavior:
- support `JARVIS_STT_PROFILE=fast|balanced|accurate`
- allow explicit model/device/compute overrides
- preload selected model when practical
- expose current profile in a health or diagnostics response

Verification:
- changing profile changes model config without code changes
- invalid profile fails with a clear error

### 2. STT Benchmark Harness
Likely files:
- `scripts/voice_stt_benchmark.py`
- `runtime/artifacts/voice-benchmarks/`
- optional checked-in fixture file for phrase metadata

Required behavior:
- run multiple profiles and samples
- compute latency, CER, WER, keyword recall, and risk keyword recall
- write CSV and JSON summary
- exit non-zero on hard-gate failure

Verification:
```text
python scripts/voice_stt_benchmark.py --profiles fast,balanced,accurate --runs 3
```

### 3. OpenClaw Gateway Adapter
Likely files:
- `api/app/main.py`
- `api/app/routers/openclaw.py` or equivalent
- Electron service/client layer
- config/env loading

Required behavior:
- accept normalized voice-turn requests
- keep Gateway token out of the renderer
- forward transcript to OpenClaw session
- normalize completed, failed, blocked, and approval-pending responses

Verification:
- typed prompt from HUD reaches OpenClaw
- spoken prompt from HUD reaches OpenClaw after STT
- Gateway unavailable state is visible and recoverable

### 4. HUD Approval And TTS Safety
Likely files:
- Electron renderer components
- HUD state store
- TTS playback module

Required behavior:
- show transcript before risky dispatch
- show approval-pending state as a card
- do not speak approval-required actions as completed
- strip code fences/tables/internal metadata from speakable text

Verification:
- email/send/delete/shell/trade phrases do not produce fake completion audio

## Release Gate Checklist
Before marking the Voice Layer MVP complete:

- [ ] OpenClaw Gateway is the only active assistant-turn destination.
- [ ] JARVIS can complete a read-only voice query without Ollama installed.
- [ ] STT benchmark report exists for fast, balanced, and accurate profiles.
- [ ] Chosen default STT profile meets [[Voice_STT_Accuracy_Latency_Plan]] gates.
- [ ] Risk keyword recall is 100% on high-risk benchmark phrases.
- [ ] Destructive, network-write, shell, and financial tests do not execute silently.
- [ ] HUD displays approval-pending and failure states distinctly.
- [ ] TTS speaks only safe visible text or short pending/error summaries.
- [ ] README and [[Master_Index]] still list active docs before legacy docs.

## Negative Release Gates
Any of these blocks release:

- transcript sent to the legacy model router for normal assistant turns
- Ollama required for the active voice path
- Gateway token visible in renderer logs, browser devtools state, or frontend bundle
- TTS says an approval-required action completed before approval
- financial transaction phrasing becomes an executable instruction
- high-risk STT sample loses the core risk/action keyword
- missing benchmark report for the selected default profile

## A+ Documentation Gate
The documentation remains A+ only if:

- every active core doc has `Status`, `Purpose`, testability/acceptance criteria, and `Related Documents`
- every active implementation task maps to at least one verification step
- every safety-sensitive flow has at least one negative test
- legacy documents are visibly non-active
- link validation reports zero missing Obsidian links
- `git diff --check` reports no whitespace errors

## Related Documents
- [[JARVIS_Voice_Layer_Strategy]]
- [[Voice_STT_Accuracy_Latency_Plan]]
- [[OpenClaw_Gateway_Voice_Adapter]]
- [[Voice_Runtime_Design]]
- [[OpenClaw_Migration_Plan]]
- [[Evaluation_and_Acceptance]]
- [[Legacy_Documentation_Index]]
