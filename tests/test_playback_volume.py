"""Unit tests for Playback and Volume Controllers (VAMC-F-007 through VAMC-F-012)."""

import unittest
from src.controllers.mock_player import MockMediaPlayer
from src.controllers.dispatcher import MediaDispatcher
from src.nlu.intent_parser import IntentObject, ActionType


class TestPlaybackAndVolume(unittest.TestCase):
    def setUp(self):
        self.player = MockMediaPlayer("test_player")
        self.dispatcher = MediaDispatcher(default_controller=self.player)

    def test_core_playback_states(self):
        # Play
        res = self.dispatcher.dispatch(IntentObject(action=ActionType.PLAY))
        self.assertTrue(self.player.is_playing)
        self.assertLess(res["latency_ms"], 200.0)

        # Pause
        self.dispatcher.dispatch(IntentObject(action=ActionType.PAUSE))
        self.assertFalse(self.player.is_playing)

        # Resume
        self.dispatcher.dispatch(IntentObject(action=ActionType.RESUME))
        self.assertTrue(self.player.is_playing)

        # Stop
        self.dispatcher.dispatch(IntentObject(action=ActionType.STOP))
        self.assertFalse(self.player.is_playing)
        self.assertEqual(self.player.position_seconds, 0)

    def test_relative_scrubbing(self):
        self.player.position_seconds = 100

        # Fast forward 30 seconds
        self.dispatcher.dispatch(IntentObject(action=ActionType.SEEK, params={"offset_seconds": 30}))
        self.assertEqual(self.player.position_seconds, 130)

        # Rewind 45 seconds
        self.dispatcher.dispatch(IntentObject(action=ActionType.SEEK, params={"offset_seconds": -45}))
        self.assertEqual(self.player.position_seconds, 85)

        # Clamping to lower bound
        self.dispatcher.dispatch(IntentObject(action=ActionType.SEEK, params={"offset_seconds": -200}))
        self.assertEqual(self.player.position_seconds, 0)

    def test_track_navigation_and_modes(self):
        initial_track = self.player.playlist[0]
        self.assertEqual(self.player.get_status()["current_track"], initial_track)

        # Next
        self.dispatcher.dispatch(IntentObject(action=ActionType.NEXT_TRACK))
        self.assertEqual(self.player.track_index, 1)

        # Previous
        self.dispatcher.dispatch(IntentObject(action=ActionType.PREV_TRACK))
        self.assertEqual(self.player.track_index, 0)

        # Shuffle & Repeat toggles
        self.dispatcher.dispatch(IntentObject(action=ActionType.SHUFFLE))
        self.assertTrue(self.player.shuffle_enabled)
        self.dispatcher.dispatch(IntentObject(action=ActionType.REPEAT))
        self.assertTrue(self.player.repeat_enabled)

    def test_volume_controls_and_mute(self):
        self.player.volume = 50

        # Volume Up
        self.dispatcher.dispatch(IntentObject(action=ActionType.VOLUME_UP, params={"step": 15}))
        self.assertEqual(self.player.volume, 65)

        # Volume Down
        self.dispatcher.dispatch(IntentObject(action=ActionType.VOLUME_DOWN, params={"step": 25}))
        self.assertEqual(self.player.volume, 40)

        # Absolute Volume Set
        self.dispatcher.dispatch(IntentObject(action=ActionType.VOLUME_SET, params={"level": 75}))
        self.assertEqual(self.player.volume, 75)

        # Mute and Unmute restoration
        self.dispatcher.dispatch(IntentObject(action=ActionType.MUTE))
        self.assertTrue(self.player.is_muted)
        self.assertEqual(self.player.volume, 0)

        self.dispatcher.dispatch(IntentObject(action=ActionType.UNMUTE))
        self.assertFalse(self.player.is_muted)
        self.assertEqual(self.player.volume, 75)


if __name__ == "__main__":
    unittest.main()
