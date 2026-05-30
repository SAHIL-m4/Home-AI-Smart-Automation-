"""
HomeAI Automation Engine
Core AI layer: calls Anthropic API and validates the returned workflow.
"""

import json
import anthropic
from typing import Optional


SYSTEM_PROMPT = """You are HomeAI, an intelligent Generative AI assistant for smart home automation.
Your task is to understand natural-language home automation requests and convert them into structured automation actions.

You control the following smart devices:
- Lights
- Fan
- Air Conditioner (AC)
- Smart TV
- Music System
- Door Lock
- Curtains

Goals:
1. Interpret user intent accurately.
2. Generate smart automation workflows.
3. Optimize for comfort, convenience, security, and energy efficiency.
4. Respond in clean JSON format only.

RULES:
- Always return valid JSON and nothing else.
- Do not include explanations outside JSON.
- Use percentages for brightness/fan speed (e.g., "30%").
- Use Celsius for temperature (e.g., "22°C").
- For moods like "movie night" or "romantic mode", intelligently configure multiple devices.
- For energy saving requests, reduce unnecessary device usage.
- Always include an energy_saving_tip.

JSON FORMAT:
{
  "mode": "name of automation mode",
  "actions": [
    {
      "device": "device name",
      "action": "action type",
      "value": "value/settings"
    }
  ],
  "energy_saving_tip": "short actionable suggestion"
}"""


class AutomationEngine:
    """Wraps the Anthropic client and handles prompt → workflow conversion."""

    def __init__(self, api_key: str, model: str = "claude-sonnet-4-20250514"):
        self.client = anthropic.Anthropic(api_key=api_key)
        self.model = model

    def generate(self, user_input: str, conversation_history: Optional[list] = None) -> dict:
        """
        Send user_input to Claude and return a parsed automation workflow dict.
        Raises json.JSONDecodeError if the model returns invalid JSON.
        """
        messages = conversation_history or []
        messages = messages + [{"role": "user", "content": user_input}]

        response = self.client.messages.create(
            model=self.model,
            max_tokens=1000,
            system=SYSTEM_PROMPT,
            messages=messages,
        )

        raw = response.content[0].text.strip()
        # Strip accidental markdown fences
        raw = raw.replace("```json", "").replace("```", "").strip()

        workflow = json.loads(raw)
        self._validate(workflow)
        return workflow

    @staticmethod
    def _validate(workflow: dict) -> None:
        """Raise ValueError if required fields are missing."""
        if "mode" not in workflow:
            raise ValueError("Workflow missing 'mode' field")
        if "actions" not in workflow or not isinstance(workflow["actions"], list):
            raise ValueError("Workflow missing 'actions' list")
        for a in workflow["actions"]:
            for field in ("device", "action", "value"):
                if field not in a:
                    raise ValueError(f"Action missing '{field}' field: {a}")
