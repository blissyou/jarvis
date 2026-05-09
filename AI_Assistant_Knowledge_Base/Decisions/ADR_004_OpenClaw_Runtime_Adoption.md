# ADR 004 - OpenClaw Runtime Adoption
#adr #openclaw #runtime #agent-platform #migration

## Status
Accepted as baseline by [[ADR_005_OpenClaw_First_Voice_Layer]].

## Decision
JARVIS should pivot from building a fully custom agent runtime to using OpenClaw as the primary agent runtime, channel gateway, tool execution surface, session manager, and automation layer.

The JARVIS repository should become a product-specific desktop shell, knowledge base, voice layer, and local workflow layer on top of OpenClaw rather than duplicating OpenClaw's gateway, session, tool, memory, cron, channel, model, and agent orchestration capabilities.

## Context
The current architecture defines a custom stack:
- Electron + React desktop UI
- FastAPI orchestration backend
- custom Agent Runtime
- custom Model Router
- Open Interpreter execution runtime
- MCP tool registry
- Docker isolation
- SQLite/Postgres persistence

This is coherent, but it requires rebuilding many already-existing OpenClaw capabilities:
- agent workspace and bootstrap files
- Telegram and other channel routing
- local tool execution with approvals
- memory and session persistence
- cron and heartbeat automation
- sub-agent/background task execution
- skills/plugins
- model/provider configuration
- Control UI and gateway configuration

## OpenClaw Capabilities To Reuse
- `~/.openclaw/openclaw.json` for gateway, model, tool, channel, heartbeat, and automation config
- `agents.defaults.workspace` as the agent home and context root
- workspace files such as `AGENTS.md`, `SOUL.md`, `USER.md`, `TOOLS.md`, `HEARTBEAT.md`, and `memory/`
- built-in file, command, edit, web, image, cron, session, and sub-agent tools
- skills as the extension mechanism for domain-specific JARVIS tools
- Telegram/mobile messaging as an existing remote control surface
- cron and heartbeat for scheduled briefings, inbox checks, reminders, and background tasks
- Gateway Control UI for operational configuration

## Consequences
### Positive
- Faster MVP because runtime, channels, memory, approvals, and automation are already available.
- JARVIS can focus on user experience, voice/HUD UI, personal workflows, and custom skills.
- Telegram control, background jobs, and local command execution already work.
- The Obsidian knowledge base can directly guide OpenClaw workspace files and skills.

### Negative / Risks
- JARVIS becomes coupled to OpenClaw runtime behavior and config schema.
- Some existing FastAPI endpoints may become redundant or need to become thin adapters.
- The Electron desktop app must integrate with OpenClaw Gateway rather than assuming the FastAPI API is the sole backend.
- Existing Open Interpreter-centric documents need to be downgraded from core runtime baseline to optional execution backend research.

## Implementation Rule
Do not rewrite everything at once. Migrate in layers:
1. Treat OpenClaw as the operating runtime.
2. Treat JARVIS as the voice/HUD layer.
3. Convert JARVIS-specific behavior into workspace instructions and skills.
4. Keep Electron UI as the product shell.
5. Keep FastAPI only for STT/TTS, transcript UX, and product-specific APIs not provided by OpenClaw.
6. Remove Ollama/model-router dependencies from the active voice path.
7. Re-evaluate Open Interpreter after OpenClaw tool/skill coverage is mapped.

## Supersedes / Changes
- Partially supersedes [[ADR_003_Open_Interpreter_and_MCP]] as the default runtime decision.
- Keeps MCP as a possible tool interoperability strategy.
- Keeps Docker isolation as a security goal where OpenClaw sandboxing or external execution requires it.

## Related Documents
- [[ADR_005_OpenClaw_First_Voice_Layer]]
- [[JARVIS_Voice_Layer_Strategy]]
- [[Voice_STT_Accuracy_Latency_Plan]]
- [[OpenClaw_Runtime_Architecture]]
- [[OpenClaw_Migration_Plan]]
- [[OpenClaw_Workspace_Strategy]]
- [[Legacy_Documentation_Index]]
