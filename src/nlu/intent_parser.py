"""Natural Language Intent Parsing and Entity Parameter Extraction (VAMC-F-005).

Parses transcribed text into structured IntentObjects containing ActionType,
target player, and entity parameters (e.g. seek offset, volume level).
"""

import re
from enum import Enum
from typing import Dict, Any, Optional
from dataclasses import dataclass, field


class ActionType(str, Enum):
    # Playback controls (VAMC-F-007)
    PLAY = "PLAY"
    PAUSE = "PAUSE"
    RESUME = "RESUME"
    TOGGLE = "TOGGLE"
    STOP = "STOP"

    # Scrubbing controls (VAMC-F-008)
    SEEK = "SEEK"

    # Navigation controls (VAMC-F-009)
    NEXT_TRACK = "NEXT_TRACK"
    PREV_TRACK = "PREV_TRACK"
    RESTART = "RESTART"
    SHUFFLE = "SHUFFLE"
    REPEAT = "REPEAT"

    # Volume controls (VAMC-F-010, F-011, F-012)
    VOLUME_UP = "VOLUME_UP"
    VOLUME_DOWN = "VOLUME_DOWN"
    VOLUME_SET = "VOLUME_SET"
    MUTE = "MUTE"
    UNMUTE = "UNMUTE"

    # Display & Subtitles (VAMC-F-016, F-017, F-018)
    FULLSCREEN = "FULLSCREEN"
    EXIT_FULLSCREEN = "EXIT_FULLSCREEN"
    SUBTITLES_TOGGLE = "SUBTITLES_TOGGLE"
    SUBTITLES_TRACK = "SUBTITLES_TRACK"
    PLAYBACK_RATE = "PLAYBACK_RATE"

    UNKNOWN = "UNKNOWN"


@dataclass
class IntentObject:
    action: ActionType
    target_player: Optional[str] = None
    params: Dict[str, Any] = field(default_factory=dict)
    raw_text: str = ""
    confidence: float = 1.0


class IntentParser:
    """Extracts structured intent and parameter entities from conversational voice commands."""

    PLAYER_KEYWORDS = {
        "spotify": "spotify",
        "youtube": "youtube",
        "vlc": "vlc",
        "mpv": "mpv",
    }

    def parse(self, text: str) -> IntentObject:
        """Parses speech text into an IntentObject."""
        raw_text = text.lower().strip()
        cleaned = re.sub(r"^(hey\s+assistant|assistant|please)\s*", "", raw_text).strip()

        # Extract target player if mentioned explicitly
        target_player = None
        for kw, player in self.PLAYER_KEYWORDS.items():
            if re.search(r"\b" + kw + r"\b", cleaned):
                target_player = player
                cleaned = re.sub(r"\b(on|in|with|using)\s+" + kw + r"\b", "", cleaned).strip()
                cleaned = re.sub(r"\b" + kw + r"\b", "", cleaned).strip()

        # 1. Scrubbing / Seeking (VAMC-F-008)
        # e.g. "rewind 30 seconds", "fast forward 1 minute", "skip ahead 10 seconds", "back 15s"
        seek_match = re.search(
            r"\b(fast\s*forward|skip\s*ahead|forward|ahead|rewind|skip\s*back|back)\s+(\d+)\s*(seconds?|secs?|s|minutes?|mins?|m)\b",
            cleaned,
        )
        if seek_match:
            direction_word = seek_match.group(1).lower()
            val = int(seek_match.group(2))
            unit = seek_match.group(3).lower()
            seconds = val * 60 if "m" in unit else val
            if any(d in direction_word for d in ["rewind", "back"]):
                seconds = -seconds
            return IntentObject(
                action=ActionType.SEEK,
                target_player=target_player,
                params={"offset_seconds": seconds},
                raw_text=raw_text,
            )

        # 2. Volume controls (VAMC-F-010, F-011, F-012)
        if re.search(r"\b(unmute|sound\s*on)\b", cleaned):
            return IntentObject(action=ActionType.UNMUTE, target_player=target_player, raw_text=raw_text)

        if re.search(r"\b(mute|silence|quiet)\b", cleaned):
            return IntentObject(action=ActionType.MUTE, target_player=target_player, raw_text=raw_text)

        vol_set_match = re.search(r"\b(set\s+volume\s+to|volume\s+to|volume)\s+(\d+)\s*%?\b", cleaned)
        if vol_set_match and ("up" not in cleaned and "down" not in cleaned):
            pct = int(vol_set_match.group(2))
            return IntentObject(
                action=ActionType.VOLUME_SET,
                target_player=target_player,
                params={"level": min(100, max(0, pct))},
                raw_text=raw_text,
            )

        if re.search(r"\b(volume\s*up|louder|turn\s*it\s*up|increase\s*volume)\b", cleaned):
            step = 10
            step_match = re.search(r"(\d+)\s*%", cleaned)
            if step_match:
                step = int(step_match.group(1))
            return IntentObject(
                action=ActionType.VOLUME_UP,
                target_player=target_player,
                params={"step": step},
                raw_text=raw_text,
            )

        if re.search(r"\b(volume\s*down|softer|turn\s*it\s*down|decrease\s*volume)\b", cleaned):
            step = 10
            step_match = re.search(r"(\d+)\s*%", cleaned)
            if step_match:
                step = int(step_match.group(1))
            return IntentObject(
                action=ActionType.VOLUME_DOWN,
                target_player=target_player,
                params={"step": step},
                raw_text=raw_text,
            )

        # 3. Navigation controls (VAMC-F-009)
        if re.search(r"\b(next\s*track|next\s*song|skip\s*track|skip|next)\b", cleaned):
            return IntentObject(action=ActionType.NEXT_TRACK, target_player=target_player, raw_text=raw_text)

        if re.search(r"\b(previous\s*track|previous\s*song|prev\s*track|previous|prev)\b", cleaned):
            return IntentObject(action=ActionType.PREV_TRACK, target_player=target_player, raw_text=raw_text)

        if re.search(r"\b(restart\s*track|restart\s*song|replay)\b", cleaned):
            return IntentObject(action=ActionType.RESTART, target_player=target_player, raw_text=raw_text)

        if re.search(r"\b(shuffle|toggle\s*shuffle)\b", cleaned):
            return IntentObject(action=ActionType.SHUFFLE, target_player=target_player, raw_text=raw_text)

        if re.search(r"\b(repeat|toggle\s*repeat|loop)\b", cleaned):
            return IntentObject(action=ActionType.REPEAT, target_player=target_player, raw_text=raw_text)

        # 4. Core Playback (VAMC-F-007)
        if re.search(r"\b(pause|freeze|hold)\b", cleaned):
            return IntentObject(action=ActionType.PAUSE, target_player=target_player, raw_text=raw_text)

        if re.search(r"\b(resume|unpause)\b", cleaned):
            return IntentObject(action=ActionType.RESUME, target_player=target_player, raw_text=raw_text)

        if re.search(r"\b(stop)\b", cleaned):
            return IntentObject(action=ActionType.STOP, target_player=target_player, raw_text=raw_text)

        if re.search(r"\b(play\s+or\s+pause|toggle\s+playback|toggle)\b", cleaned):
            return IntentObject(action=ActionType.TOGGLE, target_player=target_player, raw_text=raw_text)

        if re.search(r"\b(play)\b", cleaned):
            # Check for query text e.g. "play bohemian rhapsody"
            query_match = re.search(r"\bplay\s+(.+)$", cleaned)
            query = query_match.group(1).strip() if query_match else None
            return IntentObject(
                action=ActionType.PLAY,
                target_player=target_player,
                params={"query": query} if query else {},
                raw_text=raw_text,
            )

        # 5. Display & Subtitles & Rate (Sprint 2 features hooked in parser)
        if re.search(r"\b(fullscreen|maximize\s*video)\b", cleaned) and "exit" not in cleaned:
            return IntentObject(action=ActionType.FULLSCREEN, target_player=target_player, raw_text=raw_text)

        if re.search(r"\b(exit\s*fullscreen|leave\s*fullscreen|minimize\s*video)\b", cleaned):
            return IntentObject(action=ActionType.EXIT_FULLSCREEN, target_player=target_player, raw_text=raw_text)

        if re.search(r"\b(subtitles?\s*on|subtitles?\s*off|toggle\s*subtitles?)\b", cleaned):
            enable = False if "off" in cleaned else True
            return IntentObject(
                action=ActionType.SUBTITLES_TOGGLE,
                target_player=target_player,
                params={"enable": enable},
                raw_text=raw_text,
            )

        rate_match = re.search(r"\b(speed\s*up\s*to|playback\s*speed|speed)\s*(\d+(\.\d+)?)x?\b", cleaned)
        if rate_match:
            rate_val = float(rate_match.group(2))
            return IntentObject(
                action=ActionType.PLAYBACK_RATE,
                target_player=target_player,
                params={"rate": rate_val},
                raw_text=raw_text,
            )

        return IntentObject(action=ActionType.UNKNOWN, target_player=target_player, raw_text=raw_text, confidence=0.0)
