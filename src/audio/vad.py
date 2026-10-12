"""Voice Activity Detection (VAD) and Trailing Silence Clipping (VAMC-F-003).

Detects beginning and end of speech segments, automatically concluding capture
buffer upon 500ms of sustained trailing silence.
"""

import time
from typing import List


class VoiceActivityDetector:
    """Monitors incoming frame energy and detects trailing silence boundaries."""

    def __init__(
        self,
        energy_threshold: float = 300.0,
        trailing_silence_limit_ms: float = 500.0,
        frame_duration_ms: float = 20.0,
    ):
        self.energy_threshold = energy_threshold
        self.trailing_silence_limit_ms = trailing_silence_limit_ms
        self.frame_duration_ms = frame_duration_ms
        self.reset()

    def reset(self) -> None:
        """Resets the internal speech accumulator state."""
        self.speech_started = False
        self.speech_finished = False
        self.consecutive_silence_ms = 0.0
        self.speech_frames: List[bytes] = []

    def is_speech_frame(self, frame: bytes) -> bool:
        """Computes root-mean-square (RMS) energy to detect speech presence."""
        if not frame:
            return False

        # 16-bit signed PCM frames
        count = len(frame) // 2
        if count == 0:
            return False

        sum_squares = 0
        for i in range(0, len(frame), 2):
            val = int.from_bytes(frame[i : i + 2], byteorder="little", signed=True)
            sum_squares += val * val

        rms = (sum_squares / count) ** 0.5
        return rms >= self.energy_threshold

    def process_frame(self, frame: bytes) -> bool:
        """Feeds a single audio frame into the VAD state machine.

        Returns:
            True if recording should continue, False if 500ms trailing silence reached.
        """
        if self.speech_finished:
            return False

        speech_present = self.is_speech_frame(frame)

        if speech_present:
            self.speech_started = True
            self.consecutive_silence_ms = 0.0
            self.speech_frames.append(frame)
            return True

        if self.speech_started:
            self.consecutive_silence_ms += self.frame_duration_ms
            self.speech_frames.append(frame)

            if self.consecutive_silence_ms >= self.trailing_silence_limit_ms:
                self.speech_finished = True
                return False

        return True

    def get_trimmed_audio(self) -> bytes:
        """Returns the accumulated speech buffer with trailing silence clipped."""
        # Clip trailing silence frames
        frames_to_cut = int(self.consecutive_silence_ms / self.frame_duration_ms)
        if frames_to_cut > 0 and len(self.speech_frames) >= frames_to_cut:
            active_frames = self.speech_frames[:-frames_to_cut]
        else:
            active_frames = self.speech_frames
        return b"".join(active_frames)
