from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


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
    id: str
    name: str
    priority: str
    mode: str
    enabled: bool
    objective: str
    sources: list[str] = field(default_factory=list)
    probe_urls: list[str] = field(default_factory=list)
    required_markers: list[str] = field(default_factory=list)
    block_markers: list[str] = field(default_factory=list)
    api_eligibility: str = "UNVERIFIED"
    japan_status: str = "LEGAL_REVIEW_REQUIRED"


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
