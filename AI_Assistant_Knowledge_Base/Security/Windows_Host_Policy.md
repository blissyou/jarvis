# Windows Host Policy
#security #windows #powershell #host-actions

## Purpose
Define Windows-specific host execution rules for JARVIS. This document complements the Docker and general permission model with concrete Windows path, PowerShell, process, and credential constraints.

## Scope
JARVIS runs on a Windows workstation during early development. Host actions must be treated as higher risk than sandboxed actions because they can affect the user's real files, shell profile, credentials, and installed software.

## Default Windows Policy
| Action Class | Default | Notes |
|---|---|---|
| Read selected workspace files | Allow | Must remain inside approved workspace root |
| List directories outside workspace | Ask | Useful but may reveal private names |
| Write inside workspace | Ask | Show diff or file preview first |
| Write outside workspace | Deny | Explicit approval and exact path required |
| Delete files | Deny by default | MVP should only allow temporary artifact cleanup |
| Run PowerShell commands | Ask | Must show command and working directory |
| Edit PowerShell profile | Deny | Treat as `system_admin` |
| Install packages or binaries | Ask high-risk | Requires source, command, and rollback note |
| Access credential stores | Deny | Includes browser profiles, SSH keys, Windows Credential Manager |

## Path Rules
- Resolve every path to an absolute canonical path before policy evaluation.
- Compare resolved paths against the approved workspace root using case-insensitive Windows semantics.
- Reject paths containing unresolved wildcards for write, delete, upload, or shell execution.
- Reject writes to common sensitive locations:
  - `C:\Windows`
  - `C:\Program Files`
  - `C:\Program Files (x86)`
  - user shell profile directories
  - browser profile directories
  - SSH and cloud credential folders

## PowerShell Execution Rules
| Rule | Requirement |
|---|---|
| Shell selection | Use PowerShell explicitly for Windows host commands |
| Working directory | Must be set and logged |
| Command preview | Required before execution |
| Environment changes | Must be scoped to the process unless explicitly approved |
| Long-running process | Must stream logs and support cancellation |
| Destructive command | Deny unless user explicitly requested it and approved exact scope |

## Host Action Gate
Host actions must pass through a narrow adapter, never raw UI execution.

```json
{
  "host_action_id": "host_01JARVIS",
  "kind": "powershell",
  "cwd": "C:/Users/PC/Desktop/project/jarvis",
  "command": "git status --short",
  "risk_class": "read_local",
  "requires_approval": false
}
```

## MVP Restrictions
- No autonomous file deletion.
- No registry edits.
- No Windows service creation or modification.
- No shell profile edits.
- No credential export.
- No browser automation for logged-in sessions unless a future policy document allows it.

## Interaction Points
- General security: [[Security_Model]]
- Approval rules: [[Permission_and_Approval_Model]]
- Sandbox rules: [[Docker_Isolation_Strategy]]
- Execution runtime: [[Open_Interpreter_Runtime]]
