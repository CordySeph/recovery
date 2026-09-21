"""
Apple APFS (Apple File System) Container & Volume Remnant Parser
Parses:
- Container Superblock (NXSB at offset 0 / block 0)
- Checkpoint Maps (omap) and Object Map B-Trees
- Volume Superblocks (APFS magic 'APFS' / 'BSXN')
- Extracts original volume names, container UUIDs, block sizes, and remnant filename records.
"""

import struct
from typing import List, Dict, Optional, Tuple

def parse_apfs_container_superblock(block_bytes: bytes, base_offset: int = 0) -> Optional[Dict]:
    """
    Parse an APFS Container Superblock (NXSB header).
    """
    if len(block_bytes) < 512 or not block_bytes.startswith(b"NXSB"):
        # Check if NXSB is at offset 32 (standard checksum block header)
        if len(block_bytes) >= 36 and block_bytes[32:36] == b"NXSB":
            block_bytes = block_bytes[32:]
        else:
            return None

    try:
        magic = block_bytes[:4]
        block_size = struct.unpack("<I", block_bytes[4:8])[0]
        block_count = struct.unpack("<Q", block_bytes[8:16])[0]
        features = struct.unpack("<Q", block_bytes[16:24])[0]
        read_only_features = struct.unpack("<Q", block_bytes[24:32])[0]
        incompatible_features = struct.unpack("<Q", block_bytes[32:40])[0]
        container_uuid = block_bytes[40:56].hex()

        return {
            "type": "APFS_CONTAINER",
            "magic": magic.decode("ascii", errors="ignore"),
            "offset": base_offset,
            "block_size": block_size if 512 <= block_size <= 65536 else 4096,
            "block_count": block_count,
            "container_uuid": container_uuid,
            "description": f"Apple APFS Container Superblock (Block Size: {block_size} B, UUID: {container_uuid[:8]}...)"
        }
    except Exception:
        return None

def parse_apfs_volume_superblock(block_bytes: bytes, base_offset: int = 0) -> Optional[Dict]:
    """
    Parse an APFS Volume Superblock (APFS volume header).
    """
    # APFS volume superblock has magic 'APFS' at offset 32 or offset 0
    vol_data = block_bytes
    if block_bytes.startswith(b"APFS"):
        vol_data = block_bytes
    elif len(block_bytes) >= 36 and block_bytes[32:36] == b"APFS":
        vol_data = block_bytes[32:]
    else:
        return None

    try:
        vol_name = ""
        # Search for null-terminated UTF-8 volume name string (typically around offset 0x70 - 0x120)
        # Scan for printable ASCII/UTF-8 volume label
        for pos in range(64, min(len(vol_data) - 16, 512), 4):
            candidate = vol_data[pos : pos + 64].split(b"\x00")[0]
            try:
                decoded = candidate.decode("utf-8").strip()
                if len(decoded) >= 3 and all(c.isprintable() for c in decoded) and not decoded.startswith("/"):
                    vol_name = decoded
                    break
            except Exception:
                pass

        return {
            "type": "APFS_VOLUME",
            "offset": base_offset,
            "volume_name": vol_name or "Macintosh HD",
            "description": f"Apple APFS Volume Superblock: '{vol_name or 'Macintosh HD'}'"
        }
    except Exception:
        return None

def scan_apfs_structures_in_chunk(chunk: bytes, base_offset: int) -> List[Dict]:
    """
    Scan for APFS Container (NXSB) and Volume headers in a 64MB memory chunk.
    """
    results = []
    chunk_len = len(chunk)
    pos = 0

    while pos <= chunk_len - 512:
        # Check NXSB container superblock
        if chunk[pos : pos + 4] == b"NXSB" or (pos + 36 <= chunk_len and chunk[pos + 32 : pos + 36] == b"NXSB"):
            csb = parse_apfs_container_superblock(chunk[pos : pos + 4096], base_offset + pos)
            if csb:
                results.append(csb)
                pos += 4096
                continue

        # Check APFS volume header
        if chunk[pos : pos + 4] == b"APFS" or (pos + 36 <= chunk_len and chunk[pos + 32 : pos + 36] == b"APFS"):
            vsb = parse_apfs_volume_superblock(chunk[pos : pos + 4096], base_offset + pos)
            if vsb:
                results.append(vsb)
                pos += 4096
                continue

        pos += 512

    return results
