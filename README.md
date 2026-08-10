# Airdrop Agent Engine

A safety-gated engine for continuously monitoring crypto points/rewards/airdrop candidates against current official sources.

## Current scope

The first four adapters are enabled: Pacifica, Hibachi, Kyan and Lighter. Sixteen additional targets are registered as disabled placeholders so they can be added without changing the core architecture.

The scheduled GitHub Actions job runs every 6 hours. Each run:

1. fetches current official points/rewards/API/Terms pages,
2. checks required eligibility markers and stop markers,
3. probes a public API/MCP or official developer endpoint,
4. fails closed on conflicting program signals or source failures,
5. records JSON evidence as a GitHub Actions artifact.

## Safety boundary

This repository is deliberately **DRY_RUN only**. The compiled build contains no implementation that can submit an order, deposit, withdrawal, bridge, wallet signature, contract approval or asset transfer. Setting an environment variable cannot turn live trading on.

Japan-resident eligibility is also fail-closed as `LEGAL_REVIEW_REQUIRED`. Absence of Japan from a prohibited-jurisdiction list is not treated as affirmative permission to use an offshore derivatives service.

## Run locally

```bash
python -m pip install -e ".[dev]"
pytest -q
python -m airdrop_agent.cli run --output-dir artifacts
```

The latest machine-readable result is written to `artifacts/latest.json`.

## Adding another adapter

Add official source URLs and conservative markers to `config/targets.json`, implement a small adapter under `airdrop_agent/adapters/`, register it in `airdrop_agent/runner.py`, and add tests. Do not add authenticated financial actions to the scheduled workflow.

## Official sources currently monitored

- Pacifica points, Terms, and API documentation
- Hibachi FAQ, Points, and API/developer documentation
- Kyan MCP/developer documentation and Krystals announcement
- Lighter Points documentation, market-maker/retail pages, Terms, and public orderBooks API

Rewards have unknown future value. The engine does not assign a speculative dollar value to points or airdrop eligibility.
