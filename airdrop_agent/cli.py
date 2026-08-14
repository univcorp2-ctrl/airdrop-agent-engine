from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

from .dashboard import render_dashboard, serve
from .execution_guard import LiveExecutionBlocked, evaluate_live_gate
from .http_client import PublicGetClient
from .models import MODES
from .registry import enabled_targets, get_target, load_targets
from .reporting import html_report, markdown_report, write_reports
from .runner import run_targets


def parse_mode(value: str) -> str:
    normalized = value.strip().upper().replace("-", "_")
    if normalized not in MODES:
        raise argparse.ArgumentTypeError(f"mode must be one of {', '.join(MODES)}")
    return normalized


def _common(parser: argparse.ArgumentParser, *, output: bool = True) -> None:
    parser.add_argument("--config", default="config/targets.json")
    if output:
        parser.add_argument("--output-dir", default="artifacts")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="airdrop-agent", description="Safety-gated airdrop/points DRY_RUN engine")
    sub = parser.add_subparsers(dest="command", required=True)

    doctor = sub.add_parser("doctor"); _common(doctor, output=False); doctor.add_argument("--network", action="store_true"); doctor.add_argument("--json", action="store_true")
    status = sub.add_parser("status"); _common(status, output=False); status.add_argument("--json", action="store_true")
    scout = sub.add_parser("scout"); _common(scout); scout.add_argument("--network", action="store_true")
    run = sub.add_parser("run"); _common(run); run.add_argument("--target"); run.add_argument("--all", action="store_true"); run.add_argument("--mode", type=parse_mode, default="DRY_RUN"); run.add_argument("--network", action="store_true")
    run_all = sub.add_parser("run-all"); _common(run_all); run_all.add_argument("--mode", type=parse_mode, default="DRY_RUN"); run_all.add_argument("--network", action="store_true")
    report = sub.add_parser("report"); _common(report); report.add_argument("--format", choices=["json", "markdown", "html"], default="markdown")
    dashboard = sub.add_parser("dashboard"); _common(dashboard); dashboard.add_argument("--host", default="127.0.0.1"); dashboard.add_argument("--port", type=int, default=8765); dashboard.add_argument("--check", action="store_true")
    listing = sub.add_parser("list"); _common(listing, output=False); listing.add_argument("--json", action="store_true", default=True)
    return parser


def _credential_env(target_id: str) -> str:
    return f"{target_id.upper().replace('-', '_')}_API_KEY"


def doctor_payload(config: str, network: bool) -> dict:
    targets = load_targets(config)
    secrets = {_credential_env(t.id): bool(os.getenv(_credential_env(t.id))) for t in targets if t.requires_api_key}
    if network:
        client = PublicGetClient()
        health = {t.id: [client.get(url).to_dict() for url in t.health_urls] for t in targets if t.health_urls and (t.wave == 1 or t.status == "READY_DRY_RUN")}
    else:
        health = {t.id: {"status": "SKIPPED_USE_--network"} for t in targets if t.wave == 1 or t.status == "READY_DRY_RUN"}
    gate = evaluate_live_gate()
    return {"python": sys.version.split()[0], "target_count": len(targets), "config_valid": True, "secrets_presence_only": secrets, "api_health": health, "live_gate": {"allowed": gate.allowed, "blocked_by": list(gate.missing), "live_compiled": False}}


def status_rows(config: str) -> list[dict]:
    return [{"target": t.id, "status": t.status, "mode": t.mode, "program": t.program_status, "api": t.api_available, "api_reward": t.api_reward_eligible, "japan": t.japan_status} for t in load_targets(config)]


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        if args.command == "doctor":
            print(json.dumps(doctor_payload(args.config, args.network), ensure_ascii=False, indent=2)); return 0
        if args.command in {"status", "list"}:
            rows = status_rows(args.config)
            if getattr(args, "json", False) or args.command == "list":
                print(json.dumps(rows, ensure_ascii=False, indent=2))
            else:
                print("TARGET\tSTATUS\tMODE\tPROGRAM\tAPI_REWARD\tJAPAN")
                for row in rows: print(f"{row['target']}\t{row['status']}\t{row['mode']}\t{row['program']}\t{row['api_reward']}\t{row['japan']}")
            return 0
        if args.command == "scout":
            payload = run_targets(load_targets(args.config), args.output_dir, requested_mode="SCOUT", network=args.network)
            print(json.dumps(payload, ensure_ascii=False, indent=2)); return 0
        if args.command == "run":
            # v0.1 compatibility: no --target means enabled targets; --all means every target.
            targets = load_targets(args.config) if args.all else [get_target(args.target, args.config)] if args.target else enabled_targets(args.config)
            payload = run_targets(targets, args.output_dir, requested_mode=args.mode, network=args.network)
            print(json.dumps(payload, ensure_ascii=False, indent=2)); return 0
        if args.command == "run-all":
            payload = run_targets(load_targets(args.config), args.output_dir, requested_mode=args.mode, network=args.network)
            print(json.dumps(payload, ensure_ascii=False, indent=2)); return 0
        if args.command == "report":
            latest = Path(args.output_dir) / "latest.json"
            if not latest.exists(): run_targets(load_targets(args.config), args.output_dir, requested_mode="DRY_RUN", network=False)
            payload = json.loads(latest.read_text(encoding="utf-8")); write_reports(payload, args.output_dir)
            print(json.dumps(payload, ensure_ascii=False, indent=2) if args.format == "json" else html_report(payload) if args.format == "html" else markdown_report(payload)); return 0
        if args.command == "dashboard":
            latest = str(Path(args.output_dir) / "latest.json")
            if args.check:
                page = render_dashboard(args.config, latest); print(f"dashboard_ok bytes={len(page.encode('utf-8'))}"); return 0
            serve(args.host, args.port, args.config, latest); return 0
    except (KeyError, ValueError, LiveExecutionBlocked) as exc:
        print(f"ERROR: {exc}", file=sys.stderr); return 2
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
