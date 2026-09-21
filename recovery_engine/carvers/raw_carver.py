"""
RAW Photo & Professional Camera Image Carver
Supports:
- Canon RAW (.cr2, .cr3)
- Nikon RAW (.nef)
- Sony RAW (.arw)
- Adobe Digital Negative (.dng)
- Tagged Image File Format (.tiff / .tif)
Extracts Camera Make, Model, and Capture Date from TIFF/EXIF IFD0 tags.
"""

import struct
from typing import List, Dict, Optional, Tuple

def parse_tiff_metadata(data: bytes) -> Dict:
    """
    Parse TIFF Header (Little Endian 'II' or Big Endian 'MM') and IFD0 tags.
    Extracts: make, model, datetime, width, height, is_cr2, is_nef, is_arw, is_dng
    """
    meta = {
        "make": "",
        "model": "",
        "datetime": "",
        "file_type": "tiff"
    }

    if len(data) < 8:
        return meta

    endian = data[:2]
    if endian == b"II":
        fmt = "<"
    elif endian == b"MM":
        fmt = ">"
    else:
        return meta

    try:
        magic_42 = struct.unpack(f"{fmt}H", data[2:4])[0]
        if magic_42 != 42:
            return meta

        ifd0_offset = struct.unpack(f"{fmt}I", data[4:8])[0]
        if ifd0_offset >= len(data) - 2:
            return meta

        # Check CR2 signature at offset 8 (CR\x02\x00)
        if len(data) >= 12 and data[8:12] == b"CR\x02\x00":
            meta["file_type"] = "cr2"

        num_entries = struct.unpack(f"{fmt}H", data[ifd0_offset : ifd0_offset + 2])[0]
        idx = ifd0_offset + 2

        for _ in range(min(num_entries, 64)):
            if idx + 12 > len(data):
                break

            tag_id = struct.unpack(f"{fmt}H", data[idx : idx + 2])[0]
            tag_type = struct.unpack(f"{fmt}H", data[idx + 2 : idx + 4])[0]
            tag_count = struct.unpack(f"{fmt}I", data[idx + 4 : idx + 8])[0]
            val_offset = struct.unpack(f"{fmt}I", data[idx + 8 : idx + 12])[0]

            # Type 2 is ASCII string
            if tag_type == 2 and tag_count > 0:
                # If length <= 4, string is in val_offset directly, otherwise at offset
                if tag_count <= 4:
                    raw_str = data[idx + 8 : idx + 8 + tag_count]
                elif val_offset + tag_count <= len(data):
                    raw_str = data[val_offset : val_offset + tag_count]
                else:
                    raw_str = b""
                
                clean_str = raw_str.decode("utf-8", errors="ignore").strip("\x00").strip()

                if tag_id == 0x010F:  # Make (e.g. Canon, NIKON CORPORATION, SONY)
                    meta["make"] = clean_str
                elif tag_id == 0x0110:  # Model (e.g. Canon EOS 5D Mark IV, NIKON D850, ILCE-7M3)
                    meta["model"] = clean_str
                elif tag_id in (0x0132, 0x9003):  # DateTime / DateTimeOriginal
                    if len(clean_str) >= 10 and clean_str[4] in (":", "-") and clean_str[7] in (":", "-"):
                        meta["datetime"] = clean_str[:10].replace(":", "-")

            # Detect DNG / NEF / ARW specific tags
            if tag_id == 0xC612:  # DNGVersion tag
                meta["file_type"] = "dng"

            idx += 12

        # Infer file type from camera make if still tiff
        if meta["file_type"] == "tiff":
            make_lower = meta["make"].lower()
            if "nikon" in make_lower:
                meta["file_type"] = "nef"
            elif "sony" in make_lower:
                meta["file_type"] = "arw"
            elif "canon" in make_lower:
                meta["file_type"] = "cr2"

    except Exception:
        pass

    return meta

def scan_raw_photos_in_chunk(chunk: bytes, base_offset: int, max_file_size: int = 150 * 1024 * 1024) -> List[Dict]:
    """
    Scan for RAW photo signatures (CR2, CR3, NEF, ARW, DNG, TIFF) in memory chunk.
    """
    results = []
    chunk_len = len(chunk)
    pos = 0

    while pos < chunk_len - 16:
        # 1. Canon CR3 (ISO base media file format with 'crx ' or 'ftypcrx')
        if chunk[pos + 4 : pos + 8] == b"ftyp" and chunk[pos + 8 : pos + 12] in (b"crx ", b"cr3 ", b"isom"):
            atom_size = struct.unpack(">I", chunk[pos : pos + 4])[0]
            if 16 <= atom_size <= chunk_len - pos:
                results.append({
                    "offset": base_offset + pos,
                    "file_type": "cr3",
                    "category": "raw_photos",
                    "estimated_size": min(atom_size * 2, max_file_size),
                    "meta": {"make": "Canon", "model": "Canon CR3 RAW"}
                })
                pos += 16
                continue

        # 2. TIFF-based RAW (Canon CR2, Nikon NEF, Sony ARW, Adobe DNG, TIFF)
        if chunk[pos : pos + 4] in (b"II*\x00", b"MM\x00*"):
            header_sub = chunk[pos : min(pos + 65536, chunk_len)]
            meta = parse_tiff_metadata(header_sub)
            ft = meta.get("file_type", "tiff")

            # Default size estimate based on typical RAW file size (approx 20MB - 60MB)
            estimated_size = 35 * 1024 * 1024

            results.append({
                "offset": base_offset + pos,
                "file_type": ft,
                "category": "raw_photos",
                "estimated_size": estimated_size,
                "meta": meta,
                "timestamp": meta.get("datetime", "")
            })
            pos += 512
            continue

        pos += 512  # Align to standard sector boundary for RAW photos

    return results
