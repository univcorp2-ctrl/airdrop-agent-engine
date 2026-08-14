from __future__ import annotations
import os
from dataclasses import dataclass
class LiveExecutionBlocked(RuntimeError): pass
LIVE_TRADING_COMPILED=False
PROHIBITED_ACTIONS=frozenset({"place_order","modify_order","cancel_live_order","deposit","withdraw","bridge","approve_contract","sign_wallet_message","add_signer","change_signer","raise_leverage","raise_capital_limit","raise_loss_limit","transfer_asset","submit_transaction"})
HUMAN_GATES=frozenset({"initial_deposit","withdrawal","bridge","new_contract_approval","unknown_wallet_signature","add_signer","change_signer","raise_leverage_limit","raise_capital_limit","raise_loss_limit","withdrawal_enabled_api_key"})
@dataclass(frozen=True,slots=True)
class GateResult:
    allowed: bool
    missing: tuple[str,...]
def assert_action_allowed(action: str)->None:
    if action in PROHIBITED_ACTIONS: raise LiveExecutionBlocked(f"{action} is hard-blocked in this DRY_RUN build")
def assert_live_disabled()->None:
    if LIVE_TRADING_COMPILED: raise RuntimeError("Safety invariant violated: LIVE_TRADING_COMPILED must remain False")
def evaluate_live_gate(env: dict[str,str] | None=None)->GateResult:
    values=env or os.environ
    required={"LIVE_APPROVED":"true","TARGET_LIVE_APPROVED":"true","LEGAL_STATUS":"PASS","TERMS_STATUS":"PASS","PROGRAM_STATUS":"ACTIVE","API_REWARD_ELIGIBLE":"true","RISK_STATUS":"PASS"}
    missing=tuple(key for key,expected in required.items() if values.get(key,"").strip()!=expected)
    if not LIVE_TRADING_COMPILED: missing=missing+("LIVE_TRADING_COMPILED",)
    return GateResult(allowed=not missing, missing=missing)
def block_live()->None:
    gate=evaluate_live_gate(); raise LiveExecutionBlocked("LIVE execution unavailable; blocked gates: "+", ".join(gate.missing))
