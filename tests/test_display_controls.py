"""Tests for VAMC-F-016/017/018 display, subtitle and playback-rate controls."""

import unittest

from src.controllers.dispatcher import MediaDispatcher
from src.controllers.ipc_players import MPVController, VLCController
from src.controllers.mock_player import MockMediaPlayer
from src.nlu.intent_parser import ActionType, IntentParser


class TestDisplayParsing(unittest.TestCase):
    def setUp(self):
        self.parser = IntentParser()

    def test_fullscreen_and_exit(self):
        self.assertEqual(self.parser.parse("go fullscreen").action, ActionType.FULLSCREEN)
        self.assertEqual(self.parser.parse("exit fullscreen").action, ActionType.EXIT_FULLSCREEN)

    def test_subtitle_toggle(self):
        self.assertFalse(self.parser.parse("subtitles off").params["enable"])
        self.assertTrue(self.parser.parse("subtitles on").params["enable"])

    def test_subtitle_track_selection(self):
        intent = self.parser.parse("subtitles track 2")
        self.assertEqual(intent.action, ActionType.SUBTITLES_TRACK)
        self.assertEqual(intent.params["track"], "2")
        self.assertEqual(self.parser.parse("subtitles to english").params["track"], "english")

    def test_playback_rate(self):
        intent = self.parser.parse("playback speed 1.5x")
        self.assertEqual(intent.action, ActionType.PLAYBACK_RATE)
        self.assertEqual(intent.params["rate"], 1.5)


class TestDisplayDispatch(unittest.TestCase):
    def setUp(self):
        self.player = MockMediaPlayer("m")
        self.dispatcher = MediaDispatcher(self.player)
        self.parser = IntentParser()

    def run_cmd(self, text):
        return self.dispatcher.dispatch(self.parser.parse(text))

    def test_fullscreen_state(self):
        self.run_cmd("fullscreen")
        self.assertTrue(self.player.fullscreen)
        self.run_cmd("exit fullscreen")
        self.assertFalse(self.player.fullscreen)

    def test_subtitle_track_enables_subtitles(self):
        self.run_cmd("subtitles track 3")
        self.assertTrue(self.player.subtitles_enabled)
        self.assertEqual(self.player.subtitle_track, "3")

    def test_rate_is_clamped_to_supported_range(self):
        self.assertEqual(self.run_cmd("playback speed 5")["player_status"]["rate"], 2.0)
        self.assertEqual(self.run_cmd("playback speed 0.1")["player_status"]["rate"], 0.5)

    def test_unsupported_player_reports_failure(self):
        from src.controllers.base import BaseMediaController

        class AudioOnly(MockMediaPlayer):
            set_fullscreen = BaseMediaController.set_fullscreen

        d = MediaDispatcher(AudioOnly("audio"))
        res = d.dispatch(self.parser.parse("fullscreen"))
        self.assertFalse(res["success"])


class TestIPCDisplayPayloads(unittest.TestCase):
    def test_mpv_payloads(self):
        sent = []
        p = MPVController(sent.append)
        p.set_fullscreen(True)
        p.set_playback_rate(1.25)
        self.assertEqual(sent[0], {"command": ["set_property", "fullscreen", True]})
        self.assertEqual(sent[1], {"command": ["set_property", "speed", 1.25]})

    def test_vlc_payloads(self):
        sent = []
        p = VLCController(sent.append)
        p.select_subtitle_track("2")
        p.set_playback_rate(2.0)
        self.assertEqual(sent[0], {"command": "subtitle_track", "val": "2"})
        self.assertEqual(sent[1], {"command": "rate", "val": "2.0"})


if __name__ == "__main__":
    unittest.main()
