"""Tests for Spotify Device Caching."""
import unittest
from src.controllers.device_cache import SpotifyDeviceCache

class TestDeviceCache(unittest.TestCase):
    def test_cache_hit(self):
        calls = 0
        def fetch():
            nonlocal calls
            calls += 1
            return [{"id": "dev1", "name": "Desktop"}]
        cache = SpotifyDeviceCache(fetch, cache_ttl_seconds=10.0)
        self.assertEqual(len(cache.get_devices()), 1)
        self.assertEqual(len(cache.get_devices()), 1)
        self.assertEqual(calls, 1)

if __name__ == '__main__':
    unittest.main()
