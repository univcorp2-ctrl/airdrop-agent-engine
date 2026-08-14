from __future__ import annotations
from dataclasses import dataclass
@dataclass(frozen=True,slots=True)
class KillSwitchState:
    stopped: bool
    reasons: tuple[str,...]
def evaluate_kill_switch(*,api_errors:int=0,data_age_seconds:int=0,max_data_age_seconds:int=120,program_status:str="ACTIVE",terms_changed:bool=False,contract_changed:bool=False,fee_cap_exceeded:bool=False,loss_cap_exceeded:bool=False,leverage_cap_exceeded:bool=False,legal_status:str="LEGAL_REVIEW_REQUIRED",reward_eligibility_lost:bool=False)->KillSwitchState:
    reasons=[]
    if api_errors>=3: reasons.append("API_ERRORS_3_CONSECUTIVE")
    if data_age_seconds>max_data_age_seconds: reasons.append("MARKET_DATA_STALE")
    if program_status in {"PAUSED","ENDED","INACTIVE"}: reasons.append("PROGRAM_NOT_ACTIVE")
    if terms_changed: reasons.append("TERMS_MAJOR_CHANGE")
    if contract_changed: reasons.append("CONTRACT_OR_ADDRESS_CHANGED")
    if fee_cap_exceeded: reasons.append("FEE_CAP_EXCEEDED")
    if loss_cap_exceeded: reasons.append("LOSS_CAP_EXCEEDED")
    if leverage_cap_exceeded: reasons.append("LEVERAGE_CAP_EXCEEDED")
    if legal_status in {"REGION_BLOCKED","STOPPED"}: reasons.append("LEGAL_STATUS_WORSENED")
    if reward_eligibility_lost: reasons.append("REWARD_ELIGIBILITY_UNKNOWN_OR_LOST")
    return KillSwitchState(bool(reasons),tuple(reasons))
