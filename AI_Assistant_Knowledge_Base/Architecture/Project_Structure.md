# Project Structure
#architecture #repository #folders

## Purpose
Define the production repository layout for implementation, deployment, and plugin growth.

## Repository Tree
```text
jarvis/
├── desktop/
│   ├── electron/
│   ├── src/
│   │   ├── app/
│   │   ├── components/
│   │   ├── features/
│   │   ├── hooks/
│   │   └── lib/
│   └── package.json
├── api/
│   ├── app/
│   │   ├── main.py
│   │   ├── routers/
│   │   ├── schemas/
│   │   ├── services/
│   │   ├── persistence/
│   │   └── security/
│   ├── tests/
│   └── requirements.txt
├── agent/
│   ├── planner/
│   ├── router/
│   ├── memory/
│   ├── policies/
│   └── prompts/
├── interpreter/
│   ├── runtime/
│   ├── profiles/
│   ├── adapters/
│   └── tests/
├── mcp/
│   ├── client/
│   ├── registry/
│   ├── schemas/
│   └── servers/
│       ├── stock/
│       ├── news/
│       └── filesystem/
├── docker/
│   ├── sandbox/
│   ├── seccomp/
│   ├── compose/
│   └── images/
├── docs/
├── scripts/
├── runtime/
│   ├── logs/
│   ├── artifacts/
│   └── sessions/
└── AI_Assistant_Knowledge_Base/
```

## Folder Boundary Rules
- `desktop/` only owns UI, IPC, and user interaction state.
- `api/` owns orchestration endpoints and audit persistence.
- `agent/` owns prompts, routing, policies, and execution planning.
- `interpreter/` owns Open Interpreter runtime profiles and host/container adapters.
- `mcp/` owns registry, client adapters, tool schemas, and first-party MCP servers.
- `docker/` owns sandbox images, seccomp profiles, compose files, and runtime hardening.

## Interaction Points
- Architecture source: [[Platform_Architecture]]
- Tool packaging: [[Tool_Registry_Design]]
- Sandbox packaging: [[Docker_Isolation_Strategy]]
- Decision link: [[ADR_003_Open_Interpreter_and_MCP]]
