from __future__ import annotations


class LiveExecutionBlocked(RuntimeError):
    pass


# This build intentionally contains no path that can submit financial actions.
LIVE_TRADING_COMPILED = False
PROHIBITED_ACTIONS = frozenset(
    {
        "place_order",
        "modify_order",
        "deposit",
        "withdraw",
        "bridge",
        "approve_contract",
        "sign_wallet_message",
        "change_signer",
        "raise_leverage",
        "transfer_asset",
    }
)


def assert_action_allowed(action: str) -> None:
    if action in PROHIBITED_ACTIONS:
        raise LiveExecutionBlocked(
            f"{action} is hard-blocked in this DRY_RUN build; a code change and separate review are required."
        )


def assert_live_disabled() -> None:
    if LIVE_TRADING_COMPILED:
        raise RuntimeError("Safety invariant violated: LIVE_TRADING_COMPILED must remain False")
