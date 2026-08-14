#!/usr/bin/env sh
set -eu
python -m airdrop_agent.cli doctor --json
python -m airdrop_agent.cli status
python -m airdrop_agent.cli run --target pacifica --mode dry-run >/dev/null
python -m airdrop_agent.cli run --target hibachi --mode dry-run >/dev/null
python -m airdrop_agent.cli run --target kyan --mode dry-run >/dev/null
python -m airdrop_agent.cli run --target lighter --mode dry-run >/dev/null
python -m airdrop_agent.cli run-all --mode dry-run >/dev/null
python -m airdrop_agent.cli report --format markdown >/dev/null
python -m airdrop_agent.cli dashboard --check
