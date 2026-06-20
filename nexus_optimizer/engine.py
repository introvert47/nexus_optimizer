import time
from managers.memory_manager import MemoryManager
from managers.scheduler_manager import SchedulerManager
from managers.power_manager import PowerManager

class OptimizationEngine:
    def __init__(self, bloatware_names: set):
        self.memory_mgr = MemoryManager()
        self.scheduler_mgr = SchedulerManager(blacklist=bloatware_names)
        self.power_mgr = PowerManager()
        self.running = False

    def start(self, interval: float = 2.0):
        print("[+] Optimization Engine Started Successfully.")
        self.running = True
        
        try:
            while self.running:
                self.scheduler_mgr.optimize_priorities()
                
                fg_pid = self.scheduler_mgr.get_foreground_pid()
                fg_name = self.scheduler_mgr.get_process_name(fg_pid)
                
                if fg_name:
                    self.power_mgr.evaluate_and_switch({fg_name})
                
                time.sleep(interval)
                
        except KeyboardInterrupt:
            self.stop()

    def stop(self):
        print("[-] Stopping Optimization Engine...")
        self.running = False