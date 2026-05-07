# OpenClaw Migration Plan
#openclaw #migration #roadmap #implementation

## Purpose
Define a practical migration plan for changing JARVIS from a custom local agent scaffold into an OpenClaw-powered assistant.

## Migration Principle
Use OpenClaw for the boring but difficult runtime layer. Keep JARVIS for the product experience, local workflows, voice interface, and opinionated personal-assistant behavior.

## Phase 0 - Inventory
Status: active

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
Goal: turn the Electron app into an OpenClaw client.

Tasks:
- Replace direct assumptions about FastAPI orchestration with OpenClaw Gateway integration.
- Show session state, tool activity, and approval cards.
- Keep voice-first UI, but let OpenClaw own execution.
- Add a settings panel for current workspace, model, heartbeat, and channel status.

Acceptance checks:
- typed prompt from desktop reaches OpenClaw.
- approval-required action appears as an approval card.
- background task status is visible.
- failed tool calls are shown safely.

## Phase 4 - Retire Or Re-scope FastAPI
Goal: remove duplicated runtime code or make it a thin product adapter.

Options:
1. Remove most FastAPI runtime code and rely on OpenClaw Gateway.
2. Keep FastAPI only for UI-specific aggregation.
3. Keep FastAPI for experimental features but do not make it the source of truth.

Recommendation: choose option 2 only if the Electron HUD needs API shaping not available from OpenClaw.

## Phase 5 - Production Hardening
Tasks:
- Enable appropriate sandboxing for risky work.
- Harden Telegram and owner allowlists.
- Define backup rules for workspace, knowledge base, and config.
- Add regression checks for approval bypass, destructive actions, and silent cloud escalation.
- Document recovery steps for Gateway/config/session failures.

## Immediate Next Actions
1. Decide whether the active OpenClaw workspace should stay at `~/.openclaw/workspace` or become a JARVIS-specific workspace.
2. Create a JARVIS OpenClaw workspace profile if needed.
3. Convert key knowledge-base rules into OpenClaw bootstrap files.
4. Pick the first real skill to implement: Gmail, stocks, or Obsidian maintenance.

## Related Documents
- [[ADR_004_OpenClaw_Runtime_Adoption]]
- [[OpenClaw_Runtime_Architecture]]
- [[OpenClaw_Workspace_Strategy]]
- [[Evaluation_and_Acceptance]]
- [[First_Party_Tool_Schemas]]
