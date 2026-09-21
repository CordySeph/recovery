"""
File Integrity & Structural Corruption Validators
"""

import io
import struct
import zipfile
from typing import Tuple

def validate_file_integrity(file_type: str, data: bytes) -> Tuple[bool, str]:
    """
    Validate the internal binary structure of recovered data.
    Returns (is_valid: bool, status_message: str).
    """
    if not data or len(data) < 16:
        return False, "Too short / empty"

    ft = file_type.lower()

    if ft in ("jpg", "jpeg"):
        if data.startswith(b"\xFF\xD8\xFF") and b"\xFF\xD9" in data[-1024:]:
            return True, "Valid JPEG (SOI & EOI found)"
        elif data.startswith(b"\xFF\xD8\xFF"):
            return True, "JPEG partial (SOI found)"
        return False, "Corrupted JPEG header"

    elif ft == "png":
        if data.startswith(b"\x89PNG\r\n\x1a\n") and (b"IEND" in data[-32:] or b"IHDR" in data[:32]):
            return True, "Valid PNG structure"
        return False, "Corrupted PNG header"

    elif ft == "gif":
        if (data.startswith(b"GIF87a") or data.startswith(b"GIF89a")) and data.endswith(b"\x3B"):
            return True, "Valid GIF (Header & Trailer 0x3B)"
        elif data.startswith(b"GIF87a") or data.startswith(b"GIF89a"):
            return True, "GIF partial (Header found)"
        return False, "Corrupted GIF header"

    elif ft == "webp":
        if data.startswith(b"RIFF") and len(data) >= 12 and data[8:12] == b"WEBP":
            return True, "Valid WebP RIFF"
        return False, "Invalid WebP header"

    elif ft == "bmp":
        if data.startswith(b"BM"):
            return True, "Valid BMP structure"
        return False, "Invalid BMP header"

    elif ft == "pdf":
        if data.startswith(b"%PDF-"):
            if b"%%EOF" in data[-2048:]:
                return True, "Valid PDF (%%EOF verified)"
            return True, "PDF partial (Header verified)"
        return False, "Corrupted PDF header"

    elif ft in ("docx", "xlsx", "pptx", "zip"):
        if data.startswith(b"PK\x03\x04"):
            try:
                with zipfile.ZipFile(io.BytesIO(data), "r") as zf:
                    bad = zf.testzip()
                    if bad is None:
                        return True, f"Valid {ft.upper()} Archive"
                    else:
                        return False, f"Corrupted entry {bad}"
            except Exception:
                if b"PK\x05\x06" in data[-2048:]:
                    return True, f"Valid {ft.upper()} (EOCD marker)"
                return True, f"{ft.upper()} partial archive"
        return False, f"Invalid {ft.upper()} signature"

    elif ft in ("sqlite", "db"):
        if data.startswith(b"SQLite format 3\x00"):
            try:
                page_size = struct.unpack(">H", data[16:18])[0]
                if page_size in (512, 1024, 2048, 4096, 8192, 16384, 32768, 65536, 1):
                    return True, f"Valid SQLite (Page Size: {page_size})"
            except Exception:
                pass
            return True, "SQLite database header verified"
        return False, "Invalid SQLite signature"

    elif ft in ("mp4", "mov"):
        if len(data) >= 8:
            box_len = struct.unpack(">I", data[0:4])[0]
            box_type = data[4:8]
            if box_type in (b"ftyp", b"moov", b"mdat", b"free", b"wide"):
                return True, f"Valid MP4/MOV atom ({box_type.decode('ascii', errors='ignore')})"
        return False, "Invalid MP4/MOV container"

    elif ft == "cctv":
        if data.startswith(b"\x78\x56\x34\x12H264"):
            return True, "Valid Xiongmai H.264 DVR Stream"
        return False, "Invalid CCTV Stream signature"

    elif ft == "mp3":
        if data.startswith(b"ID3") or data.startswith(b"\xFF\xFB") or data.startswith(b"\xFF\xF3") or data.startswith(b"\xFF\xF2"):
            return True, "Valid MP3 Audio Stream"
        return False, "Invalid MP3 stream header"

    elif ft == "wav":
        if data.startswith(b"RIFF") and len(data) >= 12 and data[8:12] == b"WAVE":
            return True, "Valid WAV Audio RIFF"
        return False, "Invalid WAV audio structure"

    elif ft == "flac":
        if data.startswith(b"fLaC"):
            return True, "Valid FLAC Lossless Audio"
        return False, "Invalid FLAC stream header"

    elif ft == "ogg":
        if data.startswith(b"OggS"):
            return True, "Valid OGG Audio Container"
        return False, "Invalid OGG container"

    elif ft == "m4a":
        if len(data) >= 8 and (b"ftyp" in data[:12] or b"moov" in data[:12]):
            return True, "Valid M4A / AAC Audio Container"
        return False, "Invalid M4A audio container"

    # Default for other types: Check non-empty
    return True, "Raw Stream Extracted"
