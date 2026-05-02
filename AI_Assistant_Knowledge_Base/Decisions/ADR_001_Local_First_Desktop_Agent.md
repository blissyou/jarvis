# ADR 001 - Local-First Desktop Agent
#adr #desktop #privacy

## Status
Accepted

## Decision
JARVIS will be a desktop-first local AI agent rather than a web dashboard or browser-first assistant.

## Context
The new product must execute developer tasks on the user's machine, preserve privacy, and support local execution. A browser dashboard cannot safely or ergonomically own privileged machine operations.

## Consequences
- Electron becomes the primary UI shell
- FastAPI becomes the local orchestration backend
- Workspace and host policy become first-class concepts
- Cloud dependency becomes optional rather than foundational

## Related Documents
- [[Platform_Architecture]]
- [[Project_Structure]]
- [[Security_Model]]
