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

## Vault Structure
- `Architecture/`
  - runtime layers, data flow, project structure, scaling
- `Agent/`
  - planning, routing, state management, guardrails
- `Interpreter/`
  - Open Interpreter integration and execution runtime
- `MCP/`
  - tool registry, invocation contract, examples
- `Docker/`
  - sandboxing, container lifecycle, isolation policies
- `Workflows/`
  - end-to-end execution flows and developer workflows
- `Security/`
  - permission gates, safe execution, filesystem policy
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
