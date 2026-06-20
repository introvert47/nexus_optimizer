import ctypes
from ctypes import wintypes
from core.bindings import kernel32, advapi32

TOKEN_ADJUST_PRIVILEGES = 0x0020
TOKEN_QUERY = 0x0008
SE_PRIVILEGE_ENABLED = 0x00000002

class LUID(ctypes.Structure):
    _fields_ = [("LowPart", wintypes.DWORD), ("HighPart", wintypes.LONG)]

class TOKEN_PRIVILEGES(ctypes.Structure):
    _fields_ = [
        ("PrivilegeCount", wintypes.DWORD),
        ("Luid", LUID),
        ("Attributes", wintypes.DWORD)
    ]

def enable_privilege(privilege_name: str) -> bool:
    h_token = wintypes.HANDLE()
    if not advapi32.OpenProcessToken(kernel32.GetCurrentProcess(), TOKEN_ADJUST_PRIVILEGES | TOKEN_QUERY, ctypes.byref(h_token)):
        return False

    luid = LUID()
    if not advapi32.LookupPrivilegeValueW(None, privilege_name, ctypes.byref(luid)):
        kernel32.CloseHandle(h_token)
        return False

    tp = TOKEN_PRIVILEGES()
    tp.PrivilegeCount = 1
    tp.Luid = luid
    tp.Attributes = SE_PRIVILEGE_ENABLED

    size = ctypes.sizeof(TOKEN_PRIVILEGES) 
    advapi32.AdjustTokenPrivileges(h_token, False, ctypes.byref(tp), size, None, None)
    
    error = kernel32.GetLastError()
    kernel32.CloseHandle(h_token)
    return error == 0