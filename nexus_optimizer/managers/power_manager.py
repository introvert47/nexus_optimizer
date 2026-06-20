import ctypes
from ctypes import wintypes
from core.bindings import powrprof

GUID_HIGH_PERFORMANCE = "{8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c}"
GUID_ULTIMATE_PERFORMANCE = "{e9a42b02-d5df-448d-aa00-03f14749eb61}"
GUID_BALANCED = "{381b4222-f694-41f0-9685-ff5bb260df2e}"

# Windows GUID structure for API compatibility
class GUID(ctypes.Structure):
    _fields_ = [
        ("Data1", ctypes.c_ulong),
        ("Data2", ctypes.c_ushort),
        ("Data3", ctypes.c_ushort),
        ("Data4", ctypes.c_ubyte * 8)
    ]

class PowerManager:
    def __init__(self):
        self.active_scheme = None

    def get_active_scheme(self) -> str:
        p_guid = wintypes.LPWSTR()
        if powrprof.PowerGetActiveScheme(None, ctypes.byref(p_guid)) == 0:
            return p_guid.value
        return ""

    def set_power_scheme(self, guid_str: str) -> bool:
        """Converts a string GUID into a binary structure and applies the scheme."""
        import uuid
        try:
            # Parse the string GUID and extract its raw hex components
            hex_str = uuid.UUID(guid_str).hex
            g = GUID(
                int(hex_str[0:8], 16),
                int(hex_str[8:12], 16),
                int(hex_str[12:16], 16),
                (ctypes.c_ubyte * 8)(*[int(hex_str[i:i+2], 16) for i in range(16, 32, 2)])
            )
            status = powrprof.PowerSetActiveScheme(None, ctypes.byref(g))
            return status == 0
        except Exception:
            return False

    def evaluate_and_switch(self, running_executables: set):
        # Games or apps that trigger ultimate performance mode
        heavy_apps = {"minecraft.exe", "forzahorizon4.exe", "gta5.exe"}
        
        if running_executables.intersection(heavy_apps):
            target = GUID_ULTIMATE_PERFORMANCE
        else:
            target = GUID_BALANCED

        if self.get_active_scheme() != target:
            if not self.set_power_scheme(target) and target == GUID_ULTIMATE_PERFORMANCE:
                # Fall back to High Performance if Ultimate isn't unlocked on this system
                self.set_power_scheme(GUID_HIGH_PERFORMANCE)