"""OAuth2 Token Refresh Interceptor for Spotify Web API."""
import time
from typing import Optional, Dict

class OAuthTokenManager:
    def __init__(self, refresh_callback, ttl_buffer_seconds: int = 60):
        self._refresh_cb = refresh_callback
        self._token: Optional[str] = None
        self._expires_at: float = 0.0
        self._buffer = ttl_buffer_seconds

    def get_token(self) -> str:
        now = time.time()
        if self._token is None or (now >= self._expires_at - self._buffer):
            new_tok, expires_in = self._refresh_cb()
            self._token = new_tok
            self._expires_at = now + expires_in
        return self._token
