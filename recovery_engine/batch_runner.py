"""
Multi-Device Batch Recovery & Concurrent Disk Imaging Orchestrator
Executes parallel recovery or bitstream cloning across multiple physical drives simultaneously.
"""

import os
import sys
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from typing import List, Dict, Set, Optional

from recovery_engine.scanner import recover_universal
from recovery_engine.disk_io import clone_disk_to_image

def worker_batch_disk(args_tuple: tuple) -> Dict:
    """
    Subprocess worker executing recovery on a specific individual drive.
    """
    dev_path, out_base_dir, enabled_types, cores_per_disk, auto_confirm, clone_mode = args_tuple
    dev_clean = os.path.basename(dev_path).replace("rdisk", "disk").replace("dev_", "")
    target_out = os.path.join(out_base_dir, f"recovery_{dev_clean}")
    os.makedirs(target_out, exist_ok=True)

    start_t = time.time()
    result = {"device": dev_path, "output_dir": target_out, "success": False, "duration": 0}

    try:
        if clone_mode:
            img_file = os.path.join(target_out, f"{dev_clean}_clone.img")
            clone_disk_to_image(dev_path, img_file)
            result["success"] = True
        else:
            recover_universal(
                source_device=dev_path,
                output_dir=target_out,
                enabled_types=enabled_types,
                num_workers=cores_per_disk,
                auto_confirm=auto_confirm
            )
            result["success"] = True
    except Exception as e:
        result["error"] = str(e)

    result["duration"] = time.time() - start_t
    return result

def run_batch_recovery(
    devices: List[str],
    output_base_dir: str,
    enabled_types: Set[str],
    max_concurrent_disks: int = 2,
    cores_per_disk: int = 4,
    clone_mode: bool = False
) -> List[Dict]:
    """
    Run concurrent recovery across multiple physical disks.
    """
    print("\n" + "=" * 80)
    print(f"⚡ BATCH DATA RECOVERY ORCHESTRATOR: {len(devices)} Target Drives")
    print(f"[*] Target Devices       : {', '.join(devices)}")
    print(f"[*] Base Output Folder   : {os.path.abspath(output_base_dir)}")
    print(f"[*] Max Concurrent Drives: {max_concurrent_disks} (Cores per disk: {cores_per_disk})")
    print("=" * 80 + "\n")

    tasks = [
        (dev.strip(), output_base_dir, enabled_types, cores_per_disk, True, clone_mode)
        for dev in devices if dev.strip()
    ]

    results = []
    with ProcessPoolExecutor(max_workers=max_concurrent_disks) as executor:
        futures = [executor.submit(worker_batch_disk, t) for t in tasks]
        for f in as_completed(futures):
            res = f.result()
            results.append(res)
            status_str = "SUCCESS" if res["success"] else f"FAILED ({res.get('error', 'unknown')})"
            print(f"[+] Finished batch task for {res['device']} -> [{status_str}] in {res['duration']:.1f}s")

    return results
