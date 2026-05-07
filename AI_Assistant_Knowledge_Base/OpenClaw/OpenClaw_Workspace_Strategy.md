# OpenClaw Workspace Strategy
#openclaw #workspace #obsidian #memory #skills

## Purpose
Define how the JARVIS Obsidian knowledge base should interact with the OpenClaw workspace model.

## Key Fact
OpenClaw uses one active agent workspace as the working directory and context home. That workspace normally contains bootstrap files such as `AGENTS.md`, `SOUL.md`, `USER.md`, `TOOLS.md`, `HEARTBEAT.md`, and memory files.

The JARVIS Obsidian vault is larger and more architectural. It should not be blindly injected into every prompt. Instead, it should be treated as a project knowledge source that can be read, summarized, and distilled into OpenClaw workspace rules.

## Recommended Layout
Keep the JARVIS repo and Obsidian vault where they are:

```text
~/Desktop/my_fucking_project/Project/jarvis/
  AI_Assistant_Knowledge_Base/
```

Keep OpenClaw workspace as the operational assistant home:

```text
~/.openclaw/workspace/
  AGENTS.md
  SOUL.md
  USER.md
  TOOLS.md
  HEARTBEAT.md
  memory/
```

Then add a `TOOLS.md` note pointing to the JARVIS repo and vault path.

## Why Not Make The Whole Vault The OpenClaw Workspace?
Reasons:
- the vault has many long architecture files
- bootstrap injection could become noisy and expensive
- Obsidian docs are project design, not always runtime instructions
- OpenClaw workspace may contain private memory and operational notes that should not be mixed into a public repo

## Distillation Rule
Use this hierarchy:

1. Obsidian vault = source of product architecture
2. OpenClaw workspace files = compact operational instructions
3. Daily memory = raw working notes
4. Long-term memory = curated user/project context

## What To Put In OpenClaw `AGENTS.md`
- JARVIS repo path
- approval rules for repo edits
- how to update Obsidian docs
- coding/test expectations
- migration priority

## What To Put In OpenClaw `TOOLS.md`
- local paths
- commands for running JARVIS
- Obsidian vault location
- preferred scripts
- Gmail/stock/news tool setup notes as they become real

## What To Put In `HEARTBEAT.md`
- check pending migration tasks
- check failing background tasks
- optionally summarize important unread project updates
- avoid noisy status pings

## Obsidian Maintenance Rules
- Preserve wikilinks like `[[OpenClaw_Migration_Plan]]`.
- Keep active architecture docs separate from legacy numeric folders.
- Add new OpenClaw-related docs under `OpenClaw/` or `Decisions/`.
- Update `00_Index/Master_Index.md` when adding canonical docs.
- Do not store secrets in the vault.

## Related Documents
- [[OpenClaw_Runtime_Architecture]]
- [[OpenClaw_Migration_Plan]]
- [[ADR_004_OpenClaw_Runtime_Adoption]]
- [[Memory_and_Privacy_Model]]
