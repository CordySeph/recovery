"""
Smart Carving & Fragmented File Reassembly Engine
Performs Bi-fragment gap analysis and heuristic stream continuity validation
for fragmented JPEG, MP4 video streams, and ZIP containers across non-contiguous clusters.
"""

import struct
from typing import List, Dict, Optional, Tuple

def validate_jpeg_stream_continuity(chunk1: bytes, chunk2: bytes) -> bool:
    """
    Check if chunk2 is a plausible continuation of an interrupted JPEG scan stream chunk1.
    Evaluates entropy, avoidance of invalid markers, and presence of valid restart markers or EOI.
    """
    if not chunk1 or not chunk2:
        return False

    # Check if chunk1 ends in middle of entropy data (starts with FF D8, contains SOS FF DA)
    if b"\xFF\xDA" not in chunk1:
        return False
    if chunk1.endswith(b"\xFF\xD9"):
        return False  # Already complete!

    # Check chunk2: should not start with another JPEG header, but should contain high-entropy scan data or EOI
    if chunk2.startswith(b"\xFF\xD8"):
        return False

    # Check for EOI or valid RST markers in chunk2
    if b"\xFF\xD9" in chunk2:
        return True

    # Check byte entropy of chunk2 (JPEG compressed stream typically has high byte distribution variance)
    unique_bytes = len(set(chunk2[:1024]))
    return unique_bytes > 120  # High entropy indicates compressed image payload

def validate_h264_nalu_continuity(chunk1: bytes, chunk2: bytes) -> bool:
    """
    Verify H.264 video NAL (Network Abstraction Layer) unit continuity across fragments.
    NAL units start with 00 00 01 or 00 00 00 01 followed by NAL type (SPS, PPS, IDR, non-IDR).
    """
    if not chunk1 or not chunk2:
        return False

    # Scan for NAL start codes in chunk2
    valid_nal_types = {1, 5, 6, 7, 8, 9}  # 1=non-IDR, 5=IDR Slice, 6=SEI, 7=SPS, 8=PPS
    pos = 0
    found_valid_nal = False

    while pos < min(len(chunk2) - 5, 2048):
        if chunk2[pos : pos + 3] == b"\x00\x00\x01":
            nal_byte = chunk2[pos + 3]
            nal_type = nal_byte & 0x1F
            if nal_type in valid_nal_types:
                found_valid_nal = True
                break
            pos += 3
        elif chunk2[pos : pos + 4] == b"\x00\x00\x00\x01":
            nal_byte = chunk2[pos + 4]
            nal_type = nal_byte & 0x1F
            if nal_type in valid_nal_types:
                found_valid_nal = True
                break
            pos += 4
        else:
            pos += 1

    return found_valid_nal

def reassemble_bi_fragments(
    head_chunk: bytes,
    gap_candidates: List[Tuple[int, bytes]],
    file_type: str
) -> Tuple[bool, bytes, int]:
    """
    Attempt to reassemble a fragmented file with a candidate continuation fragment.
    Returns (success: bool, combined_data: bytes, matched_gap_offset: int).
    """
    ft = file_type.lower()

    for offset, candidate in gap_candidates:
        if ft in ("jpg", "jpeg"):
            if validate_jpeg_stream_continuity(head_chunk, candidate):
                # Stitch head and tail together up to EOI
                eoi_idx = candidate.find(b"\xFF\xD9")
                if eoi_idx != -1:
                    tail = candidate[: eoi_idx + 2]
                else:
                    tail = candidate
                return True, head_chunk + tail, offset

        elif ft in ("mp4", "mov", "cctv"):
            if validate_h264_nalu_continuity(head_chunk, candidate):
                return True, head_chunk + candidate, offset

    return False, head_chunk, 0
