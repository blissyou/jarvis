> Legacy note: This document is preserved for historical context. The active direction is [[JARVIS_Voice_Layer_Strategy]].

# Open Interpreter Runtime
#interpreter #execution #code #sandbox

## Purpose
Describe how Open Interpreter is embedded as the core action engine for generated code, shell tasks, and developer workflows.

## Why Open Interpreter
Open Interpreter already models the pattern JARVIS needs:
- model-guided code generation
- shell and Python execution
- local execution support
- compatibility with local model providers including Ollama

Open Interpreter documents local execution and local providers in its local running guide. [Open Interpreter local guide](https://docs.openinterpreter.com/guides/running-locally)

## Responsibility Boundary
Open Interpreter is not the top-level orchestrator.
- It should not decide product policy
- It should not own final approval UX
- It should not directly expose raw system power to the UI

Instead it receives a constrained execution plan from the agent layer.

## Runtime Contract
```json
{
  "execution_id": "exec_01JARVIS",
  "profile": "python-sandbox",
  "workspace_root": "/workspace",
  "network_policy": "disabled",
  "allowed_paths": [
    "/workspace"
  ],
  "task": {
    "goal": "Write and run a Python script that parses a log file and reports top errors.",
    "artifacts": [
      "/workspace/logs/app.log"
    ]
  }
}
```

## Recommended Profiles
- `python-sandbox`
  - Python code, no host writes outside mounted workspace
- `node-sandbox`
  - JS/TS tasks for build or lint flows
- `shell-readonly`
  - inspection-only shell work
- `host-trusted`
  - narrow host actions allowed only after approval

## Safety Notes
Open Interpreter safe mode is explicitly documented as experimental and not a guarantee of safety. It disables autorun and can scan generated code with Semgrep, but docs do not claim full containment. [Open Interpreter safe mode docs](https://docs.openinterpreter.com/safety/safe-mode)

Therefore JARVIS must not rely on Open Interpreter safe mode alone. Docker remains the actual isolation boundary for risky execution.

## Interaction Points
- Upstream planner: [[Agent_Runtime]]
- Isolation boundary: [[Docker_Isolation_Strategy]]
- Security policy: [[Security_Model]]
- Workflow examples: [[Execution_Flows]]
