"""Volatile RAM audio zeroization (PRJ-SR-001).

Raw microphone audio is held in a mutable buffer that is overwritten with zeros
as soon as processing finishes (or fails), so no recoverable audio remains in
the buffer we control. Audio is never written to disk.
"""

from typing import Optional


class SecureAudioBuffer:
    """Mutable audio buffer that zeroizes itself on context exit."""

    def __init__(self, data: Optional[bytes] = None):
        self._buf = bytearray(data) if data else bytearray()
        self._disposed = False

    def __len__(self) -> int:
        return len(self._buf)

    @property
    def disposed(self) -> bool:
        return self._disposed

    def view(self) -> memoryview:
        """Zero-copy read-only view for consumers (avoids creating extra immutable copies)."""
        if self._disposed:
            raise ValueError("buffer already zeroized")
        return memoryview(self._buf).toreadonly()

    def zeroize(self) -> None:
        """Overwrites every byte with 0x00 in place. Idempotent."""
        for i in range(len(self._buf)):
            self._buf[i] = 0
        self._disposed = True

    def is_zeroed(self) -> bool:
        return not any(self._buf)

    def __enter__(self) -> "SecureAudioBuffer":
        return self

    def __exit__(self, exc_type, exc, tb) -> bool:
        self.zeroize()
        return False
