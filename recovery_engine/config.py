"""
Configuration, Constants, Signatures & Helper Utilities
"""

import os
import datetime

# Timezone (Default UTC+7 Bangkok)
TIMEZONE = datetime.timezone(datetime.timedelta(hours=7))

# Default buffer sizes
CHUNK_SIZE = 64 * 1024 * 1024  # 64 MB buffer per read for maximum I/O throughput
OVERLAP_SIZE = 2 * 1024 * 1024  # 2 MB overlap between chunks to avoid boundary misses
SECTOR_SIZE = 512              # Standard sector size for bad sector retry
DEFAULT_CORES = os.cpu_count() or 4

# Magic Signatures
MAGIC_CCTV_H264 = b"\x78\x56\x34\x12H264"
SIG_JPEG = b"\xFF\xD8\xFF"
SIG_PNG = b"\x89PNG\r\n\x1a\n"
SIG_GIF87 = b"GIF87a"
SIG_GIF89 = b"GIF89a"
SIG_WEBP_RIFF = b"RIFF"
SIG_BMP = b"BM"
SIG_TIFF_LE = b"II*\x00"
SIG_TIFF_BE = b"MM\x00*"
SIG_CR2 = b"II*\x00CR\x02\x00"
SIG_PSD = b"8BPS"
SIG_PDF = b"%PDF-"
SIG_ZIP = b"PK\x03\x04"
SIG_7Z = b"7z\xBC\xAF\x27\x1C"
SIG_RAR_V4 = b"Rar!\x1A\x07\x00"
SIG_RAR_V5 = b"Rar!\x1A\x07\x01\x00"
SIG_SQLITE = b"SQLite format 3\x00"
SIG_MP3_ID3 = b"ID3"
SIG_FLAC = b"fLaC"
SIG_OGG = b"OggS"
SIG_AVI_RIFF = b"RIFF"
SIG_VMDK = b"KDMV"
SIG_VHDX = b"vhdxfile"
SIG_PST = b"!BDN"
SIG_EXT4_MAGIC = b"\x53\xEF" # 0xEF53 little endian at offset 0x38 in superblock
SIG_NTFS_MFT = b"FILE"
SIG_FAT_BOOT = b"\xEB\x58\x90"

# Supported File Categories
FILE_CATEGORIES = {
    "images": {"jpg", "jpeg", "png", "gif", "webp", "bmp", "heic"},
    "raw_photos": {"cr2", "cr3", "nef", "arw", "dng", "tiff"},
    "videos": {"mp4", "mov", "avi", "cctv"},
    "audio": {"mp3", "wav", "flac", "aac", "m4a", "ogg"},
    "documents": {"pdf", "docx", "xlsx", "pptx", "txt"},
    "graphics": {"psd", "ai", "eps", "svg"},
    "archives": {"zip", "7z", "rar", "tar", "gz"},
    "database": {"sqlite", "db"},
    "virtual_disks": {"vmdk", "vhd", "vhdx", "iso"},
    "emails": {"eml", "msg", "pst"},
    "code": {"py", "js", "html", "json", "csv", "sql"},
}

def parse_size_str(size_str: str) -> int:
    """
    Parse human-readable size string into bytes.
    e.g. '50k', '10m', '1.5g', '500b', '1000'
    """
    if not size_str:
        return 0
    s = size_str.strip().lower()
    if s.endswith("bytes") or s.endswith("byte"):
        s = s.rstrip("bytes").rstrip("byte").strip()
    multiplier = 1
    if s.endswith("k") or s.endswith("kb"):
        multiplier = 1024
        s = s.rstrip("kb").rstrip("k")
    elif s.endswith("m") or s.endswith("mb"):
        multiplier = 1024 * 1024
        s = s.rstrip("mb").rstrip("m")
    elif s.endswith("g") or s.endswith("gb"):
        multiplier = 1024 * 1024 * 1024
        s = s.rstrip("gb").rstrip("g")
    elif s.endswith("t") or s.endswith("tb"):
        multiplier = 1024 * 1024 * 1024 * 1024
        s = s.rstrip("tb").rstrip("t")
    elif s.endswith("b"):
        s = s.rstrip("b")
    
    try:
        return int(float(s) * multiplier)
    except ValueError:
        return 0
