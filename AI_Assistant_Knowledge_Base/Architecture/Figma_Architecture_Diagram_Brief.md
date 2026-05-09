# Figma Architecture Diagram Brief
#figma #architecture #diagram #openclaw #voice-layer

## Status
Active design brief for creating the visual JARVIS/OpenClaw architecture diagram in Figma.

## Purpose
Provide a Figma-ready drawing brief for the overall OpenClaw-first JARVIS architecture.

The final Figma output should make the current product direction obvious:

```text
JARVIS = Voice Layer + Desktop HUD
OpenClaw = assistant runtime + tools + approvals + sessions + memory
Legacy runtime/model-router/Ollama = not active MVP path
```

## Recommended Figma Frame
- Frame name: `JARVIS OpenClaw-First Voice Architecture`
- Size: `1920 x 1080`
- Layout: left-to-right system flow with a safety/control lane below
- Style: dark background, clear colored domains, minimal text

## Visual Domains
Use five grouped regions:

| Region | Color Hint | Contents |
|---|---|---|
| User / Desktop | blue | user, microphone, speaker, Electron HUD |
| JARVIS Voice Layer | violet | recording lifecycle, silence trim, STT, transcript confirmation, response shaping, TTS |
| OpenClaw Runtime | green | Gateway, sessions, model providers, tools, approvals, memory, background tasks |
| Safety / Policy | amber/red | transcript risk gate, approval pending, financial block, failure states |
| Legacy / Optional | gray | Ollama, custom model router, Open Interpreter, Docker, MCP registry |

## Main Flow
Draw the primary happy path as numbered arrows:

```text
1. User speaks
2. Electron HUD records audio
3. JARVIS Voice Layer trims audio and runs STT
4. Transcript appears in HUD
5. Risk gate decides confirm vs send
6. Transcript is sent to OpenClaw Gateway
7. OpenClaw runs assistant turn, tools, approvals, memory, and model providers
8. OpenClaw returns completed / awaiting approval / failed / blocked state
9. JARVIS shapes visible text into speakable text
10. TTS streams to speaker and HUD transcript updates
```

## Safety Flow
Draw a separate lower lane:

```text
Risky transcript
-> confirmation required
-> OpenClaw approval state
-> HUD approval card
-> TTS says pending, not completed
```

Add explicit blocked case:

```text
Financial transaction / payment / trade request
-> preserve transcript
-> block/refuse
-> no executable action
```

## Legacy Boundary
Draw the legacy area as a gray box off the main path with a dashed border.

Label:

```text
Legacy / Optional Research
Not active MVP path
```

Include:
- Ollama
- custom JARVIS model router
- Open Interpreter
- Docker execution
- MCP registry design

The gray legacy box must not have primary arrows from the active voice path.

## Suggested Diagram Text
Use concise labels inside nodes:

### User / Desktop
- `User`
- `Mic / Push-to-talk`
- `Electron HUD`
- `Speaker`

### JARVIS Voice Layer
- `Record + Trim`
- `STT Profile: fast / balanced / accurate`
- `Transcript UX`
- `Risk Gate`
- `TTS Stream`

### OpenClaw Runtime
- `Gateway`
- `Session Message`
- `Model Providers`
- `Tools`
- `Approvals`
- `Memory`
- `Background Tasks`

### Safety / States
- `Completed`
- `Awaiting Approval`
- `Failed`
- `Blocked`
- `Financial Execution Block`

## Figma Prompt For Designer Or AI Diagram Tool
Use this prompt if Figma AI, FigJam AI, or a designer is creating the diagram:

```text
Create a clean 1920x1080 architecture diagram for JARVIS as an OpenClaw-first voice assistant.

Show JARVIS as a high-quality Voice Layer and desktop HUD, not as an LLM runtime. The main left-to-right flow is:
User voice -> Electron HUD -> JARVIS Voice Layer API -> STT -> transcript confirmation/risk gate -> OpenClaw Gateway -> OpenClaw runtime sessions/tools/approvals/memory/model providers -> response state -> JARVIS TTS -> speaker and HUD.

Use separate colored domains:
1. User/Desktop in blue
2. JARVIS Voice Layer in violet
3. OpenClaw Runtime in green
4. Safety/Policy lane in amber/red
5. Legacy/Optional research in gray with dashed border

Make the safety lane show that risky transcripts require confirmation and OpenClaw approval, TTS says pending rather than completed, and financial transaction/trade/payment requests are blocked/refused.

Show legacy items as off-path gray nodes: Ollama, custom JARVIS model router, Open Interpreter, Docker execution, MCP registry. Label them 'Legacy / optional research, not active MVP path'. Do not connect them to the main active path.

The final diagram should be implementation-oriented, readable at README size, and suitable for export as PNG/SVG.
```

## Export Requirements
Export from Figma as:

```text
AI_Assistant_Knowledge_Base/assets/jarvis-openclaw-voice-architecture.png
AI_Assistant_Knowledge_Base/assets/jarvis-openclaw-voice-architecture.svg
```

If only one format is exported, prefer PNG for README compatibility.

## README Integration
After the Figma export exists, add this image near the README `Current Architecture Summary` section:

```markdown
![JARVIS OpenClaw-first Voice Architecture](assets/jarvis-openclaw-voice-architecture.png)
```

If the Figma file is public or shareable, also add:

```markdown
Figma source: <FIGMA_LINK_HERE>
```

## Acceptance Criteria
- Diagram clearly shows OpenClaw as runtime owner.
- Diagram clearly shows JARVIS as Voice Layer + HUD owner.
- Active flow does not route through Ollama or the legacy model router.
- Safety lane includes transcript confirmation, approval-pending state, and financial block.
- Export path is README-compatible.
- README links to this brief and includes the image placeholder or final export.

## Related Documents
- [[README]]
- [[Master_Index]]
- [[JARVIS_Voice_Layer_Strategy]]
- [[OpenClaw_Gateway_Voice_Adapter]]
- [[Voice_Runtime_Design]]
- [[Voice_Layer_Implementation_Readiness]]
- [[Legacy_Documentation_Index]]
