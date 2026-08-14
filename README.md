# Airdrop Agent Engine

A safety-gated research, READ_ONLY monitoring and DRY_RUN preparation engine for 20 crypto airdrop / points / XP / rewards targets. Residence defaults to Japan; legal eligibility is fail-closed.

## Safety invariants

- **No live order or transaction submission implementation exists in v1.** `execute()` hard-fails and `LIVE_TRADING_COMPILED=false`.
- Deposits, withdrawals, bridges, new contract approvals, unknown wallet signatures, signer changes and risk-limit increases are Human Gates.
- Sybil farming, self/wash/circular trading, fake liquidity, manipulation, quote stuffing, KYC/bot/anti-Sybil/geo-restriction evasion are blocked by policy.
- Point/token future monetary value is `UNKNOWN` unless officially guaranteed.
- API/SDK/MCP existence is never treated as reward eligibility. A target is only marked `api_reward_eligible=true` when a current official Program/FAQ explicitly connects API-originated activity to rewards.
- Japan not appearing in a prohibited-country list does **not** produce legal PASS.

## Current highlights — verified 2026-08-14

- Pacifica — `READY_DRY_RUN`: official points rules explicitly include organic GUI/API trading.
- Hibachi — `READY_DRY_RUN`: official FAQ states points use the same activity formula regardless of UI/API path.
- GRVT — `READY_DRY_RUN`: Rewards Season 2.0 explicitly awards API trades, but UI trades earn more points.
- Kyan — `UNVERIFIED`: current MCP/API and Krystals-from-own-trading are official; explicit API-originated Krystals eligibility was not located.
- Lighter — `INACTIVE`: official Points Season 2 ended 2025-12-26.
- All targets remain `LEGAL_REVIEW_REQUIRED` for Japan and therefore cannot become LIVE.

The remaining programs are represented by fail-closed adapters. Current program signals are recorded for StandX, Decibel, Reya, Extended, Nado, Ethereal, HyprEarn, OKX.AI and 01 Exchange without incorrectly promoting API reward eligibility.

## Install / test

```bash
python -m pip install -e ".[dev]"
pytest -q
RUN_PUBLIC_GET_TESTS=1 pytest -q -m network
```

## CLI

```bash
airdrop-agent doctor
airdrop-agent doctor --network
airdrop-agent scout
airdrop-agent status
airdrop-agent run --target pacifica --mode dry-run
airdrop-agent run --target hibachi --mode dry-run
airdrop-agent run --target kyan --mode dry-run
airdrop-agent run --target lighter --mode dry-run
airdrop-agent run-all --mode dry-run
airdrop-agent report --format markdown
airdrop-agent dashboard --host 127.0.0.1 --port 8765
```

For backward compatibility, `airdrop-agent run` without `--target` runs only `enabled=true` targets. `run-all --mode dry-run` respects each target's configured mode ceiling, so SCOUT remains SCOUT and READ_ONLY remains READ_ONLY.

## Outputs

`artifacts/latest.json` is the latest machine-readable state. Runs also produce `artifacts/logs/runs.jsonl`, `artifacts/report.md`, and `artifacts/report.html`. Credential values are never written; `doctor` reports presence booleans only.

See `SECURITY.md`, `RUNBOOK.md`, `IMPLEMENTATION_STATUS.md`, and `RESEARCH_MATRIX.md`.
