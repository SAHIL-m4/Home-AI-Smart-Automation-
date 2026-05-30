# HomeAI — 6-Minute Demo Video Script
## Samsung PRISM GenAI Hackathon 2025

---

## 🎬 SEGMENT 1 — Introduction (0:00–0:45)

**[Screen: Title slide — "HomeAI: Generative AI Powered Smart Home Automation"]**

> *"Hi everyone. Today I'm presenting HomeAI — a smart home assistant that lets you control every device in your house using plain English.*
>
> *The problem we're solving: most smart home apps force you to open an app, navigate menus, and tap individual controls. HomeAI removes all of that. You just say what you want — and the AI figures out exactly how to make it happen."*

**[Screen: Switch to the live dashboard]**

> *"Here's our prototype running live. On the left you can see 7 simulated smart devices — lights, fan, AC, TV, music system, door lock, and curtains. On the right is real-time energy monitoring. And in the center is the AI chat interface."*

---

## 🎬 SEGMENT 2 — Architecture Overview (0:45–1:30)

**[Screen: Architecture diagram from docs/architecture.md]**

> *"Let me quickly show you the architecture. The user types a natural-language command. That goes to our Automation Engine, which calls the Anthropic Claude API with a carefully engineered system prompt that casts Claude in the role of HomeAI.*
>
> *Claude returns a structured JSON automation workflow — listing exactly which devices to control, with what actions and values. Our Device Simulator layer applies those actions in real time, and the Energy Tracker records any savings.*
>
> *The key insight: the AI doesn't just chat — it generates executable machine-readable workflows. That's what makes this technically deep, not just a chatbot."*

---

## 🎬 SEGMENT 3 — Live Demo: Movie Night (1:30–2:45)

**[Screen: Chat interface — type the command live]**

> *"Let's try our first command. I'll type: 'Set movie night mode'."*

**[Type and hit enter. Show the AI thinking indicator, then the JSON response appearing.]**

> *"Watch what happens. HomeAI calls the Claude API, and within about two seconds, returns this structured JSON workflow.*
>
> *It's dimmed the lights to 30%, set the AC to 22°C for comfort, turned on the Smart TV, closed the curtains to reduce glare, and lowered the music volume so it doesn't compete with the TV audio.*
>
> *Five devices — configured intelligently from three words. And notice the energy tip: 'Turn off unused devices after the movie.' That's the AI proactively thinking about efficiency."*

**[Point to device panel updating on the left]**

> *"All devices update in real time. The energy monitor also adjusts to reflect the new device states."*

---

## 🎬 SEGMENT 4 — Live Demo: Energy Saver (2:45–3:45)

**[Type: "Save electricity, nobody is home"]**

> *"Now a more practical scenario. I'm leaving the house and I say: 'Save electricity, nobody is home'.*
>
> *HomeAI turns off the lights, shuts down the AC, turns off the TV and music system — and locks the door. Notice the door was already locked, so HomeAI correctly keeps it that way.*
>
> *The energy usage dropped from 2.4 kWh to 0.1 kWh — an 85% reduction. The savings counter ticks up. That's real, measurable impact — and it took one sentence."*

---

## 🎬 SEGMENT 5 — Live Demo: Custom Command (3:45–4:30)

**[Type: "I have a headache, make it quiet and dim"]**

> *"Let's try something the AI has never been explicitly trained on — a health-context command: 'I have a headache, make it quiet and dim'.*
>
> *The AI correctly infers: dim the lights to 10%, turn off the TV, lower the fan speed to reduce noise, turn off the music, and set the AC to a comfortable 23°C.*
>
> *There's no 'headache mode' in our system. Claude reasons from the user's context and derives the right device configuration. That's genuine generative intelligence — not just keyword matching."*

---

## 🎬 SEGMENT 6 — Technical Depth (4:30–5:15)

**[Screen: Show the code / test results]**

> *"Let me briefly highlight the technical architecture.*
>
> *The system has three layers: the Automation Engine wraps the Anthropic API with a structured system prompt that enforces JSON-only output and defines all 7 devices. The Device Simulator is a deterministic state machine with alias resolution — so 'Air Conditioner', 'AC', and 'air conditioning' all map to the same device. And the Energy Tracker logs savings with timestamps.*
>
> *We have 19 unit tests, all passing, covering device state transitions, workflow application, edge cases like unknown devices, and JSON schema validation.*
>
> *The entire backend is modular — swapping the Anthropic API for Samsung's on-device AI model would require changing exactly one file: automation_engine.py."*

---

## 🎬 SEGMENT 7 — Impact & Future Scope (5:15–5:45)

**[Screen: Future scope slide]**

> *"HomeAI addresses a real gap. Smart home adoption is growing fast, but complexity is the #1 barrier. Elderly users, non-technical users, anyone who finds apps frustrating — they can talk to HomeAI.*
>
> *In the future, this connects to Samsung SmartThings for real device control, adds voice input, learns your habits over time, and integrates with renewable energy systems to optimize for solar availability.*
>
> *The Samsung PRISM context is a perfect fit: SmartThings + Bixby + a GenAI reasoning layer = the future of home automation."*

---

## 🎬 SEGMENT 8 — Closing (5:45–6:00)

> *"HomeAI demonstrates that Generative AI can go far beyond conversation. It can reason, plan, and act — making real-world systems more intelligent and accessible.*
>
> *Thank you. The GitHub repository, architecture docs, and full test suite are all ready for review. Happy to take questions."*

---

## 📝 Demo Tips

- Have the dashboard open and warmed up before recording
- Use a clean browser window — no other tabs visible
- Run through the script once to make sure API calls complete within 3 seconds
- If the API is slow, pre-record the AI response segment and cut to it
- Show the JSON block on screen for at least 5 seconds per demo — judges will read it
- Keep the energy monitor visible whenever possible — it shows real-time impact
