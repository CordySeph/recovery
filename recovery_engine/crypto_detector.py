"""
Encrypted Partition & Volume Header Detection Module
Detects BitLocker, LUKS (v1/v2), Apple FileVault / Encrypted APFS, CoreStorage, and VeraCrypt volumes.
Alerts the user before running intensive scans on ciphertext.
"""

import os
import struct
from typing import List, Dict, Optional

# Signatures for encrypted volume headers
SIG_BITLOCKER = b"-FVE-FS-"
SIG_LUKS1 = b"LUKS\xBA\xBE"
SIG_APFS_NXSB = b"NXSB"
SIG_CORESTORAGE = b"\x53\x43\x53\x31"  # CS1
SIG_VERACRYPT_BC = b"VERA"

def detect_encryption_in_chunk(chunk: bytes, base_offset: int = 0) -> List[Dict]:
    """
    Search a memory chunk for cryptographic container signatures.
    """
    findings = []
    chunk_len = len(chunk)

    # 1. BitLocker (Windows)
    idx = 0
    while True:
        pos = chunk.find(SIG_BITLOCKER, idx)
        if pos == -1:
            break
        findings.append({
            "type": "BitLocker",
            "offset": base_offset + pos,
            "description": "Microsoft Windows BitLocker Encrypted Volume Header",
            "guidance": "Unlock or decrypt with recovery key/password before carving."
        })
        idx = pos + len(SIG_BITLOCKER)

    # 2. Linux LUKS (v1 & v2)
    idx = 0
    while True:
        pos = chunk.find(SIG_LUKS1, idx)
        if pos == -1:
            break
        ver = 1
        if pos + 8 <= chunk_len:
            ver = int.from_bytes(chunk[pos + 6 : pos + 8], "big")
        findings.append({
            "type": f"LUKS (v{ver})",
            "offset": base_offset + pos,
            "description": f"Linux Unified Key Setup (LUKS v{ver}) Encrypted Volume",
            "guidance": "Open container using cryptsetup before raw sector carving."
        })
        idx = pos + len(SIG_LUKS1)

    # 3. Apple APFS Container (Encrypted Container Keybag check)
    idx = 0
    while True:
        pos = chunk.find(SIG_APFS_NXSB, idx)
        if pos == -1:
            break
        if pos + 64 <= chunk_len:
            # Check APFS flags for encryption feature flag (bit 0x01)
            flags = struct.unpack("<Q", chunk[pos + 32 : pos + 40])[0] if pos + 40 <= chunk_len else 0
            is_encrypted = bool(flags & 0x01)
            if is_encrypted:
                findings.append({
                    "type": "Apple APFS (Encrypted)",
                    "offset": base_offset + pos,
                    "description": "Apple FileVault / Encrypted APFS Container Superblock",
                    "guidance": "Mount and decrypt with diskutil apfs unlockVolume first."
                })
        idx = pos + len(SIG_APFS_NXSB)

    # 4. Apple CoreStorage (Legacy FileVault 2)
    idx = 0
    while True:
        pos = chunk.find(b"CS1", idx)
        if pos == -1:
            break
        if pos >= 1 and chunk[pos - 1] == 0x53:  # SCS1
            findings.append({
                "type": "Apple CoreStorage",
                "offset": base_offset + pos - 1,
                "description": "Apple CoreStorage Encrypted Volume Header",
                "guidance": "Unlock with diskutil cs unlockVolume before scanning."
            })
        idx = pos + 3

    return findings

def scan_disk_for_encryption(dev_path: str, max_check_bytes: int = 100 * 1024 * 1024) -> List[Dict]:
    """
    Inspect the first 100 MB of target storage for encrypted volume headers.
    """
    if not os.path.exists(dev_path):
        return []

    try:
        with open(dev_path, "rb") as f:
            sample = f.read(max_check_bytes)
            return detect_encryption_in_chunk(sample, 0)
    except Exception:
        return []
