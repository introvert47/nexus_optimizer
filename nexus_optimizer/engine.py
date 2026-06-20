import time
import psutil

class OptimizationEngine:
    def __init__(self, bloatware_names=None):
        # Default games list (Minecraft, Forza 4, GTA 5, and Java for Minecraft Java Edition)
        self.game_names = {"Minecraft.Windows.exe", "ForzaHorizon4.exe", "GTA5.exe", "javaw.exe"} 
        self.bloatware_names = bloatware_names if bloatware_names else {"chrome.exe", "msedge.exe", "discord.exe", "spotify.exe"}
        self.is_running = False

    def start(self):
        self.is_running = True
        game_was_running = False

        while self.is_running:
            game_found = False
            
            # Scan active system processes
            for proc in psutil.process_iter(['pid', 'name']):
                try:
                    if proc.info['name'] in self.game_names:
                        game_found = True
                        
                        # Set to HIGH priority if it wasn't boosted already
                        if not game_was_running:
                            proc.set_priority(psutil.HIGH_PRIORITY_CLASS)
                            game_was_running = True
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue

            # If the game was running but closed down, turn off the engine safely
            if game_was_running and not game_found:
                try:
                    self.stop() 
                except Exception:
                    pass
                self.is_running = False 
                break

            time.sleep(2) 

    def stop(self):
        self.is_running = False
