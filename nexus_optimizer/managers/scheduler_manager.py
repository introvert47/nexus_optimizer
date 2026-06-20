import ctypes
from ctypes import wintypes
from core.bindings import user32, kernel32
from core.handles import SafeHandle

HIGH_PRIORITY_CLASS = 0x00000080
IDLE_PRIORITY_CLASS = 0x00000040

SYSTEM_CRITICAL_PROCESSES = {
    "csrss.exe", "wininit.exe", "services.exe", "lsass.exe", 
    "svchost.exe", "smss.exe", "dwm.exe", "system"
}

class SchedulerManager:
    def __init__(self, blacklist: set):
        self.blacklist = {name.lower() for name in blacklist}
        self.current_foreground_pid = 0

    def get_foreground_pid(self) -> int:
        hwnd = user32.GetForegroundWindow()
        pid = wintypes.DWORD()
        user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
        return pid.value

    def get_process_name(self, pid: int) -> str:
        PROCESS_QUERY_LIMITED_INFORMATION = 0x1000
        h_proc = kernel32.OpenProcess(PROCESS_QUERY_LIMITED_INFORMATION, False, pid)
        if not h_proc:
            return ""
        
        with SafeHandle(h_proc) as handle:
            buf = ctypes.create_unicode_buffer(260)
            size = wintypes.DWORD(260)
            if kernel32.QueryFullProcessImageNameW(handle, 0, buf, ctypes.byref(size)):
                return buf.value.split("\\")[-1].lower()
        return ""

    def optimize_priorities(self):
        fg_pid = self.get_foreground_pid()
        if not fg_pid or fg_pid == self.current_foreground_pid:
            return

        fg_name = self.get_process_name(fg_pid)
        if not fg_name or fg_name in SYSTEM_CRITICAL_PROCESSES:
            return

        print(f"[Focus Change] Focused on: {fg_name} (PID: {fg_pid})")
        self.current_foreground_pid = fg_pid

        if self._set_priority(fg_pid, HIGH_PRIORITY_CLASS):
            print(f"  [+] Boosted foreground process: {fg_name}")

        self._throttle_background_bloat(fg_pid)

    def _throttle_background_bloat(self, active_pid: int):
        TH32CS_SNAPPROCESS = 0x00000002
        
        class PROCESSENTRY32(ctypes.Structure):
            _fields_ = [
                ('dwSize', wintypes.DWORD), ('cntUsage', wintypes.DWORD),
                ('th32ProcessID', wintypes.DWORD), ('th32DefaultHeapID', ctypes.c_void_p),
                ('th32ModuleID', wintypes.DWORD), ('cntThreads', wintypes.DWORD),
                ('th32ParentProcessID', wintypes.DWORD), ('pcPriClassBase', wintypes.LONG),
                ('dwFlags', wintypes.DWORD), ('szExeFile', ctypes.c_wchar * 260)
            ]

        h_snapshot = kernel32.CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0)
        if h_snapshot == -1:
            return

        pe = PROCESSENTRY32()
        pe.dwSize = ctypes.sizeof(PROCESSENTRY32)

        if kernel32.Process32FirstW(h_snapshot, ctypes.byref(pe)):
            while True:
                exe_name = pe.szExeFile.lower()
                pid = pe.th32ProcessID

                if exe_name in self.blacklist and pid != active_pid:
                    if self._set_priority(pid, IDLE_PRIORITY_CLASS):
                        print(f"  [-] Throttled background bloatware: {exe_name} (PID: {pid})")

                if not kernel32.Process32NextW(h_snapshot, ctypes.byref(pe)):
                    break

        kernel32.CloseHandle(h_snapshot)

    def _set_priority(self, pid: int, priority: int) -> bool:
        PROCESS_SET_INFORMATION = 0x0200
        h_proc = kernel32.OpenProcess(PROCESS_SET_INFORMATION, False, pid)
        if not h_proc:
            return False
        
        with SafeHandle(h_proc) as handle:
            return bool(kernel32.SetPriorityClass(handle, priority))