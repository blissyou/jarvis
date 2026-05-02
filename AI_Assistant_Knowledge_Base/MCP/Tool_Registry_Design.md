# Tool Registry Design
#mcp #registry #discovery #plugins

## Purpose
Define how JARVIS discovers, stores, and governs MCP-compatible tools.

## Registry Responsibilities
- Register first-party and third-party MCP servers
- Store tool schemas, trust levels, and execution constraints
- Support enable/disable by user or profile
- Separate tool discovery from invocation

## Registry Schema
```json
{
  "server_name": "market-data",
  "transport": "stdio",
  "entrypoint": "python -m mcp_servers.market_data",
  "trust_level": "external_read",
  "tools": [
    {
      "name": "stocks.get_quote",
      "description": "Fetch a real-time or delayed stock quote",
      "input_schema": {
        "type": "object",
        "properties": {
          "symbol": {
            "type": "string"
          }
        },
        "required": ["symbol"]
      },
      "risk_class": "read_only"
    }
  ]
}
```

## Trust Classes
- `local_read`
- `local_write`
- `external_read`
- `external_write`
- `admin`

## Discovery Model
- Static first-party registry file in the repo
- Optional sync with official MCP registry for discoverability only
- Manual approval before enabling external third-party servers

The official MCP Registry exists as a discovery surface, but enabling a server in JARVIS is a separate trust decision. [Official MCP Registry](https://registry.modelcontextprotocol.io/)

## Interaction Points
- Invocation semantics: [[Tool_Invocation_Model]]
- Security policy: [[Security_Model]]
- Plugin growth: [[Scaling_Strategy]]
- Decision record: [[ADR_003_Open_Interpreter_and_MCP]]
