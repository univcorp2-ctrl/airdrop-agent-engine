import pytest

from airdrop_agent.execution_guard import LiveExecutionBlocked, assert_action_allowed, assert_live_disabled


def test_live_mode_is_compiled_out():
    assert_live_disabled()


def test_financial_action_is_hard_blocked():
    with pytest.raises(LiveExecutionBlocked):
        assert_action_allowed("place_order")
