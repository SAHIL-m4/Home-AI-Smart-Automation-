# Home-AI-Smart-Automation-

HomeAI is a Generative AI–powered smart home automation prototype that lets users control their entire home using natural language. Instead of tapping buttons in an app, you simply say:

"Set movie night mode" → HomeAI dims lights, adjusts AC, closes curtains, turns on the TV, and suggests energy-saving actions — all from a single sentence.


HomeAI — What was built and how it all fits together
The prototype has three parts delivered across this conversation.
1. The live interactive dashboard (above)
This runs entirely in your browser. It calls the real Anthropic Claude API on every message and returns a structured JSON automation workflow. Here's what each section does:
Left panel — Devices. Seven simulated smart devices (Lights, Fan, AC, Smart TV, Music, Door Lock, Curtains). Each card shows on/off state and the current setting (brightness %, temperature, etc.). They update automatically when the AI runs an automation. You can also toggle any device manually by clicking its card.
Center — AI chat. Type any natural language command or click a quick-mode button. The AI interprets your intent, generates a JSON workflow, and the execution log shows each device action completing. The full JSON is shown so judges can see the AI output directly.
Right panel — Energy monitor. Shows simulated kWh consumption based on which devices are on (AC = heaviest, door lock = lightest). Tracks ₹ savings when an energy-saver mode runs. Activity log records everything that happens.
Quick mode buttons — six preset commands (Movie Night, Sleep, Good Morning, Energy Saver, Work Mode, Romantic) that pre-fill the prompt and send it immediately.
┌─────────────────────────────────────────────────────────┐
│                    USER INTERFACE                       │
│     Streamlit Dashboard  /  Web Chat Interface          │
└────────────────────────┬────────────────────────────────┘
                         │ Natural Language Input
                         ▼
┌─────────────────────────────────────────────────────────┐
│              AUTOMATION ENGINE (AI Layer)               │
│                                                         │
│  ┌─────────────┐    ┌──────────────┐   ┌─────────────┐ │
│  │System Prompt│───▶│  Anthropic   │──▶│JSON Workflow│ │
│  │(HomeAI role)│    │  Claude API  │   │  Validator  │ │
│  └─────────────┘    └──────────────┘   └──────┬──────┘ │
└────────────────────────────────────────────────┼────────┘
                                                 │
                         ┌───────────────────────┘
                         ▼
┌─────────────────────────────────────────────────────────┐
│             DEVICE SIMULATOR LAYER                      │
│                                                         │
│  💡 Lights   🌀 Fan   ❄️ AC   📺 TV   🎵 Music         │
│  🔒 Door Lock          🪟 Curtains                      │
│                                                         │
│  apply_workflow(json) → execution_log[]                 │
└─────────────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│             ENERGY TRACKER                              │
│  Monitors kWh usage, calculates ₹ savings, logs events │
└─────────────────────────────────────────────────────────┘
