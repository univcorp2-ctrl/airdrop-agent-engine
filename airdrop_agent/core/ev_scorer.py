from __future__ import annotations
from ..models import TargetConfig
def score_target(target: TargetConfig)->dict[str,object]:
    reward=1.0 if target.api_reward_eligible is True and target.program_status=="ACTIVE" else 0.0
    automation=1.0 if target.api_available is True and target.mode=="DRY_RUN" else 0.5 if target.mode in {"READ_ONLY","SCOUT"} else 0.0
    legal=1.0 if target.japan_status=="PASS" else 0.0
    operational=1.0 if target.status=="READY_DRY_RUN" else 0.4 if target.status in {"READ_ONLY","UNVERIFIED"} else 0.0
    return {"reward_certainty":reward,"api_automation_suitability":automation,"japan_legal_certainty":legal,"operational_readiness":operational,"overall_confidence":round((reward+automation+legal+operational)/4.0,3),"future_token_value":"UNKNOWN"}
