"""Operating System Memory Page Locking (mlock) Wrapper."""
import ctypes
import os

class MemoryLock:
    @staticmethod
    def lock_memory(buf: bytearray) -> bool:
        try:
            # POSIX mlock syscall
            libc = ctypes.CDLL(None)
            addr = (ctypes.c_char * len(buf)).from_buffer(buf)
            res = libc.mlock(ctypes.byref(addr), ctypes.c_size_t(len(buf)))
            return res == 0
        except Exception:
            return False

    @staticmethod
    def unlock_memory(buf: bytearray) -> bool:
        try:
            libc = ctypes.CDLL(None)
            addr = (ctypes.c_char * len(buf)).from_buffer(buf)
            res = libc.munlock(ctypes.byref(addr), ctypes.c_size_t(len(buf)))
            return res == 0
        except Exception:
            return False
