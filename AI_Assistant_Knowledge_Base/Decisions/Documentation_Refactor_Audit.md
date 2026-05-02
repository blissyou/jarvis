# Documentation Refactor Audit
#decisions #audit #knowledge-base

## Purpose
Record what was outdated in the previous vault and how the new architecture-oriented structure replaces it.

## Outdated Patterns Detected
- Dashboard-centric framing instead of agent runtime framing
- Web-first assumptions instead of desktop-first assumptions
- Narrow MVP centered on news, stocks, and email
- Missing isolation model for generated code execution
- No first-class Open Interpreter runtime document
- No MCP registry or invocation design
- Weak linkage between model routing, safety, and execution

## Deprecated or Shallow Documents
- `09_Product/PRD.md`
  - Too focused on news, stock, and email workflows
- `02_Architecture/System_Architecture.md`
  - Web + API + Postgres/Redis framing is outdated for the new local platform
- `07_Tech_Stack/Tech_Stack_Decision.md`
  - Next.js web stack is not the target primary UI anymore
- `13_Workflow_Visualization/*`
  - Useful as event-model inspiration, but too coupled to dashboard-style workflow display

## Replacement Map
| Old topic | New canonical document |
|---|---|
| System architecture | [[Platform_Architecture]] |
| Tool execution model | [[Open_Interpreter_Runtime]], [[Tool_Invocation_Model]] |
| MVP product framing | [[Developer_Workflows]], [[Execution_Flows]] |
| Security model | [[Security_Model]], [[Permission_and_Approval_Model]] |
| Tech stack decision | [[ADR_001_Local_First_Desktop_Agent]], [[ADR_002_Model_Routing]], [[ADR_003_Open_Interpreter_and_MCP]] |

## Migration Rule
Old docs remain as historical context only. New design and implementation work should link to the new folder structure first.

## Interaction Points
- Entry surface: [[Master_Index]]
- Strategic baseline: [[Platform_Architecture]]
