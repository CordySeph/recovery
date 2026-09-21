"""
Document File Carver (PDF, DOCX, XLSX, PPTX)
"""

from typing import List, Dict
from recovery_engine.config import SIG_PDF, SIG_ZIP

def scan_documents_in_chunk(chunk: bytes, base_offset: int, max_file_size: int = 50 * 1024 * 1024) -> List[Dict]:
    """
    Scan a memory buffer for PDF and Office XML documents (DOCX, XLSX, PPTX).
    """
    results = []
    chunk_len = len(chunk)

    # 1. PDF Document Scanner
    idx = 0
    while True:
        pos = chunk.find(SIG_PDF, idx)
        if pos == -1:
            break
        
        search_limit = min(chunk_len, pos + max_file_size)
        eof_pos = chunk.find(b"%%EOF", pos + 5)
        
        file_len = (eof_pos + 5 - pos) if (eof_pos != -1 and eof_pos < search_limit) else min(25 * 1024 * 1024, chunk_len - pos)
        
        results.append({
            "offset": base_offset + pos,
            "category": "Documents",
            "file_type": "pdf",
            "size_bytes": file_len,
            "chunk_rel_pos": pos,
        })
        idx = pos + 5

    # 2. Office OpenXML Documents (DOCX, XLSX, PPTX based on ZIP PK\x03\x04)
    idx = 0
    while True:
        pos = chunk.find(SIG_ZIP, idx)
        if pos == -1:
            break
        
        # Check within next 2KB for Office Content Types
        sample = chunk[pos : min(chunk_len, pos + 2048)]
        ext = None
        if b"[Content_Types].xml" in sample:
            if b"word/" in sample:
                ext = "docx"
            elif b"xl/" in sample or b"worksheets/" in sample:
                ext = "xlsx"
            elif b"ppt/" in sample or b"presentation" in sample:
                ext = "pptx"

        if ext:
            eocd_pos = chunk.find(b"PK\x05\x06", pos + 30)
            file_len = (eocd_pos + 22 - pos) if (eocd_pos != -1 and (eocd_pos - pos) < max_file_size) else min(30 * 1024 * 1024, chunk_len - pos)
            results.append({
                "offset": base_offset + pos,
                "category": "Documents",
                "file_type": ext,
                "size_bytes": file_len,
                "chunk_rel_pos": pos,
            })
            idx = pos + file_len
        else:
            idx = pos + 4

    return results
