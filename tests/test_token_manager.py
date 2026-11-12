"""Tests for OAuth Token Refresh Interceptor."""
import unittest
from src.controllers.token_manager import OAuthTokenManager

class TestOAuthTokenManager(unittest.TestCase):
    def test_fetches_token_on_initial_call(self):
        mgr = OAuthTokenManager(lambda: ("initial_token", 3600))
        self.assertEqual(mgr.get_token(), "initial_token")

    def test_reuses_token_within_lifetime(self):
        calls = 0
        def refresh():
            nonlocal calls
            calls += 1
            return (f"token_{calls}", 3600)
        mgr = OAuthTokenManager(refresh)
        self.assertEqual(mgr.get_token(), "token_1")
        self.assertEqual(mgr.get_token(), "token_1")
        self.assertEqual(calls, 1)

if __name__ == '__main__':
    unittest.main()
