"""Tests for POSIX Memory Locking Wrapper."""
import unittest
from src.security.mlock import MemoryLock

class TestMemoryLock(unittest.TestCase):
    def test_lock_unlock_bytearray_does_not_crash(self):
        buf = bytearray(b"sensitive audio samples")
        MemoryLock.lock_memory(buf)
        MemoryLock.unlock_memory(buf)
        self.assertEqual(len(buf), len(b"sensitive audio samples"))

if __name__ == '__main__':
    unittest.main()
