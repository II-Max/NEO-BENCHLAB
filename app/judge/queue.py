import asyncio
from typing import Any, Generic, TypeVar, Optional
from dataclasses import dataclass, field

T = TypeVar('T')

@dataclass
class QueueItem(Generic[T]):
    """Wrapper for queue items with metadata."""
    data: T
    priority: int = 0
    timestamp: float = field(default_factory=lambda: asyncio.get_event_loop().time())

class BenchmarkQueue:
    """Async queue for managing benchmark submissions."""
    
    def __init__(self, maxsize: int = 100):
        self.queue: asyncio.Queue[Any] = asyncio.Queue(maxsize=maxsize)
        self.processed_count = 0
        self.failed_count = 0

    async def push(self, item: Any, priority: int = 0) -> None:
        """Add an item to the queue."""
        wrapped = QueueItem(data=item, priority=priority)
        await self.queue.put(wrapped)

    async def pop(self, timeout: Optional[float] = None) -> Any:
        """Remove and return an item from the queue."""
        try:
            if timeout:
                item = await asyncio.wait_for(self.queue.get(), timeout=timeout)
            else:
                item = await self.queue.get()
            return item.data if isinstance(item, QueueItem) else item
        except asyncio.TimeoutError:
            raise TimeoutError("Queue pop timeout")

    def task_done(self) -> None:
        """Mark a task as done."""
        self.queue.task_done()
        self.processed_count += 1

    def task_failed(self) -> None:
        """Mark a task as failed."""
        self.failed_count += 1

    async def join(self) -> None:
        """Wait for all tasks to complete."""
        await self.queue.join()

    def qsize(self) -> int:
        """Return the size of the queue."""
        return self.queue.qsize()

    def stats(self) -> dict:
        """Get queue statistics."""
        return {
            "size": self.qsize(),
            "processed": self.processed_count,
            "failed": self.failed_count,
        }
