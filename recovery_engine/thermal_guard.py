"""
Real-Time Thermal Guard & Drive Auto-Throttle Module
Monitors storage drive temperature during long-running parallel scans.
Automatically cools down and pauses I/O if threshold is exceeded to protect HDD motors & heads.
"""

import time
import sys
from typing import Optional
from recovery_engine.smart_checker import run_smartctl

class ThermalGuard:
    def __init__(self, dev_path: str, max_temp_c: int = 55, check_interval_sec: int = 45):
        self.dev_path = dev_path
        self.max_temp_c = max_temp_c
        self.check_interval_sec = check_interval_sec
        self.last_check_time = 0.0
        self.last_temp: Optional[int] = None
        self.is_enabled = bool(dev_path and not dev_path.endswith((".img", ".raw", ".dd", ".iso")))

    def check_and_throttle_if_hot(self) -> bool:
        """
        Check drive temperature if interval elapsed.
        If hot, sleeps for cooldown period. Returns True if throttling occurred.
        """
        if not self.is_enabled:
            return False

        now = time.time()
        if now - self.last_check_time < self.check_interval_sec:
            return False

        self.last_check_time = now
        smart_data = run_smartctl(self.dev_path)
        if not smart_data or smart_data.get("temperature_c") is None:
            return False

        current_temp = smart_data["temperature_c"]
        self.last_temp = current_temp

        if current_temp >= self.max_temp_c:
            print(f"\n[⚠️ THERMAL GUARD ALERT] Drive temperature reached {current_temp}°C (Limit: {self.max_temp_c}°C)!")
            print(f"[*] Auto-throttling: Pausing I/O for 20 seconds to allow drive hardware to cool down...")
            for remaining in range(20, 0, -5):
                sys.stdout.write(f"\r  ❄️ Cooling down... {remaining}s remaining ")
                sys.stdout.flush()
                time.sleep(5)
            print("\n[*] Resuming recovery scan safely.\n")
            return True

        return False
