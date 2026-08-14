from __future__ import annotations
from ..core.ev_scorer import score_target
from ..models import TargetConfig
def scout_record(target: TargetConfig)->dict[str,object]:
    return {"target":target.id,"protocol":target.name,"official_url":target.official_url or None,"program_status":target.program_status,"qualifying_activities":"UNVERIFIED" if target.api_reward_eligible is None else "official-reward-rule-recorded","api_availability":target.api_available,"automation_eligibility":target.api_reward_eligible,"estimated_cost":{"future_reward_value":"UNKNOWN"},"confidence":score_target(target)["overall_confidence"],"notes":target.notes}
