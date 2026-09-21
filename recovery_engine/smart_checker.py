"""
Pre-Scan S.M.A.R.T. Health Diagnostics Module
Inspects physical drive health, SMART attributes, temperature, and calculates failure risk score
before scanning or stressing the storage media.
"""

import os
import sys
import shutil
import subprocess
import plistlib
import re
from typing import Dict, Any, Optional

def get_diskutil_smart_status(dev_path: str) -> Dict[str, Any]:
    """
    Get basic macOS SMART status and media information via diskutil.
    """
    info = {
        "smart_status": "Unknown",
        "protocol": "",
        "device_model": "",
        "is_ssd": False,
        "is_internal": False,
    }
    if sys.platform != "darwin":
        return info

    try:
        # Standardize /dev/rdiskX to diskX
        base_node = os.path.basename(dev_path).replace("rdisk", "disk")
        cmd = ["diskutil", "info", "-plist", base_node]
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=False)
        if res.returncode == 0:
            plist = plistlib.loads(res.stdout)
            info["smart_status"] = plist.get("SMARTStatus", "Not Supported")
            info["protocol"] = plist.get("BusProtocol", "")
            info["device_model"] = plist.get("MediaName", "") or plist.get("DeviceModel", "")
            info["is_ssd"] = bool(plist.get("SolidState", False))
            info["is_internal"] = bool(plist.get("Internal", False))
    except Exception:
        pass

    return info

def run_smartctl(dev_path: str) -> Optional[Dict[str, Any]]:
    """
    Query smartctl (from smartmontools) if installed on the host.
    """
    smartctl = shutil.which("smartctl") or "/opt/homebrew/bin/smartctl" or "/usr/local/bin/smartctl"
    if not smartctl or not os.path.exists(smartctl):
        return None

    try:
        # Clean path for smartctl
        node = dev_path
        if sys.platform == "darwin" and node.startswith("/dev/rdisk"):
            node = node.replace("/dev/rdisk", "/dev/disk")

        cmd = [smartctl, "-a", node]
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
        out = res.stdout

        result = {
            "passed": None,
            "reallocated_sectors": 0,
            "pending_sectors": 0,
            "uncorrectable_sectors": 0,
            "crc_errors": 0,
            "temperature_c": None,
            "power_on_hours": None,
            "model_family": "",
            "raw_output": out
        }

        if "SMART overall-health self-assessment test result: PASSED" in out or "SMART Health Status: OK" in out:
            result["passed"] = True
        elif "SMART overall-health self-assessment test result: FAILED" in out or "SMART Health Status: BAD" in out:
            result["passed"] = False

        # Parse SMART attributes table
        for line in out.splitlines():
            line_s = line.strip()
            # Temperature
            if "Temperature_Celsius" in line_s or "Airflow_Temperature" in line_s or "Temperature:" in line_s:
                nums = re.findall(r"\b\d+\b", line_s)
                if nums:
                    result["temperature_c"] = int(nums[-1])
            # Reallocated Sectors (ID 05)
            elif "Reallocated_Sector_Ct" in line_s or "Reallocated_Event_Count" in line_s:
                nums = re.findall(r"\b\d+\b", line_s)
                if nums:
                    result["reallocated_sectors"] = int(nums[-1])
            # Current Pending Sectors (ID 197 / C5)
            elif "Current_Pending_Sector" in line_s:
                nums = re.findall(r"\b\d+\b", line_s)
                if nums:
                    result["pending_sectors"] = int(nums[-1])
            # Offline Uncorrectable (ID 198 / C6)
            elif "Offline_Uncorrectable" in line_s:
                nums = re.findall(r"\b\d+\b", line_s)
                if nums:
                    result["uncorrectable_sectors"] = int(nums[-1])
            # UltraDMA CRC Errors (ID 199)
            elif "UDMA_CRC_Error_Count" in line_s:
                nums = re.findall(r"\b\d+\b", line_s)
                if nums:
                    result["crc_errors"] = int(nums[-1])
            # Power On Hours (ID 09)
            elif "Power_On_Hours" in line_s:
                nums = re.findall(r"\b\d+\b", line_s)
                if nums:
                    result["power_on_hours"] = int(nums[-1])
            elif "Device Model:" in line_s or "Model Family:" in line_s:
                result["model_family"] = line_s.split(":", 1)[-1].strip()

        return result
    except Exception:
        return None

def evaluate_disk_health(dev_path: str) -> Dict[str, Any]:
    """
    Comprehensive drive health evaluation.
    Calculates overall health score (0-100%) and generates safety advice.
    """
    smart_data = run_smartctl(dev_path)
    diskutil_data = get_diskutil_smart_status(dev_path)

    health_score = 100
    risk_level = "LOW"
    status_label = "HEALTHY"
    recommendations = []

    # If full smartctl telemetry is available
    if smart_data:
        if smart_data.get("passed") is False:
            health_score -= 60
            status_label = "FAILING"
            risk_level = "CRITICAL"
            recommendations.append("SMART self-test has FAILED! Drive hardware is degraded.")

        pending = smart_data.get("pending_sectors", 0)
        reallocated = smart_data.get("reallocated_sectors", 0)
        uncorrectable = smart_data.get("uncorrectable_sectors", 0)

        if pending > 0:
            health_score -= min(40, pending * 5)
            recommendations.append(f"Found {pending} UNSTABLE pending sectors. Read errors expected.")
        if reallocated > 0:
            health_score -= min(30, reallocated * 2)
            recommendations.append(f"Found {reallocated} REALLOCATED bad sectors (Disk surface damage).")
        if uncorrectable > 0:
            health_score -= min(40, uncorrectable * 5)
            recommendations.append(f"Found {uncorrectable} UNCORRECTABLE sectors.")

        temp = smart_data.get("temperature_c")
        if temp and temp > 55:
            health_score -= 10
            recommendations.append(f"Drive temperature is HIGH ({temp}°C). Provide active cooling.")

    elif diskutil_data:
        st = diskutil_data.get("smart_status", "").lower()
        if st in ("verified", "ok"):
            health_score = 100
            status_label = "HEALTHY (Verified)"
        elif st in ("failing", "about to fail", "bad"):
            health_score = 25
            status_label = "CRITICAL FAILING"
            risk_level = "CRITICAL"
            recommendations.append("macOS reports disk SMART status as FAILING!")
        else:
            status_label = f"SMART {diskutil_data.get('smart_status', 'Unknown')}"
            health_score = 95

    # Final scoring clamp
    health_score = max(0, min(100, health_score))

    if health_score < 50:
        risk_level = "CRITICAL"
        recommendations.append("🚨 HIGH RISK OF HEAD CRASH: CLONE TO IMAGE FILE IMMEDIATELY BEFORE SCANNING!")
    elif health_score < 80:
        risk_level = "MODERATE"
        recommendations.append("Drive shows warning signs. Avoid heavy stress.")
    else:
        recommendations.append("Drive appears healthy for direct recovery scan.")

    return {
        "device": dev_path,
        "health_score": health_score,
        "risk_level": risk_level,
        "status_label": status_label,
        "smartctl_data": smart_data,
        "diskutil_data": diskutil_data,
        "recommendations": recommendations,
    }

def print_health_report(eval_res: Dict[str, Any]):
    """Print ASCII S.M.A.R.T. Health Diagnostic Report."""
    score = eval_res["health_score"]
    risk = eval_res["risk_level"]
    status = eval_res["status_label"]
    dev = eval_res["device"]

    print("\n" + "=" * 80)
    print("🩺 S.M.A.R.T. DRIVE HEALTH DIAGNOSTIC REPORT")
    print("=" * 80)
    print(f"Target Device          : {dev}")
    print(f"Health Condition       : {status} (Score: {score}/100)")
    print(f"Risk Assessment        : [{risk}]")

    sm = eval_res.get("smartctl_data")
    if sm:
        print(f"Reallocated Sectors    : {sm.get('reallocated_sectors', 0)}")
        print(f"Pending Weak Sectors   : {sm.get('pending_sectors', 0)}")
        print(f"Uncorrectable Sectors  : {sm.get('uncorrectable_sectors', 0)}")
        if sm.get("temperature_c"):
            print(f"Drive Temperature      : {sm.get('temperature_c')}°C")
        if sm.get("power_on_hours"):
            print(f"Power-On Hours         : {sm.get('power_on_hours')} hrs (~{sm.get('power_on_hours') // 24} days)")

    print("-" * 80)
    print("📋 Diagnostic Recommendations:")
    for rec in eval_res["recommendations"]:
        print(f"  • {rec}")
    print("=" * 80 + "\n")
