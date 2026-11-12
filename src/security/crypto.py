"""Cryptographic Model Weight Signature Verification."""
import hashlib

class ModelIntegrityVerifier:
    @staticmethod
    def calculate_sha256(weights_bytes: bytes) -> str:
        return hashlib.sha256(weights_bytes).hexdigest()

    @classmethod
    def verify_checksum(cls, weights_bytes: bytes, expected_hash: str) -> bool:
        return cls.calculate_sha256(weights_bytes) == expected_hash.lower()
