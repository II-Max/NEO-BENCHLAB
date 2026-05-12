import json
import csv
import time
from dataclasses import dataclass
from typing import Any, Dict, List
from app.utils.config import AppConfig

@dataclass
class BenchmarkReportGenerator:
    config: AppConfig

    def generate(self, result: Any) -> Dict[str, Any]:
        return {
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "metadata": result.metadata,
            "metrics": result.metrics,
        }

    def list_reports(self) -> Dict[str, Any]:
        return {"reports": []}

    def export_json(self, filename: str, payload: Dict[str, Any]) -> str:
        with open(filename, "w", encoding="utf-8") as handle:
            json.dump(payload, handle, indent=2)
        return filename

    def export_csv(self, filename: str, payload: Dict[str, Any]) -> str:
        with open(filename, "w", newline="", encoding="utf-8") as handle:
            writer = csv.writer(handle)
            writer.writerow(["metric", "value"])
            for section, values in payload.items():
                writer.writerow([section, values])
        return filename
