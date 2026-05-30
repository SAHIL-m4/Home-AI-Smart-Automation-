"""
HomeAI Test Suite
Run with: pytest tests/test_homeai.py -v
"""

import json
import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from device_simulator import DeviceSimulator
from energy_tracker import EnergyTracker


# ─── DeviceSimulator Tests ──────────────────────────────────────────────────

class TestDeviceSimulator:

    def setup_method(self):
        self.sim = DeviceSimulator()

    def _make_workflow(self, actions):
        return {"mode": "Test", "actions": actions, "energy_saving_tip": "tip"}

    def test_initial_state(self):
        assert self.sim.devices["lights"]["on"] is True
        assert self.sim.devices["ac"]["on"] is False

    def test_power_on(self):
        wf = self._make_workflow([{"device": "AC", "action": "Power", "value": "ON"}])
        self.sim.apply_workflow(wf)
        assert self.sim.devices["ac"]["on"] is True

    def test_power_off(self):
        wf = self._make_workflow([{"device": "Lights", "action": "Power", "value": "OFF"}])
        self.sim.apply_workflow(wf)
        assert self.sim.devices["lights"]["on"] is False

    def test_brightness(self):
        wf = self._make_workflow([{"device": "Lights", "action": "Brightness", "value": "30%"}])
        self.sim.apply_workflow(wf)
        assert "30%" in self.sim.devices["lights"]["detail"]
        assert self.sim.devices["lights"]["on"] is True

    def test_temperature(self):
        wf = self._make_workflow([{"device": "AC", "action": "Temperature", "value": "22°C"}])
        self.sim.apply_workflow(wf)
        assert "22°C" in self.sim.devices["ac"]["detail"]

    def test_movie_night_workflow(self):
        wf = {
            "mode": "Movie Night",
            "actions": [
                {"device": "Lights", "action": "Brightness", "value": "30%"},
                {"device": "AC", "action": "Temperature", "value": "22°C"},
                {"device": "Smart TV", "action": "Power", "value": "ON"},
                {"device": "Curtains", "action": "Close", "value": "Closed"},
            ],
            "energy_saving_tip": "Turn off unused devices after the movie."
        }
        log = self.sim.apply_workflow(wf)
        assert len(log) == 4
        assert self.sim.devices["tv"]["on"] is True
        assert self.sim.devices["ac"]["on"] is True

    def test_energy_saver_workflow(self):
        wf = {
            "mode": "Energy Saver",
            "actions": [
                {"device": "Lights", "action": "Power", "value": "OFF"},
                {"device": "AC", "action": "Power", "value": "OFF"},
                {"device": "Door Lock", "action": "Lock", "value": "Locked"},
            ],
            "energy_saving_tip": "Use motion sensors."
        }
        self.sim.apply_workflow(wf)
        assert self.sim.devices["lights"]["on"] is False
        assert self.sim.devices["ac"]["on"] is False

    def test_unknown_device_skipped(self):
        wf = self._make_workflow([{"device": "Robot Vacuum", "action": "Power", "value": "ON"}])
        log = self.sim.apply_workflow(wf)
        assert any("skipped" in l for l in log)

    def test_energy_usage_increases_with_devices(self):
        # Turn everything off first
        for dev in self.sim.devices.values():
            dev["on"] = False
        baseline = self.sim.get_energy_usage()
        # Turn AC on (heaviest consumer)
        self.sim.devices["ac"]["on"] = True
        assert self.sim.get_energy_usage() > baseline

    def test_reset(self):
        self.sim.devices["lights"]["on"] = False
        self.sim.reset()
        assert self.sim.devices["lights"]["on"] is True

    def test_device_aliases(self):
        aliases = ["Air Conditioner", "air conditioning", "AC"]
        for alias in aliases:
            self.sim.reset()
            wf = self._make_workflow([{"device": alias, "action": "Power", "value": "ON"}])
            self.sim.apply_workflow(wf)
            assert self.sim.devices["ac"]["on"] is True, f"Alias '{alias}' failed"


# ─── EnergyTracker Tests ─────────────────────────────────────────────────────

class TestEnergyTracker:

    def setup_method(self):
        self.tracker = EnergyTracker()

    def test_initial_savings_zero(self):
        assert self.tracker.total_savings == 0

    def test_record_saving(self):
        self.tracker.record_saving(25)
        assert self.tracker.total_savings == 25

    def test_multiple_savings(self):
        self.tracker.record_saving(25)
        self.tracker.record_saving(15)
        assert self.tracker.total_savings == 40

    def test_saving_percentage(self):
        self.tracker.record_saving(30)
        pct = self.tracker.saving_percentage()
        assert 0 < pct <= 100

    def test_summary_structure(self):
        self.tracker.record_saving(20, reason="Movie Night optimisation")
        summary = self.tracker.summary()
        assert "total_savings_inr" in summary
        assert "saving_pct" in summary
        assert "events" in summary
        assert summary["events"][0]["reason"] == "Movie Night optimisation"


# ─── JSON Workflow Schema Tests ──────────────────────────────────────────────

class TestWorkflowSchema:

    VALID_WORKFLOW = {
        "mode": "Movie Night",
        "actions": [
            {"device": "Lights", "action": "Brightness", "value": "30%"},
            {"device": "AC", "action": "Temperature", "value": "22°C"},
            {"device": "Smart TV", "action": "Power", "value": "ON"},
        ],
        "energy_saving_tip": "Turn off unused devices after the movie."
    }

    def test_valid_json_parses(self):
        raw = json.dumps(self.VALID_WORKFLOW)
        parsed = json.loads(raw)
        assert parsed["mode"] == "Movie Night"

    def test_all_required_fields(self):
        wf = self.VALID_WORKFLOW
        assert "mode" in wf
        assert "actions" in wf
        assert "energy_saving_tip" in wf

    def test_action_fields(self):
        for action in self.VALID_WORKFLOW["actions"]:
            assert "device" in action
            assert "action" in action
            assert "value" in action
