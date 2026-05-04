# First Party Tool Schemas
#mcp #tools #schemas #gmail #filesystem #git

## Purpose
Define MVP tool schemas for first-party JARVIS tools. These schemas are the starting point for MCP registration and model tool-call exposure.

## Risk Classes
| Risk Class | Meaning |
|---|---|
| `read_local` | Reads local workspace data |
| `write_workspace` | Writes within approved workspace |
| `network_read` | Fetches external data |
| `network_write` | Sends, uploads, posts, or changes remote state |
| `system_admin` | Changes system configuration or installed software |

## `filesystem.read_text`
```json
{
  "name": "filesystem.read_text",
  "risk_class": "read_local",
  "requires_approval": false,
  "input_schema": {
    "type": "object",
    "properties": {
      "path": { "type": "string" },
      "max_bytes": { "type": "integer", "default": 200000 }
    },
    "required": ["path"]
  }
}
```

## `filesystem.write_text`
```json
{
  "name": "filesystem.write_text",
  "risk_class": "write_workspace",
  "requires_approval": true,
  "input_schema": {
    "type": "object",
    "properties": {
      "path": { "type": "string" },
      "content": { "type": "string" },
      "overwrite": { "type": "boolean", "default": false }
    },
    "required": ["path", "content"]
  }
}
```

## `git.status_summary`
```json
{
  "name": "git.status_summary",
  "risk_class": "read_local",
  "requires_approval": false,
  "input_schema": {
    "type": "object",
    "properties": {
      "repo_path": { "type": "string" }
    },
    "required": ["repo_path"]
  }
}
```

## `news.search_headlines`
```json
{
  "name": "news.search_headlines",
  "risk_class": "network_read",
  "requires_approval": false,
  "input_schema": {
    "type": "object",
    "properties": {
      "query": { "type": "string" },
      "limit": { "type": "integer", "default": 10 },
      "language": { "type": "string", "default": "ko" }
    },
    "required": ["query"]
  }
}
```

## `stocks.get_quote`
```json
{
  "name": "stocks.get_quote",
  "risk_class": "network_read",
  "requires_approval": false,
  "input_schema": {
    "type": "object",
    "properties": {
      "symbol": { "type": "string" },
      "market": { "type": "string", "default": "US" }
    },
    "required": ["symbol"]
  }
}
```

## `gmail.create_draft`
```json
{
  "name": "gmail.create_draft",
  "risk_class": "network_write",
  "requires_approval": true,
  "input_schema": {
    "type": "object",
    "properties": {
      "to": { "type": "array", "items": { "type": "string" } },
      "subject": { "type": "string" },
      "body": { "type": "string" }
    },
    "required": ["to", "subject", "body"]
  }
}
```

## `gmail.send_draft`
```json
{
  "name": "gmail.send_draft",
  "risk_class": "network_write",
  "requires_approval": true,
  "input_schema": {
    "type": "object",
    "properties": {
      "draft_id": { "type": "string" }
    },
    "required": ["draft_id"]
  }
}
```

## Implementation Rules
- All path tools must run path normalization before invocation.
- `gmail.send_draft` must show recipient, subject, and body preview before approval.
- `network_read` tools must include source URL and fetched timestamp in results.
- Tool results must follow [[API_and_Tool_Contracts]].

## Interaction Points
- Registry: [[Tool_Registry_Design]]
- Invocation: [[Tool_Invocation_Model]]
- OAuth: [[OAuth_and_Secrets_Model]]
- Windows path policy: [[Windows_Host_Policy]]
