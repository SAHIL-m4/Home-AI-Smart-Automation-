# 🏠 HomeAI — Generative AI Powered Smart Home Automation

> **Samsung PRISM GenAI Hackathon 2025** | Theme: Home AI & Smart Automation

[![Python](https://img.shields.io/badge/Python-3.10+-blue)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.35+-red)](https://streamlit.io)
[![Anthropic](https://img.shields.io/badge/Claude-Sonnet_4-orange)](https://anthropic.com)
[![Tests](https://img.shields.io/badge/Tests-19_passed-green)](#testing)
[![License](https://img.shields.io/badge/License-MIT-purple)](LICENSE)

---

## 📌 Overview

**HomeAI** is a Generative AI–powered smart home automation prototype that lets users control their entire home using natural language. Instead of tapping buttons in an app, you simply say:

> *"Set movie night mode"* → HomeAI dims lights, adjusts AC, closes curtains, turns on the TV, and suggests energy-saving actions — all from a single sentence.

Built with **Claude claude-sonnet-4-20250514** (Anthropic) as the reasoning engine, HomeAI translates any free-form user request into a structured **JSON automation workflow**, which is then executed on a simulated device layer.

---

## 🎯 Stakeholders

| Stakeholder | Role |
|---|---|
| **Homeowners** | Primary users — interact via natural language |
| **Samsung SmartThings** | Integration target for real device control |
| **Electricity boards / utilities** | Benefit from AI-driven load reduction |
| **Property developers** | Embed HomeAI in smart apartments |
| **Elderly / accessibility users** | Hands-free home control |

---

## 🏗️ Architecture

```
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
```

---

## 🚀 Quick Start

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/homeai.git
cd homeai
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Add your API key
Create `.streamlit/secrets.toml`:
```toml
ANTHROPIC_API_KEY = "sk-ant-YOUR_KEY_HERE"
```
Get a free key at [console.anthropic.com](https://console.anthropic.com)

### 4. Run the app
```bash
streamlit run src/app.py
```

Open `http://localhost:8501` in your browser. ✅

---

## 💡 Example Commands

| Command | Mode Activated |
|---|---|
| `"Set movie night mode"` | Movie Night — dims lights, cool AC, TV on, curtains closed |
| `"Save electricity, nobody's home"` | Energy Saver — all non-essentials off, door locked |
| `"Good morning routine"` | Morning — full brightness, fresh air, curtains open |
| `"Set romantic dinner ambiance"` | Romantic — warm dim lights, soft music, AC mild |
| `"Prepare for sleep"` | Sleep Mode — lights off, fan low, lock door |
| `"Work from home mode"` | Work Mode — bright lights, cool AC, music soft |
| `"Turn AC to 20 degrees"` | Custom — single device command |

---

## 📋 JSON Automation Workflow Format

Every user command generates a structured JSON workflow:

```json
{
  "mode": "Movie Night",
  "actions": [
    { "device": "Lights",    "action": "Brightness",   "value": "30%"    },
    { "device": "AC",        "action": "Temperature",  "value": "22°C"   },
    { "device": "Smart TV",  "action": "Power",        "value": "ON"     },
    { "device": "Curtains",  "action": "Close",        "value": "Closed" },
    { "device": "Music System", "action": "Volume",   "value": "20%"    }
  ],
  "energy_saving_tip": "Switch to LED bulbs to reduce lighting energy by 60%."
}
```

---

## 📁 Project Structure

```
homeai/
├── src/
│   ├── app.py                 # Main Streamlit application
│   ├── automation_engine.py   # Anthropic API wrapper + prompt
│   ├── device_simulator.py    # Smart device state machine
│   └── energy_tracker.py      # Energy usage + savings tracker
├── tests/
│   └── test_homeai.py         # 19 unit tests (100% pass)
├── docs/
│   ├── architecture.md        # System design document
│   └── demo_script.md         # 6-minute demo video script
├── assets/
│   └── homeai_dashboard.html  # Standalone web demo (no backend)
├── .streamlit/
│   └── secrets.toml           # API key (not committed)
├── requirements.txt
└── README.md
```

---

## 🧪 Testing

```bash
# Run all tests
pytest tests/test_homeai.py -v

# Expected output: 19 passed
```

Test coverage includes:
- Device state transitions (on/off, brightness, temperature)
- Workflow application (movie night, energy saver, etc.)
- Device alias resolution (e.g. "Air Conditioner" = "AC")
- Energy tracker savings accumulation
- JSON schema validation
- Edge cases (unknown devices, missing fields)

---

## 🔌 Tech Stack

| Component | Technology |
|---|---|
| AI Engine | Anthropic Claude claude-sonnet-4-20250514 |
| Frontend | Streamlit + HTML/CSS/JS |
| Device Simulation | Python (custom state machine) |
| API Client | `anthropic` Python SDK |
| Testing | pytest |
| Config | Streamlit secrets / dotenv |

---

## ⚡ Generative AI Integration

HomeAI uses Claude as its **core reasoning engine**, not just a chatbot. The AI:

1. **Understands intent** — "nobody's home" → Energy Saver mode
2. **Infers context** — "movie night" → dims lights + AC + TV (multi-device)
3. **Generates workflows** — structured JSON, not plain text
4. **Provides energy tips** — actionable suggestions per mode
5. **Handles ambiguity** — graceful fallback for unknown requests

The system prompt locks Claude into the role of HomeAI, enforcing JSON-only output and device-awareness.

---

## 🌍 Future Scope

- **Samsung SmartThings SDK** integration for real device control
- **Voice input** via Web Speech API or Whisper
- **Scheduled automations** — "set sleep mode at 11 PM daily"
- **ML-based habit learning** — auto-suggest modes based on time/context
- **Multi-room support** — bedroom, kitchen, living room zones
- **WhatsApp / Telegram bot** interface
- **Zigbee / Matter protocol** bridge for generic smart devices
- **Solar panel integration** — optimize for renewable energy availability
- **Family profiles** — personalized modes per family member

---

## 👥 Team

Built for **Samsung PRISM GenAI Hackathon 2025**

---

## 📄 License

MIT License — see [LICENSE](LICENSE)
