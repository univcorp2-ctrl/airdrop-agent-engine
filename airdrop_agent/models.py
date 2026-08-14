from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any

STATUSES = {
    "READY_DRY_RUN", "READ_ONLY", "API_KEY_REQUIRED", "UNVERIFIED", "INACTIVE",
    "REGION_BLOCKED", "LEGAL_REVIEW_REQUIRED", "API_NOT_REWARD_ELIGIBLE", "LIVE_READY", "STOPPED",
}
MODES = ("SCOUT", "READ_ONLY", "DRY_RUN", "LIVE")


@dataclass(slots=True)
class FetchResult:
    url: str
    ok: bool
    status_code: int | None
    text: str = ""
    error: str | None = None

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        if len(data["text"]) > 500:
            data["text"] = data["text"][:500] + "..."
        return data


@dataclass(slots=True)
class TargetConfig:
    # First fields preserve the original v0.1 construction contract.
    id: str
    name: str
    mode: str
    enabled: bool
    objective: str
    priority: str = ""
    wave: int = 3
    status: str = "UNVERIFIED"
    program_status: str = "UNKNOWN"
    api_available: bool | None = None
    api_reward_eligible: bool | None = None
    japan_status: str = "LEGAL_REVIEW_REQUIRED"
    terms_status: str = "REVIEW_REQUIRED"
    risk_status: str = "DRY_RUN_ONLY"
    reward_unit: str = "UNKNOWN"
    official_url: str = ""
    sources: list[str] = field(default_factory=list)
    health_urls: list[str] = field(default_factory=list)
    requires_api_key: bool = False
    estimated_fee_bps: float | None = None
    program_version: str = "UNKNOWN"
    notes: list[str] = field(default_factory=list)
    # Legacy preflight fields retained for non-destructive compatibility.
    probe_urls: list[str] = field(default_factory=list)
    required_markers: list[str] = field(default_factory=list)
    block_markers: list[str] = field(default_factory=list)
    api_eligibility: str = "UNVERIFIED"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class PreflightResult:
    target: str
    status: str
    program_status: str
    api_eligibility: str
    japan_status: str
    reward_rule: str
    actions_taken: list[str]
    actions_blocked: list[str]
    next_best_action: str
    source_checks: list[dict[str, Any]]
    probe_checks: list[dict[str, Any]]
    evidence: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
