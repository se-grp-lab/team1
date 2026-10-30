"""Local media player integration over IPC (VAMC-F-013).

`MPVController` speaks mpv's JSON IPC protocol (unix socket / named pipe) and
`VLCController` speaks VLC's HTTP interface commands. Both mirror player state
locally (via MockMediaPlayer) so `get_status()` stays consistent, and push every
state-changing call through an injectable transport, which keeps the logic
testable without a running player.
"""

import json
import socket
import urllib.parse
import urllib.request
from typing import Any, Callable, Optional

from .mock_player import MockMediaPlayer

Transport = Callable[[Any], None]

# Methods that mutate player state and must be forwarded to the real player.
_FORWARDED = (
    "play", "pause", "resume", "toggle", "stop", "seek", "next_track", "prev_track",
    "restart_track", "toggle_shuffle", "toggle_repeat", "volume_up", "volume_down",
    "volume_set", "mute", "unmute", "set_fullscreen", "set_subtitles",
    "select_subtitle_track", "set_playback_rate",
)


class IPCPlayerController(MockMediaPlayer):
    """State-mirroring controller that forwards operations to a transport."""

    def __init__(self, name: str, transport: Transport):
        super().__init__(name)
        self._transport = transport

    def encode(self, op: str, *args: Any) -> Optional[Any]:
        """Translates an operation into a protocol payload. Overridden per player."""
        raise NotImplementedError

    def _send(self, op: str, *args: Any) -> None:
        payload = self.encode(op, *args)
        if payload is not None:
            self._transport(payload)


def _forward(op: str):
    def method(self, *args: Any, **kwargs: Any):
        result = getattr(MockMediaPlayer, op)(self, *args, **kwargs)
        # Forward the post-state value (e.g. clamped volume) rather than raw arguments.
        self._send(op, *args)
        return result

    method.__name__ = op
    return method


for _op in _FORWARDED:
    setattr(IPCPlayerController, _op, _forward(_op))


class MPVController(IPCPlayerController):
    """mpv JSON IPC (`--input-ipc-server`) controller."""

    def __init__(self, transport: Transport, name: str = "mpv"):
        super().__init__(name, transport)

    def encode(self, op: str, *args: Any) -> Optional[Any]:
        table = {
            "play": ["set_property", "pause", False],
            "resume": ["set_property", "pause", False],
            "pause": ["set_property", "pause", True],
            "toggle": ["cycle", "pause"],
            "stop": ["stop"],
            "next_track": ["playlist-next"],
            "prev_track": ["playlist-prev"],
            "restart_track": ["seek", 0, "absolute"],
            "toggle_shuffle": ["playlist-shuffle"],
            "toggle_repeat": ["cycle-values", "loop-file", "inf", "no"],
            "mute": ["set_property", "mute", True],
            "unmute": ["set_property", "mute", False],
        }
        if op == "seek":
            return {"command": ["seek", args[0], "relative"]}
        if op == "set_fullscreen":
            return {"command": ["set_property", "fullscreen", bool(args[0])]}
        if op == "set_subtitles":
            return {"command": ["set_property", "sub-visibility", bool(args[0])]}
        if op == "select_subtitle_track":
            return {"command": ["set_property", "sid", int(args[0]) if str(args[0]).isdigit() else "auto"]}
        if op == "set_playback_rate":
            return {"command": ["set_property", "speed", self.playback_rate]}
        if op == "volume_set":
            return {"command": ["set_property", "volume", self.volume]}
        if op in ("volume_up", "volume_down"):
            return {"command": ["set_property", "volume", self.volume]}
        return {"command": table[op]} if op in table else None


class VLCController(IPCPlayerController):
    """VLC HTTP interface (`/requests/status.json?command=...`) controller."""

    def __init__(self, transport: Transport, name: str = "vlc"):
        super().__init__(name, transport)

    def encode(self, op: str, *args: Any) -> Optional[Any]:
        vlc_volume = round(self.volume * 2.56)  # VLC scale: 0-512 (256 = 100%)
        table = {
            "play": {"command": "pl_play"},
            "resume": {"command": "pl_forceresume"},
            "pause": {"command": "pl_forcepause"},
            "toggle": {"command": "pl_pause"},
            "stop": {"command": "pl_stop"},
            "next_track": {"command": "pl_next"},
            "prev_track": {"command": "pl_previous"},
            "restart_track": {"command": "seek", "val": "0"},
            "toggle_shuffle": {"command": "pl_random"},
            "toggle_repeat": {"command": "pl_repeat"},
            "mute": {"command": "volume", "val": "0"},
            "unmute": {"command": "volume", "val": str(vlc_volume)},
            "volume_set": {"command": "volume", "val": str(vlc_volume)},
            "volume_up": {"command": "volume", "val": str(vlc_volume)},
            "volume_down": {"command": "volume", "val": str(vlc_volume)},
        }
        if op == "seek":
            return {"command": "seek", "val": f"{args[0]:+d}s"}
        if op == "set_fullscreen":
            return {"command": "fullscreen"}
        if op == "set_subtitles":
            return {"command": "subtitle_track", "val": "1" if args[0] else "-1"}
        if op == "select_subtitle_track":
            return {"command": "subtitle_track", "val": str(args[0])}
        if op == "set_playback_rate":
            return {"command": "rate", "val": str(self.playback_rate)}
        return table.get(op)


class MPVSocketTransport:
    """Writes newline-delimited JSON to an mpv unix IPC socket."""

    def __init__(self, socket_path: str = "/tmp/mpvsocket"):
        self.socket_path = socket_path

    def __call__(self, payload: Any) -> None:
        with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as sock:
            sock.settimeout(0.2)
            sock.connect(self.socket_path)
            sock.sendall((json.dumps(payload) + "\n").encode("utf-8"))


class VLCHttpTransport:
    """Issues VLC HTTP interface requests (password-only basic auth)."""

    def __init__(self, password: str, host: str = "127.0.0.1", port: int = 8080):
        self.base = f"http://{host}:{port}/requests/status.json"
        mgr = urllib.request.HTTPPasswordMgrWithDefaultRealm()
        mgr.add_password(None, self.base, "", password)
        self._opener = urllib.request.build_opener(urllib.request.HTTPBasicAuthHandler(mgr))

    def __call__(self, payload: Any) -> None:
        self._opener.open(f"{self.base}?{urllib.parse.urlencode(payload)}", timeout=0.2).read()
