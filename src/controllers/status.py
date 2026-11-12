"""Standardized Unified Media Player Status Schema."""
from dataclasses import dataclass, field
from typing import Optional, Dict, Any

@dataclass
class UnifiedPlayerStatus:
    player_name: str
    is_playing: bool
    volume: int
    position_seconds: float
    duration_seconds: float
    track_title: Optional[str] = None
    track_artist: Optional[str] = None
    rate: float = 1.0
    subtitles_active: bool = False
    metadata: Dict[str, Any] = field(default_factory=dict)
