"""Spotify Web API / Connect integration (VAMC-F-014).

Maps VAMC operations onto the Spotify Web API player endpoints. The HTTP layer
and access-token source are injected, so the OAuth token can come from the
OS keyring (VAMC credential store) and tests can run offline.
"""

import json
import urllib.parse
import urllib.request
from typing import Any, Callable, Dict, Optional

from .base import BaseMediaController
from .mock_player import MockMediaPlayer

API_BASE = "https://api.spotify.com/v1"

HttpFn = Callable[[str, str, Dict[str, Any], Optional[dict], str], None]


def urllib_http(method: str, path: str, params: Dict[str, Any], body: Optional[dict], token: str) -> None:
    """Default HTTP implementation using urllib (no third-party dependency)."""
    url = f"{API_BASE}{path}"
    if params:
        url += "?" + urllib.parse.urlencode(params)
    data = json.dumps(body).encode("utf-8") if body is not None else None
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Authorization", f"Bearer {token}")
    req.add_header("Content-Type", "application/json")
    urllib.request.urlopen(req, timeout=2).read()


class SpotifyController(MockMediaPlayer):
    """Controls the active Spotify Connect device via the Web API."""

    def __init__(self, token_provider: Callable[[], str], http: HttpFn = urllib_http,
                 device_id: Optional[str] = None, name: str = "spotify"):
        super().__init__(name)
        self._token_provider = token_provider
        self._http = http
        self.device_id = device_id

    def _call(self, method: str, path: str, params: Optional[Dict[str, Any]] = None,
              body: Optional[dict] = None) -> None:
        params = dict(params or {})
        if self.device_id:
            params["device_id"] = self.device_id
        token = self._token_provider()
        if not token:
            raise PermissionError("Spotify access token unavailable; authenticate first")
        self._http(method, path, params, body, token)

    def play(self, query: Optional[str] = None) -> bool:
        body = None
        if query:
            # Resolve by search query; Spotify context URIs are looked up by the caller's catalog.
            body = {"context_uri": query} if query.startswith("spotify:") else None
        self._call("PUT", "/me/player/play", body=body)
        return super().play(query)

    def pause(self) -> bool:
        self._call("PUT", "/me/player/pause")
        return super().pause()

    def resume(self) -> bool:
        self._call("PUT", "/me/player/play")
        return super().resume()

    def toggle(self) -> bool:
        return self.pause() if self.is_playing else self.resume()

    def stop(self) -> bool:
        self._call("PUT", "/me/player/pause")
        self._call("PUT", "/me/player/seek", {"position_ms": 0})
        return super().stop()

    def seek(self, offset_seconds: int) -> int:
        pos = super().seek(offset_seconds)
        self._call("PUT", "/me/player/seek", {"position_ms": pos * 1000})
        return pos

    def next_track(self) -> str:
        self._call("POST", "/me/player/next")
        return super().next_track()

    def prev_track(self) -> str:
        self._call("POST", "/me/player/previous")
        return super().prev_track()

    def restart_track(self) -> bool:
        self._call("PUT", "/me/player/seek", {"position_ms": 0})
        return super().restart_track()

    def toggle_shuffle(self) -> bool:
        state = super().toggle_shuffle()
        self._call("PUT", "/me/player/shuffle", {"state": str(state).lower()})
        return state

    def toggle_repeat(self) -> bool:
        state = super().toggle_repeat()
        self._call("PUT", "/me/player/repeat", {"state": "context" if state else "off"})
        return state

    def _push_volume(self) -> int:
        self._call("PUT", "/me/player/volume", {"volume_percent": self.volume})
        return self.volume

    def volume_up(self, step: int = 10) -> int:
        super().volume_up(step)
        return self._push_volume()

    def volume_down(self, step: int = 10) -> int:
        super().volume_down(step)
        return self._push_volume()

    def volume_set(self, level: int) -> int:
        super().volume_set(level)
        return self._push_volume()

    def mute(self) -> bool:
        super().mute()
        self._push_volume()
        return True

    def unmute(self) -> bool:
        super().unmute()
        self._push_volume()
        return True

    # Spotify is audio-only: display, subtitle and rate controls are unsupported.
    set_fullscreen = BaseMediaController.set_fullscreen
    set_subtitles = BaseMediaController.set_subtitles
    select_subtitle_track = BaseMediaController.select_subtitle_track
    set_playback_rate = BaseMediaController.set_playback_rate
