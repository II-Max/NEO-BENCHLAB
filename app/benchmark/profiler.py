from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class Profiler:
    enabled: bool = False

    def profile(self, target: str, duration: float) -> Dict[str, Any]:
        return {
            "target": target,
            "duration": duration,
            "flamegraph": None,
        }

    def generate_flamegraph(self, profile_data: Dict[str, Any], output_path: str) -> str:
        return output_path
