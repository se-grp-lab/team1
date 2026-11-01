"""Voice Assistant for Multimedia Controls (VAMC) - Main Application Daemon.

Orchestrates the entire offline touchless pipeline:
Audio Ingestion -> ASR -> NLU -> Alias Resolution -> Media Dispatcher -> Silent Feedback.
"""

import time
from typing import Optional, Dict, Any

from src.audio.wake_word import WakeWordDetector
from src.audio.hotkey import PushToTalkController
from src.audio.vad import VoiceActivityDetector
from src.nlu.asr_engine import ASREngine
from src.nlu.intent_parser import IntentParser
from src.config.alias_manager import AliasManager
from src.controllers.dispatcher import MediaDispatcher
from src.ui.silent_feedback import SilentFeedbackDispatcher


class VAMCDaemon:
    """Central daemon tying all Sprint 1 subsystems into an integrated pipeline."""

    def __init__(self, config_path: Optional[str] = None):
        self.wake_detector = WakeWordDetector(wake_phrase="hey assistant")
        self.ptt_controller = PushToTalkController()
        self.vad = VoiceActivityDetector()
        self.asr = ASREngine()
        self.parser = IntentParser()
        self.alias_mgr = AliasManager(config_path=config_path)
        self.dispatcher = MediaDispatcher()
        self.feedback = SilentFeedbackDispatcher()
        self._last_e2e_latency_ms: float = 0.0

    def start(self) -> None:
        """Starts background listeners."""
        self.wake_detector.start_listening()
        self.ptt_controller.register()

    def stop(self) -> None:
        """Stops background listeners."""
        self.wake_detector.stop_listening()
        self.ptt_controller.unregister()

    def process_voice_command(self, audio_pcm: bytes, simulated_text: Optional[str] = None) -> Dict[str, Any]:
        """Executes the full end-to-end voice pipeline:

        1. ASR Transcription (offline)
        2. Alias Resolution
        3. Intent Parsing
        4. Media Controller Dispatch
        5. Silent Visual Feedback Dispatch
        """
        start_time = time.perf_counter()

        # Step 1: Offline Speech Recognition
        transcription = self.asr.transcribe(audio_pcm, simulated_text=simulated_text)

        # Step 2: Custom Alias Mapping
        canonical_text = self.alias_mgr.resolve(transcription)

        # Step 3: Intent & Entity Parsing
        intent = self.parser.parse(canonical_text)

        # Step 4: Dispatch to Media Controller
        dispatch_result = self.dispatcher.dispatch(intent)

        # Step 5: Silent Feedback Pill (0 dB emission)
        icon = f"[{intent.action.value}]"
        feedback_event = self.feedback.notify(
            icon=icon,
            message=dispatch_result["message"],
            confidence=intent.confidence,
        )

        total_latency_ms = (time.perf_counter() - start_time) * 1000.0
        self._last_e2e_latency_ms = total_latency_ms

        return {
            "transcription": transcription,
            "resolved_text": canonical_text,
            "intent": intent,
            "dispatch": dispatch_result,
            "feedback": feedback_event,
            "e2e_latency_ms": total_latency_ms,
        }

    @property
    def last_e2e_latency_ms(self) -> float:
        """Returns the total end-to-end latency in ms (target <= 400ms per VAMC-NF-001)."""
        return self._last_e2e_latency_ms


if __name__ == "__main__":
    daemon = VAMCDaemon()
    daemon.start()
    print("VAMC Daemon running. Triggering sample command 'play'...")
    res = daemon.process_voice_command(b"\x00" * 32000, simulated_text="play")
    print(f"Status: {res['dispatch']['message']} in {res['e2e_latency_ms']:.2f} ms")
    daemon.stop()
