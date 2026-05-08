# JARVIS AI Agent Platform Knowledge Base
#agent-platform #desktop-ai #open-interpreter #mcp #docker #ollama #fastapi #electron

## Purpose
This vault is the system-of-record for JARVIS as a local-first desktop AI agent platform. It no longer describes a passive dashboard or a narrow voice assistant. It documents a production-oriented execution system that can understand requests, route models, invoke tools, run code, and operate safely on a developer workstation.

## What Changed
JARVIS previously leaned toward dashboard-style information display, news aggregation, and lightweight approval UX. That direction is deprecated. The new product direction is:

- A local AI operator for the user's machine
- A developer productivity agent for logs, terminals, builds, and debugging
- A platform that can be extended with MCP-compatible tools and plugins
- An offline-first architecture that can fall back to cloud models when required

The most important consequence is that documentation is now organized around execution boundaries rather than feature lists.

## Canonical Reading Order
1. [[Master_Index]]
2. [[OpenClaw_Runtime_Architecture]]
3. [[OpenClaw_Migration_Plan]]
4. [[OpenClaw_Architecture_Visual]]
5. [[OpenClaw_Workspace_Strategy]]
6. [[Platform_Architecture]]
6. [[Agent_Runtime]]
7. [[Open_Interpreter_Runtime]]
8. [[Tool_Invocation_Model]]
9. [[Docker_Isolation_Strategy]]
10. [[Security_Model]]
11. [[Execution_Flows]]
12. [[Model_Routing_Architecture]]
13. [[Model_Router_Design]]
14. [[Project_Structure]]
15. [[Scaling_Strategy]]
16. [[Cost_and_Budget_Model]]
17. [[Evaluation_and_Acceptance]]
18. [[Voice_Runtime_Design]]
19. [[Memory_and_Privacy_Model]]
20. [[Failure_Recovery_and_Budgets]]
21. [[API_and_Tool_Contracts]]
22. [[Windows_Host_Policy]]
23. [[OAuth_and_Secrets_Model]]
24. [[Persistence_and_Data_Model]]
25. [[First_Party_Tool_Schemas]]
26. [[Cost_Calculation_Worksheet]]
27. [[Test_Automation_Strategy]]
28. [[Desktop_UI_Spec]]
29. [[Voice_First_Minimal_UI]]
30. [[Local_Model_Benchmarking]]
31. [[Setup_and_Deployment]]

## OpenClaw Migration Note
The active migration direction is to evaluate OpenClaw as the runtime layer for JARVIS. Start with [[ADR_004_OpenClaw_Runtime_Adoption]], [[OpenClaw_Runtime_Architecture]], [[OpenClaw_Migration_Plan]], [[OpenClaw_Architecture_Visual]], and [[OpenClaw_Workspace_Strategy]] before extending the custom FastAPI/Agent Runtime scaffold.

## Vault Structure
- `Architecture/`
  - runtime layers, data flow, project structure, scaling
- `Agent/`
  - planning, routing, state management, guardrails
- `Interpreter/`
  - Open Interpreter integration and execution runtime
- `MCP/`
  - tool registry, invocation contract, examples
- `MCP/API_and_Tool_Contracts.md`
  - stable envelopes for requests, approvals, tools, and results
- `MCP/First_Party_Tool_Schemas.md`
  - concrete MVP schemas for filesystem, git, news, stocks, and Gmail tools
- `Architecture/Cost_and_Budget_Model.md`
  - runtime cost limits and budget failure behavior
- `Architecture/Cost_Calculation_Worksheet.md`
  - monthly cost worksheet and runtime counters
- `Architecture/Voice_Runtime_Design.md`
  - local and cloud voice pipeline constraints
- `Architecture/Memory_and_Privacy_Model.md`
  - long-term memory policy and privacy controls
- `Architecture/Persistence_and_Data_Model.md`
  - active SQLite/Postgres schema baseline
- `Architecture/Desktop_UI_Spec.md`
  - MVP desktop views, approval cards, and activity log events
- `Architecture/Voice_First_Minimal_UI.md`
  - voice-first HUD-inspired minimal UI and chat fallback design
- `Architecture/Setup_and_Deployment.md`
  - local development startup, health checks, and environment variables
- `Agent/Failure_Recovery_and_Budgets.md`
  - retry limits, circuit breakers, and fail-closed behavior
- `Agent/Local_Model_Benchmarking.md`
  - local model acceptance tests for routing and tool planning
- `Workflows/Evaluation_and_Acceptance.md`
  - release gates and golden test commands
- `Workflows/Test_Automation_Strategy.md`
  - automated unit, contract, integration, agent, and UI test plan
- `Docker/`
  - sandboxing, container lifecycle, isolation policies
- `Workflows/`
  - end-to-end execution flows and developer workflows
- `Security/`
  - permission gates, safe execution, filesystem policy
- `Security/Windows_Host_Policy.md`
  - Windows path, PowerShell, and host action restrictions
- `Security/OAuth_and_Secrets_Model.md`
  - token handling, OAuth scopes, and secret redaction
- `Decisions/`
  - refactor audit and architectural decisions

## Documentation Quality Rules
- Every document must define purpose, responsibilities, flow, and interaction points.
- No one-line notes, no vague brainstorming, no dashboard-era filler.
- Documents must link to upstream and downstream components.
- Design claims must trace back to official docs or explicit project assumptions.

## Legacy Note
The numeric folders from the previous vault iteration are retained only as historical material. They should not be treated as the active architecture baseline unless a new document explicitly links back to them for context.

## Related Documents
- [[Master_Index]]
- [[Documentation_Refactor_Audit]]
- [[Platform_Architecture]]
- [[Model_Routing_Architecture]]
- [[Security_Model]]
- [[Official_References]]
