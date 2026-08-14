from __future__ import annotations
import os,uuid
from datetime import datetime,timezone
from typing import Any
from ..core.ev_scorer import score_target
from ..core.legal_gate import evaluate_japan
from ..core.risk_engine import simulated_notional_usd
from ..execution_guard import LiveExecutionBlocked,assert_live_disabled,block_live
from ..http_client import PublicGetClient
from ..models import TargetConfig
class BaseAdapter:
    def __init__(self,target:TargetConfig,client:PublicGetClient|None=None): self.target=target; self.client=client or PublicGetClient()
    def probe(self,network:bool=False)->dict[str,Any]:
        if not network: return {"network":False,"status":"SKIPPED","checks":[]}
        checks=[self.client.get(url).to_dict() for url in self.target.health_urls]; return {"network":True,"status":"OK" if any(i["ok"] for i in checks) else "UNREACHABLE","checks":checks}
    def fetch_program_rules(self)->dict[str,Any]: return {"program_status":self.target.program_status,"program_version":self.target.program_version,"reward_unit":self.target.reward_unit,"api_reward_eligible":self.target.api_reward_eligible,"sources":self.target.sources}
    def fetch_terms_status(self)->dict[str,Any]:
        legal=evaluate_japan(self.target); return {"terms_status":self.target.terms_status,"japan_status":legal.status,"reason":legal.reason}
    def fetch_api_capabilities(self)->dict[str,Any]: return {"api_available":self.target.api_available,"public_get_only_in_agent":True,"live_submission_methods":0}
    def fetch_account_state(self)->dict[str,Any]:
        key_name=f"{self.target.id.upper().replace('-', '_')}_API_KEY"; present=bool(os.getenv(key_name)) if self.target.requires_api_key else False
        return {"auth_used":False,"credential_present":present,"balance":"UNREAD","position":"UNREAD","margin":"UNREAD","collateral":"UNREAD"}
    def fetch_rewards_state(self)->dict[str,Any]: return {"reward_unit":self.target.reward_unit,"reward_amount":"UNKNOWN","points_delta":"UNKNOWN","future_token_value":"UNKNOWN"}
    def estimate_cost(self,notional_usd:float|None=None)->dict[str,Any]:
        n=simulated_notional_usd() if notional_usd is None else max(0.0,notional_usd); fee=None if self.target.estimated_fee_bps is None else round(n*self.target.estimated_fee_bps/10000.0,8)
        return {"simulated_notional_usd":n,"fee_usd":fee if fee is not None else "UNKNOWN","spread_usd":"UNKNOWN","slippage_usd":"UNKNOWN","funding_usd":"UNKNOWN","gas_usd":"UNKNOWN","borrow_usd":"UNKNOWN","bridge_usd":"UNKNOWN","capital_lockup":"UNKNOWN","liquidation_risk":"NOT_APPLICABLE_NO_POSITION_OPENED","future_token_value":"UNKNOWN"}
    def build_candidate(self,notional_usd:float)->dict[str,Any]: return {"candidate_id":str(uuid.uuid4()),"kind":"generic_simulation","target":self.target.id,"notional_usd":notional_usd,"send":False,"signed":False,"http_method":"SIMULATED"}
    def dry_run(self,notional_usd:float|None=None)->dict[str,Any]:
        assert_live_disabled(); n=simulated_notional_usd() if notional_usd is None else max(0.0,notional_usd); blocked=[]
        if self.target.program_status!="ACTIVE": blocked.append("PROGRAM_NOT_ACTIVE")
        if self.target.api_reward_eligible is not True and self.target.mode=="DRY_RUN": blocked.append("API_REWARD_ELIGIBILITY_NOT_VERIFIED")
        if evaluate_japan(self.target).status!="PASS": blocked.append("LEGAL_REVIEW_REQUIRED_FOR_LIVE")
        candidate=self.build_candidate(n); candidate["executable"]=False
        return {"timestamp":datetime.now(timezone.utc).isoformat(),"target":self.target.id,"status":self.target.status,"program_status":self.target.program_status,"api_available":self.target.api_available,"api_reward_eligible":self.target.api_reward_eligible,"japan_status":evaluate_japan(self.target).status,"mode":"DRY_RUN","order_candidate_id":candidate["candidate_id"],"transaction_candidate_id":None,"candidate":candidate,"cost":self.estimate_cost(n),"rewards":self.fetch_rewards_state(),"open_exposure_usd":0.0,"reason":self.target.objective,"confidence":score_target(self.target)["overall_confidence"],"blocked_reasons":blocked,"stop_condition":blocked[0] if blocked and self.target.program_status!="ACTIVE" else None,"financial_actions_submitted":0,"wallet_signatures_requested":0,"network_writes":0}
    def execute(self,*_:Any,**__:Any)->None: block_live(); raise LiveExecutionBlocked("unreachable")
    def healthcheck(self,network:bool=False)->dict[str,Any]: return self.probe(network=network)
