# Runbook

## Safe start

```bash
python -m pip install -e ".[dev]"
airdrop-agent doctor --network
pytest -q
airdrop-agent run-all --mode dry-run
airdrop-agent report --format markdown
airdrop-agent dashboard --check
```

Start the local dashboard with `airdrop-agent dashboard --host 127.0.0.1 --port 8765` and open `http://127.0.0.1:8765/` locally.

## Wave 1 smoke

```bash
airdrop-agent run --target pacifica --mode dry-run
airdrop-agent run --target hibachi --mode dry-run
airdrop-agent run --target kyan --mode dry-run
airdrop-agent run --target lighter --mode dry-run
```

Every DRY_RUN must report `financial_actions_submitted=0`, `wallet_signatures_requested=0`, `network_writes=0` and `open_exposure_usd=0`. Kyan must block reward optimization until API-origin reward eligibility is explicit. Lighter must block on inactive points program.

## Scheduler

Only program/Terms/API/points/market-data monitoring and DRY_RUN are automation-eligible. LIVE trading scheduling is disabled. Existing GitHub Actions DRY_RUN scheduling must never receive trading secrets or LIVE flags.

## Future LIVE promotion

A separately reviewed future build would require all of `LIVE_APPROVED=true`, `TARGET_LIVE_APPROVED=true`, `LEGAL_STATUS=PASS`, `TERMS_STATUS=PASS`, `PROGRAM_STATUS=ACTIVE`, `API_REWARD_ELIGIBLE=true`, and `RISK_STATUS=PASS`. v1 still rejects LIVE because `LIVE_TRADING_COMPILED=false` and contains no write client.
