"""
Video Carving Module (MP4, MOV, AVI, and Xiongmai CCTV H.264 Streams)
"""

import sys
import os
import struct
import datetime
import subprocess
import shutil
from typing import List, Dict, Optional, Tuple
from recovery_engine.config import MAGIC_CCTV_H264, SIG_AVI_RIFF, TIMEZONE

def find_ffmpeg_binary() -> Optional[str]:
    """Find FFmpeg binary across system PATH or local application directories."""
    candidates = (
        shutil.which("ffmpeg"),
        shutil.which("ffmpeg.exe"),
        os.path.join(os.path.dirname(sys.executable or sys.argv[0]), "ffmpeg"),
        os.path.join(os.path.dirname(sys.executable or sys.argv[0]), "ffmpeg.exe"),
        os.path.join(os.getcwd(), "ffmpeg"),
        os.path.join(os.getcwd(), "ffmpeg.exe"),
        "/opt/homebrew/bin/ffmpeg",
        "/usr/local/bin/ffmpeg",
        "/usr/bin/ffmpeg",
    )
    for cand in candidates:
        if cand and os.path.exists(cand) and (os.access(cand, os.X_OK) or sys.platform == "win32"):
            return cand
    return None

def parse_cctv_timestamp(chunk: bytes, offset: int) -> Optional[datetime.datetime]:
    """
    Parse timestamp from Xiongmai H.264 frame header.
    Format: 8 bytes at offset+12 (2 bytes year, 1 byte month, 1 byte day, 1 byte hour, 1 byte min, 1 byte sec).
    """
    try:
        if offset + 20 > len(chunk):
            return None
        year, month, day, hour, minute, second = struct.unpack(">HBBBBB", chunk[offset + 12 : offset + 19])
        if 2000 <= year <= 2040 and 1 <= month <= 12 and 1 <= day <= 31 and 0 <= hour <= 23 and 0 <= minute <= 59 and 0 <= second <= 59:
            return datetime.datetime(year, month, day, hour, minute, second, tzinfo=TIMEZONE)
    except Exception:
        pass
    return None

def scan_videos_in_chunk(chunk: bytes, base_offset: int, max_file_size: int = 500 * 1024 * 1024) -> List[Dict]:
    """
    Scan a memory buffer for MP4, MOV, AVI, and Xiongmai CCTV H.264 streams.
    """
    results = []
    chunk_len = len(chunk)

    # 1. MP4 / MOV Container Scanner (ftyp Box)
    idx = 0
    while True:
        pos = chunk.find(b"ftyp", idx)
        if pos == -1:
            break
        if pos >= 4:
            box_start = pos - 4
            box_len = struct.unpack(">I", chunk[box_start:pos])[0]
            if 8 <= box_len <= 1024:
                brand = chunk[pos+4:pos+8] if pos + 8 <= chunk_len else b""
                ext = "mov" if brand in (b"qt  ", b"moov") else "mp4"
                
                # Estimate video stream length by looking for next ftyp or max_file_size
                next_ftyp = chunk.find(b"ftyp", pos + 8)
                est_len = (next_ftyp - 4 - box_start) if (next_ftyp != -1 and (next_ftyp - box_start) < max_file_size) else min(100 * 1024 * 1024, chunk_len - box_start)
                
                results.append({
                    "offset": base_offset + box_start,
                    "category": "Videos",
                    "file_type": ext,
                    "size_bytes": est_len,
                    "chunk_rel_pos": box_start,
                })
        idx = pos + 4

    # 2. AVI Scanner
    idx = 0
    while True:
        pos = chunk.find(SIG_AVI_RIFF, idx)
        if pos == -1:
            break
        if pos + 12 <= chunk_len and chunk[pos+8:pos+12] == b"AVI ":
            riff_len = struct.unpack("<I", chunk[pos+4:pos+8])[0]
            file_len = min(riff_len + 8, max_file_size)
            results.append({
                "offset": base_offset + pos,
                "category": "Videos",
                "file_type": "avi",
                "size_bytes": file_len,
                "chunk_rel_pos": pos,
            })
            idx = pos + file_len
        else:
            idx = pos + 4

    # 3. Xiongmai CCTV H.264 Header Scanner
    idx = 0
    while True:
        pos = chunk.find(MAGIC_CCTV_H264, idx)
        if pos == -1:
            break
        
        ts = parse_cctv_timestamp(chunk, pos)
        ts_str = ts.strftime("%Y-%m-%d %H:%M:%S") if ts else ""
        
        # Look ahead for next clip header or default clip length
        next_cctv = chunk.find(MAGIC_CCTV_H264, pos + 1024)
        clip_len = (next_cctv - pos) if (next_cctv != -1 and (next_cctv - pos) < 50 * 1024 * 1024) else min(30 * 1024 * 1024, chunk_len - pos)

        results.append({
            "offset": base_offset + pos,
            "category": "Videos",
            "file_type": "cctv",
            "size_bytes": clip_len,
            "timestamp": ts_str,
            "datetime_obj": ts,
            "chunk_rel_pos": pos,
        })
        idx = pos + clip_len if clip_len > 1024 else pos + len(MAGIC_CCTV_H264)

    return results

def convert_h264_to_mp4(h264_file_path: str, mp4_file_path: str, ffmpeg_bin: Optional[str] = None) -> bool:
    """Remux raw H.264 stream into standard MP4 container via FFmpeg."""
    ffmpeg = ffmpeg_bin or find_ffmpeg_binary()
    if not ffmpeg:
        return False
    try:
        cmd = [
            ffmpeg,
            "-y",
            "-hide_banner",
            "-loglevel", "error",
            "-i", h264_file_path,
            "-c", "copy",
            mp4_file_path
        ]
        res = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return res.returncode == 0
    except Exception:
        return False
