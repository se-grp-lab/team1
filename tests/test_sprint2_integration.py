"""Sprint 2 end-to-end integration: HUD, adaptation, zeroization wired into the daemon."""

import unittest

from src.main import VAMCDaemon


class TestSprint2Integration(unittest.TestCase):
    def setUp(self):
        self.daemon = VAMCDaemon()

    def test_command_shows_silent_hud_pill(self):
        self.daemon.process_voice_command(b"\x00" * 3200, simulated_text="fullscreen")
        self.assertTrue(self.daemon.hud.visible)
        self.assertFalse(self.daemon.hud.state.accepts_focus)
        self.assertEqual(self.daemon.hud.state.message, "Fullscreen")

    def test_learned_correction_changes_intent(self):
        for _ in range(2):
            self.daemon.adapter.observe("pause the sung", "pause")
        res = self.daemon.process_voice_command(b"\x00" * 3200, simulated_text="pause the sung")
        self.assertEqual(res["intent"].action.value, "PAUSE")

    def test_playback_rate_end_to_end(self):
        res = self.daemon.process_voice_command(b"\x00" * 3200, simulated_text="playback speed 1.5x")
        self.assertEqual(res["dispatch"]["player_status"]["rate"], 1.5)


if __name__ == "__main__":
    unittest.main()
