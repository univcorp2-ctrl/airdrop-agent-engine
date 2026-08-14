from pathlib import Path
import os
import pytest

from airdrop_agent.adapters import adapter_for
from airdrop_agent.core.kill_switch import evaluate_kill_switch
from airdrop_agent.core.policy_engine import PROHIBITED_BEHAVIORS, assert_behavior_allowed
from airdrop_agent.dashboard import render_dashboard
from airdrop_agent.execution_guard import LiveExecutionBlocked, PROHIBITED_ACTIONS, assert_action_allowed, evaluate_live_gate
from airdrop_agent.http_client import PublicGetClient
from airdrop_agent.registry import get_target, load_targets
from airdrop_agent.runner import run_targets

REQUIRED = ["probe","fetch_program_rules","fetch_terms_status","fetch_api_capabilities","fetch_account_state","fetch_rewards_state","estimate_cost","dry_run","execute","healthcheck"]


def test_registry_has_exactly_twenty_targets_and_valid_statuses():
    targets = load_targets(); assert len(targets) == 20; assert len({t.id for t in targets}) == 20


def test_all_adapters_implement_contract_and_no_dry_run_writes():
    for target in load_targets():
        adapter = adapter_for(target)
        for method in REQUIRED: assert callable(getattr(adapter, method))
        if target.mode == "DRY_RUN":
            result = adapter.dry_run(100); assert result["financial_actions_submitted"] == 0; assert result["wallet_signatures_requested"] == 0; assert result["network_writes"] == 0; assert result["candidate"]["send"] is False; assert result["open_exposure_usd"] == 0


def test_wave1_pacifica_hibachi_kyan_lighter_rules():
    pacifica = get_target("pacifica"); p = adapter_for(pacifica).dry_run(100); assert pacifica.status == "READY_DRY_RUN" and pacifica.api_reward_eligible is True and p["candidate"]["send"] is False
    hibachi = get_target("hibachi"); h = adapter_for(hibachi).dry_run(100); assert hibachi.api_reward_eligible is True and h["candidate"]["ui_vs_api_points"] == "OFFICIAL_FAQ_SAME_ACTIVITY_FORMULA"
    kyan = get_target("kyan"); k = adapter_for(kyan).dry_run(100); assert kyan.api_reward_eligible is None and "API_REWARD_ELIGIBILITY_NOT_VERIFIED" in k["blocked_reasons"] and k["candidate"]["mcp_secret_forwarding"] is False
    lighter = get_target("lighter"); l = adapter_for(lighter).dry_run(100); assert lighter.status == "INACTIVE" and "PROGRAM_NOT_ACTIVE" in l["blocked_reasons"]


def test_grvt_explicit_api_points_rule_is_recorded():
    grvt = get_target("grvt"); assert grvt.status == "READY_DRY_RUN"; assert grvt.program_status == "ACTIVE"; assert grvt.api_reward_eligible is True; assert any("UI-based" in note for note in grvt.notes)


def test_live_is_hard_blocked_even_when_all_env_gates_are_supplied():
    env = {"LIVE_APPROVED":"true","TARGET_LIVE_APPROVED":"true","LEGAL_STATUS":"PASS","TERMS_STATUS":"PASS","PROGRAM_STATUS":"ACTIVE","API_REWARD_ELIGIBLE":"true","RISK_STATUS":"PASS"}
    gate = evaluate_live_gate(env); assert not gate.allowed; assert "LIVE_TRADING_COMPILED" in gate.missing
    with pytest.raises(LiveExecutionBlocked): adapter_for(get_target("pacifica")).execute()


def test_prohibited_financial_and_abuse_actions_are_blocked():
    for action in PROHIBITED_ACTIONS:
        with pytest.raises(LiveExecutionBlocked): assert_action_allowed(action)
    for behavior in PROHIBITED_BEHAVIORS:
        with pytest.raises(PermissionError): assert_behavior_allowed(behavior)


def test_kill_switch_conditions():
    state = evaluate_kill_switch(api_errors=3, data_age_seconds=121, max_data_age_seconds=120, program_status="INACTIVE", legal_status="PASS", reward_eligibility_lost=True)
    assert state.stopped; assert {"API_ERRORS_3_CONSECUTIVE","MARKET_DATA_STALE","PROGRAM_NOT_ACTIVE","REWARD_ELIGIBILITY_UNKNOWN_OR_LOST"} <= set(state.reasons)


def test_run_all_dry_run_and_reports_are_safe(tmp_path):
    payload = run_targets(load_targets(), str(tmp_path), requested_mode="DRY_RUN", network=False)
    assert payload["result_count"] == 20; assert payload["invariants"] == {"real_orders_sent":0,"real_transactions_sent":0,"wallet_signatures_requested":0}; assert all(row["financial_actions_submitted"] == 0 for row in payload["results"])
    assert (tmp_path / "latest.json").exists(); assert (tmp_path / "report.md").exists(); assert (tmp_path / "report.html").exists()


def test_dashboard_renders_status_and_live_disabled():
    page = render_dashboard(); assert "Airdrop Agent Dashboard" in page; assert all(x in page for x in ("pacifica","hibachi","kyan","lighter","grvt")); assert "LIVE disabled" in page


def test_env_example_has_no_api_secret_values_and_public_client_is_get_only():
    for line in Path(".env.example").read_text(encoding="utf-8").splitlines():
        if "_API_KEY=" in line: assert line.endswith("=")
    public = {name for name in dir(PublicGetClient) if not name.startswith("_")}; assert "get" in public and "fetch" in public; assert not ({"post","put","patch","delete","send_order","submit_transaction"} & public)


@pytest.mark.network
def test_public_get_endpoints_when_enabled():
    if os.getenv("RUN_PUBLIC_GET_TESTS") != "1": pytest.skip("set RUN_PUBLIC_GET_TESTS=1")
    client = PublicGetClient(timeout=20)
    for target_id in ("pacifica","hibachi","lighter","grvt"):
        target = get_target(target_id); result = client.get(target.health_urls[0]); assert result.status_code is not None, f"{target_id}: {result.error}"
    kyan = client.get("https://sandbox.kyan.sh/api/v1/exchange_info"); assert kyan.status_code is not None, kyan.error
