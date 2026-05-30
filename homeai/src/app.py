"""
HomeAI - Generative AI Powered Smart Home Automation
Samsung PRISM GenAI Hackathon 2025
Main Streamlit Application
"""

import streamlit as st
import anthropic
import json
import time
from datetime import datetime
from device_simulator import DeviceSimulator
from energy_tracker import EnergyTracker

# ─── Page Config ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="HomeAI - Smart Home Assistant",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── Custom CSS ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .stApp { background-color: #0a0f1e; color: #e2e8f0; }
    .metric-card {
        background: #111827;
        border: 1px solid #1e2d4a;
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 12px;
    }
    .device-on  { color: #34d399; font-weight: bold; }
    .device-off { color: #64748b; }
    .json-block {
        background: #060a14;
        border-radius: 8px;
        padding: 12px;
        font-family: monospace;
        font-size: 12px;
        border: 1px solid #1e2d4a;
    }
    .energy-tip {
        background: #0f2235;
        border-left: 3px solid #3b82f6;
        border-radius: 4px;
        padding: 10px 14px;
        margin-top: 10px;
    }
</style>
""", unsafe_allow_html=True)

# ─── Initialise Session State ────────────────────────────────────────────────
if "simulator" not in st.session_state:
    st.session_state.simulator = DeviceSimulator()
if "energy" not in st.session_state:
    st.session_state.energy = EnergyTracker()
if "messages" not in st.session_state:
    st.session_state.messages = []
if "activity_log" not in st.session_state:
    st.session_state.activity_log = []

# ─── HomeAI System Prompt ────────────────────────────────────────────────────
SYSTEM_PROMPT = """You are HomeAI, an intelligent Generative AI assistant for smart home automation.
Your task is to understand natural-language home automation requests and convert them into structured automation actions.

You control: Lights, Fan, Air Conditioner (AC), Smart TV, Music System, Door Lock, Curtains.

Goals: 
1. Interpret user intent accurately.
2. Generate smart automation workflows.
3. Optimize for comfort, convenience, security, and energy efficiency.

ALWAYS respond with ONLY valid JSON in this exact format:
{
  "mode": "name of automation mode",
  "actions": [
    { "device": "device name", "action": "action type", "value": "value/settings" }
  ],
  "energy_saving_tip": "short actionable suggestion"
}

Rules:
- Use percentages for brightness/fan speed (e.g., "30%")
- Use Celsius for temperature (e.g., "22°C")  
- For moods like "movie night" or "romantic mode", configure multiple devices
- For energy saving, turn off non-essential devices
- Always include a practical energy_saving_tip
- Return ONLY JSON - no preamble, no explanation outside JSON"""


# ─── AI Automation Engine ────────────────────────────────────────────────────
def generate_automation(user_input: str) -> dict:
    """Call Anthropic API and parse JSON automation workflow."""
    client = anthropic.Anthropic(api_key=st.secrets.get("ANTHROPIC_API_KEY", ""))
    
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1000,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_input}]
    )
    
    raw = response.content[0].text.strip()
    # Strip potential markdown fences
    raw = raw.replace("```json", "").replace("```", "").strip()
    return json.loads(raw)


# ─── Sidebar: Device Dashboard ───────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🏠 HomeAI Dashboard")
    st.caption(f"Samsung PRISM GenAI 2025  •  {datetime.now().strftime('%I:%M %p')}")
    st.divider()

    # Device Status
    st.markdown("### 📡 Device Status")
    sim = st.session_state.simulator
    
    for device_id, device in sim.devices.items():
        col1, col2 = st.columns([3, 1])
        with col1:
            icon = device["icon"]
            name = device["name"]
            detail = device["detail"]
            st.markdown(f"{icon} **{name}**  \n<small style='color:#64748b'>{detail}</small>", 
                       unsafe_allow_html=True)
        with col2:
            status_color = "device-on" if device["on"] else "device-off"
            label = "ON" if device["on"] else "OFF"
            st.markdown(f"<span class='{status_color}'>{label}</span>", unsafe_allow_html=True)

    st.divider()

    # Energy Monitor
    st.markdown("### ⚡ Energy Monitor")
    usage = sim.get_energy_usage()
    savings = st.session_state.energy.total_savings
    
    col1, col2 = st.columns(2)
    col1.metric("Usage", f"{usage:.1f} kWh", delta="-0.3 kWh")
    col2.metric("Saved", f"₹{savings}", delta=f"+₹{savings}")
    
    usage_pct = min(usage / 6.0 * 100, 100)
    st.progress(usage_pct / 100, text=f"{usage_pct:.0f}% of daily budget")

    st.divider()

    # Quick Presets
    st.markdown("### 🎯 Quick Presets")
    presets = {
        "🎬 Movie Night": "Set movie night mode",
        "🌙 Sleep Mode": "Prepare for sleep, dim everything",
        "☀️ Good Morning": "Start my morning routine",
        "⚡ Energy Saver": "Save electricity, nobody is home",
        "💼 Work Mode": "Set up home office work mode",
        "🕯️ Romantic": "Set romantic dinner ambiance"
    }
    
    for label, prompt in presets.items():
        if st.button(label, use_container_width=True):
            st.session_state["preset_input"] = prompt


# ─── Main Chat Interface ──────────────────────────────────────────────────────
st.markdown("# 🏠 HomeAI — Smart Home Assistant")
st.markdown("> *Powered by Generative AI — Control your home with natural language*")

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        if msg["role"] == "user":
            st.write(msg["content"])
        else:
            st.write(f"**{msg.get('mode', 'Automation')} mode activated.**")
            
            if "json_data" in msg:
                with st.expander("📋 View Automation Workflow (JSON)", expanded=True):
                    st.json(msg["json_data"])
            
            if "exec_log" in msg:
                st.markdown("**Execution Log:**")
                for item in msg["exec_log"]:
                    st.success(f"✅ {item}")
            
            if "tip" in msg:
                st.info(f"💡 **Energy Tip:** {msg['tip']}")

# Chat input
preset_val = st.session_state.pop("preset_input", "")
user_input = st.chat_input("Tell HomeAI what you need...") or preset_val

if user_input:
    # Show user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    # Generate AI response
    with st.chat_message("assistant"):
        with st.spinner("🤖 HomeAI is thinking..."):
            try:
                workflow = generate_automation(user_input)
                
                # Apply to device simulator
                exec_log = st.session_state.simulator.apply_workflow(workflow)
                
                # Track energy savings
                if "energy" in workflow.get("mode", "").lower() or "saver" in workflow.get("mode", "").lower():
                    st.session_state.energy.record_saving(25)
                
                # Log activity
                ts = datetime.now().strftime("%H:%M")
                st.session_state.activity_log.append({
                    "time": ts,
                    "action": f"{workflow.get('mode', 'Custom')} mode activated",
                    "actions": len(workflow.get("actions", []))
                })
                
                # Display result
                mode = workflow.get("mode", "Automation")
                st.success(f"✨ **{mode}** mode activated!")
                
                with st.expander("📋 Automation Workflow (JSON)", expanded=True):
                    st.json(workflow)
                
                st.markdown("**⚡ Executing actions:**")
                for item in exec_log:
                    time.sleep(0.1)
                    st.success(f"✅ {item}")
                
                tip = workflow.get("energy_saving_tip", "")
                if tip:
                    st.info(f"💡 **Energy Tip:** {tip}")
                
                # Save to session
                st.session_state.messages.append({
                    "role": "assistant",
                    "mode": mode,
                    "json_data": workflow,
                    "exec_log": exec_log,
                    "tip": tip
                })
                
                st.rerun()

            except json.JSONDecodeError:
                st.error("HomeAI returned invalid JSON. Please retry.")
            except anthropic.AuthenticationError:
                st.error("Invalid API key. Add ANTHROPIC_API_KEY to .streamlit/secrets.toml")
            except Exception as e:
                st.error(f"Error: {str(e)}")
