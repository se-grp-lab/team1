"""Unit tests for Audio Ingestion subsystem (VAMC-F-001, VAMC-F-002, VAMC-F-003)."""

import unittest
from src.audio.wake_word import WakeWordDetector
from src.audio.hotkey import PushToTalkController
from src.audio.vad import VoiceActivityDetector


class TestAudioIngestion(unittest.TestCase):
    def test_wake_word_detection(self):
        triggered = []
        detector = WakeWordDetector(
            wake_phrase="hey assistant",
            callback=lambda: triggered.append(True),
        )
        detector.start_listening()

        # Frame with matching text hint
        result = detector.process_audio_frame(b"\x00" * 640, text_hint="hey assistant play music")
        self.assertTrue(result)
        self.assertEqual(len(triggered), 1)
        self.assertLess(detector.last_detection_latency_ms, 150.0)

        # Frame with non-matching text hint
        result_neg = detector.process_audio_frame(b"\x00" * 640, text_hint="hello world")
        self.assertFalse(result_neg)

    def test_push_to_talk_trigger(self):
        ptt_events = []
        ptt = PushToTalkController(on_trigger=lambda: ptt_events.append(True))

        # Not registered
        self.assertFalse(ptt.trigger())

        # Registered
        self.assertTrue(ptt.register())
        self.assertTrue(ptt.trigger())
        self.assertEqual(len(ptt_events), 1)
        self.assertLess(ptt.last_activation_latency_ms, 50.0)

        # Unregistered
        self.assertTrue(ptt.unregister())
        self.assertFalse(ptt.trigger())

    def test_vad_silence_clipping(self):
        vad = VoiceActivityDetector(energy_threshold=100.0, trailing_silence_limit_ms=100.0, frame_duration_ms=20.0)

        # Generate loud speech frame (16-bit PCM values around 1000)
        loud_sample = (1000).to_bytes(2, byteorder="little", signed=True) * 160
        # Generate silent frame
        silent_sample = (0).to_bytes(2, byteorder="little", signed=True) * 160

        # Feed 3 loud frames (60ms)
        for _ in range(3):
            continue_rec = vad.process_frame(loud_sample)
            self.assertTrue(continue_rec)

        self.assertTrue(vad.speech_started)

        # Feed 5 silent frames (100ms silence = limit)
        for i in range(4):
            continue_rec = vad.process_frame(silent_sample)
            self.assertTrue(continue_rec)

        # 5th silent frame should hit 100ms limit and return False
        continue_rec = vad.process_frame(silent_sample)
        self.assertFalse(continue_rec)
        self.assertTrue(vad.speech_finished)

        # Verify trimmed audio contains speech frames without trailing silence
        trimmed = vad.get_trimmed_audio()
        self.assertEqual(len(trimmed), len(loud_sample) * 3)


if __name__ == "__main__":
    unittest.main()
