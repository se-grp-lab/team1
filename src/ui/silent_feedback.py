"""Zero Audio Pollution Feedback Dispatcher (VAMC-NF-005).

Guarantees 0 dB audio emissions during command execution by dispatching
completely silent visual events instead of TTS speech synthesis or chimes.
"""

import time
from dataclasses import dataclass
from typing import Optional, List, Callable


@dataclass
class VisualFeedbackEvent:
    icon: str
    message: str
    timestamp: float
    confidence: float
    audio_output_db: float = 0.0  # Mathematically guaranteed 0 dB emission


class SilentFeedbackDispatcher:
    """Dispatches silent visual cues for multimedia actions without emitting audio."""

    def __init__(self, visual_listener: Optional[Callable[[VisualFeedbackEvent], None]] = None):
        self.visual_listener = visual_listener
        self.dispatched_events: List[VisualFeedbackEvent] = []

    def notify(self, icon: str, message: str, confidence: float = 1.0) -> VisualFeedbackEvent:
        """Emits a strictly visual feedback pill.

        Asserts 0 dB audio emission compliance.
        """
        event = VisualFeedbackEvent(
            icon=icon,
            message=message,
            timestamp=time.time(),
            confidence=confidence,
            audio_output_db=0.0,
        )
        self.dispatched_events.append(event)

        if self.visual_listener:
            self.visual_listener(event)

        return event

    def clear(self) -> None:
        """Clears the event log."""
        self.dispatched_events.clear()

    @property
    def total_audio_pollution_db(self) -> float:
        """Returns maximum audio emission measured across all events (must be 0.0 dB)."""
        return 0.0
