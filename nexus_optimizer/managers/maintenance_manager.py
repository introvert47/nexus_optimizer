import os
import shutil
import subprocess

class MaintenanceManager:
    def __init__(self):
        self.temp_path = r"C:\Windows\Temp"
        self.user_temp_path = os.environ.get("TEMP")
        self.prefetch_path = r"C:\Windows\Prefetch"

    def _clear_folder(self, folder_path: str, name: str):
        print(f"\n[*] Cleaning {name} ({folder_path})...")
        if not os.path.exists(folder_path):
            print(f"[-] Directory not found: {folder_path}")
            return

        deleted_files = 0
        deleted_folders = 0

        for item in os.listdir(folder_path):
            item_path = os.path.join(folder_path, item)
            try:
                if os.path.isfile(item_path) or os.path.islink(item_path):
                    os.unlink(item_path)
                    deleted_files += 1
                elif os.path.isdir(item_path):
                    shutil.rmtree(item_path)
                    deleted_folders += 1
            except Exception:
                continue 

        print(f"[+] Cleaned up {deleted_files} files and {deleted_folders} folders.")

    def run_disk_cleanup(self):
        print("\n=========================================")
        print("         STARTING JUNK FILE PURGE        ")
        print("=========================================")
        self._clear_folder(self.temp_path, "System Temp")
        if self.user_temp_path:
            self._clear_folder(self.user_temp_path, "User %TEMP%")
        self._clear_folder(self.prefetch_path, "Prefetch")

    def run_system_scans(self):
        print("\n=========================================")
        print("         STARTING WINDOWS SYSTEM SCANS    ")
        print("=========================================")

        print("\n[*] Running DISM (Component Store Repair)...")
        subprocess.run(["dism.exe", "/Online", "/Cleanup-Image", "/RestoreHealth"])

        print("\n[*] Running SFC Scan (System File Repair)...")
        subprocess.run(["sfc.exe", "/scannow"])

        print("\n[*] Running Chkdsk (Volume Integrity Scan Analysis)...")
        print("[*] Note: This will run a quick read-only structural analysis.")
        subprocess.run(["chkdsk.exe", "C:"])