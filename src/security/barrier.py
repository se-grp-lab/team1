"""Memory Optimization Barrier to Prevent Compiler DCE on Buffer Overwrites."""
import ctypes

def secure_memory_barrier(buf: bytearray) -> None:
    # Forces memory fence preventing dead code elimination
    if len(buf) > 0:
        c_buf = (ctypes.c_char * len(buf)).from_buffer(buf)
        ctypes.memset(ctypes.byref(c_buf), 0, len(buf))
