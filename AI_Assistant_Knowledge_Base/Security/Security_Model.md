# Security Model
#security #policy #permissions #sandbox

## Purpose
Define the top-level safety posture for a local AI assistant that can execute tasks on the user's machine.

## Security Objectives
- Prevent unreviewed destructive actions
- Bound filesystem access
- Separate planning from execution
- Make every action observable and auditable
- Preserve local privacy by preferring local inference

## Threat Model
### Primary threats
- Prompt-driven arbitrary command execution
- Accidental deletion or overwrite of user files
- Secret leakage through model prompts or tool outputs
- Container breakout or host privilege escalation
- Untrusted third-party MCP server behavior

### Non-goals
- Nation-state grade host hardening
- Guaranteed containment against every kernel exploit

## Control Layers
1. Model routing policy
2. Approval and permission gate
3. Tool schema validation
4. Docker sandbox
5. Filesystem scope enforcement
6. Audit log persistence

## High-Risk Action Classes
- Delete or overwrite files outside workspace
- Execute network-enabled generated code
- Install packages or binaries
- Send messages, upload files, or modify cloud state
- Change shell startup files, credentials, or system settings

## Policy Defaults
- Local inference first
- No write actions without explicit approval
- Generated code executes in Docker by default
- Network disabled in the sandbox unless explicitly approved

## Related Documents
- [[Permission_and_Approval_Model]]
- [[Docker_Isolation_Strategy]]
- [[Open_Interpreter_Runtime]]
- [[Tool_Registry_Design]]
