from .base import BaseAdapter
class PacificaAdapter(BaseAdapter):
    def build_candidate(self,notional_usd:float)->dict[str,object]:
        c=super().build_candidate(notional_usd); c.update({"kind":"limit_order_candidate","transport":"Pacifica REST/WebSocket metadata only","symbol":"BTC","side":"bid","tif":"ALO","price":"MARKET_REFERENCE_REQUIRED","amount":"DERIVE_FROM_REFERENCE_PRICE","signature":None,"send":False,"safety":["no self-trade","no sybil","no wash trade","no manipulation"]}); return c
