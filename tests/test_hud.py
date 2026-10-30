"""Tests for VAMC-F-019 (HUD pill) and VAMC-F-020 (auto-dismiss, no focus stealing)."""

import unittest

from src.ui.hud import HUDOverlay
from src.ui.silent_feedback import SilentFeedbackDispatcher


class FakeClock:
    def __init__(self):
        self.now = 100.0

    def __call__(self):
        return self.now


class TestHUDOverlay(unittest.TestCase):
    def setUp(self):
        self.clock = FakeClock()
        self.rendered = []
        self.hud = HUDOverlay(self.rendered.append, dismiss_after_s=2.0, clock=self.clock)
        self.feedback = SilentFeedbackDispatcher(visual_listener=self.hud.show)

    def test_feedback_event_shows_translucent_pill(self):
        self.feedback.notify("[PLAY]", "Playing")
        self.assertTrue(self.hud.visible)
        self.assertEqual(self.hud.state.message, "Playing")
        self.assertLess(self.hud.state.opacity, 1.0)
        self.assertTrue(self.hud.state.always_on_top)

    def test_pill_never_steals_focus(self):
        self.feedback.notify("[PLAY]", "Playing")
        self.assertFalse(self.hud.state.accepts_focus)
        self.assertTrue(self.hud.state.click_through)

    def test_auto_dismiss_after_timeout(self):
        self.feedback.notify("[PAUSE]", "Paused")
        self.clock.now += 1.9
        self.assertFalse(self.hud.tick())
        self.assertTrue(self.hud.visible)
        self.clock.now += 0.2
        self.assertTrue(self.hud.tick())
        self.assertFalse(self.hud.visible)
        self.assertIsNone(self.rendered[-1])

    def test_new_event_restarts_timer(self):
        self.feedback.notify("[PLAY]", "Playing")
        self.clock.now += 1.5
        self.feedback.notify("[VOLUME_UP]", "Volume 60%")
        self.clock.now += 1.5
        self.assertFalse(self.hud.tick())
        self.assertEqual(self.hud.state.message, "Volume 60%")

    def test_invalid_configuration_rejected(self):
        with self.assertRaises(ValueError):
            HUDOverlay(opacity=1.0)
        with self.assertRaises(ValueError):
            HUDOverlay(dismiss_after_s=0)

    def test_hud_stays_silent(self):
        event = self.feedback.notify("[PLAY]", "Playing")
        self.assertEqual(event.audio_output_db, 0.0)


if __name__ == "__main__":
    unittest.main()
