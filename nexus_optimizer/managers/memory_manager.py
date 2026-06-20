import ctypes
from ctypes import wintypes
from core.bindings import psapi, ntdll, kernel32
from core.handles import SafeHandle
from core.privileges import enable_privilege

SystemMemoryListInformation = 0x50
MemoryPurgeStandbyList = 0x2

class MemoryManager:
    def __init__(self):
        enable_privilege("SeIncreaseQuotaPrivilege") 

    def empty_process_working_set(self, pid: int) -> bool:
        PROCESS_QUERY_LIMITED_INFORMATION = 0x1000
        PROCESS_SET_QUOTA = 0x0100

        h_proc = kernel32.OpenProcess(PROCESS_QUERY_LIMITED_INFORMATION | PROCESS_SET_QUOTA, False, pid)
        if not h_proc:
            return False

        with SafeHandle(h_proc) as handle:
            return bool(psapi.EmptyWorkingSet(handle))

    def clear_system_standby_list(self) -> bool:
        if not enable_privilege("SeDebugPrivilege"):
            return False

        command = wintypes.ULONG(MemoryPurgeStandbyList)
        status = ntdll.NtSetSystemInformation(
            SystemMemoryListInformation,
            ctypes.byref(command),
            ctypes.sizeof(command)
        )
        return status == 0