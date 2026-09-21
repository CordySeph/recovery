"""
Hash-Based File Deduplication Engine
"""

import hashlib
from typing import Dict, Set, Tuple

class HashDeduplicator:
    """
    Tracks and filters duplicate files based on MD5 checksums.
    Prevents duplicate files from wasting disk space on fragmented drives.
    """
    def __init__(self, enabled: bool = True):
        self.enabled = enabled
        self.seen_hashes: Set[str] = set()
        self.total_checked = 0
        self.duplicate_count = 0
        self.bytes_saved = 0

    def compute_hash(self, data: bytes) -> str:
        """Compute MD5 hash string for binary data."""
        return hashlib.md5(data).hexdigest()

    def compute_sha256(self, data: bytes) -> str:
        """Compute SHA-256 hash string for forensic validation."""
        return hashlib.sha256(data).hexdigest()

    def compute_hashes(self, data: bytes) -> Tuple[str, str]:
        """Compute both MD5 and SHA-256 hashes simultaneously."""
        return hashlib.md5(data).hexdigest(), hashlib.sha256(data).hexdigest()

    def check_and_register(self, data: bytes) -> Tuple[bool, str, str]:
        """
        Check if data is unique or duplicate.
        Returns (is_unique: bool, md5_hash: str, sha256_hash: str).
        """
        self.total_checked += 1
        md5_hash, sha256_hash = self.compute_hashes(data)

        if not self.enabled:
            return True, md5_hash, sha256_hash

        if md5_hash in self.seen_hashes:
            self.duplicate_count += 1
            self.bytes_saved += len(data)
            return False, md5_hash, sha256_hash

        self.seen_hashes.add(md5_hash)
        return True, md5_hash, sha256_hash

    def check_and_register_hash(self, md5_hash: str, sha256_hash: str = "", size_bytes: int = 0) -> bool:
        """
        Check if MD5 hash is unique or duplicate using pre-computed hash string.
        Returns True if unique, False if duplicate.
        """
        self.total_checked += 1
        if not self.enabled or not md5_hash:
            return True

        if md5_hash in self.seen_hashes:
            self.duplicate_count += 1
            self.bytes_saved += size_bytes
            return False

        self.seen_hashes.add(md5_hash)
        return True

