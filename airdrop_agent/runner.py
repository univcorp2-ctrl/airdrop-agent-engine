from __future__ import annotations
from datetime import datetime,timezone
from pathlib import Path
from typing import Any
from .adapters import adapter_for
from .core.ev_scorer import score_target
from .core.legal_gate import evaluate_japan
from .core.logger import append_jsonl
from .core.scout import scout_record
from .execution_guard import LiveExecutionBlocked,assert_live_disabled
from .models import MODES,TargetConfig
from .reporting import write_reports
MODE_RANK={name:i for i,name in enumerate(MODES)}
def effective_mode(requested:str,configured:str)->str:
    requested=requested.upper()
    if requested=="LIVE": raise LiveExecutionBlocked("LIVE is not compiled in this release")
    return requested if MODE_RANK[requested]<=MODE_RANK[configured] else configured
def _base_row(target:TargetConfig,mode:str)->dict[str,Any]:
    legal=evaluate_japan(target); return {"target":target.id,"name":target.name,"status":target.status,"mode":mode,"program_status":target.program_status,"api_available":target.api_available,"api_reward_eligible":target.api_reward_eligible,"japan_status":legal.status,"current_reward":"UNKNOWN","points_delta":"UNKNOWN","estimated_fees_usd":"UNKNOWN","estimated_total_cost_usd":"UNKNOWN","open_risk":"NONE_REAL_FUNDS","last_error":None,"next_action":"VERIFY_CURRENT_OFFICIAL_RULES" if target.status=="UNVERIFIED" else "REVIEW_DRY_RUN_OUTPUT","financial_actions_submitted":0,"wallet_signatures_requested":0,"network_writes":0,"confidence":score_target(target)["overall_confidence"],"future_token_value":"UNKNOWN"}
def run_targets(targets:list[TargetConfig],output_dir:str="artifacts",requested_mode:str="DRY_RUN",network:bool=False)->dict[str,Any]:
    assert_live_disabled(); results=[]; log_path=Path(output_dir)/"logs"/"runs.jsonl"
    for target in targets:
        adapter=adapter_for(target); mode=effective_mode(requested_mode,target.mode); row=_base_row(target,mode)
        try:
            row["health"]=adapter.healthcheck(network=network); row["program_rules"]=adapter.fetch_program_rules(); row["terms"]=adapter.fetch_terms_status(); row["api_capabilities"]=adapter.fetch_api_capabilities()
            if mode=="SCOUT": row["scout"]=scout_record(target)
            elif mode=="READ_ONLY": row["account_state"]=adapter.fetch_account_state(); row["rewards_state"]=adapter.fetch_rewards_state()
            elif mode=="DRY_RUN":
                dry=adapter.dry_run(); row["dry_run"]=dry; row["estimated_fees_usd"]=dry["cost"]["fee_usd"]; row["estimated_total_cost_usd"]=dry["cost"]["fee_usd"]; row["points_delta"]=dry["rewards"]["points_delta"]; row["financial_actions_submitted"]=dry["financial_actions_submitted"]; row["wallet_signatures_requested"]=dry["wallet_signatures_requested"]; row["network_writes"]=dry["network_writes"]
                if dry["blocked_reasons"]: row["next_action"]=",".join(dry["blocked_reasons"])
        except Exception as exc:
            row["status"]="STOPPED"; row["last_error"]=f"{type(exc).__name__}: {exc}"; row["next_action"]="REVIEW_ERROR_AND_KEEP_LIVE_DISABLED"
        results.append(row); append_jsonl({"timestamp":datetime.now(timezone.utc).isoformat(),**row},log_path)
    payload={"generated_at":datetime.now(timezone.utc).isoformat(),"requested_mode":requested_mode,"live_trading_compiled":False,"result_count":len(results),"results":results,"invariants":{"real_orders_sent":0,"real_transactions_sent":0,"wallet_signatures_requested":0}}
    payload["reports"]=write_reports(payload,output_dir); return payload
