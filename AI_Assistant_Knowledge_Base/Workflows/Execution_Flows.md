# Execution Flows
#workflows #agent #execution #mcp #interpreter

## Purpose
Capture the step-by-step execution logic for representative JARVIS tasks.

## Case A: Local Task
User request: "Analyze this log file"

```mermaid
sequenceDiagram
    participant U as User
    participant UI as Electron UI
    participant API as FastAPI
    participant AG as Agent
    participant MR as Model Router
    participant OI as Open Interpreter
    participant DK as Docker

    U->>UI: Analyze this log file
    UI->>API: session request + selected file
    API->>AG: new turn
    AG->>MR: choose local or cloud model
    MR-->>AG: Ollama selected
    AG->>AG: classify as code/tool task
    AG->>OI: read and analyze log within workspace
    OI->>DK: start python-sandbox
    DK-->>OI: execution environment
    OI-->>AG: extracted errors, summary, artifacts
    AG-->>API: final response + structured findings
    API-->>UI: summary, evidence, execution log
```

### Notes
- Default route should remain local because log data is sensitive
- The interpreter can use Python parsing libraries inside the sandbox
- Approval may be skipped for read-only analysis

## Case B: External Tool via MCP
User request: "Get stock data and summarize"

```mermaid
sequenceDiagram
    participant U as User
    participant UI as Electron UI
    participant API as FastAPI
    participant AG as Agent
    participant MCP as MCP Broker
    participant STOCK as Stock Server
    participant MR as Model Router

    U->>UI: Get stock data and summarize
    UI->>API: request
    API->>AG: new turn
    AG->>MCP: invoke stocks.get_quote
    MCP->>STOCK: tool call
    STOCK-->>MCP: structured quote payload
    MCP-->>AG: normalized result
    AG->>MR: summarize result
    MR-->>AG: Korean summary
    AG-->>API: final response
    API-->>UI: result card + audit log
```

### Notes
- The model does not scrape stock data itself
- MCP tool result is the source of truth
- Summarization can remain local if quality is acceptable

## Case C: Code Execution
User request: "Write and run a Python script"

```mermaid
sequenceDiagram
    participant U as User
    participant UI as Electron UI
    participant API as FastAPI
    participant AG as Agent
    participant OI as Open Interpreter
    participant DK as Docker

    U->>UI: Write and run a Python script
    UI->>API: request
    API->>AG: new turn
    AG->>AG: classify as code execution
    AG->>API: create approval request
    API-->>UI: approval card
    U->>UI: approve
    UI->>API: approval accepted
    API->>OI: execution plan
    OI->>DK: create python-sandbox
    DK-->>OI: isolated workspace
    OI->>DK: write file and run script
    DK-->>OI: stdout/stderr/artifacts
    OI-->>AG: structured result
    AG-->>API: execution summary
    API-->>UI: final output and artifacts
```

## Interaction Points
- Architecture: [[Platform_Architecture]]
- Agent logic: [[Agent_Runtime]]
- Tool model: [[Tool_Invocation_Model]]
- Sandbox: [[Docker_Isolation_Strategy]]
