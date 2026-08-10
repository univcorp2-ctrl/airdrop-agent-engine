from __future__ import annotations

import argparse
import json
from dataclasses import asdict

from .registry import enabled_targets, load_targets
from .runner import run_targets


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Airdrop/points DRY_RUN monitoring agent")
    parser.add_argument("command", choices=["run", "list"])
    parser.add_argument("--config", default="config/targets.json")
    parser.add_argument("--output-dir", default="artifacts")
    parser.add_argument("--all", action="store_true", help="Include disabled placeholder targets")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    targets = load_targets(args.config) if args.all else enabled_targets(args.config)
    if args.command == "list":
        print(json.dumps([asdict(target) for target in targets], ensure_ascii=False, indent=2))
        return 0
    payload = run_targets(targets, args.output_dir)
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
