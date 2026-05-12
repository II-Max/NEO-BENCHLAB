import os
import resource
import subprocess
from dataclasses import dataclass
from typing import Dict, Any, Optional

@dataclass
class SandboxConfig:
    """Configuration for code execution sandbox."""
    cpu_limit: float = 1.0
    memory_limit_mb: int = 256
    timeout_seconds: int = 5
    max_processes: int = 10

class SandboxManager:
    """Manages secure subprocess execution with resource limits."""
    
    def __init__(self, config: Optional[SandboxConfig] = None):
        self.config = config or SandboxConfig()
        self.processes: list = []

    def prepare(self, source_path: str) -> Dict[str, Any]:
        """Prepare a sandbox environment for code execution."""
        return {
            "source_path": source_path,
            "limits": {
                "cpu": self.config.cpu_limit,
                "memory_mb": self.config.memory_limit_mb,
                "timeout": self.config.timeout_seconds,
                "max_processes": self.config.max_processes,
            },
            "status": "prepared"
        }

    def cleanup(self, path: str) -> None:
        """Clean up sandbox resources."""
        if os.path.exists(path):
            try:
                os.remove(path)
            except OSError:
                pass
    
    def terminate_all(self) -> None:
        """Terminate all running processes in sandbox."""
        for proc in self.processes:
            try:
                if proc.poll() is None:
                    proc.terminate()
            except:
                pass
        self.processes.clear()

    def get_stats(self) -> Dict[str, Any]:
        """Get sandbox statistics."""
        return {
            "active_processes": len([p for p in self.processes if p.poll() is None]),
            "config": {
                "cpu_limit": self.config.cpu_limit,
                "memory_limit_mb": self.config.memory_limit_mb,
                "timeout_seconds": self.config.timeout_seconds,
            }
        }
