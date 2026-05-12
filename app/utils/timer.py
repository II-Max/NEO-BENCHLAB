import time
from functools import wraps
from typing import Callable, Any


def timing(func: Callable[..., Any]) -> Callable[..., Any]:
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        print(f"[timer] {func.__name__} took {end - start:.4f}s")
        return result

    return wrapper
