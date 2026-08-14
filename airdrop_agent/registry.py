from __future__ import annotations
import json
from pathlib import Path
from .models import MODES, STATUSES, TargetConfig
def load_targets(path: str="config/targets.json")->list[TargetConfig]:
    targets=[TargetConfig(**item) for item in json.loads(Path(path).read_text(encoding="utf-8"))]; validate_targets(targets); return targets
def validate_targets(targets: list[TargetConfig])->None:
    ids=[t.id for t in targets]
    if len(ids)!=len(set(ids)): raise ValueError("target ids must be unique")
    for target in targets:
        if target.mode not in MODES: raise ValueError(f"invalid mode for {target.id}: {target.mode}")
        if target.status not in STATUSES: raise ValueError(f"invalid status for {target.id}: {target.status}")
        if target.japan_status=="PASS" and target.terms_status!="PASS": raise ValueError(f"Japan legal PASS requires explicit terms PASS for {target.id}")
def enabled_targets(path: str="config/targets.json")->list[TargetConfig]: return [t for t in load_targets(path) if t.enabled]
def get_target(target_id: str,path: str="config/targets.json")->TargetConfig:
    for target in load_targets(path):
        if target.id==target_id: return target
    raise KeyError(target_id)
