"""Exponential Backoff Retry Helper for Socket IPC Connections."""
import time
from typing import Callable, TypeVar, Any

T = TypeVar("T")

def retry_socket_call(fn: Callable[..., T], max_attempts: int = 3, base_delay_s: float = 0.01) -> T:
    last_err = None
    for attempt in range(max_attempts):
        try:
            return fn()
        except (ConnectionRefusedError, FileNotFoundError, OSError) as e:
            last_err = e
            time.sleep(base_delay_s * (2 ** attempt))
    raise last_err
