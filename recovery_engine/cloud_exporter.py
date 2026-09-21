"""
Cloud Storage Direct Exporter (AWS S3, Google Cloud Storage, Cloudflare R2)
Uploads extracted forensic evidence packages and disk images directly to Cloud Object Storage.
"""

import os
import mimetypes
import urllib.request
from typing import Tuple, Optional, Dict

def upload_file_to_presigned_url(file_path: str, presigned_url: str, http_method: str = "PUT") -> Tuple[bool, str]:
    """
    Upload a single evidence file or image to AWS S3 / GCS presigned URL.
    """
    if not os.path.isfile(file_path):
        return False, f"File '{file_path}' does not exist."

    try:
        file_size = os.path.getsize(file_path)
        content_type, _ = mimetypes.guess_type(file_path)
        content_type = content_type or "application/octet-stream"

        with open(file_path, "rb") as f:
            req = urllib.request.Request(
                presigned_url,
                data=f.read(),
                headers={
                    "Content-Type": content_type,
                    "Content-Length": str(file_size),
                    "User-Agent": "RecoveryEngine-CloudExporter/2.0"
                },
                method=http_method.upper()
            )
            with urllib.request.urlopen(req, timeout=120) as resp:
                if 200 <= resp.status < 300:
                    return True, f"Successfully uploaded {os.path.basename(file_path)} ({file_size / (1024*1024):.2f} MB)"
                return False, f"HTTP Status {resp.status}"
    except Exception as e:
        return False, str(e)

def upload_directory_to_cloud(dir_path: str, upload_url_map: Dict[str, str]) -> Tuple[int, int]:
    """
    Batch upload directory files using a map of relative_path -> presigned_url.
    Returns (success_count, fail_count).
    """
    success = 0
    fail = 0
    for rel_p, url in upload_url_map.items():
        full_p = os.path.join(dir_path, rel_p.lstrip("/"))
        ok, msg = upload_file_to_presigned_url(full_p, url)
        if ok:
            success += 1
        else:
            fail += 1
    return success, fail
