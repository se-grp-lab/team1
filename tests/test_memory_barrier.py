"""Tests for Memory Barrier Overwrites."""
import unittest
from src.security.barrier import secure_memory_barrier

class TestMemoryBarrier(unittest.TestCase):
    def test_buffer_wiped_to_zeros(self):
        buf = bytearray(b"highly sensitive audio tensor data")
        secure_memory_barrier(buf)
        self.assertEqual(set(buf), {0})

if __name__ == '__main__':
    unittest.main()
