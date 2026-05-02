# ADR 003 - Open Interpreter and MCP
#adr #interpreter #mcp #extensibility

## Status
Accepted

## Decision
JARVIS will use Open Interpreter as the core execution runtime and MCP as the standard tool-extension protocol.

## Context
The platform needs both local code execution and an extensible tool ecosystem. Open Interpreter addresses action execution; MCP addresses structured tool interoperability.

## Consequences
- Execution and tool access become separate layers
- Docker isolation becomes mandatory for generated code
- Tool authors can ship MCP servers without modifying the core agent planner

## Related Documents
- [[Open_Interpreter_Runtime]]
- [[Tool_Invocation_Model]]
- [[Tool_Registry_Design]]
- [[Docker_Isolation_Strategy]]
