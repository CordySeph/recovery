"""
Image File Carver (JPG, PNG, GIF, WEBP, BMP, HEIC) with Built-in EXIF Date Extraction
"""

import struct
from typing import List, Tuple, Optional, Dict
from recovery_engine.config import SIG_JPEG, SIG_PNG, SIG_GIF87, SIG_GIF89, SIG_WEBP_RIFF, SIG_BMP

def extract_exif_date(data: bytes) -> Optional[str]:
    """
    Extract date and time from JPEG EXIF metadata (DateTimeOriginal / DateTime).
    Returns string formatted as 'YYYY-MM-DD' or None if not found.
    """
    try:
        if not data.startswith(b"\xFF\xD8"):
            return None
        
        pos = 2
        data_len = min(len(data), 65536)  # Search within first 64KB for APP1

        while pos < data_len - 4:
            if data[pos] != 0xFF:
                pos += 1
                continue
            
            marker = data[pos:pos+2]
            if marker == b"\xFF\xE1":  # APP1 Exif Marker
                length = struct.unpack(">H", data[pos+2:pos+4])[0]
                app1_data = data[pos+4 : pos+2+length]
                if app1_data.startswith(b"Exif\x00\x00"):
                    tiff_data = app1_data[6:]
                    if len(tiff_data) < 8:
                        break
                    
                    endian_char = "<" if tiff_data.startswith(b"II") else ">"
                    if tiff_data[:2] not in (b"II", b"MM"):
                        break
                    
                    # Check fixed 42
                    fixed_42 = struct.unpack(f"{endian_char}H", tiff_data[2:4])[0]
                    if fixed_42 != 42:
                        break
                    
                    ifd0_offset = struct.unpack(f"{endian_char}I", tiff_data[4:8])[0]
                    
                    # Helper to scan tags inside an IFD
                    def parse_ifd(offset):
                        if offset >= len(tiff_data) - 2:
                            return None, None
                        tag_count = struct.unpack(f"{endian_char}H", tiff_data[offset:offset+2])[0]
                        exif_sub_offset = None
                        found_date = None
                        
                        idx = offset + 2
                        for _ in range(tag_count):
                            if idx + 12 > len(tiff_data):
                                break
                            tag_id = struct.unpack(f"{endian_char}H", tiff_data[idx:idx+2])[0]
                            tag_type = struct.unpack(f"{endian_char}H", tiff_data[idx+2:idx+4])[0]
                            tag_len = struct.unpack(f"{endian_char}I", tiff_data[idx+4:idx+8])[0]
                            val_offset = struct.unpack(f"{endian_char}I", tiff_data[idx+8:idx+12])[0]
                            
                            # 0x0132 = DateTime, 0x9003 = DateTimeOriginal, 0x9004 = DateTimeDigitized
                            if tag_id in (0x9003, 0x9004, 0x0132):
                                if val_offset + tag_len <= len(tiff_data):
                                    date_bytes = tiff_data[val_offset : val_offset + tag_len]
                                    date_str = date_bytes.decode("ascii", errors="ignore").strip("\x00").strip()
                                    if len(date_str) >= 10 and date_str[4] in (":", "-") and date_str[7] in (":", "-"):
                                        found_date = date_str[:10].replace(":", "-")
                            elif tag_id == 0x8769:  # ExifOffset -> SubIFD
                                exif_sub_offset = val_offset
                            
                            idx += 12
                        return found_date, exif_sub_offset

                    # 1. Check IFD0
                    date_val, sub_offset = parse_ifd(ifd0_offset)
                    if date_val:
                        return date_val
                    
                    # 2. Check Exif SubIFD if present
                    if sub_offset:
                        date_val, _ = parse_ifd(sub_offset)
                        if date_val:
                            return date_val
                break
            elif marker in (b"\xFF\xDA", b"\xFF\xD9"):  # Start of Scan or EOI
                break
            else:
                # Skip marker segment
                if pos + 4 <= len(data):
                    seg_len = struct.unpack(">H", data[pos+2:pos+4])[0]
                    pos += 2 + seg_len
                else:
                    break
    except Exception:
        pass
    return None

def scan_images_in_chunk(chunk: bytes, base_offset: int, max_file_size: int = 30 * 1024 * 1024) -> List[Dict]:
    """
    Scan a memory buffer for JPEG, PNG, GIF, WEBP, BMP images.
    Returns a list of dicts with detected image offsets and estimated lengths.
    """
    results = []
    chunk_len = len(chunk)

    # 1. JPEG Scanner
    idx = 0
    while True:
        pos = chunk.find(SIG_JPEG, idx)
        if pos == -1:
            break
        
        # Look ahead for EOI marker (\xFF\xD9)
        eoi_search_limit = min(chunk_len, pos + max_file_size)
        eoi_pos = chunk.find(b"\xFF\xD9", pos + 2)
        
        file_len = (eoi_pos + 2 - pos) if (eoi_pos != -1 and eoi_pos < eoi_search_limit) else min(20 * 1024 * 1024, chunk_len - pos)
        
        results.append({
            "offset": base_offset + pos,
            "category": "Images",
            "file_type": "jpg",
            "size_bytes": file_len,
            "chunk_rel_pos": pos,
        })
        idx = pos + 4

    # 2. PNG Scanner
    idx = 0
    while True:
        pos = chunk.find(SIG_PNG, idx)
        if pos == -1:
            break
        
        # Look for IEND chunk (b"IEND\xae\x42\x60\x82")
        iend_pos = chunk.find(b"IEND\xae\x42\x60\x82", pos + 8)
        file_len = (iend_pos + 8 - pos) if (iend_pos != -1 and (iend_pos - pos) < max_file_size) else min(15 * 1024 * 1024, chunk_len - pos)
        
        results.append({
            "offset": base_offset + pos,
            "category": "Images",
            "file_type": "png",
            "size_bytes": file_len,
            "chunk_rel_pos": pos,
        })
        idx = pos + 8

    # 3. GIF Scanner
    for sig in (SIG_GIF87, SIG_GIF89):
        idx = 0
        while True:
            pos = chunk.find(sig, idx)
            if pos == -1:
                break
            
            # GIF ends with 0x3B (Trailer)
            end_search = min(chunk_len, pos + 10 * 1024 * 1024)
            trailer_pos = chunk.find(b"\x3B", pos + 6)
            file_len = (trailer_pos + 1 - pos) if (trailer_pos != -1 and trailer_pos < end_search) else min(5 * 1024 * 1024, chunk_len - pos)
            
            results.append({
                "offset": base_offset + pos,
                "category": "Images",
                "file_type": "gif",
                "size_bytes": file_len,
                "chunk_rel_pos": pos,
            })
            idx = pos + 6

    # 4. WEBP Scanner
    idx = 0
    while True:
        pos = chunk.find(SIG_WEBP_RIFF, idx)
        if pos == -1:
            break
        if pos + 12 <= chunk_len and chunk[pos+8:pos+12] == b"WEBP":
            riff_len = struct.unpack("<I", chunk[pos+4:pos+8])[0]
            file_len = min(riff_len + 8, max_file_size)
            results.append({
                "offset": base_offset + pos,
                "category": "Images",
                "file_type": "webp",
                "size_bytes": file_len,
                "chunk_rel_pos": pos,
            })
            idx = pos + file_len
        else:
            idx = pos + 4

    # 5. BMP Scanner
    idx = 0
    while True:
        pos = chunk.find(SIG_BMP, idx)
        if pos == -1:
            break
        if pos + 14 <= chunk_len:
            bmp_size = struct.unpack("<I", chunk[pos+2:pos+6])[0]
            if 54 <= bmp_size <= max_file_size:
                results.append({
                    "offset": base_offset + pos,
                    "category": "Images",
                    "file_type": "bmp",
                    "size_bytes": bmp_size,
                    "chunk_rel_pos": pos,
                })
                idx = pos + bmp_size
            else:
                idx = pos + 2
        else:
            idx = pos + 2

    return results
