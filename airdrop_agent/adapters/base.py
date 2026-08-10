from __future__ import annotations

from dataclasses import dataclass

from ..execution_guard import assert_live_disabled
from ..models import TargetConfig
from ..policy import PreflightEvaluator


@dataclass(slots=True)
class DryRunPlan:
    target: str
    mode: str
    proposed_actions: list[str]
    financial_actions_submitted: int = 0


class BaseAdapter:
    slug = "base"

    def __init__(self, config: TargetConfig, evaluator: PreflightEvaluator | None = None) -> None:
        self.config = config
        self.evaluator = evaluator or PreflightEvaluator()

    def run(self) -> tuple[dict, dict]:
        assert_live_disabled()
        preflight = self.evaluator.evaluate(self.config)
        plan = DryRunPlan(
            target=self.config.name,
            mode="DRY_RUN",
            proposed_actions=[
                "observe official reward/points rules",
                "observe public market/API availability",
                "estimate direct costs only after market-data integration",
                "stop on rule conflict, source failure, or legal uncertainty",
            ],
        )
        return preflight.to_dict(), {
            "target": plan.target,
            "mode": plan.mode,
            "proposed_actions": plan.proposed_actions,
            "financial_actions_submitted": plan.financial_actions_submitted,
        }
