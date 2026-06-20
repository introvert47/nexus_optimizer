import ctypes
from ctypes import wintypes
from core.bindings import kernel32

class SafeHandle:
    def __init__(self, handle: int, owned: bool = True):
        self.handle = wintypes.HANDLE(handle)
        self.owned = owned

    def __enter__(self):
        return self.handle

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.owned and self.handle and self.handle != -1:
            kernel32.CloseHandle(self.handle)
        return False