from __future__ import annotations
import json
from pathlib import Path
from typing import Any
def append_jsonl(record: dict[str,Any],path: str|Path)->None:
    p=Path(path); p.parent.mkdir(parents=True,exist_ok=True)
    with p.open("a",encoding="utf-8") as h: h.write(json.dumps(record,ensure_ascii=False,sort_keys=True)+"\n")
