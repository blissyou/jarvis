# Voice First Minimal UI
#ui #voice #hud #chat #mvp

## Purpose
Define the minimal JARVIS desktop interface for a voice-first assistant during early development. The UI should feel like a lightweight HUD, but it must stay simple enough to implement quickly and debug safely.

## Design Direction
The visual mood is inspired by a cyan technical HUD: dark background, thin grid lines, circular listening indicator, compact telemetry, and glowing accents. The product should not copy a movie interface literally. It should use the mood while preserving readability and developer usability.

## Product Principle
Voice is the primary interaction. Text chat is the fallback and debugging interface. The UI should not become a dashboard full of widgets because most commands will be spoken.

## MVP Screen Layout
```text
+--------------------------------------------------------------+
| Top Bar                                                      |
| JARVIS   Local/Cloud status   Workspace   Budget   Settings  |
+--------------------------------------------------------------+
|                                                              |
|                  Central Voice Core                          |
|              listening / thinking / speaking                 |
|                                                              |
|          short transcript + current agent status             |
|                                                              |
+-------------------------------+------------------------------+
| Chat Console                  | Activity / Approval Panel    |
| user text input               | tool calls, approvals, logs  |
+-------------------------------+------------------------------+
```

## Regions
| Region | Purpose | Complexity |
|---|---|---|
| Top Bar | Provider, workspace, budget, settings | Low |
| Central Voice Core | Main visual state for voice interaction | Medium |
| Transcript Strip | Last heard command and normalized intent | Low |
| Chat Console | Development fallback for typed commands | Medium |
| Activity Panel | Tool calls, model route, approvals, errors | Medium |

## Central Voice Core
The central voice core is the emotional center of the app. It replaces a complex dashboard.

### States
| State | Visual |
|---|---|
| Idle | Dim cyan ring, status text "Ready" |
| Listening | Pulsing ring, waveform line, microphone active |
| Thinking | Rotating segmented ring, route indicator |
| Tool Running | Ring plus small tool label |
| Awaiting Approval | Amber ring, approval panel highlighted |
| Speaking | Ring expands with audio waveform |
| Error | Red accent, concise failure reason |

### Required Text
- Current state: `Ready`, `Listening`, `Thinking`, `Running tool`, `Needs approval`, `Speaking`, `Blocked`
- Last transcript
- Short action summary

### Avoid
- Do not show many decorative gauges.
- Do not use unreadable tiny labels.
- Do not make every metric visible at once.
- Do not hide approval behind an animation.

## Chat Console
The chat console is for early development, debugging, and quiet usage.

### Requirements
- One message list.
- One text input.
- Send button.
- Push-to-talk button.
- Last transcript can be inserted into the input for correction.
- Assistant responses may include compact tool result cards.

### Message Types
| Type | UI Treatment |
|---|---|
| User text | Right aligned or clear user block |
| Voice transcript | User block with mic indicator |
| Assistant response | Main response block |
| Tool result | Compact bordered result row |
| Error | Red-accented message with safe next action |

## Activity and Approval Panel
This panel is collapsed by default on small screens and visible on desktop.

### Activity Items
- Model provider selected
- Tool invoked
- Approval requested
- Execution started
- Execution finished
- Budget limit warning

### Approval Card
Approval must be simple and obvious.

Required fields:
- Action summary
- Target, such as file path, email recipient, URL, or command
- Risk level
- Expected state change
- Buttons: `Approve`, `Reject`, `Edit`

## Visual Style
| Token | Value |
|---|---|
| Background | near-black blue, `#050B12` |
| Panel | transparent dark, `rgba(5, 18, 26, 0.72)` |
| Primary accent | cyan, `#00E5FF` |
| Secondary accent | teal, `#00FFA8` |
| Warning | amber, `#FFB020` |
| Danger | red, `#FF3B4F` |
| Text primary | pale cyan-white, `#E8FBFF` |
| Text secondary | muted blue-gray, `#7AA7B3` |
| Border | low-opacity cyan |

## Typography
- Use Inter or system sans-serif.
- Use normal letter spacing.
- Avoid tiny HUD text below 12px.
- Body text should be 14px to 16px.
- Status labels should be concise and readable.

## Desktop MVP Dimensions
| Element | Suggested Size |
|---|---|
| Main window | 1100 x 720 minimum |
| Central voice core | 280 to 360 px diameter |
| Chat console | 55% width bottom area |
| Activity panel | 320 px width |
| Top bar | 48 px height |

## Mobile or Narrow Layout
Not a priority for MVP. If needed:
- Central voice core remains top.
- Chat console below.
- Activity/approval becomes a slide-over panel.

## Implementation Notes
- Build the voice core with CSS and simple SVG/canvas, not heavy 3D.
- Animate only state transitions, pulse, and waveform.
- Keep all important state available as text for debugging.
- Use the same event stream as the activity log.
- The interface should work fully with keyboard and text input before voice is enabled.

## Figma Mockup Plan
If a Figma file is available, create these frames:
1. `Voice First Idle`
2. `Listening`
3. `Thinking With Tool`
4. `Awaiting Approval`
5. `Developer Chat Mode`

## Interaction Points
- Desktop UI baseline: [[Desktop_UI_Spec]]
- Voice runtime: [[Voice_Runtime_Design]]
- Approval model: [[Permission_and_Approval_Model]]
- Activity events: [[API_and_Tool_Contracts]]

