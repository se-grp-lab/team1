"""Unit tests for ASR and NLU subsystem (VAMC-F-004, VAMC-F-005)."""

import unittest
from src.nlu.asr_engine import ASREngine
from src.nlu.intent_parser import IntentParser, ActionType


class TestNLU(unittest.TestCase):
    def setUp(self):
        self.asr = ASREngine()
        self.parser = IntentParser()

    def test_asr_engine_offline_execution(self):
        self.assertTrue(self.asr.is_loaded)
        self.assertLessEqual(self.asr.resident_memory_mb, 450.0)

        # Transcribe test audio
        text = self.asr.transcribe(b"\x00" * 32000, simulated_text="pause the video")
        self.assertEqual(text, "pause the video")
        self.assertLess(self.asr.last_inference_latency_ms, 300.0)

    def test_intent_parsing_playback_commands(self):
        cases = [
            ("hey assistant pause", ActionType.PAUSE, None),
            ("resume playback", ActionType.RESUME, None),
            ("stop the music", ActionType.STOP, None),
            ("play bohemian rhapsody on spotify", ActionType.PLAY, "spotify"),
            ("toggle playback", ActionType.TOGGLE, None),
        ]
        for utterance, expected_action, expected_player in cases:
            res = self.parser.parse(utterance)
            self.assertEqual(res.action, expected_action, f"Failed on: {utterance}")
            self.assertEqual(res.target_player, expected_player, f"Failed player on: {utterance}")

    def test_intent_parsing_scrubbing(self):
        cases = [
            ("fast forward 30 seconds", ActionType.SEEK, 30),
            ("rewind 1 minute", ActionType.SEEK, -60),
            ("skip ahead 10s on youtube", ActionType.SEEK, 10),
            ("back 15 seconds", ActionType.SEEK, -15),
        ]
        for utterance, expected_action, expected_offset in cases:
            res = self.parser.parse(utterance)
            self.assertEqual(res.action, expected_action, f"Failed on: {utterance}")
            self.assertEqual(res.params.get("offset_seconds"), expected_offset, f"Failed offset on: {utterance}")

    def test_intent_parsing_volume_and_navigation(self):
        # Volume
        self.assertEqual(self.parser.parse("turn it up").action, ActionType.VOLUME_UP)
        self.assertEqual(self.parser.parse("volume down 20%").params.get("step"), 20)
        self.assertEqual(self.parser.parse("set volume to 40%").params.get("level"), 40)
        self.assertEqual(self.parser.parse("mute").action, ActionType.MUTE)
        self.assertEqual(self.parser.parse("unmute").action, ActionType.UNMUTE)

        # Navigation
        self.assertEqual(self.parser.parse("next track").action, ActionType.NEXT_TRACK)
        self.assertEqual(self.parser.parse("previous song").action, ActionType.PREV_TRACK)
        self.assertEqual(self.parser.parse("restart track").action, ActionType.RESTART)
        self.assertEqual(self.parser.parse("shuffle on spotify").action, ActionType.SHUFFLE)


if __name__ == "__main__":
    unittest.main()
