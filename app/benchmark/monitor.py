import psutil
import threading
import time
from dataclasses import dataclass, field
from typing import List, Dict

@dataclass
class SystemMonitor:
    interval: float = 0.5
    cpu_samples: List[float] = field(default_factory=list)
    ram_samples: List[float] = field(default_factory=list)
    running: bool = False
    thread: threading.Thread | None = None

    def start(self) -> None:
        self.running = True
        self.thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.thread.start()

    def stop(self) -> None:
        self.running = False
        if self.thread and self.thread.is_alive():
            self.thread.join(timeout=1.0)

    def _monitor_loop(self) -> None:
        while self.running:
            self.cpu_samples.append(psutil.cpu_percent(interval=self.interval))
            self.ram_samples.append(psutil.virtual_memory().used / 1024**2)
            time.sleep(self.interval)

    def snapshot(self) -> Dict[str, any]:
        return {
            "cpu_avg": sum(self.cpu_samples) / len(self.cpu_samples) if self.cpu_samples else 0.0,
            "cpu_peak": max(self.cpu_samples, default=0.0),
            "ram_avg_mb": sum(self.ram_samples) / len(self.ram_samples) if self.ram_samples else 0.0,
            "ram_peak_mb": max(self.ram_samples, default=0.0),
        }
