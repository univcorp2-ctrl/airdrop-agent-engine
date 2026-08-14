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
        if len(data["text"]) > 500: data["text"] = data["text"][:500] + "..."
        return data

@dataclass(slots=True)
class TargetConfig:
    id: str
    name: str
    wave: int
    mode: str
    status: str
    enabled: bool
    objective: str
    program_status: str
    api_available: bool | None
    api_reward_eligible: bool | None
    japan_status: str
    terms_status: str
    risk_status: str
    reward_unit: str
    official_url: str
    sources: list[str] = field(default_factory=list)
    health_urls: list[str] = field(default_factory=list)
    requires_api_key: bool = False
    estimated_fee_bps: float | None = None
    program_version: str = "UNKNOWN"
    notes: list[str] = field(default_factory=list)
    def to_dict(self) -> dict[str, Any]: return asdict(self)
