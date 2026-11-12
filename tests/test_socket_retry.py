"""Tests for Socket Reconnection Backoff."""
import unittest
from src.controllers.retry import retry_socket_call

class TestSocketRetry(unittest.TestCase):
    def test_immediate_success(self):
        res = retry_socket_call(lambda: "connected")
        self.assertEqual(res, "connected")

    def test_success_after_retries(self):
        attempts = 0
        def flaky():
            nonlocal attempts
            attempts += 1
            if attempts < 2:
                raise ConnectionRefusedError("Socket not ready")
            return "recovered"
        res = retry_socket_call(flaky, max_attempts=3)
        self.assertEqual(res, "recovered")
        self.assertEqual(attempts, 2)

    def test_exhaustion_raises(self):
        def failing():
            raise FileNotFoundError("Socket file missing")
        with self.assertRaises(FileNotFoundError):
            retry_socket_call(failing, max_attempts=2)

if __name__ == '__main__':
    unittest.main()
