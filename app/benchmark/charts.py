from typing import Dict, Any, List

class ChartBuilder:
    @staticmethod
    def build_latency_chart(metrics: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "type": "line",
            "data": metrics,
        }

    @staticmethod
    def build_resource_chart(samples: List[float]) -> Dict[str, Any]:
        return {
            "type": "area",
            "data": samples,
        }
