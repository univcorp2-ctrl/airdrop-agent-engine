from __future__ import annotations

import html
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from .registry import load_targets


def status_payload(config: str = "config/targets.json", latest: str = "artifacts/latest.json") -> dict:
    path = Path(latest)
    if path.exists(): return json.loads(path.read_text(encoding="utf-8"))
    results = [{"target": t.id, "status": t.status, "mode": t.mode, "program_status": t.program_status, "api_available": t.api_available, "api_reward_eligible": t.api_reward_eligible, "japan_status": t.japan_status, "current_reward": "UNKNOWN", "points_delta": "UNKNOWN", "estimated_fees_usd": "UNKNOWN", "estimated_total_cost_usd": "UNKNOWN", "open_risk": "NONE_REAL_FUNDS", "last_error": None, "next_action": "RUN_DRY_RUN" if t.wave == 1 else "VERIFY_CURRENT_OFFICIAL_RULES"} for t in load_targets(config)]
    return {"generated_at": "CONFIG_ONLY", "result_count": len(results), "results": results}


def render_dashboard(config: str = "config/targets.json", latest: str = "artifacts/latest.json") -> str:
    payload = status_payload(config, latest); generated = payload.get("generated_at", "UNKNOWN"); rows = []
    for row in payload.get("results", []):
        values = [row.get("target"), row.get("status"), row.get("program_status"), row.get("api_available"), row.get("api_reward_eligible"), row.get("japan_status"), row.get("mode"), row.get("current_reward", "UNKNOWN"), row.get("points_delta", "UNKNOWN"), row.get("estimated_fees_usd", "UNKNOWN"), row.get("estimated_total_cost_usd", "UNKNOWN"), row.get("open_risk", "NONE_REAL_FUNDS"), generated, row.get("last_error"), row.get("next_action")]
        cells = "".join(f"<td>{html.escape(str(v))}</td>" for v in values)
        rows.append(f"<tr>{cells}<td><button disabled title='LIVE is hard-disabled in v1'>LIVE disabled</button></td></tr>")
    heads = ["Target","Status","Program","API","API reward","Japan/legal","Mode","Current reward","Points delta","Fees","Total cost","Open risk","Last run","Last error","Next action","LIVE"]
    return "<!doctype html><html><head><meta charset='utf-8'><title>Airdrop Agent</title><style>body{font-family:system-ui;margin:2rem;background:#0b1020;color:#e8edf7}table{border-collapse:collapse;width:100%;font-size:13px}th,td{padding:.5rem;border-bottom:1px solid #334155;text-align:left}th{color:#93c5fd;position:sticky;top:0;background:#0b1020}.warn{color:#fbbf24}button:disabled{opacity:.55}</style></head><body><h1>Airdrop Agent Dashboard</h1><p class='warn'>READ_ONLY / DRY_RUN only. LIVE, deposits, withdrawals, bridges, approvals and wallet signatures are not executed.</p><div style='overflow:auto'><table><thead><tr>" + "".join(f"<th>{h}</th>" for h in heads) + "</tr></thead><tbody>" + "".join(rows) + "</tbody></table></div></body></html>"


def serve(host: str = "127.0.0.1", port: int = 8765, config: str = "config/targets.json", latest: str = "artifacts/latest.json") -> None:
    class Handler(BaseHTTPRequestHandler):
        def do_GET(self) -> None:  # noqa: N802
            if self.path not in {"/", "/index.html"}: self.send_response(404); self.end_headers(); return
            body = render_dashboard(config, latest).encode("utf-8"); self.send_response(200); self.send_header("Content-Type", "text/html; charset=utf-8"); self.send_header("Content-Length", str(len(body))); self.end_headers(); self.wfile.write(body)
        def log_message(self, *_: object) -> None: return
    ThreadingHTTPServer((host, port), Handler).serve_forever()
