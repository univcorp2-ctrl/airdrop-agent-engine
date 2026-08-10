from airdrop_agent.models import FetchResult, TargetConfig
from airdrop_agent.policy import PreflightEvaluator


class FakeReader:
    def __init__(self, text: str):
        self.text = text

    def fetch(self, url: str) -> FetchResult:
        return FetchResult(url=url, ok=True, status_code=200, text=self.text)


def target(**overrides):
    data = dict(
        id="demo",
        name="Demo",
        priority="S",
        mode="DRY_RUN",
        enabled=True,
        objective="test",
        sources=["https://example.invalid/points"],
        probe_urls=[],
        required_markers=["api eligible"],
        block_markers=["program ended"],
        api_eligibility="CHECKED",
        japan_status="LEGAL_REVIEW_REQUIRED",
    )
    data.update(overrides)
    return TargetConfig(**data)


def test_legal_gate_fails_closed_even_with_positive_program_signal():
    result = PreflightEvaluator(FakeReader("api eligible active program")).evaluate(target())
    assert result.program_status == "ACTIVE_SIGNAL_FOUND"
    assert result.status == "LEGAL_REVIEW_REQUIRED"


def test_conflicting_program_signal_is_detected():
    result = PreflightEvaluator(FakeReader("api eligible but program ended")).evaluate(target())
    assert result.program_status == "CONFLICTING_OFFICIAL_SIGNALS"
