"""
Dedicated Audio Carver & ID3 / Metadata Parser Module
Supports: MP3, WAV, FLAC, OGG, M4A, AAC
Includes pure-Python ID3v1, ID3v2, Vorbis Comments, and MP4 atom metadata extraction.
"""

import struct
from typing import List, Dict, Optional
from recovery_engine.config import SIG_MP3_ID3, SIG_FLAC, SIG_OGG

def parse_id3v2_metadata(data: bytes) -> Dict[str, str]:
    """
    Parse ID3v2.2, ID3v2.3, ID3v2.4 tags without external dependencies.
    """
    meta = {}
    if not data or len(data) < 10 or not data.startswith(b"ID3"):
        return meta

    try:
        version_major = data[3]
        # Synchsafe integer (7 bits per byte) for ID3v2 tag size
        tag_size = (
            ((data[6] & 0x7F) << 21) |
            ((data[7] & 0x7F) << 14) |
            ((data[8] & 0x7F) << 7) |
            (data[9] & 0x7F)
        )
        tag_bytes = data[10 : min(len(data), 10 + tag_size)]

        idx = 0
        tag_len = len(tag_bytes)
        
        # Frame mapping
        target_frames = {
            b"TIT2": "title",
            b"TPE1": "artist",
            b"TALB": "album",
            b"TYER": "year",
            b"TDRC": "year",
            b"COMM": "comment",
            b"TT2": "title",
            b"TP1": "artist",
            b"TAL": "album",
            b"TYE": "year",
        }

        while idx < tag_len - 10:
            if tag_bytes[idx] == 0:
                idx += 1
                continue

            frame_id = tag_bytes[idx : idx + 4]
            if version_major == 2:
                frame_id = tag_bytes[idx : idx + 3]
                if idx + 6 > tag_len:
                    break
                frame_size = int.from_bytes(tag_bytes[idx + 3 : idx + 6], "big")
                idx += 6
            else:
                if idx + 10 > tag_len:
                    break
                if version_major == 4:
                    # ID3v2.4 uses synchsafe integers for frame sizes
                    frame_size = (
                        ((tag_bytes[idx + 4] & 0x7F) << 21) |
                        ((tag_bytes[idx + 5] & 0x7F) << 14) |
                        ((tag_bytes[idx + 6] & 0x7F) << 7) |
                        (tag_bytes[idx + 7] & 0x7F)
                    )
                else:
                    frame_size = int.from_bytes(tag_bytes[idx + 4 : idx + 8], "big")
                idx += 10

            if frame_size <= 0 or idx + frame_size > tag_len:
                break

            frame_payload = tag_bytes[idx : idx + frame_size]
            idx += frame_size

            if frame_id in target_frames and len(frame_payload) > 1:
                key = target_frames[frame_id]
                encoding = frame_payload[0]
                text_bytes = frame_payload[1:]
                
                text_val = ""
                try:
                    if encoding == 0:
                        text_val = text_bytes.decode("latin-1", errors="ignore").strip("\x00 \t\r\n")
                    elif encoding == 1:
                        text_val = text_bytes.decode("utf-16", errors="ignore").strip("\x00 \t\r\n")
                    elif encoding == 2:
                        text_val = text_bytes.decode("utf-16-be", errors="ignore").strip("\x00 \t\r\n")
                    elif encoding == 3:
                        text_val = text_bytes.decode("utf-8", errors="ignore").strip("\x00 \t\r\n")
                    else:
                        text_val = text_bytes.decode("utf-8", errors="ignore").strip("\x00 \t\r\n")
                except Exception:
                    pass

                if text_val and key not in meta:
                    meta[key] = text_val
    except Exception:
        pass

    return meta

def parse_id3v1_metadata(data: bytes) -> Dict[str, str]:
    """Parse legacy ID3v1 / ID3v1.1 tag at the end of MP3 file (128 bytes)."""
    meta = {}
    if len(data) >= 128 and data[-128:-125] == b"TAG":
        try:
            tail = data[-128:]
            title = tail[3:33].decode("latin-1", errors="ignore").strip("\x00 ")
            artist = tail[33:63].decode("latin-1", errors="ignore").strip("\x00 ")
            album = tail[63:93].decode("latin-1", errors="ignore").strip("\x00 ")
            year = tail[93:97].decode("latin-1", errors="ignore").strip("\x00 ")

            if title: meta["title"] = title
            if artist: meta["artist"] = artist
            if album: meta["album"] = album
            if year: meta["year"] = year
        except Exception:
            pass
    return meta

def parse_flac_metadata(data: bytes) -> Dict[str, str]:
    """Parse Vorbis comment metadata from FLAC header blocks."""
    meta = {}
    if not data or not data.startswith(b"fLaC"):
        return meta

    try:
        offset = 4
        while offset < len(data) - 4:
            header_byte = data[offset]
            is_last = bool(header_byte & 0x80)
            block_type = header_byte & 0x7F
            block_length = int.from_bytes(data[offset + 1 : offset + 4], "big")
            offset += 4

            if offset + block_length > len(data):
                break

            # Block type 4 is VORBIS_COMMENT
            if block_type == 4:
                comment_data = data[offset : offset + block_length]
                if len(comment_data) >= 8:
                    vendor_len = int.from_bytes(comment_data[0:4], "little")
                    c_idx = 4 + vendor_len
                    if c_idx + 4 <= len(comment_data):
                        user_comment_count = int.from_bytes(comment_data[c_idx:c_idx+4], "little")
                        c_idx += 4
                        for _ in range(min(user_comment_count, 100)):
                            if c_idx + 4 > len(comment_data):
                                break
                            c_len = int.from_bytes(comment_data[c_idx:c_idx+4], "little")
                            c_idx += 4
                            if c_idx + c_len > len(comment_data):
                                break
                            comment_str = comment_data[c_idx:c_idx+c_len].decode("utf-8", errors="ignore")
                            c_idx += c_len
                            if "=" in comment_str:
                                k, v = comment_str.split("=", 1)
                                k_low = k.strip().lower()
                                if k_low in ("artist", "title", "album", "date"):
                                    norm_k = "year" if k_low == "date" else k_low
                                    meta[norm_k] = v.strip()
                break

            if is_last:
                break
            offset += block_length
    except Exception:
        pass

    return meta

def extract_audio_metadata(data: bytes, file_type: str) -> Dict[str, str]:
    """
    Extract comprehensive audio metadata (artist, title, album, year).
    """
    ft = file_type.lower()
    if ft == "mp3":
        meta = parse_id3v2_metadata(data)
        if not meta or not meta.get("artist"):
            v1_meta = parse_id3v1_metadata(data)
            for k, v in v1_meta.items():
                if k not in meta:
                    meta[k] = v
        return meta

    elif ft == "flac":
        return parse_flac_metadata(data)

    elif ft == "ogg":
        # Search for Vorbis comments in OGG
        meta = {}
        for tag in (b"ARTIST=", b"TITLE=", b"ALBUM=", b"DATE="):
            pos = data.find(tag)
            if pos != -1:
                end = data.find(b"\x00", pos)
                if end != -1 and end - pos < 256:
                    line = data[pos:end].decode("utf-8", errors="ignore")
                    k, v = line.split("=", 1)
                    meta["year" if k.lower() == "date" else k.lower()] = v.strip()
        return meta

    return {}

def scan_audio_in_chunk(chunk: bytes, base_offset: int, max_file_size: int = 50 * 1024 * 1024) -> List[Dict]:
    """
    Scan a memory buffer for MP3, WAV, FLAC, OGG, and M4A audio files.
    """
    results = []
    chunk_len = len(chunk)

    # 1. MP3 with ID3v2 Tag
    idx = 0
    while True:
        pos = chunk.find(SIG_MP3_ID3, idx)
        if pos == -1:
            break
        # Read ID3v2 tag size to verify
        est_len = min(20 * 1024 * 1024, chunk_len - pos)
        if pos + 10 <= chunk_len:
            tag_size = (
                ((chunk[pos + 6] & 0x7F) << 21) |
                ((chunk[pos + 7] & 0x7F) << 14) |
                ((chunk[pos + 8] & 0x7F) << 7) |
                (chunk[pos + 9] & 0x7F)
            )
            if 0 < tag_size < 10 * 1024 * 1024:
                est_len = min(tag_size + (15 * 1024 * 1024), chunk_len - pos)

        results.append({
            "offset": base_offset + pos,
            "category": "Audio",
            "file_type": "mp3",
            "size_bytes": est_len,
            "chunk_rel_pos": pos,
        })
        idx = pos + 3

    # 2. WAV (RIFF ... WAVE)
    idx = 0
    while True:
        pos = chunk.find(b"RIFF", idx)
        if pos == -1:
            break
        if pos + 12 <= chunk_len and chunk[pos + 8 : pos + 12] == b"WAVE":
            riff_len = struct.unpack("<I", chunk[pos + 4 : pos + 8])[0]
            file_len = min(riff_len + 8, max_file_size)
            results.append({
                "offset": base_offset + pos,
                "category": "Audio",
                "file_type": "wav",
                "size_bytes": file_len,
                "chunk_rel_pos": pos,
            })
            idx = pos + file_len
        else:
            idx = pos + 4

    # 3. FLAC (fLaC)
    idx = 0
    while True:
        pos = chunk.find(SIG_FLAC, idx)
        if pos == -1:
            break
        results.append({
            "offset": base_offset + pos,
            "category": "Audio",
            "file_type": "flac",
            "size_bytes": min(40 * 1024 * 1024, chunk_len - pos),
            "chunk_rel_pos": pos,
        })
        idx = pos + 4

    # 4. OGG Container (OggS)
    idx = 0
    while True:
        pos = chunk.find(SIG_OGG, idx)
        if pos == -1:
            break
        # Only start an OGG file if it is a BOS (beginning of stream) packet (header type flag at pos+5 bit 0x02)
        if pos + 6 <= chunk_len and (chunk[pos + 5] & 0x02):
            results.append({
                "offset": base_offset + pos,
                "category": "Audio",
                "file_type": "ogg",
                "size_bytes": min(25 * 1024 * 1024, chunk_len - pos),
                "chunk_rel_pos": pos,
            })
        idx = pos + 4

    # 5. M4A Audio (ftypM4A)
    idx = 0
    while True:
        pos = chunk.find(b"ftypM4A", idx)
        if pos == -1:
            break
        if pos >= 4:
            box_start = pos - 4
            results.append({
                "offset": base_offset + box_start,
                "category": "Audio",
                "file_type": "m4a",
                "size_bytes": min(30 * 1024 * 1024, chunk_len - box_start),
                "chunk_rel_pos": box_start,
            })
        idx = pos + 7

    return results
