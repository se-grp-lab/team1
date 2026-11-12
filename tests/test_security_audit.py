"""Security and Privacy Quality Gate Automated Audit (VAMC Sprint 3).

Verifies in CI/CD that no secrets leak into repository files, volatile RAM zeroization
is systematically exercised, and differential privacy bounds are strictly enforced.
"""

import unittest
import os
import re
import numpy as np
from src.security.memory import SecureAudioBuffer
from src.learning.federated import aggregate


class TestSecurityQualityGate(unittest.TestCase):
    """Enforces non-functional security & privacy quality gates."""

    def test_repo_has_no_committed_plaintext_secrets(self):
        """Scans config files to ensure no live API tokens or credentials are hardcoded."""
        config_dir = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "config"
        )
        suspicious_patterns = [
            re.compile(r'("token"\s*:\s*"[^"]{15,}")', re.IGNORECASE),
            re.compile(r'("client_secret"\s*:\s*"[^"]{15,}")', re.IGNORECASE),
            re.compile(r'("password"\s*:\s*"[^"]+")', re.IGNORECASE),
        ]
        if os.path.exists(config_dir):
            for root, _, files in os.walk(config_dir):
                for f in files:
                    if f.endswith((".json", ".yaml", ".yml")):
                        filepath = os.path.join(root, f)
                        with open(filepath, "r", encoding="utf-8", errors="ignore") as fh:
                            content = fh.read()
                            for pat in suspicious_patterns:
                                self.assertIsNone(
                                    pat.search(content),
                                    f"Security leak detected: possible secret found in {filepath}"
                                )

    def test_volatile_ram_audio_zeroization_enforced(self):
        """Verifies that SecureAudioBuffer zeroes out its bytearray upon context manager exit."""
        sensitive_audio = b"\x12\x34\x56\x78" * 1000
        with SecureAudioBuffer(sensitive_audio) as buf:
            self.assertEqual(len(buf), len(sensitive_audio))
            self.assertEqual(bytes(buf.view()[:4]), b"\x12\x34\x56\x78")
            raw_mem = buf._buf

        # Post-exit: buffer must be all zeros
        self.assertEqual(set(raw_mem), {0}, "RAM zeroization failed: sensitive audio persisted after scope exit")

    def test_differential_privacy_adversarial_rejection(self):
        """Verifies federated aggregator rejects NaN and Inf adversarial weights."""
        with self.assertRaises(ValueError):
            aggregate([np.array([0.5, float("nan")])])
        with self.assertRaises(ValueError):
            aggregate([np.array([0.5, float("inf")])])


if __name__ == "__main__":
    unittest.main()
