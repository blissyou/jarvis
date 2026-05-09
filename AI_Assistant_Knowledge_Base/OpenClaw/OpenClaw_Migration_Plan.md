# OpenClaw Migration Plan
#openclaw #migration #roadmap #implementation

## Status
Active migration plan. Updated for the OpenClaw-first Voice Layer direction.

## Purpose
Define a practical migration plan for changing JARVIS from a custom local agent scaffold into an OpenClaw-powered assistant.

## Migration Principle
Use OpenClaw for the boring but difficult runtime layer. Keep JARVIS for the product experience, local workflows, voice interface, and opinionated personal-assistant behavior.

The target shape is **OpenClaw + JARVIS Voice Layer**:
- OpenClaw handles agent runtime, channels, approvals, tools, memory/workspace context, and background tasks.
- JARVIS Voice Layer handles microphone capture, STT, transcript UX, TTS, and the voice-first desktop feel.
- JARVIS skills package product-specific capabilities without rebuilding OpenClaw's runtime.

## Phase 0 - Inventory
Status: mostly complete

Inventory confirmed the important direction change: OpenClaw should own the assistant runtime, and JARVIS should narrow to a Voice Layer and HUD.

Tasks:
- Confirm OpenClaw Gateway runs locally.
- Confirm Telegram direct chat works.
- Confirm workspace location and bootstrap files.
- Compare JARVIS knowledge-base architecture against OpenClaw primitives.
- Identify custom FastAPI endpoints that duplicate OpenClaw.

Deliverables:
- this migration plan
- [[ADR_004_OpenClaw_Runtime_Adoption]]
- [[OpenClaw_Runtime_Architecture]]

## Phase 1 - Workspace Alignment
Goal: make OpenClaw understand JARVIS behavior without code changes.

Tasks:
- Create a JARVIS-specific OpenClaw workspace or map the existing workspace intentionally.
- Convert key product rules from the Obsidian vault into `AGENTS.md`, `SOUL.md`, `TOOLS.md`, and `HEARTBEAT.md`.
- Add project notes for the local JARVIS repo path.
- Define when the agent may read files, run commands, create docs, and ask for approval.

Acceptance checks:
- OpenClaw can answer questions about JARVIS design from workspace docs.
- OpenClaw can analyze the repo safely.
- OpenClaw can maintain the Obsidian vault without corrupting links.

## Phase 2 - Tool/Skill Mapping
Goal: replace mock tools with OpenClaw-native skills or first-class tool flows.

Current JARVIS mock/stub tools:
- `news.search_headlines`
- `stocks.get_quote`
- `gmail.create_draft`
- `git.status_summary`
- `filesystem.read_text`

Migration target:
| JARVIS tool | OpenClaw direction |
|---|---|
| filesystem.read_text | built-in read/file tools |
| git.status_summary | built-in exec/read or custom git skill |
| news.search_headlines | web search/fetch workflow or news skill |
| stocks.get_quote | finance/web workflow or market skill |
| gmail.create_draft | Gmail/Himalaya/gog-based skill with approval gate |

Acceptance checks:
- read-only tools work without unnecessary approval.
- network write tools require explicit approval.
- Gmail draft/send separation is preserved.
- tool results include source/timestamp where relevant.

## Phase 3 - Desktop HUD Integration
Goal: turn the Electron app into an OpenClaw client and remove active dependence on the legacy JARVIS model router.

Tasks:
- Replace direct assumptions about FastAPI orchestration with OpenClaw Gateway integration.
- Show session state, tool activity, and approval cards.
- Keep voice-first UI, but let OpenClaw own execution.
- Add a settings panel for current workspace, model, heartbeat, and channel status.
- Add the JARVIS Voice Layer as a thin STT/TTS and transcript wrapper around OpenClaw messages.
- Ensure voice output never implies an approval-required action has completed before OpenClaw approval is granted.

Acceptance checks:
- typed prompt from desktop reaches OpenClaw.
- approval-required action appears as an approval card.
- background task status is visible.
- failed tool calls are shown safely.
- spoken responses work for read-only answers and degrade to text when STT/TTS fails.
- approval-required actions are shown as cards and spoken as pending, not completed.

## Phase 4 - Retire Or Re-scope FastAPI
Goal: remove duplicated runtime code and keep FastAPI as the JARVIS Voice Layer adapter.

Active recommendation:
1. Keep FastAPI for microphone/STT/TTS, transcript shaping, and local HUD convenience endpoints.
2. Route actual assistant turns to OpenClaw Gateway.
3. Retire or quarantine custom sessions, approvals, tools, and model-router endpoints that duplicate OpenClaw.
4. Do not require Ollama for the active MVP path.

Legacy local model routing may remain for experiments, but it is not the product direction.

## Phase 5 - Production Hardening
Tasks:
- Enable appropriate sandboxing for risky work.
- Harden Telegram and owner allowlists.
- Define backup rules for workspace, knowledge base, and config.
- Add regression checks for approval bypass, destructive actions, and silent cloud escalation.
- Document recovery steps for Gateway/config/session failures.

## MVP Non-Goal: Payments And Financial Transactions
Financial data lookup remains allowed for informational briefings, but JARVIS must not execute or prepare money movement in the MVP.

Explicitly excluded from MVP:
- payments, transfers, remittances, and bill payment
- stock/crypto/FX order placement
- brokerage trading, portfolio rebalancing, or automated investment actions
- card, bank, wallet, or exchange actions that move funds or create financial obligations
- storing payment credentials beyond read-only API tokens required for informational data

Allowed MVP finance scope:
- read-only stock or market information
- source-linked market/news briefings
- clearly non-advisory summaries that do not claim to make investment decisions

## Migration Acceptance Criteria
- Desktop typed prompts and voice transcripts can reach an OpenClaw session.
- JARVIS no longer requires Ollama or the legacy model router for active MVP voice turns.
- Electron HUD can display normal responses, tool activity, failures, and approval-pending states.
- FastAPI endpoints that remain in the active path are voice-specific or adapter-specific.
- High-risk voice requests preserve transcript confirmation and OpenClaw approval behavior.
- Financial transaction requests are blocked or refused rather than converted into executable actions.
- [[Voice_Layer_Implementation_Readiness]] release gates pass before MVP completion.

## Immediate Next Actions
1. Implement STT profile configuration and benchmark `base`, `small`, and `medium` for Korean.
2. Build or extend voice loopback benchmarks for accuracy and latency.
3. Connect Electron/JARVIS Voice Layer transcript submission to OpenClaw Gateway using [[OpenClaw_Gateway_Voice_Adapter]].
4. Convert approval cards to reflect OpenClaw approval state.
5. Remove Ollama/model-router assumptions from the active voice path.
6. Decide whether the active OpenClaw workspace should stay at `~/.openclaw/workspace` or become a JARVIS-specific workspace.
7. Convert key knowledge-base rules into OpenClaw bootstrap files.

## Related Documents
- [[ADR_005_OpenClaw_First_Voice_Layer]]
- [[JARVIS_Voice_Layer_Strategy]]
- [[Voice_STT_Accuracy_Latency_Plan]]
- [[ADR_004_OpenClaw_Runtime_Adoption]]
- [[OpenClaw_Runtime_Architecture]]
- [[OpenClaw_Workspace_Strategy]]
- [[Evaluation_and_Acceptance]]
- [[Voice_Layer_Implementation_Readiness]]
- [[Legacy_Documentation_Index]]
