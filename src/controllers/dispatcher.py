"""Media command dispatcher (VAMC-F-007 to VAMC-F-012).

Dispatches structured IntentObjects to active or targeted media controllers
with latency tracking ensuring execution within <= 200 ms.
"""

import time
from typing import Dict, Any, Optional
from src.nlu.intent_parser import IntentObject, ActionType
from .base import BaseMediaController
from .mock_player import MockMediaPlayer
from .router import PlayerRouter


class MediaDispatcher:
    """Routes IntentObjects to the appropriate media controller."""

    def __init__(self, default_controller: Optional[BaseMediaController] = None,
                 router: Optional[PlayerRouter] = None):
        self.router = router
        self.default_controller = default_controller or MockMediaPlayer("system_default")
        self.controllers: Dict[str, BaseMediaController] = {
            "default": self.default_controller,
        }
        self._last_dispatch_latency_ms: float = 0.0

    def register_controller(self, name: str, controller: BaseMediaController) -> None:
        """Registers a named media controller (e.g. 'vlc', 'spotify')."""
        self.controllers[name.lower()] = controller

    def get_controller(self, target_player: Optional[str] = None) -> BaseMediaController:
        """Resolves target controller (explicit, auto-detected, then default)."""
        if self.router is not None:
            target_player = self.router.resolve(target_player, available=self.controllers.keys())
        if target_player and target_player.lower() in self.controllers:
            return self.controllers[target_player.lower()]
        return self.default_controller

    def dispatch(self, intent: IntentObject) -> Dict[str, Any]:
        """Executes the action on the resolved media player controller.

        Returns execution result summary dictionary.
        """
        start = time.perf_counter()
        controller = self.get_controller(intent.target_player)
        action = intent.action
        params = intent.params

        res_msg = ""
        success = True

        if action == ActionType.PLAY:
            query = params.get("query")
            controller.play(query)
            res_msg = f"Playing {query}" if query else "Playing"

        elif action == ActionType.PAUSE:
            controller.pause()
            res_msg = "Paused"

        elif action == ActionType.RESUME:
            controller.resume()
            res_msg = "Resumed"

        elif action == ActionType.TOGGLE:
            state = controller.toggle()
            res_msg = "Playing" if state else "Paused"

        elif action == ActionType.STOP:
            controller.stop()
            res_msg = "Stopped"

        elif action == ActionType.SEEK:
            offset = params.get("offset_seconds", 0)
            new_pos = controller.seek(offset)
            direction = "Forward" if offset >= 0 else "Rewound"
            res_msg = f"{direction} {abs(offset)}s (at {new_pos}s)"

        elif action == ActionType.NEXT_TRACK:
            track = controller.next_track()
            res_msg = f"Next: {track}"

        elif action == ActionType.PREV_TRACK:
            track = controller.prev_track()
            res_msg = f"Previous: {track}"

        elif action == ActionType.RESTART:
            controller.restart_track()
            res_msg = "Restarted Track"

        elif action == ActionType.SHUFFLE:
            st = controller.toggle_shuffle()
            res_msg = f"Shuffle {'On' if st else 'Off'}"

        elif action == ActionType.REPEAT:
            st = controller.toggle_repeat()
            res_msg = f"Repeat {'On' if st else 'Off'}"

        elif action == ActionType.VOLUME_UP:
            step = params.get("step", 10)
            lvl = controller.volume_up(step)
            res_msg = f"Volume {lvl}%"

        elif action == ActionType.VOLUME_DOWN:
            step = params.get("step", 10)
            lvl = controller.volume_down(step)
            res_msg = f"Volume {lvl}%"

        elif action == ActionType.VOLUME_SET:
            lvl = params.get("level", 50)
            lvl = controller.volume_set(lvl)
            res_msg = f"Volume {lvl}%"

        elif action == ActionType.MUTE:
            controller.mute()
            res_msg = "Muted"

        elif action == ActionType.UNMUTE:
            controller.unmute()
            res_msg = "Unmuted"

        elif action in (ActionType.FULLSCREEN, ActionType.EXIT_FULLSCREEN):
            enable = action == ActionType.FULLSCREEN
            success = controller.set_fullscreen(enable)
            res_msg = ("Fullscreen" if enable else "Exited Fullscreen") if success else "Fullscreen unsupported"

        elif action == ActionType.SUBTITLES_TOGGLE:
            enable = params.get("enable", True)
            success = controller.set_subtitles(enable)
            res_msg = (f"Subtitles {'On' if enable else 'Off'}") if success else "Subtitles unsupported"

        elif action == ActionType.SUBTITLES_TRACK:
            track = params.get("track", "default")
            success = controller.select_subtitle_track(track)
            res_msg = f"Subtitles: {track}" if success else "Subtitles unsupported"

        elif action == ActionType.PLAYBACK_RATE:
            rate = controller.set_playback_rate(params.get("rate", 1.0))
            res_msg = f"Speed {rate:g}x"

        else:
            success = False
            res_msg = f"Unhandled action {action}"

        self._last_dispatch_latency_ms = (time.perf_counter() - start) * 1000.0

        return {
            "success": success,
            "message": res_msg,
            "action": action.value,
            "latency_ms": self._last_dispatch_latency_ms,
            "player_status": controller.get_status(),
        }

    @property
    def last_dispatch_latency_ms(self) -> float:
        """Returns the latency of the last dispatch operation (target < 200ms)."""
        return self._last_dispatch_latency_ms
