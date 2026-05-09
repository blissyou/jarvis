# Voice STT Accuracy And Latency Plan
#voice #stt #korean #latency #benchmark #openclaw

## Status
Active implementation specification.

## Purpose
Improve JARVIS voice accuracy and speed now that OpenClaw owns the assistant runtime. The Voice Layer should compete on speech quality, not on local LLM routing.

This document is not only a plan. It defines measurable benchmark inputs, output schemas, acceptance gates, and implementation tasks.

## Product Hypothesis
A high-value JARVIS can be built by combining:
- OpenClaw for reasoning and action
- high-quality Korean STT for input
- fast transcript confirmation for safety
- low-cost natural TTS for output

If STT accuracy is high and latency is predictable, the user experience feels premium even without a custom local LLM stack.

## Measurement Definitions
| Term | Definition |
|---|---|
| STT latency | elapsed milliseconds from audio file ready to transcript returned |
| End-to-transcript latency | elapsed milliseconds from recording stop to transcript visible in HUD |
| CER | character error rate between expected Korean text and transcript |
| WER | whitespace-token word error rate; useful but less reliable for Korean spacing |
| Keyword recall | required keywords found in transcript divided by expected required keywords |
| Risk keyword recall | required safety/action keywords found for risky commands |
| Pass | sample meets both latency and accuracy gates for its profile |

For Korean, CER and keyword recall are more important than WER because spacing differences can distort WER.

## Metrics And Gates
| Metric | Target | Hard Gate | Notes |
|---|---:|---:|---|
| Short command STT latency | <= 1.5s | <= 2.0s | 1-5 second utterances |
| Medium utterance STT latency | <= 3.0s | <= 4.0s | 5-12 second utterances |
| Short command CER | <= 8% | <= 12% | after normalization |
| Medium utterance CER | <= 12% | <= 18% | after normalization |
| Command keyword recall | >= 95% | >= 90% | action verbs and target nouns |
| Risk keyword recall | 100% | 100% | delete/send/trade/payment/shell terms |
| False execution from bad transcript | 0 | 0 | safety gate, not just STT gate |
| TTS start latency after OpenClaw answer | <= 1.0s | <= 1.5s | streaming preferred |

## STT Profiles
The implementation should support profile switching without code changes.

| Profile | Model | Compute | Beam | Best Of | Use Case |
|---|---|---|---:|---:|---|
| fast | faster-whisper base | int8 CPU | 1 | 1 | shortest commands, low latency |
| balanced | faster-whisper small | int8 CPU | 3 | 3 | expected default after benchmark |
| accurate | faster-whisper medium | int8 CPU | 3 | 3 | harder Korean, slower accuracy mode |

Environment mapping:

```text
JARVIS_STT_PROFILE=fast|balanced|accurate
JARVIS_STT_MODEL=base|small|medium
JARVIS_STT_DEVICE=cpu|cuda
JARVIS_STT_COMPUTE_TYPE=int8|float16|float32
JARVIS_STT_BEAM_SIZE=1|3|5
JARVIS_STT_BEST_OF=1|3|5
```

Profile defaults should apply only when explicit environment values are absent.

## Benchmark Dataset
Store benchmark phrase definitions as JSON or YAML, for example:

```json
[
  {
    "id": "status_001",
    "text": "엘리스 지금 컴퓨터 상태 알려줘",
    "category": "status",
    "risk": "low",
    "requiredKeywords": ["컴퓨터", "상태", "알려줘"],
    "forbiddenFailure": false
  }
]
```

Minimum dataset:

| ID | Text | Category | Risk | Required Keywords |
|---|---|---|---|---|
| status_001 | 엘리스 지금 컴퓨터 상태 알려줘 | status | low | 컴퓨터, 상태, 알려줘 |
| git_001 | 자비스 깃 상태 확인해줘 | developer | low | 깃, 상태, 확인 |
| gateway_001 | 오픈클로 게이트웨이 상태 확인해줘 | openclaw | low | 오픈클로, 게이트웨이, 상태 |
| read_001 | 이 파일은 삭제하지 말고 읽기만 해줘 | file_safety | medium | 파일, 삭제하지, 읽기 |
| reminder_001 | 내일 아침 아홉시에 알려줘 | reminder | medium | 내일, 아침, 아홉시, 알려줘 |
| finance_read_001 | 엔비디아 주식 브리핑만 해줘 | finance_readonly | medium | 엔비디아, 주식, 브리핑 |
| finance_block_001 | 엔비디아 십 주 매수해줘 | finance_block | high | 엔비디아, 십, 주, 매수 |
| send_001 | 이 내용을 민수에게 이메일로 보내줘 | network_write | high | 내용, 이메일, 보내줘 |
| shell_001 | 파워셸에서 깃 상태 명령어 실행해줘 | shell | high | 파워셸, 깃, 상태, 실행 |
| delete_001 | 다운로드 폴더에서 임시 파일 삭제해줘 | destructive | high | 다운로드, 임시, 파일, 삭제 |

## Benchmark Harness Specification
Create or extend a script such as:

```text
python scripts/voice_stt_benchmark.py --profiles fast,balanced,accurate --runs 3
```

Required behavior:
1. Load phrase dataset.
2. Generate repeatable Korean audio with TTS or load checked-in/manual samples.
3. Run STT for each profile and sample.
4. Measure latency with a monotonic clock.
5. Normalize expected text and transcript.
6. Compute CER, WER, keyword recall, and risk keyword recall.
7. Write CSV and JSON reports.
8. Exit non-zero if hard gates fail.

## Normalization Rules
Before scoring:
- trim whitespace
- collapse repeated whitespace
- normalize Korean punctuation variants
- remove filler punctuation that does not change intent
- preserve numbers, names, action verbs, and safety keywords
- do not over-normalize risky terms such as 매수, 매도, 삭제, 보내, 실행

## Report Output Schema
Reports should be written under:

```text
runtime/artifacts/voice-benchmarks/YYYYMMDD-HHMMSS/
```

### CSV Columns
```text
run_id,profile,sample_id,category,risk,expected_text,transcript,
latency_ms,audio_duration_ms,cer,wer,keyword_recall,risk_keyword_recall,
passed_latency,passed_accuracy,passed_safety,passed_overall,error
```

### JSON Summary
```json
{
  "createdAt": "2026-05-09T22:30:00+09:00",
  "profiles": {
    "balanced": {
      "samples": 10,
      "passRate": 0.95,
      "avgLatencyMs": 1320,
      "p95LatencyMs": 1880,
      "avgCer": 0.06,
      "keywordRecall": 0.97,
      "riskKeywordRecall": 1.0
    }
  },
  "failures": []
}
```

## Acceptance Gates
A profile can become default only if:
- overall pass rate >= 90%
- risk keyword recall = 100%
- p95 short-command latency <= 2.0s
- average CER <= 10%
- no high-risk sample loses the core action keyword

Recommended promotion path:
1. Run benchmark with synthetic TTS samples.
2. Run benchmark with at least 20 real microphone recordings from the target user.
3. Promote the best profile to default.
4. Keep previous profile as fallback.

## Transcript Safety Policy
The Voice Layer must not treat STT as trusted intent. It should pass a transcript to OpenClaw, but risky actions require confirmation and OpenClaw approval.

Rules:
- Always show the transcript in the HUD.
- If transcript contains deletion, shell execution, file write, sending messages, calendar changes, or financial terms, show confirmation/approval state clearly.
- If confidence is low or transcript is malformed, ask the user to repeat.
- Never speak as if an approval-required action has completed before OpenClaw confirms completion.
- Never rewrite a risky transcript into a more executable command.

## Speed Optimizations
- Preload STT model at startup.
- Keep the selected STT model warm.
- Use push-to-talk first; add VAD only after benchmark stability.
- Trim leading/trailing silence before STT.
- Cap max utterance duration for command mode.
- Stream TTS where possible.
- Speak a short acknowledgement only when it does not hide the real action state.

## OpenClaw Integration Requirements
The final pipeline should be:
```text
record audio -> STT -> transcript -> OpenClaw session message -> OpenClaw response -> TTS
```

Do not route the transcript into the legacy JARVIS model router for active MVP behavior. See [[OpenClaw_Gateway_Voice_Adapter]].

## Benchmark Dataset File Shape
Recommended fixture path:

```text
AI_Assistant_Knowledge_Base/Workflows/voice_stt_benchmark_dataset.example.json
```

Implementation may copy the fixture into `tests/fixtures/voice/` or `runtime/fixtures/voice/` when code is added.

Required fields:
| Field | Type | Required | Notes |
|---|---|---|---|
| `id` | string | yes | stable test case ID |
| `text` | string | yes | expected Korean phrase |
| `category` | string | yes | status, shell, finance, etc. |
| `risk` | low/medium/high | yes | drives safety gate |
| `requiredKeywords` | string[] | yes | must survive transcription |
| `riskKeywords` | string[] | high-risk cases | safety/action terms that must be recalled |
| `maxLatencyMs` | number | no | per-sample override |
| `notes` | string | no | implementation hints |

## Failure Triage
When a sample fails:

| Failure | First Action | Release Impact |
|---|---|---|
| latency only | compare fast/balanced profile and model warmup | block only if hard gate fails |
| CER high but keywords preserved | inspect transcript UX; may pass low-risk cases | warn unless repeated |
| required keyword missing | add confirmation or improve profile | block default promotion |
| risk keyword missing | fail safety gate | block release |
| malformed transcript | ask user to repeat; record artifact | block if frequent |

## Implementation Tasks
1. Add voice profile config: `JARVIS_STT_PROFILE=fast|balanced|accurate`.
2. Map profile to model, beam size, best_of, compute type.
3. Add phrase dataset file.
4. Add `scripts/voice_stt_benchmark.py`.
5. Write CSV and JSON benchmark reports.
6. Update voice loopback test to include safety-sensitive phrases.
7. Add OpenClaw Gateway message adapter.
8. Remove active Ollama dependency from the voice path.
9. Update docs and README after benchmark results.
10. Track readiness through [[Voice_Layer_Implementation_Readiness]].

## Related Documents
- [[JARVIS_Voice_Layer_Strategy]]
- [[OpenClaw_Gateway_Voice_Adapter]]
- [[Voice_Runtime_Design]]
- [[OpenClaw_Migration_Plan]]
- [[Voice_Layer_Implementation_Readiness]]
- [[Evaluation_and_Acceptance]]
