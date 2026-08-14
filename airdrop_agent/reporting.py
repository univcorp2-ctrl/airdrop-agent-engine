from __future__ import annotations
import html,json
from pathlib import Path
from typing import Any
def _rows(payload:dict[str,Any])->list[dict[str,Any]]: return list(payload.get("results",[]))
def markdown_report(payload:dict[str,Any])->str:
    lines=["# Airdrop Agent Status","",f"Generated: {payload.get('generated_at','UNKNOWN')}","","| Target | Status | Mode | Program | API reward | Japan/legal | Actions sent |","|---|---|---|---|---|---|---:|"]
    for r in _rows(payload): lines.append(f"| {r.get('target')} | {r.get('status')} | {r.get('mode')} | {r.get('program_status')} | {r.get('api_reward_eligible')} | {r.get('japan_status')} | {r.get('financial_actions_submitted',0)} |")
    lines += ["","Future token/point monetary value: **UNKNOWN unless an official guaranteed value exists.**",""]; return "\n".join(lines)
def html_report(payload:dict[str,Any])->str:
    rows=[]
    for r in _rows(payload):
        cells=[r.get("target"),r.get("status"),r.get("mode"),r.get("program_status"),r.get("api_available"),r.get("api_reward_eligible"),r.get("japan_status"),r.get("estimated_total_cost_usd","UNKNOWN"),r.get("last_error"),r.get("next_action")]; rows.append("<tr>"+"".join(f"<td>{html.escape(str(v))}</td>" for v in cells)+"</tr>")
    return "<!doctype html><html><head><meta charset='utf-8'><title>Airdrop Agent</title><style>body{font-family:system-ui;margin:2rem;background:#0b1020;color:#e8edf7}table{border-collapse:collapse;width:100%}th,td{padding:.55rem;border-bottom:1px solid #334155;text-align:left}th{color:#93c5fd}.warn{color:#fbbf24}</style></head><body><h1>Airdrop Agent Dashboard</h1><p class='warn'>LIVE is disabled. Human-gated asset actions are never performed.</p><table><thead><tr><th>Target</th><th>Status</th><th>Mode</th><th>Program</th><th>API</th><th>API Reward</th><th>Japan/Legal</th><th>Cost</th><th>Last error</th><th>Next action</th></tr></thead><tbody>"+"".join(rows)+"</tbody></table></body></html>"
def write_reports(payload:dict[str,Any],output_dir:str|Path)->dict[str,str]:
    o=Path(output_dir); o.mkdir(parents=True,exist_ok=True); paths={"json":o/"latest.json","markdown":o/"report.md","html":o/"report.html"}
    paths["json"].write_text(json.dumps(payload,ensure_ascii=False,indent=2),encoding="utf-8"); paths["markdown"].write_text(markdown_report(payload),encoding="utf-8"); paths["html"].write_text(html_report(payload),encoding="utf-8"); return {k:str(v) for k,v in paths.items()}
