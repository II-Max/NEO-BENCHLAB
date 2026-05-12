import asyncio
import time
from dataclasses import dataclass
from typing import Any, Dict
from app.benchmark.monitor import SystemMonitor
from app.benchmark.report import BenchmarkReportGenerator
from app.benchmark.stress import StressTester
from app.judge.executor import ExecutionResult, Executor
from app.judge.compiler import Compiler
from app.judge.languages import LANGUAGES
from app.utils.config import AppConfig

@dataclass
class BenchmarkResult:
    metadata: Dict[str, Any]
    metrics: Dict[str, Any]

class BenchmarkRunner:
    def __init__(self, config: AppConfig):
        self.config = config
        self.monitor = SystemMonitor()
        self.compiler = Compiler()
        self.executor = Executor()
        self.reporter = BenchmarkReportGenerator(config=config)
        self.stress_tester = StressTester(config=config)
        self.start_time = time.perf_counter()

    async def run_submission(self, language: str, source: str) -> BenchmarkResult:
        self.monitor.start()
        language_config = LANGUAGES[language]

        compile_result = await self.compiler.compile_source(language_config, source)
        execution_result = await self.executor.execute(language_config, source)

        if self.config.enable_stress_test:
            await self.stress_tester.run_stress_test(language_config, source)

        self.monitor.stop()

        return BenchmarkResult(
            metadata={
                "language": language,
                "compile_success": compile_result.success,
                "execution_success": execution_result.success,
            },
            metrics={
                "system": self.monitor.snapshot(),
                "compile": compile_result.to_dict(),
                "execution": execution_result.to_dict(),
            },
        )

    def collect_system_stats(self) -> Dict[str, Any]:
        return self.monitor.snapshot()

    def get_uptime_seconds(self) -> float:
        return time.perf_counter() - self.start_time
