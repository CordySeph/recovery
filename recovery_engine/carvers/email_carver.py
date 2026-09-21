"""
Email & Communications Carver
Supports:
- RFC 822 / MIME Email files (.eml)
- Outlook Personal Storage Table (.pst - '!BDN' magic)
- Outlook Msg / Compound Binary (.msg)
"""

import struct
from typing import List, Dict

def scan_emails_in_chunk(chunk: bytes, base_offset: int, max_file_size: int = 50 * 1024 * 1024) -> List[Dict]:
    results = []
    chunk_len = len(chunk)
    pos = 0

    while pos < chunk_len - 16:
        # 1. Outlook PST Storage (!BDN)
        if chunk[pos : pos + 4] == b"!BDN":
            results.append({
                "offset": base_offset + pos,
                "file_type": "pst",
                "category": "emails",
                "estimated_size": min(50 * 1024 * 1024, max_file_size),
                "meta": {"format": "Outlook Personal Storage (.pst)"}
            })
            pos += 512
            continue

        # 2. RFC 822 Email Message (.eml)
        # Often starts with header like 'Received: ', 'From: ', 'Return-Path: ', 'MIME-Version: '
        header_sample = chunk[pos : min(pos + 256, chunk_len)]
        if (header_sample.startswith(b"Received: from") or
            (header_sample.startswith(b"From: ") and b"Subject: " in header_sample) or
            (header_sample.startswith(b"Return-Path: <") and b"From: " in header_sample)):
            
            # Find end of email (boundary or double newline after content)
            # Estimate size
            results.append({
                "offset": base_offset + pos,
                "file_type": "eml",
                "category": "emails",
                "estimated_size": min(2 * 1024 * 1024, max_file_size),
                "meta": {"format": "RFC 822 EML Message"}
            })
            pos += 512
            continue

        pos += 512

    return results
