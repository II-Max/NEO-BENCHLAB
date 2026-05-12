from typing import Dict, Any, List
import json

class ChartBuilder:
    """Build visualizations for benchmark metrics using Plotly format."""
    
    @staticmethod
    def build_latency_chart(metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Build a line chart for latency metrics."""
        if not metrics:
            return {"type": "line", "data": [], "title": "Latency Metrics"}
        
        return {
            "type": "line",
            "title": "Latency Over Time",
            "data": metrics,
            "layout": {
                "xaxis": {"title": "Time"},
                "yaxis": {"title": "Duration (seconds)"}
            }
        }

    @staticmethod
    def build_resource_chart(samples: List[float]) -> Dict[str, Any]:
        """Build an area chart for resource usage (CPU/Memory)."""
        return {
            "type": "area",
            "title": "Resource Usage",
            "data": {
                "x": list(range(len(samples))),
                "y": samples,
                "fill": "tozeroy"
            },
            "layout": {
                "xaxis": {"title": "Sample"},
                "yaxis": {"title": "Usage (%)"}
            }
        }
    
    @staticmethod
    def build_comparison_chart(results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Build a bar chart comparing multiple benchmark results."""
        return {
            "type": "bar",
            "title": "Benchmark Comparison",
            "data": results,
            "layout": {
                "xaxis": {"title": "Benchmark"},
                "yaxis": {"title": "Metric Value"}
            }
        }
