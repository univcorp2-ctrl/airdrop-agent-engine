from .base import BaseAdapter
class HibachiAdapter(BaseAdapter):
    def build_candidate(self,notional_usd:float)->dict[str,object]:
        c=super().build_candidate(notional_usd); c.update({"kind":"api_order_candidate","transport":"Hibachi API/SDK metadata only","market":"BTC/USDT-PERP","side":"two-sided-evaluation-only","order_type":"limit","signature":None,"send":False,"ui_vs_api_points":"OFFICIAL_FAQ_SAME_ACTIVITY_FORMULA","safety":["no wash trading","no multi-account farming","no market manipulation"]}); return c
