from __future__ import annotations
from dataclasses import dataclass
from ..models import TargetConfig
@dataclass(frozen=True,slots=True)
class LegalDecision:
    status: str
    reason: str
def evaluate_japan(target: TargetConfig)->LegalDecision:
    if target.japan_status=="REGION_BLOCKED": return LegalDecision("REGION_BLOCKED","Official rules explicitly block the target residence or access path.")
    if target.japan_status=="PASS" and target.terms_status=="PASS": return LegalDecision("PASS","Explicit legal and terms review recorded.")
    return LegalDecision("LEGAL_REVIEW_REQUIRED","No explicit Japan legal PASS has been recorded.")
