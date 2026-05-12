import json
from pathlib import Path
from typing import Any


def read_json(path: str) -> Any:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def write_json(path: str, data: Any) -> None:
    Path(path).write_text(json.dumps(data, indent=2), encoding="utf-8")
