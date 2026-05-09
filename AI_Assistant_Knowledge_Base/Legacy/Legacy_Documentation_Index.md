# Legacy Documentation Index
#legacy #archive #documentation

## Status
Active archive boundary document. This index defines what is legacy and prevents older runtime documents from being mistaken for the current architecture.

## Purpose
Separate older JARVIS architecture documents from the active OpenClaw-first Voice Layer direction.

Legacy documents are preserved for historical context and may contain useful ideas, but they are not the active source of truth unless an active document explicitly links to them.

## Active Direction Summary
The current direction is:
```text
JARVIS = high-quality voice layer and desktop HUD
OpenClaw = assistant runtime, model execution, tools, approvals, sessions, memory, channels, background tasks
```

Start with:
1. [[JARVIS_Voice_Layer_Strategy]]
2. [[Voice_STT_Accuracy_Latency_Plan]]
3. [[ADR_005_OpenClaw_First_Voice_Layer]]
4. [[OpenClaw_Migration_Plan]]
5. [[OpenClaw_Runtime_Architecture]]
6. [[OpenClaw_Workspace_Strategy]]

## Legacy Categories

### Legacy Custom Runtime
These documents describe the former custom runtime direction. They are superseded by OpenClaw-first architecture.
- [[Platform_Architecture]]
- [[Layered_Runtime_and_Data_Flow]]
- [[Agent_Runtime]]
- [[Open_Interpreter_Runtime]]
- [[Tool_Invocation_Model]]
- [[Tool_Registry_Design]]
- [[API_and_Tool_Contracts]]
- [[First_Party_Tool_Schemas]]

### Legacy Local Model / Ollama Direction
These documents are no longer active MVP requirements because JARVIS will not depend on Ollama for the main assistant path.
- [[ADR_002_Model_Routing]]
- [[ADR_Model_Provider_Strategy]]
- [[Model_Routing_Logic]]
- [[Model_Routing_Architecture]]
- [[Model_Router_Design]]
- [[Local_Model_Benchmarking]]

### Legacy Open Interpreter / Docker Direction
These remain useful as execution research, but OpenClaw is the active execution surface.
- [[ADR_003_Open_Interpreter_and_MCP]]
- [[Open_Interpreter_Runtime]]
- [[Docker_Isolation_Strategy]]

### Legacy Product / Dashboard Era
These documents are historical and should not drive new implementation without review.
- [[Feasibility]]
- [[Reality_vs_Jarvis]]
- [[System_Architecture]]
- [[Tool_Execution_Model]]
- [[Voice_Pipeline]]
- [[Feature_Difficulty_Table]]
- [[Feature_List]]
- [[MVP_Definition]]
- [[User_Flows]]
- [[Development_Roadmap]]
- [[Tech_Stack_Decision]]
- [[Practical_Constraints]]
- [[PRD]]
- [[System_Prompt]]
- [[API_Spec]]
- [[Database_Schema]]

### Legacy Workflow Visualization
Useful for ideas, not active architecture.
- [[Agent_Workflow]]
- [[Mermaid_Generation_Strategy]]
- [[Mermaid_Generator_Code]]
- [[Task_State_Model]]
- [[Workflow_API_Design]]
- [[Workflow_E2E_Test_Scenarios]]
- [[Workflow_Log_Format]]
- [[Workflow_Pydantic_Models]]
- [[Workflow_Service_Layer]]
- [[Workflow_SQL_DDL]]

## Legacy Boundary Acceptance Criteria
- Every legacy category states why the documents are not active.
- Active reading paths point first to OpenClaw-first Voice Layer documents.
- Legacy documents are preserved for context but do not override [[ADR_005_OpenClaw_First_Voice_Layer]].
- Any reactivation of legacy runtime/model/tooling ideas requires a new ADR.
- New active docs must link here when they intentionally reference historical material.

## Rule For Future Updates
When editing legacy documents, add a clear note near the top:

```markdown
> Legacy note: This document is preserved for historical context. The active direction is [[JARVIS_Voice_Layer_Strategy]].
```

Do not promote a legacy design back into the active direction unless a new ADR accepts it.

## Related Documents
- [[Master_Index]]
- [[README]]
- [[JARVIS_Voice_Layer_Strategy]]
- [[ADR_005_OpenClaw_First_Voice_Layer]]
- [[OpenClaw_Migration_Plan]]
- [[Voice_Layer_Implementation_Readiness]]
