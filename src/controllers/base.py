"""Base media controller interface (VAMC-NF-008).

Defines unified interface adapter pattern for desktop and cloud multimedia targets.
"""

from abc import ABC, abstractmethod
from typing import Optional, Dict, Any


class BaseMediaController(ABC):
    """Abstract interface adapter for multimedia players."""

    @abstractmethod
    def play(self, query: Optional[str] = None) -> bool:
        """Starts or plays multimedia."""
        pass

    @abstractmethod
    def pause(self) -> bool:
        """Pauses multimedia playback."""
        pass

    @abstractmethod
    def resume(self) -> bool:
        """Resumes multimedia playback."""
        pass

    @abstractmethod
    def toggle(self) -> bool:
        """Toggles between play and pause."""
        pass

    @abstractmethod
    def stop(self) -> bool:
        """Stops playback and resets position."""
        pass

    @abstractmethod
    def seek(self, offset_seconds: int) -> int:
        """Seeks relative offset seconds. Returns new position."""
        pass

    @abstractmethod
    def next_track(self) -> str:
        """Transitions to the next track."""
        pass

    @abstractmethod
    def prev_track(self) -> str:
        """Transitions to the previous track."""
        pass

    @abstractmethod
    def restart_track(self) -> bool:
        """Restarts the current track to 0s."""
        pass

    @abstractmethod
    def toggle_shuffle(self) -> bool:
        """Toggles shuffle mode."""
        pass

    @abstractmethod
    def toggle_repeat(self) -> bool:
        """Toggles repeat mode."""
        pass

    @abstractmethod
    def volume_up(self, step: int = 10) -> int:
        """Increments volume by step percentage."""
        pass

    @abstractmethod
    def volume_down(self, step: int = 10) -> int:
        """Decrements volume by step percentage."""
        pass

    @abstractmethod
    def volume_set(self, level: int) -> int:
        """Sets volume to exact percentage (0-100)."""
        pass

    @abstractmethod
    def mute(self) -> bool:
        """Mutes audio output."""
        pass

    @abstractmethod
    def unmute(self) -> bool:
        """Unmutes audio output and restores prior level."""
        pass

    @abstractmethod
    def get_status(self) -> Dict[str, Any]:
        """Returns player status dictionary."""
        pass

    # Display, subtitle and rate controls (VAMC-F-016, F-017, F-018).
    # Concrete defaults report "unsupported" so audio-only players need not implement them.
    def set_fullscreen(self, enabled: bool) -> bool:
        """Enters or exits fullscreen. Returns False when unsupported."""
        return False

    def set_subtitles(self, enabled: bool) -> bool:
        """Shows or hides subtitles. Returns False when unsupported."""
        return False

    def select_subtitle_track(self, track: str) -> bool:
        """Selects a subtitle track by index or language. Returns False when unsupported."""
        return False

    def set_playback_rate(self, rate: float) -> float:
        """Sets playback rate (0.5x-2.0x). Returns the applied rate, or 1.0 when unsupported."""
        return 1.0
