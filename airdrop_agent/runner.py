from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from .adapters import HibachiAdapter, KyanAdapter, LighterAdapter, PacificaAdapter
from .models import TargetConfig

ADAPTERS = {
    "pacifica": PacificaAdapter,
    "hibachi": HibachiAdapter,
    "kyan": KyanAdapter,
    "lighter": LighterAdapter,
}


def run_targets(targets: list[TargetConfig], output_dir: str | Path = "artifacts") -> dict:
    now = datetime.now(timezone.utc)
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    results: list[dict] = []

    for target in targets:
        adapter_cls = ADAPTERS.get(target.id)
        if adapter_cls is None:
            results.append(
                {
                    "target": target.name,
                    "status": "ADAPTER_NOT_IMPLEMENTED",
                    "mode": target.mode,
                    "financial_actions_submitted": 0,
                }
            )
            continue
        preflight, plan = adapter_cls(target).run()
        results.append({"preflight": preflight, "plan": plan})

    payload = {
        "generated_at": now.isoformat(),
        "mode": "DRY_RUN",
        "live_trading_compiled": False,
        "result_count": len(results),
        "results": results,
    }
    latest = output / "latest.json"
    latest.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    history = output / "history.jsonl"
    with history.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, ensure_ascii=False) + "\n")
    return payload
