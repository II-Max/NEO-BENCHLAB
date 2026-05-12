import asyncio
from typing import Any

class BenchmarkQueue:
    def __init__(self, maxsize: int = 100):
        self.queue: asyncio.Queue[Any] = asyncio.Queue(maxsize=maxsize)

    async def push(self, item: Any) -> None:
        await self.queue.put(item)

    async def pop(self) -> Any:
        return await self.queue.get()

    def task_done(self) -> None:
        self.queue.task_done()

    async def join(self) -> None:
        await self.queue.join()
