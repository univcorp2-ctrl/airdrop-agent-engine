from .base import BaseAdapter
class KyanAdapter(BaseAdapter):
    def build_candidate(self,notional_usd:float)->dict[str,object]:
        c=super().build_candidate(notional_usd); c.update({"kind":"mcp_api_route_candidate","transport":"official Kyan MCP/API discovery only","official_mcp_docs":"https://docs.kyan.blue/docs/mcp","public_exchange_info":"https://sandbox.kyan.sh/api/v1/exchange_info","tool_intent":"prepare_order_route","mcp_secret_forwarding":False,"signature":None,"send":False,"reward_eligibility":"UNVERIFIED_FOR_API_ORIGINATED_TRADES"}); return c
