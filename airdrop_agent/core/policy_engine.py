from __future__ import annotations

from dataclasses import dataclass

from ..core.legal_gate import evaluate_japan
from ..models import TargetConfig

PROHIBITED_BEHAVIORS = frozenset({"sybil_farming","multi_wallet_impersonation","kyc_deception","self_trading","wash_trading","circular_volume","fake_liquidity","market_manipulation","quote_stuffing","self_referral_abuse","bot_detection_evasion","anti_sybil_evasion","geo_restriction_evasion"})

@dataclass(frozen=True, slots=True)
class PolicyDecision:
    allowed: bool
    reasons: tuple[str, ...]


def evaluate_reward_automation(target: TargetConfig) -> PolicyDecision:
    reasons: list[str] = []
    if target.program_status != "ACTIVE": reasons.append("PROGRAM_NOT_ACTIVE")
    if target.mode == "DRY_RUN" and target.api_reward_eligible is not True: reasons.append("API_REWARD_ELIGIBILITY_NOT_VERIFIED")
    if evaluate_japan(target).status != "PASS": reasons.append("LEGAL_REVIEW_REQUIRED_FOR_LIVE")
    # This decision controls future LIVE promotion only; DRY_RUN research remains allowed.
    return PolicyDecision(allowed=not reasons, reasons=tuple(reasons))


def assert_behavior_allowed(name: str) -> None:
    if name in PROHIBITED_BEHAVIORS: raise PermissionError(f"prohibited behavior: {name}")
