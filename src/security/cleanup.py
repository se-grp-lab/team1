"""Emergency Process Termination Credential Wipe Hook."""
import atexit
from typing import List, Callable

class ExitCleanupRegistry:
    _handlers: List[Callable[[], None]] = []

    @classmethod
    def register(cls, fn: Callable[[], None]):
        cls._handlers.append(fn)

    @classmethod
    def cleanup_all(cls):
        for h in cls._handlers:
            try:
                h()
            except Exception:
                pass

atexit.register(ExitCleanupRegistry.cleanup_all)
