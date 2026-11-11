#!/usr/bin/env python3
"""Live Microphone Voice Listener for VAMC.

Captures real-time audio from the system microphone using pw-record/arecord,
transcribes the speech, and executes it through the central VAMCDaemon pipeline.
"""

import sys
import os
import subprocess
import tempfile
import time

from src.main import VAMCDaemon

def record_audio_clip(duration_sec: float = 3.5, output_wav: str = "/tmp/vamc_mic.wav") -> bool:
    """Records audio from default system microphone using PipeWire/ALSA."""
    cmd = ["pw-record", "--rate", "16000", "--channels", "1", output_wav]
    try:
        proc = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(duration_sec)
        proc.terminate()
        proc.wait(timeout=1.0)
        return os.path.exists(output_wav) and os.path.getsize(output_wav) > 1000
    except Exception as e:
        # Fallback to arecord if pw-record fails
        try:
            subprocess.run(
                ["arecord", "-d", str(int(duration_sec)), "-r", "16000", "-c", "1", "-f", "S16_LE", output_wav],
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            return True
        except Exception:
            return False

def transcribe_audio(wav_path: str) -> str:
    """Transcribes WAV file using SpeechRecognition."""
    try:
        import speech_recognition as sr
        r = sr.Recognizer()
        with sr.AudioFile(wav_path) as source:
            audio = r.record(source)
        try:
            return r.recognize_google(audio).lower().strip()
        except sr.UnknownValueError:
            return ""
        except sr.RequestError:
            return ""
    except ImportError:
        # Fallback helper via uv run if package is in uv cache
        res = subprocess.run(
            ["uv", "run", "--quiet", "--with", "SpeechRecognition", "python3", "-c", f"""
import speech_recognition as sr
r = sr.Recognizer()
with sr.AudioFile('{wav_path}') as source:
    audio = r.record(source)
try:
    print(r.recognize_google(audio).lower().strip())
except Exception:
    pass
"""],
            capture_output=True,
            text=True
        )
        return res.stdout.strip()

def main():
    print("=" * 64)
    print(" 🎙️  VAMC Live Microphone Voice Controller")
    print(" Press ENTER to start speaking, or 'q' to quit.")
    print("=" * 64)

    daemon = VAMCDaemon()
    daemon.start()

    try:
        while True:
            prompt = input("\n👉 Press [ENTER] and speak into your mic (or type 'q' to quit): ")
            if prompt.strip().lower() in ("q", "quit", "exit"):
                break

            print("🔴 LISTENING... (Speak now for ~3 seconds)...", flush=True)
            wav_file = tempfile.mktemp(suffix=".wav")
            success = record_audio_clip(duration_sec=3.0, output_wav=wav_file)

            if not success:
                print("❌ Could not capture audio from microphone. Check PipeWire/ALSA input.")
                continue

            print("⚡ Transcribing speech...", flush=True)
            spoken_text = transcribe_audio(wav_file)

            try:
                os.remove(wav_file)
            except OSError:
                pass

            if not spoken_text:
                print("❓ Could not understand audio (or no speech detected). Try speaking louder or closer.")
                continue

            print(f"🗣️  You said : \"{spoken_text}\"")

            # Feed through VAMC Daemon Pipeline
            with open("/dev/null", "rb") as f:
                fake_pcm = b"\x00" * 16000
            res = daemon.process_voice_command(fake_pcm, simulated_text=spoken_text)

            intent = res["intent"]
            fb = res["feedback"]
            alias_note = f" (Alias -> '{res['resolved_text']}')" if res['resolved_text'] != res['transcription'] else ""

            print(f"🎯 Action   : {intent.action.name}{alias_note}")
            print(f"📻 Dispatch : {res['dispatch']['message']}")
            print(f"💊 Feedback : {fb.icon} {fb.message} (0.0 dB silent emission)")
            print(f"⏱️  Latency  : {res['e2e_latency_ms']:.2f} ms")

    except (KeyboardInterrupt, EOFError):
        print("\nExiting...")
    finally:
        daemon.stop()

if __name__ == "__main__":
    main()
