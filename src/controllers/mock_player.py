"""Mock Media Player implementation for Sprint 1 verification and testing.

Simulates active media session state, timeline scrubbing, queue navigation,
and master audio mixer levels.
"""

from typing import Optional, Dict, Any, List
from .base import BaseMediaController


class MockMediaPlayer(BaseMediaController):
    """In-memory reference media player implementation."""

    def __init__(self, name: str = "mock_player"):
        self.name = name
        self.is_playing = False
        self.position_seconds = 0
        self.duration_seconds = 300
        self.playlist: List[str] = ["Track 1 - Prelude", "Track 2 - Fugue", "Track 3 - Allegro"]
        self.track_index = 0
        self.volume = 50
        self.pre_mute_volume = 50
        self.is_muted = False
        self.shuffle_enabled = False
        self.repeat_enabled = False

    def play(self, query: Optional[str] = None) -> bool:
        self.is_playing = True
        return True

    def pause(self) -> bool:
        self.is_playing = False
        return True

    def resume(self) -> bool:
        self.is_playing = True
        return True

    def toggle(self) -> bool:
        self.is_playing = not self.is_playing
        return self.is_playing

    def stop(self) -> bool:
        self.is_playing = False
        self.position_seconds = 0
        return True

    def seek(self, offset_seconds: int) -> int:
        new_pos = self.position_seconds + offset_seconds
        self.position_seconds = max(0, min(self.duration_seconds, new_pos))
        return self.position_seconds

    def next_track(self) -> str:
        self.track_index = (self.track_index + 1) % len(self.playlist)
        self.position_seconds = 0
        return self.playlist[self.track_index]

    def prev_track(self) -> str:
        self.track_index = (self.track_index - 1) % len(self.playlist)
        self.position_seconds = 0
        return self.playlist[self.track_index]

    def restart_track(self) -> bool:
        self.position_seconds = 0
        return True

    def toggle_shuffle(self) -> bool:
        self.shuffle_enabled = not self.shuffle_enabled
        return self.shuffle_enabled

    def toggle_repeat(self) -> bool:
        self.repeat_enabled = not self.repeat_enabled
        return self.repeat_enabled

    def volume_up(self, step: int = 10) -> int:
        if self.is_muted:
            self.unmute()
        self.volume = min(100, self.volume + step)
        return self.volume

    def volume_down(self, step: int = 10) -> int:
        if self.is_muted:
            self.unmute()
        self.volume = max(0, self.volume - step)
        return self.volume

    def volume_set(self, level: int) -> int:
        if self.is_muted:
            self.unmute()
        self.volume = max(0, min(100, level))
        return self.volume

    def mute(self) -> bool:
        if not self.is_muted:
            self.pre_mute_volume = self.volume
            self.volume = 0
            self.is_muted = True
        return True

    def unmute(self) -> bool:
        if self.is_muted:
            self.volume = self.pre_mute_volume
            self.is_muted = False
        return True

    def get_status(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "is_playing": self.is_playing,
            "position": self.position_seconds,
            "current_track": self.playlist[self.track_index],
            "volume": self.volume,
            "is_muted": self.is_muted,
            "shuffle": self.shuffle_enabled,
            "repeat": self.repeat_enabled,
        }
