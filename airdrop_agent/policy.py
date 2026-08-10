from __future__ import annotations

from .http_client import UrlReader
from .models import PreflightResult, TargetConfig


class PreflightEvaluator:
    def __init__(self, reader: UrlReader | None = None) -> None:
        self.reader = reader or UrlReader()

    def evaluate(self, target: TargetConfig) -> PreflightResult:
        source_results = [self.reader.fetch(url) for url in target.sources]
        probe_results = [self.reader.fetch(url) for url in target.probe_urls]
        readable = [result for result in source_results if result.ok]
        corpus = " ".join(result.text.lower() for result in readable)

        required = [marker.lower() for marker in target.required_markers]
        blockers = [marker.lower() for marker in target.block_markers]
        missing_required = [marker for marker in required if marker not in corpus]
        hit_blockers = [marker for marker in blockers if marker in corpus]

        if not target.sources:
            program_status = "UNCONFIGURED"
        elif not readable:
            program_status = "SOURCE_UNREACHABLE"
        elif hit_blockers and not missing_required:
            program_status = "CONFLICTING_OFFICIAL_SIGNALS"
        elif hit_blockers:
            program_status = "INACTIVE_OR_CHANGED"
        elif missing_required:
            program_status = "UNVERIFIED_OR_CHANGED"
        else:
            program_status = "ACTIVE_SIGNAL_FOUND"

        probe_ok = bool(probe_results) and all(item.ok for item in probe_results)
        program_ok = program_status == "ACTIVE_SIGNAL_FOUND"

        # Japan is intentionally fail-closed. Absence from a prohibited-country list is
        # not treated as affirmative authorization for a Japan-resident derivatives user.
        if target.japan_status != "ELIGIBLE_CONFIRMED":
            status = "LEGAL_REVIEW_REQUIRED"
        elif not program_ok:
            status = f"BLOCKED_{program_status}"
        elif target.probe_urls and not probe_ok:
            status = "BLOCKED_API_PROBE_FAILED"
        else:
            status = "READY_DRY_RUN"

        actions_taken = ["FETCH_OFFICIAL_SOURCES", "CHECK_REWARD_MARKERS"]
        if target.probe_urls:
            actions_taken.append("PROBE_PUBLIC_API_OR_MCP_ENDPOINT")
        actions_blocked = [
            "PLACE_REAL_ORDER",
            "DEPOSIT",
            "WITHDRAW",
            "BRIDGE",
            "WALLET_SIGNATURE",
            "SMART_CONTRACT_APPROVAL",
        ]

        return PreflightResult(
            target=target.name,
            status=status,
            program_status=program_status,
            api_eligibility=target.api_eligibility,
            japan_status=target.japan_status,
            reward_rule=target.objective,
            actions_taken=actions_taken,
            actions_blocked=actions_blocked,
            next_best_action=(
                "Resolve Japan-resident legal/ToS eligibility before any live financial action."
                if target.japan_status != "ELIGIBLE_CONFIRMED"
                else "Continue DRY_RUN monitoring; live execution is not implemented."
            ),
            source_checks=[result.to_dict() for result in source_results],
            probe_checks=[result.to_dict() for result in probe_results],
            evidence={
                "missing_required_markers": missing_required,
                "hit_block_markers": hit_blockers,
                "all_probes_ok": probe_ok,
            },
        )
