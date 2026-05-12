import os
from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class SandboxConfig:
    cpu_limit: float = 1.0
    memory_limit_mb: int = 256
    timeout_seconds: int = 5

class SandboxManager:
    def __init__(self, config: SandboxConfig | None = None):
        self.config = config or SandboxConfig()

    def prepare(self, source_path: str) -> Dict[str, Any]:
        return {
            "source_path": source_path,
            "limits": {
                "cpu": self.config.cpu_limit,
                "memory_mb": self.config.memory_limit_mb,
                "timeout": self.config.timeout_seconds,
            },
        }

    def cleanup(self, path: str) -> None:
        if os.path.exists(path):
            os.remove(path)
