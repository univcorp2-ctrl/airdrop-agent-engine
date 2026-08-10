from __future__ import annotations

import json
from pathlib import Path

from .models import TargetConfig


def load_targets(path: str | Path = "config/targets.json") -> list[TargetConfig]:
    raw = json.loads(Path(path).read_text(encoding="utf-8"))
    return [TargetConfig(**item) for item in raw]


def enabled_targets(path: str | Path = "config/targets.json") -> list[TargetConfig]:
    return [target for target in load_targets(path) if target.enabled]
