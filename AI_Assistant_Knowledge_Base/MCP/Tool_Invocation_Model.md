> Legacy note: This document is preserved for historical context. The active direction is [[JARVIS_Voice_Layer_Strategy]].

# Tool Invocation Model
#mcp #tools #json #protocol

## Purpose
Define the invocation contract between the agent runtime and MCP-style tools.

## MCP Role in JARVIS
MCP is the extensibility layer. It lets JARVIS connect the agent to structured tools, resources, and prompts using a standard client/server protocol. The official MCP SDK page states that official SDKs support building servers and clients with tools, resources, prompts, and local/remote transports. [MCP SDK docs](https://modelcontextprotocol.io/docs/sdk)

## Invocation Steps
1. Agent selects tool by capability and policy
2. MCP broker resolves tool metadata from the registry
3. Broker validates JSON arguments against the tool schema
4. Broker invokes the tool over the chosen transport
5. Result is normalized into a shared envelope
6. Agent summarizes result for the user or chains additional steps

## Tool Call Envelope
```json
{
  "tool_name": "stocks.get_quote",
  "server": "market-data",
  "transport": "stdio",
  "arguments": {
    "symbol": "AAPL",
    "currency": "USD"
  },
  "timeout_seconds": 15
}
```

## Result Envelope
```json
{
  "status": "ok",
  "tool_name": "stocks.get_quote",
  "data": {
    "symbol": "AAPL",
    "price": 212.14,
    "change_percent": 1.2
  },
  "metadata": {
    "latency_ms": 241,
    "server": "market-data"
  }
}
```

## JSON and Function-Calling Compatibility
The agent layer should internally treat MCP tools as function-call targets:
- name
- description
- JSON schema for arguments
- structured result envelope

This keeps local Ollama tool calls and OpenAI tool calls aligned with the same internal contract.

## Example Tools
- `news.search_headlines`
- `stocks.get_quote`
- `filesystem.read_text`
- `git.status_summary`
- `docker.list_containers`

## Interaction Points
- Registry details: [[Tool_Registry_Design]]
- Agent planner: [[Agent_Runtime]]
- Execution examples: [[Execution_Flows]]
- Security constraints: [[Permission_and_Approval_Model]]
