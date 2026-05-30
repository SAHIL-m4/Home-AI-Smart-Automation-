"""
HomeAI Device Simulator
Simulates smart home devices and applies AI-generated automation workflows.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any


class DeviceSimulator:
    """Simulates a set of smart home devices."""

    DEVICE_DEFAULTS = {
        "lights":   {"name": "Lights",         "icon": "💡", "on": True,  "detail": "Brightness: 80%"},
        "fan":      {"name": "Fan",             "icon": "🌀", "on": True,  "detail": "Speed: 60%"},
        "ac":       {"name": "Air Conditioner", "icon": "❄️", "on": False, "detail": "Temp: 24°C"},
        "tv":       {"name": "Smart TV",        "icon": "📺", "on": False, "detail": "Standby"},
        "music":    {"name": "Music System",    "icon": "🎵", "on": False, "detail": "Volume: 40%"},
        "door":     {"name": "Door Lock",       "icon": "🔒", "on": True,  "detail": "Locked"},
        "curtains": {"name": "Curtains",        "icon": "🪟", "on": True,  "detail": "Open"},
    }

    # Maps AI-returned device names → internal device IDs
    DEVICE_ALIASES: Dict[str, str] = {
        "lights":       "lights",
        "light":        "lights",
        "fan":          "fan",
        "ac":           "ac",
        "air conditioner": "ac",
        "air conditioning": "ac",
        "smart tv":     "tv",
        "tv":           "tv",
        "television":   "tv",
        "music system": "music",
        "music":        "music",
        "speaker":      "music",
        "door lock":    "door",
        "door":         "door",
        "lock":         "door",
        "curtains":     "curtains",
        "curtain":      "curtains",
        "blinds":       "curtains",
    }

    def __init__(self):
        # Deep-copy defaults into mutable state
        self.devices: Dict[str, Dict[str, Any]] = {
            k: dict(v) for k, v in self.DEVICE_DEFAULTS.items()
        }

    # ── Public API ────────────────────────────────────────────────────────────

    def apply_workflow(self, workflow: dict) -> List[str]:
        """Apply an AI-generated automation workflow. Returns human-readable execution log."""
        log: List[str] = []
        actions = workflow.get("actions", [])

        for action in actions:
            device_name = action.get("device", "").lower().strip()
            action_type = action.get("action", "").strip()
            value       = action.get("value", "").strip()

            device_id = self.DEVICE_ALIASES.get(device_name)
            if not device_id:
                log.append(f"⚠️  Unknown device '{device_name}' — skipped")
                continue

            result = self._apply_action(device_id, action_type, value)
            log.append(result)

        return log

    def get_energy_usage(self) -> float:
        """Returns simulated kWh based on active devices."""
        weights = {"lights": 0.3, "fan": 0.2, "ac": 1.2, "tv": 0.5,
                   "music": 0.15, "door": 0.05, "curtains": 0.1}
        return sum(
            weights.get(dev_id, 0.1)
            for dev_id, dev in self.devices.items()
            if dev["on"]
        )

    def get_status_summary(self) -> Dict[str, str]:
        """Returns {device_name: status_string} for all devices."""
        return {
            dev["name"]: ("ON  — " + dev["detail"]) if dev["on"] else "OFF"
            for dev in self.devices.values()
        }

    # ── Private helpers ───────────────────────────────────────────────────────

    def _apply_action(self, device_id: str, action_type: str, value: str) -> str:
        dev = self.devices[device_id]
        name = dev["name"]
        action_lower = action_type.lower()

        if action_lower == "power":
            dev["on"] = value.upper() == "ON"
            dev["detail"] = f"Power: {value}"
        elif action_lower in ("brightness",):
            dev["on"] = True
            dev["detail"] = f"Brightness: {value}"
        elif action_lower in ("temperature", "temp"):
            dev["on"] = True
            dev["detail"] = f"Temperature: {value}"
        elif action_lower in ("speed", "fan speed"):
            dev["on"] = True
            dev["detail"] = f"Speed: {value}"
        elif action_lower in ("volume",):
            dev["on"] = True
            dev["detail"] = f"Volume: {value}"
        elif action_lower in ("close", "lock"):
            dev["on"] = True
            dev["detail"] = value
        elif action_lower in ("open", "unlock"):
            dev["on"] = False
            dev["detail"] = value
        else:
            # Generic fallback
            dev["on"] = value.upper() not in ("OFF", "LOCKED")
            dev["detail"] = f"{action_type}: {value}"

        status = "ON" if dev["on"] else "OFF"
        return f"{name} — {action_type}: {value} ({status})"

    def reset(self):
        """Reset all devices to factory defaults."""
        self.devices = {k: dict(v) for k, v in self.DEVICE_DEFAULTS.items()}
