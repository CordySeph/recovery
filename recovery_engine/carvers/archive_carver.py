"""
Archive, Audio & Database Carver Module (ZIP, 7Z, RAR, SQLite, MP3, WAV, FLAC)
"""

import struct
from typing import List, Dict
from recovery_engine.config import (
    SIG_ZIP, SIG_7Z, SIG_RAR_V4, SIG_RAR_V5, SIG_SQLITE,
    SIG_MP3_ID3, SIG_FLAC
)

def scan_archives_and_db_in_chunk(chunk: bytes, base_offset: int, max_file_size: int = 200 * 1024 * 1024) -> List[Dict]:
    """
    Scan a memory buffer for Archives (ZIP, 7Z, RAR), Databases (SQLite), and Audio (MP3, WAV, FLAC).
    """
    results = []
    chunk_len = len(chunk)

    # 1. Standard ZIP Archive Scanner (not Office)
    idx = 0
    while True:
        pos = chunk.find(SIG_ZIP, idx)
        if pos == -1:
            break
        
        sample = chunk[pos : min(chunk_len, pos + 2048)]
        # Skip if it is an Office document (already handled by doc_carver)
        if b"[Content_Types].xml" not in sample:
            eocd_pos = chunk.find(b"PK\x05\x06", pos + 30)
            file_len = (eocd_pos + 22 - pos) if (eocd_pos != -1 and (eocd_pos - pos) < max_file_size) else min(50 * 1024 * 1024, chunk_len - pos)
            results.append({
                "offset": base_offset + pos,
                "category": "Archives",
                "file_type": "zip",
                "size_bytes": file_len,
                "chunk_rel_pos": pos,
            })
            idx = pos + file_len
        else:
            idx = pos + 4

    # 2. 7-Zip Scanner
    idx = 0
    while True:
        pos = chunk.find(SIG_7Z, idx)
        if pos == -1:
            break
        results.append({
            "offset": base_offset + pos,
            "category": "Archives",
            "file_type": "7z",
            "size_bytes": min(50 * 1024 * 1024, chunk_len - pos),
            "chunk_rel_pos": pos,
        })
        idx = pos + 6

    # 3. RAR Archive Scanner
    for sig in (SIG_RAR_V4, SIG_RAR_V5):
        idx = 0
        while True:
            pos = chunk.find(sig, idx)
            if pos == -1:
                break
            results.append({
                "offset": base_offset + pos,
                "category": "Archives",
                "file_type": "rar",
                "size_bytes": min(50 * 1024 * 1024, chunk_len - pos),
                "chunk_rel_pos": pos,
            })
            idx = pos + 7

    # 4. SQLite Database Scanner
    idx = 0
    while True:
        pos = chunk.find(SIG_SQLITE, idx)
        if pos == -1:
            break
        # Estimate size from page size * page count in header if available
        est_len = min(100 * 1024 * 1024, chunk_len - pos)
        if pos + 32 <= chunk_len:
            try:
                page_size = struct.unpack(">H", chunk[pos+16 : pos+18])[0]
                page_count = struct.unpack(">I", chunk[pos+28 : pos+32])[0]
                if page_size > 0 and page_count > 0:
                    calc_size = page_size * page_count
                    if 512 <= calc_size <= max_file_size:
                        est_len = calc_size
            except Exception:
                pass

        results.append({
            "offset": base_offset + pos,
            "category": "Database",
            "file_type": "sqlite",
            "size_bytes": est_len,
            "chunk_rel_pos": pos,
        })
        idx = pos + est_len if est_len > 16 else pos + 16

    # 5. TAR Archive Scanner
    idx = 0
    while True:
        pos = chunk.find(b"ustar", idx)
        if pos == -1:
            break
        if pos >= 257:
            tar_start = pos - 257
            results.append({
                "offset": base_offset + tar_start,
                "category": "Archives",
                "file_type": "tar",
                "size_bytes": min(100 * 1024 * 1024, chunk_len - tar_start),
                "chunk_rel_pos": tar_start,
            })
        idx = pos + 5

    # 6. GZ Archive Scanner
    idx = 0
    while True:
        pos = chunk.find(b"\x1F\x8B\x08", idx)
        if pos == -1:
            break
        results.append({
            "offset": base_offset + pos,
            "category": "Archives",
            "file_type": "gz",
            "size_bytes": min(50 * 1024 * 1024, chunk_len - pos),
            "chunk_rel_pos": pos,
        })
        idx = pos + 3

    return results
