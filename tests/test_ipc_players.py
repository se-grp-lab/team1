"""Tests for VAMC-F-013 local player IPC integration."""

import unittest

from src.controllers.ipc_players import MPVController, VLCController


class TestMPVController(unittest.TestCase):
    def setUp(self):
        self.sent = []
        self.player = MPVController(self.sent.append)

    def test_pause_and_resume_payloads(self):
        self.player.pause()
        self.player.resume()
        self.assertEqual(self.sent[0], {"command": ["set_property", "pause", True]})
        self.assertEqual(self.sent[1], {"command": ["set_property", "pause", False]})
        self.assertTrue(self.player.get_status()["is_playing"])

    def test_relative_seek(self):
        self.player.seek(-15)
        self.assertEqual(self.sent[-1], {"command": ["seek", -15, "relative"]})

    def test_volume_payload_uses_clamped_value(self):
        self.player.volume_set(250)
        self.assertEqual(self.sent[-1], {"command": ["set_property", "volume", 100]})

    def test_mute_state_mirrored(self):
        self.player.mute()
        self.assertTrue(self.player.get_status()["is_muted"])
        self.assertEqual(self.sent[-1], {"command": ["set_property", "mute", True]})


class TestVLCController(unittest.TestCase):
    def setUp(self):
        self.sent = []
        self.player = VLCController(self.sent.append)

    def test_pause_command(self):
        self.player.pause()
        self.assertEqual(self.sent[-1], {"command": "pl_forcepause"})

    def test_seek_is_signed_seconds(self):
        self.player.seek(30)
        self.assertEqual(self.sent[-1], {"command": "seek", "val": "+30s"})
        self.player.seek(-10)
        self.assertEqual(self.sent[-1], {"command": "seek", "val": "-10s"})

    def test_volume_scaled_to_vlc_range(self):
        self.player.volume_set(100)
        self.assertEqual(self.sent[-1], {"command": "volume", "val": "256"})


if __name__ == "__main__":
    unittest.main()
