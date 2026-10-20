"""Active media player auto-detection and contextual routing (VAMC-F-015).

Detects which supported players are running and picks the one a bare command
(e.g. "pause") should target. Explicit targets ("pause spotify") always win.
"""

import os
from typing import Callable, Iterable, List, Optional

# Process-name fragment -> registered controller name, in default priority order.
PROCESS_SIGNATURES = (
    ("mpv", "mpv"),
    ("vlc", "vlc"),
    ("spotify", "spotify"),
)


def list_running_processes() -> List[str]:
    """Returns lowercase process names (Linux /proc); empty list where unsupported."""
    names: List[str] = []
    try:
        for pid in os.listdir("/proc"):
            if pid.isdigit():
                try:
                    with open(f"/proc/{pid}/comm", encoding="utf-8") as fh:
                        names.append(fh.read().strip().lower())
                except OSError:
                    continue
    except OSError:
        pass
    return names


class PlayerRouter:
    """Chooses the active player from running processes, remembering the last one used."""

    def __init__(self, process_lister: Callable[[], Iterable[str]] = list_running_processes):
        self._list = process_lister
        self.last_used: Optional[str] = None

    def detect_running(self) -> List[str]:
        procs = [p.lower() for p in self._list()]
        return [name for sig, name in PROCESS_SIGNATURES if any(sig in p for p in procs)]

    def resolve(self, explicit_target: Optional[str] = None,
                available: Optional[Iterable[str]] = None) -> Optional[str]:
        """Returns the controller name to use, or None to fall back to the default."""
        if explicit_target:
            self.last_used = explicit_target
            return explicit_target
        running = self.detect_running()
        if available is not None:
            allowed = set(available)
            running = [r for r in running if r in allowed]
        if self.last_used in running:
            return self.last_used
        if running:
            self.last_used = running[0]
            return running[0]
        return None
