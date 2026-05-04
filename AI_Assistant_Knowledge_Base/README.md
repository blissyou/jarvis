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
2. [[Platform_Architecture]]
3. [[Agent_Runtime]]
4. [[Open_Interpreter_Runtime]]
5. [[Tool_Invocation_Model]]
6. [[Docker_Isolation_Strategy]]
7. [[Security_Model]]
8. [[Execution_Flows]]
9. [[Model_Routing_Architecture]]
10. [[Model_Router_Design]]
11. [[Project_Structure]]
12. [[Scaling_Strategy]]
13. [[Cost_and_Budget_Model]]
14. [[Evaluation_and_Acceptance]]
15. [[Voice_Runtime_Design]]
16. [[Memory_and_Privacy_Model]]
17. [[Failure_Recovery_and_Budgets]]
18. [[API_and_Tool_Contracts]]
19. [[Windows_Host_Policy]]
20. [[OAuth_and_Secrets_Model]]
21. [[Persistence_and_Data_Model]]
22. [[First_Party_Tool_Schemas]]
23. [[Cost_Calculation_Worksheet]]
24. [[Test_Automation_Strategy]]
25. [[Desktop_UI_Spec]]
26. [[Voice_First_Minimal_UI]]
27. [[Local_Model_Benchmarking]]
28. [[Setup_and_Deployment]]

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
