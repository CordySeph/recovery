"""
Graphics & Vector Design File Carver
Supports:
- Adobe Photoshop (.psd - 8BPS header)
- Adobe Illustrator / PostScript (.ai / .eps - %!PS-Adobe header)
- Scalable Vector Graphics (.svg - <svg header)
"""

import struct
from typing import List, Dict, Optional

def scan_graphics_in_chunk(chunk: bytes, base_offset: int, max_file_size: int = 100 * 1024 * 1024) -> List[Dict]:
    results = []
    chunk_len = len(chunk)
    pos = 0

    while pos < chunk_len - 16:
        # 1. Adobe Photoshop (.psd)
        # Signature: '8BPS' (0x38, 0x42, 0x50, 0x53), Version: 1 or 2
        if chunk[pos : pos + 4] == b"8BPS":
            if pos + 26 <= chunk_len:
                version = struct.unpack(">H", chunk[pos + 4 : pos + 6])[0]
                if version in (1, 2):  # 1 = PSD, 2 = PSB (Large Document)
                    channels = struct.unpack(">H", chunk[pos + 12 : pos + 14])[0]
                    height = struct.unpack(">I", chunk[pos + 14 : pos + 18])[0]
                    width = struct.unpack(">I", chunk[pos + 18 : pos + 22])[0]
                    depth = struct.unpack(">H", chunk[pos + 22 : pos + 24])[0]
                    color_mode = struct.unpack(">H", chunk[pos + 24 : pos + 26])[0]

                    if 1 <= width <= 300000 and 1 <= height <= 300000 and channels >= 1:
                        results.append({
                            "offset": base_offset + pos,
                            "file_type": "psd",
                            "category": "graphics",
                            "estimated_size": min(50 * 1024 * 1024, max_file_size),
                            "meta": {
                                "width": width,
                                "height": height,
                                "channels": channels,
                                "depth": depth,
                                "color_mode": color_mode
                            }
                        })
                        pos += 26
                        continue

        # 2. Adobe Illustrator / PostScript (.ai / .eps)
        # Signature: '%!PS-Adobe'
        if chunk[pos : pos + 11] == b"%!PS-Adobe-":
            # Search for %%EOF
            eof_idx = chunk.find(b"%%EOF", pos)
            if eof_idx != -1 and (eof_idx - pos) < max_file_size:
                size = (eof_idx - pos) + 5
            else:
                size = min(10 * 1024 * 1024, max_file_size)

            is_ai = b"Creator: Adobe Illustrator" in chunk[pos : min(pos + 2048, chunk_len)]
            ft = "ai" if is_ai else "eps"

            results.append({
                "offset": base_offset + pos,
                "file_type": ft,
                "category": "graphics",
                "estimated_size": size,
                "meta": {"type": "PostScript Vector Design"}
            })
            pos += 11
            continue

        # 3. Scalable Vector Graphics (.svg)
        # Signature: '<svg' or '<?xml' followed shortly by '<svg'
        if chunk[pos : pos + 4] == b"<svg" or (chunk[pos : pos + 5] == b"<?xml" and b"<svg" in chunk[pos : min(pos + 256, chunk_len)]):
            close_tag = chunk.find(b"</svg>", pos)
            if close_tag != -1 and (close_tag - pos) < 5 * 1024 * 1024:
                size = (close_tag - pos) + 6
                results.append({
                    "offset": base_offset + pos,
                    "file_type": "svg",
                    "category": "graphics",
                    "estimated_size": size,
                    "meta": {"type": "Vector Graphics"}
                })
                pos += size
                continue

        pos += 1

    return results
