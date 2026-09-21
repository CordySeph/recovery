"""
Partition Table Scanner & Heuristic Rebuilder Module
Scans physical storage to discover deleted/lost partitions, MBR, GPT, and File System VBR headers
(NTFS, FAT32, exFAT, APFS, EXT4).
"""

import os
import struct
from typing import List, Dict, Optional

def parse_mbr_partitions(sector_bytes: bytes, base_offset: int = 0) -> List[Dict]:
    """Parse standard 64-byte MBR partition table (4 entries at offset 446)."""
    partitions = []
    if len(sector_bytes) < 512 or sector_bytes[510:512] != b"\x55\xAA":
        return partitions

    pt_types = {
        0x07: "NTFS / exFAT",
        0x0B: "FAT32 (CHS)",
        0x0C: "FAT32 (LBA)",
        0x83: "Linux Native (EXT4/XFS)",
        0xAF: "Apple HFS+ / APFS",
        0xEE: "GPT Protective MBR",
    }

    for i in range(4):
        entry_offset = 446 + (i * 16)
        entry = sector_bytes[entry_offset : entry_offset + 16]
        bootable = entry[0] == 0x80
        p_type = entry[4]
        if p_type == 0x00:
            continue

        start_lba = struct.unpack("<I", entry[8:12])[0]
        sector_count = struct.unpack("<I", entry[12:16])[0]
        size_bytes = sector_count * 512

        partitions.append({
            "source": "MBR Table",
            "index": i + 1,
            "type": pt_types.get(p_type, f"Type 0x{p_type:02X}"),
            "start_lba": start_lba,
            "start_offset": base_offset + (start_lba * 512),
            "sector_count": sector_count,
            "size_gb": size_bytes / (1024 ** 3),
            "bootable": bootable,
        })
    return partitions

def scan_vbr_in_chunk(chunk: bytes, base_offset: int) -> List[Dict]:
    """Search a chunk for individual File System Boot Sectors (VBR / Superblocks)."""
    partitions = []
    chunk_len = len(chunk)

    # 1. NTFS VBR (b"NTFS    " at offset 3)
    idx = 0
    while True:
        pos = chunk.find(b"NTFS    ", idx)
        if pos == -1:
            break
        if pos >= 3:
            sec_start = pos - 3
            if sec_start + 512 <= chunk_len and chunk[sec_start + 510 : sec_start + 512] == b"\x55\xAA":
                total_sectors = struct.unpack("<Q", chunk[sec_start + 40 : sec_start + 48])[0]
                size_gb = (total_sectors * 512) / (1024 ** 3)
                partitions.append({
                    "filesystem": "NTFS",
                    "offset": base_offset + sec_start,
                    "lba": (base_offset + sec_start) // 512,
                    "total_sectors": total_sectors,
                    "size_gb": size_gb,
                    "description": "NTFS Volume Boot Record (VBR)"
                })
        idx = pos + 8

    # 2. exFAT VBR (b"EXFAT   " at offset 3)
    idx = 0
    while True:
        pos = chunk.find(b"EXFAT   ", idx)
        if pos == -1:
            break
        if pos >= 3:
            sec_start = pos - 3
            if sec_start + 512 <= chunk_len and chunk[sec_start + 510 : sec_start + 512] == b"\x55\xAA":
                vol_length = struct.unpack("<Q", chunk[sec_start + 72 : sec_start + 80])[0]
                size_gb = (vol_length * 512) / (1024 ** 3)
                partitions.append({
                    "filesystem": "exFAT",
                    "offset": base_offset + sec_start,
                    "lba": (base_offset + sec_start) // 512,
                    "total_sectors": vol_length,
                    "size_gb": size_gb,
                    "description": "exFAT Volume Boot Record (VBR)"
                })
        idx = pos + 8

    # 3. FAT32 VBR (b"FAT32   " at offset 82)
    idx = 0
    while True:
        pos = chunk.find(b"FAT32   ", idx)
        if pos == -1:
            break
        if pos >= 82:
            sec_start = pos - 82
            if sec_start + 512 <= chunk_len and chunk[sec_start + 510 : sec_start + 512] == b"\x55\xAA":
                tot_sec32 = struct.unpack("<I", chunk[sec_start + 32 : sec_start + 36])[0]
                size_gb = (tot_sec32 * 512) / (1024 ** 3)
                partitions.append({
                    "filesystem": "FAT32",
                    "offset": base_offset + sec_start,
                    "lba": (base_offset + sec_start) // 512,
                    "total_sectors": tot_sec32,
                    "size_gb": size_gb,
                    "description": "FAT32 Volume Boot Record (VBR)"
                })
        idx = pos + 8

    # 4. APFS Container Superblock (b"NXSB" at offset 0)
    idx = 0
    while True:
        pos = chunk.find(b"NXSB", idx)
        if pos == -1:
            break
        if pos + 64 <= chunk_len:
            block_size = struct.unpack("<I", chunk[pos + 36 : pos + 40])[0] if pos + 40 <= chunk_len else 4096
            block_count = struct.unpack("<Q", chunk[pos + 40 : pos + 48])[0] if pos + 48 <= chunk_len else 0
            size_gb = (block_count * block_size) / (1024 ** 3) if block_size and block_count else 0
            partitions.append({
                "filesystem": "APFS",
                "offset": base_offset + pos,
                "lba": (base_offset + pos) // 512,
                "total_sectors": (block_count * block_size) // 512 if block_size else 0,
                "size_gb": size_gb,
                "description": "Apple APFS Container Superblock"
            })
        idx = pos + 4

    # 5. Linux EXT4 Superblock (Magic 0x53EF at offset 1080)
    idx = 0
    while True:
        pos = chunk.find(b"\x53\xEF", idx)
        if pos == -1:
            break
        if pos >= 56:
            sb_start = pos - 56
            if sb_start + 1024 <= chunk_len:
                blocks_count = struct.unpack("<I", chunk[sb_start + 4 : sb_start + 8])[0]
                size_gb = (blocks_count * 4096) / (1024 ** 3)
                partitions.append({
                    "filesystem": "EXT4",
                    "offset": base_offset + sb_start,
                    "lba": (base_offset + sb_start) // 512,
                    "total_sectors": (blocks_count * 4096) // 512,
                    "size_gb": size_gb,
                    "description": "Linux EXT4 Superblock"
                })
        idx = pos + 2

    return partitions

def scan_disk_partitions(dev_path: str, max_sectors: int = 10000000) -> List[Dict]:
    """
    Scan storage device to discover MBR, GPT, and lost File System volume headers.
    """
    discovered = []
    if not os.path.exists(dev_path):
        return discovered

    try:
        with open(dev_path, "rb") as f:
            # Check sector 0 (MBR)
            first_sec = f.read(512)
            discovered.extend(parse_mbr_partitions(first_sec, 0))

            # Scan first 64MB for VBRs
            f.seek(0)
            chunk = f.read(64 * 1024 * 1024)
            discovered.extend(scan_vbr_in_chunk(chunk, 0))
    except Exception:
        pass

    return discovered

def print_partition_report(partitions: List[Dict]):
    """Print ASCII report of discovered partitions."""
    print("\n" + "=" * 80)
    print("🧩 LOST & DELETED PARTITION SCAN REPORT")
    print("=" * 80)
    if not partitions:
        print("  [!] No remnant partition tables or volume headers found.")
        print("=" * 80 + "\n")
        return

    print(f"{'#':<3} {'FileSystem / Type':<22} {'Start LBA':<12} {'Offset (Hex)':<16} {'Size (GB)':<10} {'Details'}")
    print("-" * 80)
    for idx, p in enumerate(partitions, 1):
        fs = p.get("filesystem") or p.get("type", "Unknown")
        lba = p.get("lba", p.get("start_lba", 0))
        off = p.get("offset", p.get("start_offset", 0))
        size = f"{p.get('size_gb', 0.0):.2f} GB"
        desc = p.get("description", p.get("source", ""))
        print(f"[{idx}] {fs:<22} {lba:<12} 0x{off:<14X} {size:<10} {desc}")
    print("=" * 80 + "\n")
