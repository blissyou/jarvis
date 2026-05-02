# Master Index
#agent-platform #desktop-ai #architecture #security #interpreter #mcp

## Purpose
Provide the primary navigation surface for the JARVIS knowledge graph after the product pivot to a local AI agent platform.

## Strategic Summary
JARVIS is designed as a desktop AI control plane composed of:
- Electron + React user interface
- FastAPI orchestration backend
- Agent runtime for planning, routing, and safety
- Open Interpreter as the action execution engine
- Docker as the isolation boundary for code execution
- MCP-compatible tools for external services and domain extensions
- Ollama as the default local model provider with optional OpenAI fallback

## Architecture Entry Points
- [[Platform_Architecture]]
- [[Layered_Runtime_and_Data_Flow]]
- [[Project_Structure]]
- [[Scaling_Strategy]]

## Agent & Model Entry Points
- [[Agent_Runtime]]
- [[Model_Routing_Logic]]
- [[Model_Routing_Architecture]]
- [[Model_Router_Design]]
- [[Open_Interpreter_Runtime]]

## Tooling Entry Points
- [[Tool_Invocation_Model]]
- [[Tool_Registry_Design]]

## Security Entry Points
- [[Security_Model]]
- [[Permission_and_Approval_Model]]
- [[Docker_Isolation_Strategy]]

## Workflow Entry Points
- [[Execution_Flows]]
- [[Developer_Workflows]]

## Decision Records
- [[Documentation_Refactor_Audit]]
- [[ADR_001_Local_First_Desktop_Agent]]
- [[ADR_002_Model_Routing]]
- [[ADR_Model_Provider_Strategy]]
- [[ADR_003_Open_Interpreter_and_MCP]]

## Reference Source Index
- [[Official_References]]

## Active Knowledge Graph
- [[README]]
- [[Platform_Architecture]]
- [[Layered_Runtime_and_Data_Flow]]
- [[Project_Structure]]
- [[Agent_Runtime]]
- [[Model_Routing_Architecture]]
- [[Model_Router_Design]]
- [[Open_Interpreter_Runtime]]
- [[Tool_Invocation_Model]]
- [[Docker_Isolation_Strategy]]
- [[Security/Security_Model|Security_Model]]
- [[Execution_Flows]]

## Legacy Documentation
The documents below are preserved for historical context. They are not the active source of truth and each one is superseded by the new platform-oriented architecture set.

### Legacy Research
- [[Feasibility]]
- [[Reality_vs_Jarvis]]

### Legacy Architecture
- [[System_Architecture]]
- [[Tool_Execution_Model]]
- [[Voice_Pipeline]]

### Legacy Features And MVP
- [[Feature_Difficulty_Table]]
- [[Feature_List]]
- [[MVP_Definition]]
- [[User_Flows]]

### Legacy Security
- [[Approval_System]]
- [[05_Security/Security_Model|Legacy Security_Model]]

### Legacy Product And Planning
- [[Development_Roadmap]]
- [[Tech_Stack_Decision]]
- [[Practical_Constraints]]
- [[PRD]]
- [[System_Prompt]]

### Legacy API And Data
- [[API_Spec]]
- [[Database_Schema]]

### Legacy Workflow Visualization
- [[Agent_Workflow]]
- [[Mermaid_Generation_Strategy]]
- [[Mermaid_Generator_Code]]
- [[Task_State_Model]]
- [[Workflow_API_Design]]
- [[Workflow_E2E_Test_Scenarios]]
- [[Workflow_Log_Format]]
- [[Workflow_Pydantic_Models]]
- [[Workflow_SQL_DDL]]
- [[Workflow_Service_Layer]]

### Legacy References
- [[References]]
