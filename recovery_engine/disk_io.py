"""
Disk I/O Operations, Hardware Drive Discovery, Bad-Sector Fault-Tolerant Reader & Cloning
"""

import sys
import os
import subprocess
import shutil
import time
import hashlib
from typing import List, Dict, Tuple, Optional
from recovery_engine.config import CHUNK_SIZE, SECTOR_SIZE
from recovery_engine.i18n import t

def get_available_drives(include_virtual: bool = False) -> List[Dict]:
    """
    Detect available physical drives on macOS or Linux.
    Returns a list of dicts with disk details.
    """
    drives = []
    if sys.platform == "darwin":
        try:
            import plistlib
            plist_data = subprocess.check_output(["diskutil", "list", "-plist"], stderr=subprocess.DEVNULL)
            parsed = plistlib.loads(plist_data)
            whole_disks = parsed.get("WholeDisks", [])
            for disk_id in whole_disks:
                try:
                    info_plist = subprocess.check_output(["diskutil", "info", "-plist", disk_id], stderr=subprocess.DEVNULL)
                    info = plistlib.loads(info_plist)
                    
                    is_virtual = (info.get("VirtualOrPhysical") == "Virtual") or (info.get("APFSPhysicalStores") is not None)
                    if is_virtual and not include_virtual:
                        continue
                        
                    size_bytes = info.get("TotalSize", 0) or info.get("Size", 0)
                    size_gb = size_bytes / (1024 ** 3)
                    name = info.get("MediaName") or info.get("IORegistryEntryName") or "Storage Device"
                    is_internal = info.get("Internal", False)
                    is_removable = info.get("RemovableMediaOrExternalDevice", False) or info.get("Ejectable", False)
                    protocol = info.get("BusProtocol", "")
                    
                    raw_node = f"/dev/r{disk_id}"
                    node = f"/dev/{disk_id}"
                    
                    drives.append({
                        "id": disk_id,
                        "node": node,
                        "raw_node": raw_node,
                        "size_gb": size_gb,
                        "size_bytes": size_bytes,
                        "name": name,
                        "is_internal": is_internal,
                        "is_removable": is_removable,
                        "protocol": protocol,
                    })
                except Exception:
                    pass
        except Exception:
            pass
    elif sys.platform.startswith("linux"):
        try:
            import json
            lsblk_data = subprocess.check_output(
                ["lsblk", "-J", "-b", "-o", "NAME,SIZE,TYPE,MODEL,TRAN,RM"], 
                stderr=subprocess.DEVNULL
            )
            parsed = json.loads(lsblk_data.decode("utf-8"))
            for dev in parsed.get("blockdevices", []):
                if dev.get("type") == "disk":
                    size_bytes = int(dev.get("size", 0))
                    size_gb = size_bytes / (1024 ** 3)
                    drives.append({
                        "id": dev.get("name"),
                        "node": f"/dev/{dev.get('name')}",
                        "raw_node": f"/dev/{dev.get('name')}",
                        "size_gb": size_gb,
                        "size_bytes": size_bytes,
                        "name": (dev.get("model") or "Disk").strip(),
                        "is_internal": not bool(dev.get("rm")),
                        "is_removable": bool(dev.get("rm")),
                        "protocol": dev.get("tran") or "",
                    })
        except Exception:
            pass

    # Sort so external/removable drives appear first
    drives.sort(key=lambda d: (not d["is_removable"], d["is_internal"], d["id"]))
    return drives

def get_device_size(device_path: str) -> int:
    """
    Get the total size of a block device or file in bytes.
    """
    if os.path.isfile(device_path):
        return os.path.getsize(device_path)
    
    # 1. macOS diskutil info query
    if sys.platform == "darwin":
        try:
            import plistlib
            disk_id = os.path.basename(device_path).lstrip("r")
            plist_data = subprocess.check_output(["diskutil", "info", "-plist", disk_id], stderr=subprocess.DEVNULL)
            parsed = plistlib.loads(plist_data)
            size = parsed.get("TotalSize", 0) or parsed.get("Size", 0)
            if size > 0:
                return size
        except Exception:
            pass

    # 2. Linux blockdev / lsblk query
    elif sys.platform.startswith("linux"):
        try:
            out = subprocess.check_output(["blockdev", "--getsize64", device_path], stderr=subprocess.DEVNULL)
            size = int(out.strip())
            if size > 0:
                return size
        except Exception:
            pass

    # 3. Try seek to end
    try:
        with open(device_path, "rb") as dev:
            dev.seek(0, os.SEEK_END)
            s = dev.tell()
            if s > 0:
                return s
    except Exception:
        pass
    
    # 4. Platform-specific ioctl fallbacks
    if sys.platform == "darwin":
        try:
            import fcntl
            import struct
            with open(device_path, "rb") as fd:
                buf = bytearray(8)
                fcntl.ioctl(fd.fileno(), 0x40086419, buf)
                block_count = struct.unpack("Q", buf)[0]
                buf4 = bytearray(4)
                fcntl.ioctl(fd.fileno(), 0x40046418, buf4)
                block_size = struct.unpack("I", buf4)[0]
                if block_count * block_size > 0:
                    return block_count * block_size
        except Exception:
            pass
    elif sys.platform.startswith("linux"):
        try:
            import fcntl
            import struct
            with open(device_path, "rb") as fd:
                buf = bytearray(8)
                fcntl.ioctl(fd.fileno(), 0x80081272, buf)
                return struct.unpack("Q", buf)[0]
        except Exception:
            pass
            
    return 0

def format_eta(seconds: float) -> str:
    """Format seconds into human readable ETA (e.g. '01h 25m 30s' or '45s')."""
    if seconds is None or seconds < 0 or seconds > 86400 * 30:
        return "--:--"
    sec = int(seconds)
    hours = sec // 3600
    minutes = (sec % 3600) // 60
    secs = sec % 60
    if hours > 0:
        return f"{hours:02d}h {minutes:02d}m {secs:02d}s"
    elif minutes > 0:
        return f"{minutes:02d}m {secs:02d}s"
    else:
        return f"{secs:02d}s"

def check_write_block_status(device_path: str) -> Dict:
    """
    Forensic Verification: Check whether device is operating under read-only / write-blocked conditions.
    """
    info = {
        "device": device_path,
        "is_read_only": False,
        "mode": "Software Read-Only Mode (Enforced via 'rb')",
        "forensic_safe": True
    }
    if sys.platform == "darwin" and "/dev/" in device_path:
        try:
            disk_id = os.path.basename(device_path).lstrip("r")
            out = subprocess.check_output(["diskutil", "info", "-plist", disk_id], stderr=subprocess.DEVNULL)
            import plistlib
            parsed = plistlib.loads(out)
            if parsed.get("Read-Only Media", False) or parsed.get("Writable") is False:
                info["is_read_only"] = True
                info["mode"] = "Hardware / Kernel Write-Protected"
        except Exception:
            pass
    elif sys.platform.startswith("linux") and "/dev/" in device_path:
        try:
            dev_name = os.path.basename(device_path)
            ro_file = f"/sys/block/{dev_name}/ro"
            if os.path.exists(ro_file):
                with open(ro_file, "r") as f:
                    if f.read().strip() == "1":
                        info["is_read_only"] = True
                        info["mode"] = "Linux Kernel Block Device Read-Only (RO=1)"
        except Exception:
            pass
    return info

class ResilientDiskReader:
    """
    Fault-Tolerant Disk Reader with automatic Bad Sector detection & fallback recovery.
    When a large read chunk fails due to I/O error, it switches to granular sector reads,
    fills damaged sectors with null bytes, logs the bad sectors, and continues seamlessly.
    """
    def __init__(self, device_path: str, log_dir: Optional[str] = None):
        self.device_path = device_path
        self.log_dir = log_dir or "."
        self.bad_sectors: List[int] = []
        self.bad_sector_log_file = os.path.join(self.log_dir, "bad_sectors_map.log")
        self.total_bad_bytes = 0

    def read_chunk_safe(self, fd, offset: int, size: int) -> Tuple[bytes, int]:
        """
        Safely read a chunk of bytes. If I/O error occurs, fallback to sector-by-sector read.
        Returns (chunk_bytes, actual_read_length).
        """
        try:
            fd.seek(offset)
            data = fd.read(size)
            return data, len(data)
        except OSError as e:
            # Bad sector encountered! Fallback to sector-by-sector recovery
            print(t("bad_sector_detected", offset_hex=f"0x{offset:010X}"))
            recovered_chunks = []
            current_pos = offset
            bytes_to_read = size
            sector_size = 4096  # 4KB block retry

            while bytes_to_read > 0:
                read_len = min(sector_size, bytes_to_read)
                try:
                    fd.seek(current_pos)
                    sec_data = fd.read(read_len)
                    if not sec_data:
                        break
                    recovered_chunks.append(sec_data)
                except OSError:
                    # Mark bad sector, pad with zeros
                    self.bad_sectors.append(current_pos)
                    self.total_bad_bytes += read_len
                    recovered_chunks.append(b"\x00" * read_len)
                    self._log_bad_sector(current_pos, read_len)
                
                current_pos += read_len
                bytes_to_read -= read_len

            assembled = b"".join(recovered_chunks)
            return assembled, len(assembled)

    def _log_bad_sector(self, offset: int, length: int):
        """Append bad sector entry to log file."""
        try:
            with open(self.bad_sector_log_file, "a", encoding="utf-8") as f:
                f.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] BAD_SECTOR Offset: 0x{offset:012X} ({offset} bytes) Size: {length} bytes\n")
        except Exception:
            pass

def clone_disk_to_image(source_device: str, output_image_path: str, chunk_size: int = 16 * 1024 * 1024):
    """
    Bit-by-Bit RAW Disk Cloning to .img file with SHA-256 Hash and Live Progress/ETA.
    """
    print("\n" + "=" * 80)
    print(t("clone_title"))
    print("=" * 80)
    print(f"{t('clone_source')}{source_device}")
    print(f"{t('clone_dest')}{os.path.abspath(output_image_path)}")
    print("=" * 80 + "\n")

    total_size = get_device_size(source_device)
    total_gb = total_size / (1024 ** 3) if total_size else 0

    reader = ResilientDiskReader(source_device, log_dir=os.path.dirname(output_image_path) or ".")
    sha256 = hashlib.sha256()

    start_time = time.time()
    copied_bytes = 0

    with open(source_device, "rb") as src, open(output_image_path, "wb") as dst:
        while True:
            chunk, read_len = reader.read_chunk_safe(src, copied_bytes, chunk_size)
            if not chunk or read_len == 0:
                break
            
            dst.write(chunk)
            sha256.update(chunk)
            copied_bytes += read_len

            elapsed = time.time() - start_time
            speed_mb = (copied_bytes / (1024 * 1024)) / elapsed if elapsed > 0 else 0
            
            progress_str = f"{copied_bytes / (1024**3):.2f} GB"
            if total_size > 0:
                pct = (copied_bytes / total_size) * 100
                rem_bytes = max(0, total_size - copied_bytes)
                eta_sec = rem_bytes / (speed_mb * 1024 * 1024) if speed_mb > 0 else 0
                eta_str = format_eta(eta_sec)
                sys.stdout.write(
                    f"\r[🛡️] {t('clone_progress')}: {progress_str} / {total_gb:.2f} GB ({pct:5.1f}%) | "
                    f"{t('speed')}: {speed_mb:5.1f} MB/s | {t('clone_rem_time')}: {eta_str} "
                )
            else:
                sys.stdout.write(f"\r[🛡️] {t('clone_progress')}: {progress_str} | {t('speed')}: {speed_mb:5.1f} MB/s ")
            sys.stdout.flush()

    total_time = time.time() - start_time
    digest = sha256.hexdigest()

    print("\n\n" + "=" * 80)
    print(t("clone_done", elapsed=total_time))
    print(f"📁 Image Path   : {os.path.abspath(output_image_path)}")
    print(f"📦 Total Copied : {copied_bytes / (1024**3):.2f} GB ({copied_bytes:,} bytes)")
    print(f"🔐 SHA-256 Hash : {digest}")
    if reader.bad_sectors:
        print(f"⚠️  Bad Sectors  : {len(reader.bad_sectors)} bad blocks encountered (Logged to bad_sectors_map.log)")
    print("=" * 80)
    print(f"\n{t('clone_hint')}")
    print(f"   sudo python3 recover.py {os.path.abspath(output_image_path)} --all\n")

def interactive_select_destination(default_dest: str = "./recovered_all_data") -> str:
    """Prompt user to choose output directory with free space inspection."""
    options = []
    
    # 1. Default current folder
    def_free = shutil.disk_usage(".").free / (1024 ** 3)
    options.append({
        "label": f"{default_dest}",
        "path": os.path.abspath(default_dest),
        "free_gb": def_free,
        "tag": t("tag_default_dest")
    })

    # 2. Desktop
    desktop_path = os.path.expanduser("~/Desktop/recovered_data")
    desktop_free = shutil.disk_usage(os.path.expanduser("~")).free / (1024 ** 3)
    options.append({
        "label": f"~/Desktop/recovered_data",
        "path": desktop_path,
        "free_gb": desktop_free,
        "tag": t("tag_desktop")
    })

    # 3. External Mount Points (macOS /Volumes or Linux /media)
    if sys.platform == "darwin" and os.path.exists("/Volumes"):
        try:
            for vol in os.listdir("/Volumes"):
                vol_path = os.path.join("/Volumes", vol)
                if os.path.isdir(vol_path) and not vol.startswith("Macintosh") and not vol.startswith("."):
                    vol_free = shutil.disk_usage(vol_path).free / (1024 ** 3)
                    options.append({
                        "label": f"/Volumes/{vol}/recovered_data",
                        "path": os.path.join(vol_path, "recovered_data"),
                        "free_gb": vol_free,
                        "tag": t("tag_external_dest")
                    })
        except Exception:
            pass

    print("\n" + "=" * 80)
    print(t("dest_title"))
    print("-" * 80)
    for idx, opt in enumerate(options, 1):
        free_str = f"({t('free_space')}: {opt['free_gb']:6.1f} GB)"
        print(f"  [{idx}] {opt['label']:<45} {free_str} [{opt['tag']}]")
    print("=" * 80)
    print(f"  [C] {t('opt_custom_dest')}")
    print(f"  [Q] {t('opt_quit')}")
    print("=" * 80)

    try:
        choice = input(t("prompt_select_dest", n=len(options))).strip()
    except (KeyboardInterrupt, EOFError):
        print("\n" + t("cancel_msg"))
        sys.exit(0)

    if not choice:
        return options[0]["path"]

    choice_lower = choice.lower()
    if choice_lower in ("q", "quit"):
        print(t("cancel_msg"))
        sys.exit(0)

    if choice_lower in ("c", "custom"):
        try:
            custom_dir = input(t("prompt_custom_dest")).strip()
            if custom_dir:
                return os.path.abspath(custom_dir)
        except (KeyboardInterrupt, EOFError):
            sys.exit(0)

    if choice.isdigit():
        idx = int(choice)
        if 1 <= idx <= len(options):
            return options[idx - 1]["path"]

    return options[0]["path"]
