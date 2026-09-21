"""
File System Parser & Original Filename Recovery Module
Recovers original filenames and directory paths from remnant FAT32, exFAT, and NTFS $MFT structures.
Maps physical byte offsets on disk to their original filenames.
"""

import os
import struct
import datetime
from typing import Dict, List, Optional, Tuple

class FileSystemMetadataMap:
    def __init__(self):
        # Map: offset -> dict(filename, path, size, timestamp)
        self.offset_map: Dict[int, Dict] = {}
        self.size_name_map: Dict[int, List[Dict]] = {}
        self.records_found = 0

    def add_record(self, offset: int, filename: str, path: str = "", size: int = 0, timestamp: str = ""):
        if not filename or len(filename) < 1:
            return
        rec = {
            "filename": filename,
            "path": path,
            "size": size,
            "timestamp": timestamp,
            "offset": offset
        }
        if offset > 0:
            self.offset_map[offset] = rec
        if size > 0:
            if size not in self.size_name_map:
                self.size_name_map[size] = []
            self.size_name_map[size].append(rec)
        self.records_found += 1

    def match_carved_file(self, offset: int, file_type: str, size: int) -> Optional[Dict]:
        """
        Attempt to match a carved file with original filename metadata.
        1. Exact byte offset match
        2. Cluster-boundary proximity match (+/- 4KB, 8KB, 32KB, 64KB)
        3. Exact size match with same extension
        """
        # 1. Exact match
        if offset in self.offset_map:
            return self.offset_map[offset]

        # 2. Cluster tolerance search (FAT/NTFS clusters usually 4KB-64KB aligned)
        for delta in (512, 1024, 2048, 4096, 8192, 16384, 32768, 65536):
            if (offset - delta) in self.offset_map:
                return self.offset_map[offset - delta]
            if (offset + delta) in self.offset_map:
                return self.offset_map[offset + delta]

        # 3. File size match with matching extension
        if size in self.size_name_map:
            candidates = self.size_name_map[size]
            for cand in candidates:
                if cand["filename"].lower().endswith(f".{file_type.lower()}"):
                    return cand

        return None

def parse_ntfs_mft_record(record_bytes: bytes, base_record_offset: int = 0) -> Optional[Dict]:
    """
    Parse a 1024-byte NTFS MFT Record (FILE header).
    Extracts original Unicode filename, file size, and timestamps.
    """
    if len(record_bytes) < 1024 or not record_bytes.startswith(b"FILE"):
        return None

    try:
        # Check flags (bit 0 = in use, bit 1 = directory)
        flags = struct.unpack("<H", record_bytes[22:24])[0]
        is_in_use = bool(flags & 0x01)
        is_directory = bool(flags & 0x02)

        first_attr_offset = struct.unpack("<H", record_bytes[20:22])[0]
        offset = first_attr_offset
        record_len = len(record_bytes)

        filename = ""
        file_size = 0
        timestamp = ""
        data_offset = 0

        # Iterate through MFT attributes
        while offset < record_len - 8:
            attr_type = struct.unpack("<I", record_bytes[offset : offset + 4])[0]
            if attr_type == 0xFFFFFFFF or attr_type == 0:
                break

            attr_len = struct.unpack("<I", record_bytes[offset + 4 : offset + 8])[0]
            if attr_len <= 0 or offset + attr_len > record_len:
                break

            non_resident_flag = record_bytes[offset + 8]

            # $STANDARD_INFORMATION (0x10) - Timestamps
            if attr_type == 0x10 and non_resident_flag == 0:
                content_offset = struct.unpack("<H", record_bytes[offset + 20 : offset + 22])[0]
                ts_pos = offset + content_offset
                if ts_pos + 8 <= record_len:
                    filetime = struct.unpack("<Q", record_bytes[ts_pos : ts_pos + 8])[0]
                    # Windows FILETIME (100-ns intervals since Jan 1, 1601)
                    if filetime > 116444736000000000:
                        unix_ts = (filetime - 116444736000000000) / 10000000
                        try:
                            dt = datetime.datetime.fromtimestamp(unix_ts, datetime.timezone.utc)
                            timestamp = dt.strftime("%Y-%m-%d %H:%M:%S")
                        except Exception:
                            pass

            # $FILE_NAME (0x30) - Original Filename & Real Size
            elif attr_type == 0x30 and non_resident_flag == 0:
                content_offset = struct.unpack("<H", record_bytes[offset + 20 : offset + 22])[0]
                fn_pos = offset + content_offset
                if fn_pos + 66 <= record_len:
                    real_size = struct.unpack("<Q", record_bytes[fn_pos + 48 : fn_pos + 56])[0]
                    fn_len = record_bytes[fn_pos + 64]
                    fn_str_pos = fn_pos + 66
                    if fn_str_pos + (fn_len * 2) <= record_len:
                        parsed_name = record_bytes[fn_str_pos : fn_str_pos + (fn_len * 2)].decode("utf-16le", errors="ignore")
                        # Avoid DOS 8.3 short name duplicates if long name already set
                        if not filename or len(parsed_name) > len(filename):
                            filename = parsed_name
                            file_size = real_size

            # $DATA (0x80) - Data payload or runlist
            elif attr_type == 0x80:
                if non_resident_flag == 0:
                    content_offset = struct.unpack("<H", record_bytes[offset + 20 : offset + 22])[0]
                    data_offset = base_record_offset + offset + content_offset
                else:
                    # Non-resident data runs
                    real_size = struct.unpack("<Q", record_bytes[offset + 48 : offset + 56])[0]
                    if real_size > 0 and file_size == 0:
                        file_size = real_size

            offset += attr_len

        if filename and not is_directory:
            return {
                "filename": filename,
                "size": file_size,
                "timestamp": timestamp,
                "is_directory": is_directory,
                "offset": data_offset or base_record_offset,
            }
    except Exception:
        pass

    return None

def parse_fat_directory_entries(chunk: bytes, base_offset: int) -> List[Dict]:
    """
    Parse FAT32 / VFAT Directory Entries (Short 8.3 + LFN Long File Names).
    """
    records = []
    idx = 0
    chunk_len = len(chunk)
    lfn_parts = []

    while idx <= chunk_len - 32:
        entry = chunk[idx : idx + 32]
        first_byte = entry[0]

        if first_byte == 0x00:
            # End of directory table
            idx += 32
            lfn_parts.clear()
            continue
        elif first_byte == 0xE5:
            # Deleted entry marker
            idx += 32
            lfn_parts.clear()
            continue

        attr = entry[11]

        # LFN (Long File Name) Entry
        if attr == 0x0F:
            try:
                # LFN stores 13 UTF-16LE characters per 32-byte record
                part = (
                    entry[1:11].decode("utf-16le", errors="ignore") +
                    entry[14:26].decode("utf-16le", errors="ignore") +
                    entry[28:32].decode("utf-16le", errors="ignore")
                )
                lfn_parts.insert(0, part.split("\x00")[0].split("\xff")[0])
            except Exception:
                pass
            idx += 32
            continue

        # Standard 8.3 File Entry
        if not (attr & 0x08) and not (attr & 0x10):  # Not Volume Label, Not Subdirectory
            try:
                name_short = entry[0:8].decode("latin-1", errors="ignore").strip()
                ext_short = entry[8:11].decode("latin-1", errors="ignore").strip()
                
                if lfn_parts:
                    full_filename = "".join(lfn_parts).strip()
                    lfn_parts.clear()
                else:
                    full_filename = f"{name_short}.{ext_short}" if ext_short else name_short

                file_size = struct.unpack("<I", entry[28:32])[0]
                cluster_high = struct.unpack("<H", entry[20:22])[0]
                cluster_low = struct.unpack("<H", entry[26:28])[0]
                start_cluster = (cluster_high << 16) | cluster_low

                # Time parsing
                time_val = struct.unpack("<H", entry[22:24])[0]
                date_val = struct.unpack("<H", entry[24:26])[0]
                year = ((date_val >> 9) & 0x7F) + 1980
                month = (date_val >> 5) & 0x0F
                day = date_val & 0x1F
                hour = (time_val >> 11) & 0x1F
                minute = (time_val >> 5) & 0x3F
                second = (time_val & 0x1F) * 2

                ts_str = ""
                if 1980 <= year <= 2050 and 1 <= month <= 12 and 1 <= day <= 31:
                    ts_str = f"{year:04d}-{month:02d}-{day:02d} {hour:02d}:{minute:02d}:{second:02d}"

                if full_filename and "." in full_filename and file_size > 0:
                    records.append({
                        "filename": full_filename,
                        "size": file_size,
                        "start_cluster": start_cluster,
                        "timestamp": ts_str,
                        "offset": base_offset + idx,
                    })
            except Exception:
                pass
        
        lfn_parts.clear()
        idx += 32

    return records

def parse_ext4_directory_block(block_bytes: bytes, base_offset: int = 0) -> List[Dict]:
    """
    Parse a Linux EXT4 directory block (linear directory or unindexed leaf).
    Extracts inode, file type, and original filenames.
    """
    records = []
    block_len = len(block_bytes)
    idx = 0

    while idx <= block_len - 8:
        try:
            inode = struct.unpack("<I", block_bytes[idx : idx + 4])[0]
            rec_len = struct.unpack("<H", block_bytes[idx + 4 : idx + 6])[0]
            name_len = block_bytes[idx + 6]
            file_type = block_bytes[idx + 7]

            if rec_len < 8 or idx + rec_len > block_len:
                break

            if inode != 0 and 1 <= name_len <= (rec_len - 8):
                name_bytes = block_bytes[idx + 8 : idx + 8 + name_len]
                try:
                    name_str = name_bytes.decode("utf-8", errors="ignore").strip()
                    if name_str not in (".", "..") and len(name_str) > 0:
                        records.append({
                            "filename": name_str,
                            "inode": inode,
                            "file_type_code": file_type,
                            "offset": base_offset + idx,
                            "size": 0,
                            "timestamp": ""
                        })
                except Exception:
                    pass

            idx += rec_len
        except Exception:
            break

    return records

def scan_filesystem_structures_in_chunk(chunk: bytes, base_offset: int) -> List[Dict]:
    """
    Search for NTFS MFT records, FAT directory structures, and Linux EXT4 directory blocks in a given chunk.
    """
    results = []
    chunk_len = len(chunk)

    # 1. Search for NTFS MFT records (FILE)
    idx = 0
    while True:
        pos = chunk.find(b"FILE0", idx)
        if pos == -1:
            pos = chunk.find(b"FILE*", idx)
            if pos == -1:
                break
        
        if pos + 1024 <= chunk_len:
            mft_rec = parse_ntfs_mft_record(chunk[pos : pos + 1024], base_offset + pos)
            if mft_rec:
                results.append(mft_rec)
        idx = pos + 1024

    # 2. Search for FAT directory entries
    fat_recs = parse_fat_directory_entries(chunk, base_offset)
    results.extend(fat_recs)

    # 3. Search for EXT4 directory blocks
    # Look for common EXT4 directory patterns or block alignment
    pos = 0
    while pos <= chunk_len - 4096:
        # Standard EXT4 directory blocks start with '.' (inode > 0, rec_len >= 12, name_len=1, name='.')
        if (chunk[pos + 4 : pos + 6] == b"\x0c\x00" and chunk[pos + 6 : pos + 8] == b"\x01\x02" and chunk[pos + 8] == ord('.')):
            ext4_recs = parse_ext4_directory_block(chunk[pos : pos + 4096], base_offset + pos)
            if ext4_recs:
                results.extend(ext4_recs)
            pos += 4096
            continue
        pos += 512

    # 4. Search for Apple APFS Containers & Volumes
    try:
        from recovery_engine.apfs_parser import scan_apfs_structures_in_chunk
        apfs_recs = scan_apfs_structures_in_chunk(chunk, base_offset)
        results.extend(apfs_recs)
    except Exception:
        pass

    return results
