"""Tests for PRJ-SR-001 (RAM zeroization) and PRJ-SR-002 (keyring credential storage)."""

import unittest

from src.security.credentials import CredentialStore, KeyringUnavailable
from src.security.memory import SecureAudioBuffer


class FakeKeyring:
    def __init__(self):
        self.data = {}

    def set_password(self, service, key, secret):
        self.data[(service, key)] = secret

    def get_password(self, service, key):
        return self.data.get((service, key))

    def delete_password(self, service, key):
        del self.data[(service, key)]


class TestSecureAudioBuffer(unittest.TestCase):
    def test_zeroized_on_context_exit(self):
        with SecureAudioBuffer(b"\x7f" * 1024) as buf:
            self.assertFalse(buf.is_zeroed())
            self.assertEqual(bytes(buf.view()[:2]), b"\x7f\x7f")
        self.assertTrue(buf.is_zeroed())
        self.assertTrue(buf.disposed)

    def test_zeroized_even_when_processing_raises(self):
        buf = SecureAudioBuffer(b"\x01" * 64)
        with self.assertRaises(RuntimeError):
            with buf:
                raise RuntimeError("asr failure")
        self.assertTrue(buf.is_zeroed())

    def test_view_after_disposal_is_rejected(self):
        buf = SecureAudioBuffer(b"abc")
        buf.zeroize()
        buf.zeroize()  # idempotent
        with self.assertRaises(ValueError):
            buf.view()

    def test_length_preserved_after_zeroize(self):
        buf = SecureAudioBuffer(b"\xff" * 10)
        buf.zeroize()
        self.assertEqual(len(buf), 10)


class TestCredentialStore(unittest.TestCase):
    def setUp(self):
        self.backend = FakeKeyring()
        self.store = CredentialStore(self.backend)

    def test_round_trip(self):
        self.store.set("spotify_token", "abc")
        self.assertEqual(self.store.get("spotify_token"), "abc")
        self.assertEqual(self.backend.data[("vamc", "spotify_token")], "abc")

    def test_delete_and_missing(self):
        self.store.set("k", "v")
        self.store.delete("k")
        self.assertIsNone(self.store.get("k"))
        self.store.delete("k")  # no error

    def test_empty_values_rejected(self):
        with self.assertRaises(ValueError):
            self.store.set("k", "")

    def test_no_plaintext_fallback_without_backend(self):
        try:
            import keyring  # noqa: F401
        except ImportError:
            with self.assertRaises(KeyringUnavailable):
                CredentialStore()


if __name__ == "__main__":
    unittest.main()
