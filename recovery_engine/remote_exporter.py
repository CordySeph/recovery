"""
Remote Target Streaming & Network NAS Exporter Module
Supports copying / streaming recovered files directly to Network Shares (SMB/NFS)
or SFTP / Cloud targets when local disk storage is constrained.
"""

import os
import shutil
import subprocess
from typing import Tuple, Optional

def validate_destination_target(dest_path: str) -> Tuple[bool, str, float]:
    """
    Validate if target destination is writable and returns (is_valid, msg, free_gb).
    """
    if not dest_path:
        return False, "Destination path is empty", 0.0

    try:
        os.makedirs(dest_path, exist_ok=True)
        # Check free space
        st = shutil.disk_usage(dest_path)
        free_gb = st.free / (1024 ** 3)
        return True, "Destination ready and writable", free_gb
    except Exception as e:
        return False, f"Cannot write to destination: {e}", 0.0

def sync_to_remote_sftp(local_dir: str, sftp_url: str) -> Tuple[bool, str]:
    """
    Sync recovered files to remote host via rsync / scp if URL format is user@host:path.
    """
    rsync = shutil.which("rsync")
    if not rsync:
        return False, "rsync tool not found on system"

    try:
        cmd = [rsync, "-avzP", "--delete", f"{local_dir.rstrip('/')}/", sftp_url]
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if res.returncode == 0:
            return True, "Sync completed successfully"
        else:
            return False, f"rsync failed: {res.stderr.strip()}"
    except Exception as e:
        return False, f"Error running rsync: {e}"
