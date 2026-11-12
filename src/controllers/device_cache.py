"""Spotify Connect Active Device Cache."""
import time
from typing import Optional, List, Dict, Any

class SpotifyDeviceCache:
    def __init__(self, fetch_callback, cache_ttl_seconds: float = 5.0):
        self._fetch = fetch_callback
        self._ttl = cache_ttl_seconds
        self._cached: Optional[List[Dict[str, Any]]] = None
        self._last_time: float = 0.0

    def get_devices(self) -> List[Dict[str, Any]]:
        now = time.monotonic()
        if self._cached is None or (now - self._last_time > self._ttl):
            self._cached = self._fetch()
            self._last_time = now
        return self._cached
