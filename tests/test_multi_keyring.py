"""Tests for Multi-Backend Keyring Adapter."""
import unittest
from src.security.multi_keyring import MultiBackendKeyring

class TestMultiBackendKeyring(unittest.TestCase):
    def test_backend_name_non_empty(self):
        name = MultiBackendKeyring.get_active_backend_name()
        self.assertIsInstance(name, str)
        self.assertGreater(len(name), 0)

    def test_secure_storage_availability(self):
        self.assertTrue(MultiBackendKeyring.is_secure_storage_available())

if __name__ == '__main__':
    unittest.main()
