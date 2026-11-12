"""Tests for Weight Integrity Verifier."""
import unittest
from src.security.crypto import ModelIntegrityVerifier

class TestModelIntegrityVerifier(unittest.TestCase):
    def test_sha256_generation(self):
        digest = ModelIntegrityVerifier.calculate_sha256(b"sample_weights")
        self.assertEqual(len(digest), 64)

    def test_checksum_verification(self):
        data = b"model_data"
        h = ModelIntegrityVerifier.calculate_sha256(data)
        self.assertTrue(ModelIntegrityVerifier.verify_checksum(data, h))
        self.assertFalse(ModelIntegrityVerifier.verify_checksum(data, "0" * 64))

if __name__ == '__main__':
    unittest.main()
