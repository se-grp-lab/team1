"""Tests for VAMC-F-014 (Spotify) and VAMC-F-015 (routing)."""

import unittest

from src.controllers.router import PlayerRouter
from src.controllers.spotify import SpotifyController


class TestSpotifyController(unittest.TestCase):
    def setUp(self):
        self.calls = []

        def fake_http(method, path, params, body, token):
            self.calls.append((method, path, params, body, token))

        self.player = SpotifyController(lambda: "tok123", http=fake_http, device_id="dev1")

    def test_pause_hits_pause_endpoint_with_token_and_device(self):
        self.player.pause()
        method, path, params, _, token = self.calls[-1]
        self.assertEqual((method, path, token), ("PUT", "/me/player/pause", "tok123"))
        self.assertEqual(params["device_id"], "dev1")

    def test_seek_sends_milliseconds(self):
        self.player.seek(30)
        self.assertEqual(self.calls[-1][2]["position_ms"], 30000)

    def test_volume_set_clamps_and_sends_percent(self):
        self.player.volume_set(180)
        self.assertEqual(self.calls[-1][2]["volume_percent"], 100)

    def test_shuffle_state_flag(self):
        self.player.toggle_shuffle()
        self.assertEqual(self.calls[-1][2]["state"], "true")

    def test_missing_token_raises(self):
        p = SpotifyController(lambda: "", http=lambda *a: None)
        with self.assertRaises(PermissionError):
            p.pause()


class TestPlayerRouter(unittest.TestCase):
    def test_explicit_target_wins(self):
        r = PlayerRouter(lambda: ["vlc"])
        self.assertEqual(r.resolve("spotify"), "spotify")

    def test_detects_running_player(self):
        r = PlayerRouter(lambda: ["bash", "VLC", "Xorg"])
        self.assertEqual(r.resolve(), "vlc")

    def test_priority_when_multiple_running(self):
        r = PlayerRouter(lambda: ["spotify", "mpv"])
        self.assertEqual(r.resolve(), "mpv")

    def test_sticky_last_used_player(self):
        r = PlayerRouter(lambda: ["spotify", "mpv"])
        r.resolve("spotify")
        self.assertEqual(r.resolve(), "spotify")

    def test_none_running_falls_back(self):
        r = PlayerRouter(lambda: ["bash"])
        self.assertIsNone(r.resolve())

    def test_available_filter(self):
        r = PlayerRouter(lambda: ["mpv", "vlc"])
        self.assertEqual(r.resolve(available=["vlc"]), "vlc")


class TestDispatcherRouting(unittest.TestCase):
    def test_bare_command_routes_to_detected_player(self):
        from src.controllers.dispatcher import MediaDispatcher
        from src.controllers.mock_player import MockMediaPlayer
        from src.nlu.intent_parser import IntentParser

        d = MediaDispatcher(router=PlayerRouter(lambda: ["vlc"]))
        vlc = MockMediaPlayer("vlc")
        d.register_controller("vlc", vlc)
        d.dispatch(IntentParser().parse("play"))
        self.assertTrue(vlc.is_playing)
        self.assertFalse(d.default_controller.is_playing)


if __name__ == "__main__":
    unittest.main()
