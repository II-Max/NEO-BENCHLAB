import asyncio
from dataclasses import dataclass
from typing import Dict, Any
from app.judge.executor import Executor
from app.utils.config import AppConfig

@dataclass
class StressTester:
    config: AppConfig
    executor: Executor = Executor()

    async def run_stress_test(self, language_config: Dict[str, Any], source: str) -> Dict[str, Any]:
        queue = asyncio.Queue()
        tasks = []

        for _ in range(self.config.threads):
            tasks.append(asyncio.create_task(self._worker(queue, language_config, source)))

        for _ in range(self.config.stress_requests):
            await queue.put(source)

        await queue.join()

        for _ in range(self.config.threads):
            await queue.put(None)

        await asyncio.gather(*tasks)

        return {"stress_requests": self.config.stress_requests}

    async def _worker(self, queue: asyncio.Queue, language_config: Dict[str, Any], source: str) -> None:
        while True:
            item = await queue.get()
            if item is None:
                queue.task_done()
                break
            await self.executor.execute(language_config, item)
            queue.task_done()
