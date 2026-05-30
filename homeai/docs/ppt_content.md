# HomeAI — PowerPoint Presentation Content
## Samsung PRISM GenAI Hackathon 2025
### 10 Slides

---

## SLIDE 1 — Title Slide

**Headline:** HomeAI
**Subheadline:** Generative AI Powered Smart Home Automation
**Event:** Samsung PRISM GenAI Hackathon 2025
**Theme:** Home AI & Smart Automation
**Visual:** Dark background with glowing smart home icon; subtle circuit-board pattern

---

## SLIDE 2 — The Problem

**Headline:** Smart Homes Are Not Smart Enough

**Pain points (3 columns):**
- 🖱️ **Too Complex** — Multiple apps, manual controls, separate interfaces per device
- 🧠 **No Context Awareness** — Devices don't understand human intent or context
- ⚡ **Energy Waste** — 30% of home energy wasted due to poor scheduling and manual forgetting

**Bottom stat:** 57% of smart home users find current interfaces frustrating *(Deloitte 2024)*

**Visual:** Three icons in a row; frustrated user graphic on the right

---

## SLIDE 3 — The Solution

**Headline:** HomeAI — Control Your Home With Your Words

**One-liner:** Natural language in → Intelligent automation out

**Three value props:**
- 💬 **Speak Naturally** — No menus, no app navigation, no tapping
- 🤖 **AI Understands Intent** — "Movie night" → 5 devices configured correctly
- ⚡ **Saves Energy** — AI suggests and applies optimizations automatically

**Visual:** Phone with chat bubble → smart home illustration with connected devices

---

## SLIDE 4 — Stakeholders

**Headline:** Who Benefits?

| Stakeholder | Benefit |
|---|---|
| 🏠 Homeowners | Effortless, voice/text control of entire home |
| 👴 Elderly / Accessibility Users | Hands-free, no-app-needed home management |
| ⚡ Electricity Utilities | Reduced peak load via AI-driven optimization |
| 🏗️ Property Developers | Premium smart apartment feature |
| 📱 Samsung SmartThings | Ready-to-integrate AI orchestration layer |

**Visual:** Web diagram with HomeAI at center, stakeholders as nodes

---

## SLIDE 5 — System Architecture

**Headline:** 3-Layer AI Architecture

```
[USER] → Natural Language → [AI ENGINE / Claude API]
                                      ↓ JSON Workflow
                           [DEVICE SIMULATOR LAYER]
                      💡 Fan ❄️ 📺 🎵 🔒 🪟
                                      ↓
                           [ENERGY TRACKER]
```

**Key points:**
- Claude acts as the **reasoning engine**, not just a chatbot
- AI output is **structured JSON** — machine-executable
- Device layer is **modular** — swap simulation for Samsung SmartThings SDK

**Visual:** Architecture flow diagram with color-coded layers

---

## SLIDE 6 — Generative AI Integration

**Headline:** How the AI Works

**Left: System Prompt Design**
- Defines HomeAI persona and role
- Enumerates 7 controllable devices
- Enforces JSON-only output format
- Provides value conventions (%, °C)
- Includes few-shot examples

**Right: JSON Automation Workflow**
```json
{
  "mode": "Movie Night",
  "actions": [
    {"device": "Lights", "action": "Brightness", "value": "30%"},
    {"device": "AC",     "action": "Temperature", "value": "22°C"},
    {"device": "Smart TV","action": "Power",      "value": "ON"}
  ],
  "energy_saving_tip": "Turn off devices after the movie."
}
```

**Visual:** Two-column layout with code block on right

---

## SLIDE 7 — Demo Highlights

**Headline:** Live Demo — 3 Key Scenarios

**Scenario 1: Movie Night Mode**
- Input: *"Set movie night mode"*
- Result: 5 devices configured, energy tip generated

**Scenario 2: Energy Saver**
- Input: *"Save electricity, nobody's home"*
- Result: 85% energy reduction, door locked, ₹25 saved

**Scenario 3: Context-Aware Command**
- Input: *"I have a headache, make it quiet and dim"*
- Result: AI infers correct config without explicit mode

**Bottom line:** AI reasons from context — not keyword matching

**Visual:** Three phone mockups side by side, each showing the chat + result

---

## SLIDE 8 — Technical Depth

**Headline:** Built for Real-World Extension

**4 technical highlights:**

1. **Alias Resolution Engine** — "Air Conditioner" / "AC" / "air conditioning" all resolve correctly
2. **Schema Validation** — AI output validated before device execution; graceful error handling
3. **Energy Simulation** — Device-weighted kWh calculation with per-mode savings tracking
4. **19 Unit Tests, 100% passing** — Covers state transitions, aliases, JSON schema, edge cases

**Code quality:** Modular, 3-file backend; swapping AI providers requires changing 1 file

**Visual:** Code snippet + test results screenshot

---

## SLIDE 9 — Future Scope

**Headline:** HomeAI Is Just Getting Started

**6 next steps (icon + label grid):**
- 📡 **SmartThings SDK** — Real device control (not simulation)
- 🎤 **Voice Input** — Whisper / Web Speech API integration
- 🧠 **Habit Learning** — ML model learns your daily patterns
- 🗓️ **Scheduled Automation** — "Sleep mode every night at 11 PM"
- ☀️ **Solar Integration** — Optimize devices for renewable energy
- 👨‍👩‍👧 **Family Profiles** — Personalized modes per family member

**Bottom tagline:** *The hardware already exists. HomeAI gives it intelligence.*

**Visual:** Timeline or roadmap graphic

---

## SLIDE 10 — Closing

**Headline:** HomeAI — Natural Language for Every Home

**Three impact numbers:**
- **7** smart devices controlled
- **85%** energy reduction in saver mode
- **1 sentence** to orchestrate everything

**Call to action:** *"Try it: github.com/YOUR_USERNAME/homeai"*

**Quote:** *"The best interface is no interface — just human intention."*

**Team / acknowledgements**

**Visual:** Full-screen dark background, glowing home graphic, Samsung PRISM logo

---

## Design Notes for Slides

- **Color palette:** Deep navy (#0a0f1e) background, electric blue (#3b82f6) accents, white text
- **Font:** Heading — Samsung One (or Exo 2); Body — Inter or Noto Sans
- **Animations:** Subtle fade-in per bullet point; no distracting transitions
- **Consistency:** Same icon set (Phosphor Icons or Tabler) throughout
- **Max text per slide:** 40 words — let visuals carry the story
