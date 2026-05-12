from dataclasses import dataclass
from typing import Any, Dict, List

@dataclass
class MetricSummary:
    name: str
    values: List[float]

    def to_dict(self) -> Dict[str, Any]:
        sorted_values = sorted(self.values)
        count = len(self.values)
        return {
            "count": count,
            "min": min(self.values) if self.values else 0.0,
            "max": max(self.values) if self.values else 0.0,
            "avg": sum(self.values) / count if count else 0.0,
            "median": sorted_values[count // 2] if count else 0.0,
        }
