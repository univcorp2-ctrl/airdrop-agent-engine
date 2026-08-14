from .base import BaseAdapter
class LighterAdapter(BaseAdapter):
    def build_candidate(self,notional_usd:float)->dict[str,object]:
        c=super().build_candidate(notional_usd); c.update({"kind":"inactive_points_program_candidate","transport":"Lighter API metadata only","send":False,"signature":None,"program_gate":"BLOCKED_SEASON_2_ENDED_2025_12_26","historical_api_points_rule":"organic UI/API strategies eligible during points program"}); return c
