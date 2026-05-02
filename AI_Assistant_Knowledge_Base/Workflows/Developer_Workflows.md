# Developer Workflows
#developer #terminal #logs #builds #debugging

## Purpose
Describe the developer-centric workflows that distinguish JARVIS from a consumer voice assistant.

## Priority Workflows
- Analyze local log files
- Summarize failing test output
- Run build commands inside a sandbox
- Explain stack traces
- Generate and execute one-off scripts
- Search workspace for symbols or config issues

## Workflow Design Principles
- Workspace selection must be explicit
- Risky execution requires approval
- Generated code runs in Docker first, not on host
- Final answer includes:
  - what was attempted
  - what changed
  - evidence from stdout/stderr

## Interaction Points
- Execution details: [[Execution_Flows]]
- Agent details: [[Agent_Runtime]]
- Security details: [[Permission_and_Approval_Model]]
