"""
engine.py — Nexus Suite [Optimization Engine]
Monitors background systems, targets game execution threads natively,
and applies prioritized execution rules. Cleaned of old legacy imports.
"""

import time
import psutil

class OptimizationEngine:
    def __init__(self, bloatware_names=None):
        # Target game executables (Minecraft, Forza 4, GTA 5, and Java runtime)
        self.game_names = {"Minecraft.Windows.exe", "ForzaHorizon4.exe", "GTA5.exe", "javaw.exe"} 
        
        # Background applications to monitor if needed
        self.bloatware_names = bloatware_names if bloatware_names else {"chrome.exe", "msedge.exe", "discord.exe", "spotify.exe"}
        self.is_running = False

    def start(self):
        """Starts the real-time background tracking process loop."""
        self.is_running = True
        game_was_running = False

        while self.is_running:
            game_found = False
            
            # Scan active system processes running on Windows
            for proc in psutil.process_iter(['pid', 'name']):
                try:
                    if proc.info['name'] in self.game_names:
                        game_found = True
                        
                        # Apply High Priority to the game if it hasn't been applied yet
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

            time.sleep(2) # Checks every 2 seconds to keep CPU usage close to 0%

    def stop(self):
        """Stops the engine process monitoring flags."""
        self.is_running = False
