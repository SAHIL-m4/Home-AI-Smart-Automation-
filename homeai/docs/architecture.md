# HomeAI — System Architecture

## Overview

HomeAI follows a clean **3-layer architecture** that separates AI reasoning, device control, and the UI. This makes each layer independently testable, replaceable, and extensible.

```
Layer 1: UI           →  Streamlit dashboard / Web interface
Layer 2: AI Engine    →  Claude API + system prompt + JSON validation
Layer 3: Device Layer →  DeviceSimulator + EnergyTracker
```

---

## Data Flow

```
User Input (NL)
      │
      ▼
┌─────────────────────────────────────────┐
│           AutomationEngine              │
│  1. Prepend system prompt (HomeAI role) │
│  2. POST /v1/messages to Anthropic API  │
│  3. Strip markdown fences               │
│  4. json.loads() → validate schema      │
└──────────────────┬──────────────────────┘
                   │  workflow: dict
                   ▼
┌─────────────────────────────────────────┐
│           DeviceSimulator               │
│  apply_workflow(workflow)               │
│  ├── resolve device aliases             │
│  ├── update device state                │
│  └── return execution_log[]            │
└──────────────────┬──────────────────────┘
                   │  execution_log: List[str]
                   ▼
┌─────────────────────────────────────────┐
│           EnergyTracker                 │
│  record_saving() if energy mode         │
│  get_energy_usage() from device states  │
└─────────────────────────────────────────┘
                   │
                   ▼
           UI Re-render (Streamlit)
```

---

## Component Details

### AutomationEngine (`src/automation_engine.py`)

Responsibilities:
- Holds the HomeAI system prompt
- Manages conversation history (multi-turn support)
- Calls `anthropic.messages.create()`
- Strips markdown fences from the response
- Validates required JSON fields before returning

Key design decisions:
- `model = "claude-sonnet-4-20250514"` — best balance of speed and reasoning
- `max_tokens = 1000` — sufficient for any automation workflow
- System prompt enforces JSON-only output; no natural-language wrapping
- Validation raises explicit errors rather than silently ignoring bad output

---

### DeviceSimulator (`src/device_simulator.py`)

Responsibilities:
- Maintains the state of all 7 smart devices
- Maps AI-returned device names to internal IDs (alias table)
- Applies `action + value` pairs to update device state
- Returns human-readable execution logs
- Computes simulated kWh usage from device weights

Device state model:
```python
{
    "name": "Air Conditioner",
    "icon": "❄️",
    "on":   True,
    "detail": "Temperature: 22°C"
}
```

Alias resolution handles natural language variation:
```python
"Air Conditioner" → "ac"
"air conditioning" → "ac"
"AC"              → "ac"
"Smart TV"        → "tv"
"television"      → "tv"
```

Action handlers:
| Action type | Effect |
|---|---|
| `Power ON/OFF` | Sets `on` boolean |
| `Brightness %` | Sets `on=True`, updates detail |
| `Temperature °C` | Sets `on=True`, updates detail |
| `Speed %` | Sets `on=True`, updates detail |
| `Close / Lock` | Sets `on=True` |
| `Open / Unlock` | Sets `on=False` |
| Generic | Infers from value content |

---

### EnergyTracker (`src/energy_tracker.py`)

Responsibilities:
- Accumulates ₹ savings from AI optimisations
- Tracks optimised kWh vs baseline (6 kWh/day)
- Stores timestamped event log
- Provides `saving_percentage()` for dashboard display

---

## JSON Automation Workflow Schema

```json
{
  "mode": "string — human-readable mode name",
  "actions": [
    {
      "device": "string — one of the 7 device names",
      "action": "string — action type (Power, Brightness, Temperature, …)",
      "value":  "string — the setting value"
    }
  ],
  "energy_saving_tip": "string — one actionable suggestion"
}
```

All fields are required. `actions` must be a non-empty list. Each action must have all three keys.

---

## System Prompt Design

The HomeAI system prompt follows these principles:

1. **Role assignment** — "You are HomeAI…" establishes a clear persona
2. **Device enumeration** — lists all 7 controllable devices explicitly
3. **Goal hierarchy** — comfort → convenience → security → energy efficiency
4. **Format enforcement** — "Respond in clean JSON format only"
5. **Value conventions** — percentages for brightness/speed, Celsius for temp
6. **Mode examples** — movie night, energy saver shown in-context
7. **Zero escape clause** — "Do not include explanations outside JSON"

This design exploits Claude's instruction-following capability to produce machine-parseable output reliably.

---

## Evaluation Criteria Alignment

| Criterion | How HomeAI addresses it |
|---|---|
| **GenAI integration** | Claude as the core reasoning engine, not just UI |
| **Technical depth** | 3-layer architecture, alias resolution, schema validation |
| **Working prototype** | Live Streamlit app + 19 passing unit tests |
| **Real-world impact** | Energy savings, accessibility, multi-device orchestration |
| **Stakeholder clarity** | Homeowners, utilities, Samsung SmartThings, developers |
| **GitHub quality** | Modular code, README, tests, docs, demo script |

---

## Extensibility Points

| Extension | Required change |
|---|---|
| Add a new device (e.g. Robot Vacuum) | Add to `DEVICE_DEFAULTS` and `DEVICE_ALIASES` in `device_simulator.py` |
| Switch AI provider (e.g. Gemini) | Replace `automation_engine.py` client only |
| Real device control (SmartThings) | Replace `apply_workflow()` with SDK calls |
| Voice input | Pipe Whisper transcription to `sendMessage()` |
| Scheduled automation | Wrap `generate()` call in APScheduler job |
| Multi-room support | Extend device IDs with room prefix (e.g. `bedroom_lights`) |
