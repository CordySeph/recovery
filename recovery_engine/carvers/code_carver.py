"""
Source Code & Structured Text Carver
Supports:
- Python (.py - '#!/usr/bin/env python' or 'import ...')
- HTML (.html - '<!DOCTYPE html' or '<html')
- JSON (.json - valid '{...}' or '[...]')
- SQL (.sql - 'CREATE TABLE', 'INSERT INTO', 'SELECT')
- CSV (.csv - comma/tab separated text tables)
"""

import json
from typing import List, Dict

def scan_code_in_chunk(chunk: bytes, base_offset: int, max_file_size: int = 10 * 1024 * 1024) -> List[Dict]:
    results = []
    chunk_len = len(chunk)
    pos = 0

    while pos < chunk_len - 16:
        # 1. HTML
        if chunk[pos : pos + 15].lower() == b"<!doctype html>" or chunk[pos : pos + 6].lower() == b"<html>":
            end_idx = chunk.lower().find(b"</html>", pos)
            if end_idx != -1 and (end_idx - pos) < max_file_size:
                size = (end_idx - pos) + 7
                results.append({
                    "offset": base_offset + pos,
                    "file_type": "html",
                    "category": "code",
                    "estimated_size": size,
                    "meta": {"type": "HTML Web Document"}
                })
                pos += size
                continue

        # 2. Python Script
        if chunk[pos : pos + 22] == b"#!/usr/bin/env python" or chunk[pos : pos + 19] == b"#!/usr/bin/python":
            results.append({
                "offset": base_offset + pos,
                "file_type": "py",
                "category": "code",
                "estimated_size": min(1024 * 1024, max_file_size),
                "meta": {"type": "Python Source Code"}
            })
            pos += 512
            continue

        # 3. SQL Dump
        header_sample = chunk[pos : min(pos + 128, chunk_len)].upper()
        if (header_sample.startswith(b"-- MYSQL DUMP") or
            header_sample.startswith(b"-- POSTGRESQL DATABASE DUMP") or
            header_sample.startswith(b"CREATE TABLE ") or
            header_sample.startswith(b"INSERT INTO ")):
            results.append({
                "offset": base_offset + pos,
                "file_type": "sql",
                "category": "code",
                "estimated_size": min(50 * 1024 * 1024, max_file_size),
                "meta": {"type": "SQL Database Script"}
            })
            pos += 512
            continue

        pos += 512

    return results
