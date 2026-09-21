"""
Virtual Disk & Disk Image File Carver
Supports:
- VMware Virtual Disk (.vmdk - 'KDMV' magic)
- Hyper-V Virtual Hard Disk (.vhdx - 'vhdxfile' signature)
- Microsoft Virtual Hard Disk (.vhd - 'conectix' footer/header)
- ISO 9660 Disc Images (.iso - 'CD001' volume descriptor at sector 16 / offset 0x8000)
"""

import struct
from typing import List, Dict

def scan_virtual_disks_in_chunk(chunk: bytes, base_offset: int, max_file_size: int = 500 * 1024 * 1024) -> List[Dict]:
    results = []
    chunk_len = len(chunk)
    pos = 0

    while pos < chunk_len - 16:
        # 1. VMware VMDK Sparse Header ('KDMV')
        if chunk[pos : pos + 4] == b"KDMV":
            if pos + 24 <= chunk_len:
                version = struct.unpack("<I", chunk[pos + 4 : pos + 8])[0]
                flags = struct.unpack("<I", chunk[pos + 8 : pos + 12])[0]
                capacity_sectors = struct.unpack("<Q", chunk[pos + 12 : pos + 20])[0]

                results.append({
                    "offset": base_offset + pos,
                    "file_type": "vmdk",
                    "category": "virtual_disks",
                    "estimated_size": min(50 * 1024 * 1024, max_file_size),
                    "meta": {
                        "format": "VMware VMDK",
                        "capacity_gb": f"{(capacity_sectors * 512) / (1024**3):.2f} GB"
                    }
                })
                pos += 512
                continue

        # 2. Hyper-V VHDX Header ('vhdxfile')
        if chunk[pos : pos + 8] == b"vhdxfile":
            results.append({
                "offset": base_offset + pos,
                "file_type": "vhdx",
                "category": "virtual_disks",
                "estimated_size": min(100 * 1024 * 1024, max_file_size),
                "meta": {"format": "Hyper-V VHDX"}
            })
            pos += 512
            continue

        # 3. Virtual Hard Disk VHD Footer ('conectix')
        if chunk[pos : pos + 8] == b"conectix":
            results.append({
                "offset": base_offset + pos,
                "file_type": "vhd",
                "category": "virtual_disks",
                "estimated_size": min(50 * 1024 * 1024, max_file_size),
                "meta": {"format": "Microsoft VHD"}
            })
            pos += 512
            continue

        # 4. ISO 9660 Standard Disc Image ('CD001' volume descriptor)
        # Often at offset 0x8000 (32,768) from the start of the ISO
        if chunk[pos : pos + 6] == b"\x01CD001":
            iso_start_offset = max(0, base_offset + pos - 0x8000)
            results.append({
                "offset": iso_start_offset,
                "file_type": "iso",
                "category": "virtual_disks",
                "estimated_size": min(200 * 1024 * 1024, max_file_size),
                "meta": {"format": "ISO 9660 Disc Image"}
            })
            pos += 2048
            continue

        pos += 512

    return results
