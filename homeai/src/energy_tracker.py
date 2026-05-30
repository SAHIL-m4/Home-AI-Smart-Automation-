"""
HomeAI Energy Tracker
Tracks energy savings from AI-driven optimizations.
"""

from datetime import datetime
from typing import List, Dict


class EnergyTracker:
    """Records and summarises energy-saving events."""

    def __init__(self):
        self.total_savings: int = 0          # ₹ saved
        self.events: List[Dict] = []
        self.baseline_kwh: float = 6.0       # avg daily consumption
        self.optimised_kwh: float = 6.0

    def record_saving(self, amount_inr: int, reason: str = "AI optimisation"):
        self.total_savings += amount_inr
        self.optimised_kwh = max(0.5, self.optimised_kwh - 0.3)
        self.events.append({
            "time": datetime.now().strftime("%H:%M"),
            "amount": amount_inr,
            "reason": reason,
        })

    def saving_percentage(self) -> float:
        if self.baseline_kwh == 0:
            return 0.0
        return round((1 - self.optimised_kwh / self.baseline_kwh) * 100, 1)

    def summary(self) -> Dict:
        return {
            "total_savings_inr": self.total_savings,
            "baseline_kwh": self.baseline_kwh,
            "optimised_kwh": round(self.optimised_kwh, 2),
            "saving_pct": self.saving_percentage(),
            "events": self.events[-5:],   # last 5
        }
