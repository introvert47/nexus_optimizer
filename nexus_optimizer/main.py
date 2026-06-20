"""
main.py — Nexus Suite [Persistent Terminal Edition]
Fixed the missing 'bloatware_names' argument error for the detached engine process.
"""

import os
import sys
import time
import platform
import subprocess

# Import your existing backend services
from engine import OptimizationEngine
from managers.maintenance_manager import MaintenanceManager

def clear_screen():
    """Clears the terminal screen for a clean look."""
    os.system('cls' if os.name == 'nt' else 'clear')

def show_header():
    """Prints the system information header."""
    print("=" * 50)
    print("                NEXUS SUITE v1.0                 ")
    print("               [Terminal Edition]                ")
    print("=" * 50)
    
    cpu = platform.processor() or "Generic Processor"
    if "Intel" in cpu: cpu = "Intel Core CPU"
    elif "AMD" in cpu: cpu = "AMD Ryzen CPU"
    print(f" OS     : {platform.system()} {platform.release()}")
    print(f" TARGET : {cpu}")
    print("-" * 50)

def launch_detached_booster():
    """Launches engine.py as a completely detached background process with arguments."""
    # This string explicitly defines the bloatware set and passes it into the engine
    script_content = (
        "from engine import OptimizationEngine\n"
        "bloats = {'chrome.exe', 'msedge.exe', 'discord.exe', 'spotify.exe'}\n"
        "engine = OptimizationEngine(bloatware_names=bloats)\n"
        "try:\n"
        "    engine.start()\n"
        "except Exception:\n"
        "    pass"
    )
    
    # Windows constant to detach a process from the parent terminal console
    DETACHED_PROCESS = 0x00000008
    
    try:
        subprocess.Popen(
            [sys.executable, "-c", script_content],
            creationflags=DETACHED_PROCESS,
            close_fds=True
        )
        return True
    except Exception as e:
        print(f"[X] Failed to launch background worker: {e}")
        return False

def main():
    # Setup maintenance service
    maintenance = MaintenanceManager()

    while True:
        clear_screen()
        show_header()
        print(" 1 ➔ Launch Gaming Booster Engine (Stays alive if closed)")
        print(" 2 ➔ Purge Storage Cache Clusters")
        print(" 3 ➔ Run Integrity Diagnostics Scans (SFC)")
        print(" 4 ➔ Close Nexus Suite Menu")
        print("=" * 50)
        
        choice = input("Choose an option (1-4): ").strip()
        
        if choice == "1":
            print("\n[*] Detaching performance engine from terminal hooks...")
            if launch_detached_booster():
                print("[🚀] Real-time engine engaged independently in the background!")
                print("[+] You can safely close this terminal window now; your game will stay optimized!")
            time.sleep(3.5)
            
        elif choice == "2":
            print("\n[*] Initiating storage cache purge...")
            try:
                maintenance.run_disk_cleanup()
                print("[+] Drive space directory cache optimization finalized!")
            except Exception as e:
                print(f"[X] Cleanup failed: {e}")
            input("\nPress Enter to return to menu...")
            
        elif choice == "3":
            print("\n[*] Starting structural health diagnostic scans...")
            try:
                maintenance.run_system_scans()
                print("[+] Diagnostic volume parameters validated successfully!")
            except Exception as e:
                print(f"[X] Scan failed: {e}")
            input("\nPress Enter to return to menu...")
            
        elif choice == "4":
            clear_screen()
            print("\nExiting Nexus Suite menu. Goodbye!\n")
            sys.exit(0)
            
        else:
            print("\n[X] Invalid choice! Please enter 1, 2, 3, or 4.")
            time.sleep(1.5)

if __name__ == "__main__":
    main()