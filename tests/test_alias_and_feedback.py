"""Unit tests for Custom Aliases and Silent Feedback (VAMC-F-006, VAMC-NF-005)."""

import unittest
import tempfile
import os
from src.config.alias_manager import AliasManager
from src.ui.silent_feedback import SilentFeedbackDispatcher


class TestAliasAndSilentFeedback(unittest.TestCase):
    def setUp(self):
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".json")
        self.temp_file.close()
        self.mgr = AliasManager(config_path=self.temp_file.name)

    def tearDown(self):
        if os.path.exists(self.temp_file.name):
            os.remove(self.temp_file.name)

    def test_alias_management_and_persistence(self):
        self.mgr.add_alias("chill out", "play lofi on spotify")
        self.mgr.add_alias("skip commercial", "fast forward 30 seconds")

        # Test resolution
        self.assertEqual(self.mgr.resolve("chill out"), "play lofi on spotify")
        self.assertEqual(self.mgr.resolve("skip commercial"), "fast forward 30 seconds")
        self.assertEqual(self.mgr.resolve("unrelated phrase"), "unrelated phrase")

        # Reload from disk to verify persistence
        new_mgr = AliasManager(config_path=self.temp_file.name)
        self.assertEqual(new_mgr.resolve("chill out"), "play lofi on spotify")

        # Remove alias
        self.assertTrue(new_mgr.remove_alias("chill out"))
        self.assertEqual(new_mgr.resolve("chill out"), "chill out")

    def test_zero_audio_pollution_guarantee(self):
        received_events = []
        dispatcher = SilentFeedbackDispatcher(visual_listener=lambda ev: received_events.append(ev))

        event = dispatcher.notify(icon="[PAUSE]", message="Playback Paused")

        self.assertEqual(len(received_events), 1)
        self.assertEqual(event.message, "Playback Paused")
        self.assertEqual(event.audio_output_db, 0.0)
        self.assertEqual(dispatcher.total_audio_pollution_db, 0.0)


if __name__ == "__main__":
    unittest.main()
