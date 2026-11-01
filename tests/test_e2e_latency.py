"""End-to-end integration and latency benchmark tests (VAMC-NF-001)."""

import unittest
from src.main import VAMCDaemon
from src.nlu.intent_parser import ActionType


class TestE2ELatency(unittest.TestCase):
    def setUp(self):
        self.daemon = VAMCDaemon()
        self.daemon.start()

    def tearDown(self):
        self.daemon.stop()

    def test_e2e_pipeline_execution(self):
        audio_chunk = b"\x00" * 32000
        result = self.daemon.process_voice_command(audio_chunk, simulated_text="fast forward 30 seconds")

        self.assertEqual(result["intent"].action, ActionType.SEEK)
        self.assertEqual(result["intent"].params.get("offset_seconds"), 30)
        self.assertTrue(result["dispatch"]["success"])
        self.assertEqual(result["feedback"].audio_output_db, 0.0)

        # Verify latency meets VAMC-NF-001 (<= 400ms)
        self.assertLessEqual(result["e2e_latency_ms"], 400.0)

    def test_e2e_alias_resolution_pipeline(self):
        audio_chunk = b"\x00" * 32000
        result = self.daemon.process_voice_command(audio_chunk, simulated_text="chill out")

        self.assertEqual(result["resolved_text"], "play lofi on spotify")
        self.assertEqual(result["intent"].action, ActionType.PLAY)
        self.assertEqual(result["intent"].target_player, "spotify")
        self.assertLessEqual(result["e2e_latency_ms"], 400.0)

    def test_latency_benchmark_100_runs(self):
        """Validates that 95th percentile latency is <= 400ms across 100 sample commands."""
        commands = [
            "play",
            "pause",
            "rewind 15 seconds",
            "volume up",
            "set volume to 50%",
            "mute",
            "unmute",
            "next track",
            "shuffle",
            "stop",
        ]
        latencies = []
        audio_chunk = b"\x00" * 32000

        for i in range(100):
            cmd = commands[i % len(commands)]
            res = self.daemon.process_voice_command(audio_chunk, simulated_text=cmd)
            latencies.append(res["e2e_latency_ms"])

        latencies.sort()
        p95_index = int(0.95 * len(latencies))
        p95_latency = latencies[p95_index]

        print(f"\n[Benchmark] 100 E2E Runs - Min: {latencies[0]:.2f}ms, P95: {p95_latency:.2f}ms, Max: {latencies[-1]:.2f}ms")
        self.assertLessEqual(p95_latency, 400.0, f"95th percentile latency exceeded 400ms: {p95_latency}ms")


if __name__ == "__main__":
    unittest.main()
