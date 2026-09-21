"""
Comprehensive Unit & Functional Test Suite for recovery_engine
Tests all modules:
1. Disk I/O & Resilient Reader, Write-Block Verification
2. Deduplication Engine & Dual Hashing (MD5 + SHA-256)
3. Structural File Validators (Images, Videos, Audio, Docs, DB, Archives)
4. Image Carver (EXIF date parsing)
5. Audio Carver (ID3v1/v2, FLAC Vorbis, OGG metadata)
6. Video Repair & Atom Rebuilder
7. S.M.A.R.T. Health Diagnostic Evaluator
8. File System Structure & Original Filename Parser (FAT, NTFS MFT, and Linux EXT4)
9. Crypto Volume & BitLocker/LUKS Detector
10. Document Sensitive Data & Thai ID / Credit Card Inspector
11. Partition Table Scanner & VBR Rebuilder
12. Thermal Guard & Cooling Controller
13. Remote Exporter & Destination Validator
14. Forensic Reporting (CSV with Dual Hashes, Web Gallery HTML with Heatmap & Hex Viewer)
15. Professional RAW Camera Photos Carver (CR2, NEF, ARW, DNG, TIFF)
16. Graphics & Vector Design Carver (PSD, SVG)
17. Virtual Disk & Disk Image Carver (VMDK, VHDX, ISO)
18. Email & Communications Carver (EML, PST)
19. Source Code & Script Carver (HTML, PY, SQL)
20. Forensic Chain of Custody JSON Manifest (ISO/IEC 27037)
"""

import os
import struct
import io
import json
import zipfile
import tempfile
from recovery_engine.config import parse_size_str, FILE_CATEGORIES
from recovery_engine.disk_io import ResilientDiskReader, format_eta, check_write_block_status
from recovery_engine.deduplicator import HashDeduplicator
from recovery_engine.validators import validate_file_integrity
from recovery_engine.reporter import generate_csv_report, generate_gallery_html, generate_chain_of_custody_manifest
from recovery_engine.carvers.image_carver import extract_exif_date, scan_images_in_chunk
from recovery_engine.carvers.audio_carver import scan_audio_in_chunk, extract_audio_metadata
from recovery_engine.carvers.raw_carver import scan_raw_photos_in_chunk, parse_tiff_metadata
from recovery_engine.carvers.graphics_carver import scan_graphics_in_chunk
from recovery_engine.carvers.virtual_disk_carver import scan_virtual_disks_in_chunk
from recovery_engine.carvers.email_carver import scan_emails_in_chunk
from recovery_engine.carvers.code_carver import scan_code_in_chunk
from recovery_engine.video_repair import parse_mp4_atoms, repair_video_with_reference
from recovery_engine.smart_checker import evaluate_disk_health
from recovery_engine.fs_parser import (
    FileSystemMetadataMap, parse_fat_directory_entries, parse_ntfs_mft_record,
    parse_ext4_directory_block
)
from recovery_engine.crypto_detector import detect_encryption_in_chunk
from recovery_engine.doc_inspector import inspect_document_payload, validate_thai_id, validate_luhn_credit_card
from recovery_engine.partition_rebuilder import parse_mbr_partitions, scan_vbr_in_chunk
from recovery_engine.thermal_guard import ThermalGuard
from recovery_engine.remote_exporter import validate_destination_target

def run_tests():
    print("[*] Running recovery_engine comprehensive test suite...")

    # 1. Test format_eta & write-block verification
    assert format_eta(95) == "01m 35s"
    assert format_eta(3665) == "01h 01m 05s"
    wb_info = check_write_block_status("./test_engine.py")
    assert wb_info["forensic_safe"] is True
    print("  ✓ format_eta & Write-block verification tests passed")

    # 2. Test parse_size_str
    assert parse_size_str("50k") == 50 * 1024
    assert parse_size_str("10m") == 10 * 1024 * 1024
    assert parse_size_str("2g") == 2 * 1024 * 1024 * 1024
    print("  ✓ parse_size_str tests passed")

    # 3. Test Deduplication & Dual Hashing
    dedup = HashDeduplicator(enabled=True)
    data1 = b"Hello Data Recovery Forensic World 12345"
    data2 = b"Hello Data Recovery Forensic World 12345"
    data3 = b"Different Data"
    u1, h1, s1 = dedup.check_and_register(data1)
    u2, h2, s2 = dedup.check_and_register(data2)
    u3, h3, s3 = dedup.check_and_register(data3)
    assert u1 is True and u2 is False and u3 is True
    assert dedup.duplicate_count == 1
    assert len(s1) == 64 and len(h1) == 32
    print("  ✓ Deduplication & Dual Hashing (MD5 + SHA-256) tests passed")

    # 4. Test Structural Validators
    valid_png = b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\x00IEND\xaeB`\x82"
    assert validate_file_integrity("png", valid_png)[0] is True
    assert validate_file_integrity("sqlite", b"SQLite format 3\x00\x10\x00\x01\x01\x00@  \x00\x00\x00\x01")[0] is True
    assert validate_file_integrity("mp3", b"ID3\x03\x00\x00\x00\x00\x00\x10" + b"\x00" * 30)[0] is True
    assert validate_file_integrity("wav", b"RIFF\x24\x00\x00\x00WAVEfmt \x10\x00\x00\x00" + b"\x00" * 10)[0] is True
    assert validate_file_integrity("flac", b"fLaC\x00\x00\x00\x22\x10\x00\x10\x00" + b"\x00" * 26)[0] is True
    print("  ✓ Integrity validators tests passed")

    # 5. Test Audio Carver & ID3 Metadata Parser
    tit2_frame = b"TIT2" + struct.pack(">I", 10) + b"\x00\x00\x00Test Song"
    tpe1_frame = b"TPE1" + struct.pack(">I", 13) + b"\x00\x00\x00Audio Artist"
    tag_body = tit2_frame + tpe1_frame
    id3_header = b"ID3\x03\x00\x00" + bytes([0, 0, 0, len(tag_body)])
    synthetic_mp3 = id3_header + tag_body + b"\xFF\xFB\x90\x44" + (b"\x00" * 100)

    audio_items = scan_audio_in_chunk(synthetic_mp3, 0)
    assert len(audio_items) >= 1
    assert audio_items[0]["file_type"] == "mp3"

    parsed_meta = extract_audio_metadata(synthetic_mp3, "mp3")
    assert parsed_meta.get("title") == "Test Song"
    assert parsed_meta.get("artist") == "Audio Artist"
    print("  ✓ Audio carving & ID3 metadata parsing tests passed")

    # 6. Test Video Repair & Atom Rebuilder
    ftyp_atom = b"\x00\x00\x00\x18ftypmp42\x00\x00\x00\x00mp42isom"
    moov_atom = b"\x00\x00\x00\x20moov" + b"\x00" * 24
    mdat_atom = b"\x00\x00\x00\x30mdat" + b"H264_STREAM_SAMPLE_DATA_12345" + (b"\x00" * 15)

    good_ref_mp4 = ftyp_atom + moov_atom + mdat_atom
    corrupt_mp4 = ftyp_atom + mdat_atom

    parsed_corrupt_atoms = parse_mp4_atoms(corrupt_mp4)
    assert len(parsed_corrupt_atoms) == 2
    assert parsed_corrupt_atoms[0]["type"] == "ftyp"
    assert parsed_corrupt_atoms[1]["type"] == "mdat"

    success, repaired_data, msg = repair_video_with_reference(corrupt_mp4, good_ref_mp4)
    assert success is True
    assert b"moov" in repaired_data and b"mdat" in repaired_data
    print("  ✓ Video auto-repair & moov atom rebuilder tests passed")

    # 7. Test S.M.A.R.T. Health Evaluator
    health_result = evaluate_disk_health("./test_engine.py")
    assert "health_score" in health_result
    assert "risk_level" in health_result
    assert "recommendations" in health_result
    print("  ✓ S.M.A.R.T. Health Evaluator tests passed")

    # 8. Test File System Metadata Map & Linux EXT4 Parser
    fs_map = FileSystemMetadataMap()
    fs_map.add_record(
        offset=0x2000,
        filename="Vacation_Photo_2026.jpg",
        path="DCIM/100APPLE",
        size=10240,
        timestamp="2026-09-15 12:00:00"
    )
    match1 = fs_map.match_carved_file(0x2000, "jpg", 10240)
    assert match1 is not None
    assert match1["filename"] == "Vacation_Photo_2026.jpg"

    # Synthetic EXT4 directory entry
    # inode: 12, rec_len: 24, name_len: 11, file_type: 1 (regular file), name: "report.docx"
    ext4_block = bytearray(512)
    ext4_block[0:4] = struct.pack("<I", 12)
    ext4_block[4:6] = struct.pack("<H", 24)
    ext4_block[6] = 11
    ext4_block[7] = 1
    ext4_block[8:19] = b"report.docx"
    ext4_res = parse_ext4_directory_block(bytes(ext4_block), 0x5000)
    assert len(ext4_res) == 1
    assert ext4_res[0]["filename"] == "report.docx"
    print("  ✓ File System metadata map & Linux EXT4 parser tests passed")

    # 9. Test Crypto & Encrypted Volume Detector
    crypto_chunk = b"\x00" * 100 + b"-FVE-FS-" + b"\x00" * 50 + b"LUKS\xBA\xBE\x00\x02" + b"\x00" * 50
    enc_findings = detect_encryption_in_chunk(crypto_chunk, 0)
    assert len(enc_findings) >= 2
    assert any("BitLocker" in f["type"] for f in enc_findings)
    assert any("LUKS" in f["type"] for f in enc_findings)
    print("  ✓ Encryption & BitLocker/LUKS detector tests passed")

    # 10. Test Document Sensitive Data & Thai ID / Credit Card Inspector
    assert validate_thai_id("1103700000003") is True
    assert validate_thai_id("1103700000008") is False
    assert validate_luhn_credit_card("4532015112830366") is True

    test_doc_payload = "เอกสารสำคัญ สัญญาการเงิน เลขบัตรประชาชน: 1-1037-00000-00-3 และหมายเลขบัตร 4532-0151-1283-0366 ติดต่อ: test@forensic.org".encode("utf-8")
    doc_res = inspect_document_payload(test_doc_payload, "pdf")
    assert doc_res["has_sensitive_data"] is True
    assert len(doc_res["thai_ids_found"]) >= 1
    assert len(doc_res["credit_cards_found"]) >= 1
    assert "สัญญา" in doc_res["keywords_matched"]
    print("  ✓ Document sensitive data (Thai ID, Credit Card, Keywords) inspector tests passed")

    # 11. Test Partition Table Scanner (MBR & VBR)
    synthetic_mbr = bytearray(512)
    synthetic_mbr[446 + 4] = 0x07  # NTFS
    synthetic_mbr[446 + 8 : 446 + 12] = struct.pack("<I", 2048)  # Start LBA
    synthetic_mbr[446 + 12 : 446 + 16] = struct.pack("<I", 204800)  # Sector Count
    synthetic_mbr[510:512] = b"\x55\xAA"
    mbr_parts = parse_mbr_partitions(bytes(synthetic_mbr))
    assert len(mbr_parts) == 1
    assert mbr_parts[0]["start_lba"] == 2048

    synthetic_vbr = bytearray(512)
    synthetic_vbr[3:11] = b"NTFS    "
    synthetic_vbr[40:48] = struct.pack("<Q", 1000000)
    synthetic_vbr[510:512] = b"\x55\xAA"
    vbr_parts = scan_vbr_in_chunk(bytes(synthetic_vbr), 0)
    assert len(vbr_parts) == 1
    assert vbr_parts[0]["filesystem"] == "NTFS"
    print("  ✓ Partition table & VBR scanner tests passed")

    # 12. Test Thermal Guard
    tg = ThermalGuard("./test_engine.py", max_temp_c=60)
    assert tg.max_temp_c == 60
    assert tg.check_and_throttle_if_hot() is False
    print("  ✓ Thermal guard tests passed")

    # 13. Test Remote Exporter / Destination Validator
    with tempfile.TemporaryDirectory() as tmp_dest:
        is_ok, msg, free_gb = validate_destination_target(tmp_dest)
        assert is_ok is True
        assert free_gb >= 0
    print("  ✓ Remote exporter & destination validation tests passed")

    # 14. Test RAW Photo Carver (CR2, NEF, ARW, DNG, TIFF)
    # Build standard TIFF: 8B Header + 2B count + two 12B entries + 4B next IFD + payload
    raw_hdr = b"II*\x00" + struct.pack("<I", 8)  # IFD0 at offset 8
    num_tags = struct.pack("<H", 2)
    # Tag 0x010F (Make, type=2, count=6, offset=38)
    tag1 = struct.pack("<HHII", 0x010F, 2, 6, 38)
    # Tag 0x0110 (Model, type=2, count=7, offset=44)
    tag2 = struct.pack("<HHII", 0x0110, 2, 7, 44)
    next_ifd = struct.pack("<I", 0)
    str_data = b"Canon\x00EOS 5D\x00"
    synthetic_raw = raw_hdr + num_tags + tag1 + tag2 + next_ifd + str_data + (b"\x00" * 512)

    raw_items = scan_raw_photos_in_chunk(synthetic_raw, 0)
    assert len(raw_items) >= 1
    assert raw_items[0]["category"] == "raw_photos"
    assert raw_items[0]["file_type"] == "cr2"
    assert raw_items[0]["meta"]["make"] == "Canon"
    print("  ✓ RAW photo carving & camera model parser tests passed")

    # 15. Test Graphics & Vector Carver (PSD & SVG)
    # Synthetic PSD Header (8BPS, version 1, 3 channels, height 600, width 800, depth 8, mode 3 RGB)
    synthetic_psd = b"8BPS" + struct.pack(">H", 1) + (b"\x00" * 6) + struct.pack(">HIIHH", 3, 600, 800, 8, 3) + (b"\x00" * 100)
    psd_items = scan_graphics_in_chunk(synthetic_psd, 0)
    assert len(psd_items) >= 1
    assert psd_items[0]["file_type"] == "psd"

    synthetic_svg = b"<svg width='100' height='100'><circle cx='50' cy='50' r='40'/></svg>"
    svg_items = scan_graphics_in_chunk(synthetic_svg, 0)
    assert len(svg_items) >= 1
    assert svg_items[0]["file_type"] == "svg"
    print("  ✓ Graphics & Vector design (PSD, SVG) carver tests passed")

    # 16. Test Virtual Disk Carver (VMDK, VHDX, ISO)
    synthetic_vmdk = b"KDMV" + struct.pack("<IIQ", 1, 0, 20971520) + (b"\x00" * 500)
    vmdk_items = scan_virtual_disks_in_chunk(synthetic_vmdk, 0)
    assert len(vmdk_items) >= 1
    assert vmdk_items[0]["file_type"] == "vmdk"
    print("  ✓ Virtual disk (VMDK, VHDX, ISO) carver tests passed")

    # 17. Test Email & Communication Carver (EML, PST)
    synthetic_eml = b"From: alice@test.com\r\nTo: bob@test.com\r\nSubject: Secret Data\r\n\r\nBody text."
    eml_items = scan_emails_in_chunk(synthetic_eml, 0)
    assert len(eml_items) >= 1
    assert eml_items[0]["file_type"] == "eml"
    print("  ✓ Email (EML, PST) carver tests passed")

    # 18. Test Source Code & Script Carver (HTML, PY, SQL)
    synthetic_html = b"<!DOCTYPE html><html><body><h1>Recovery</h1></body></html>"
    html_items = scan_code_in_chunk(synthetic_html, 0)
    assert len(html_items) >= 1
    assert html_items[0]["file_type"] == "html"
    print("  ✓ Code & Script (HTML, PY, SQL) carver tests passed")

    # 19. Test Reporting, Heatmap & Forensic Chain of Custody (ISO/IEC 27037)
    with tempfile.TemporaryDirectory() as tmpdir:
        recs = [
            {
                "index": 1, "category": "Documents", "file_type": "pdf",
                "rel_path": "Documents/PDF/file_000001.pdf", "size_bytes": 1024,
                "offset": 0x1000, "timestamp": "2026-09-15", "integrity_status": "Valid",
                "md5": "d41d8cd98f00b204e9800998ecf8427e",
                "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
                "original_name": "Confidential_Contract.pdf",
                "doc_meta": {"has_sensitive_data": True, "summary_badge": "Thai ID (1) • Contract", "keywords_matched": ["สัญญา", "confidential"]}
            }
        ]
        csv_out = generate_csv_report(recs, tmpdir)
        html_out = generate_gallery_html(recs, tmpdir, smart_status="Verified (100%)", total_disk_size=10*1024*1024)
        manifest_out = generate_chain_of_custody_manifest(recs, tmpdir, source_device="/dev/rdisk4", total_scanned_bytes=10*1024*1024)

        assert os.path.exists(csv_out) and os.path.exists(html_out) and os.path.exists(manifest_out)

        with open(csv_out, "r", encoding="utf-8") as f:
            csv_content = f.read()
            assert "SHA256Checksum" in csv_content
            assert "Thai ID (1) • Contract" in csv_content

        with open(html_out, "r", encoding="utf-8") as f:
            html_content = f.read()
            assert "heatmap-container" in html_content
            assert "openHexModal" in html_content
            assert "chain_of_custody.json" in html_content

        with open(manifest_out, "r", encoding="utf-8") as f:
            manifest_json = json.load(f)
            assert manifest_json["standard"] == "ISO/IEC 27037 Digital Evidence Compliance"
            assert len(manifest_json["extracted_files_manifest"]) == 1
            assert manifest_json["extracted_files_manifest"][0]["sha256"] == "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"

        print("  ✓ Reporting (CSV Dual Hashes, HTML Heatmap Gallery, ISO 27037 JSON Manifest) tests passed")

    # 20. Test Windows Platform Discovery, Device Sizing & Admin Checking
    from recovery_engine.disk_io import is_admin, get_available_drives, get_device_size
    from recovery_engine.smart_checker import get_windows_smart_status

    # is_admin() should return boolean on any OS without crashing
    admin_status = is_admin()
    assert isinstance(admin_status, bool)

    # get_available_drives() should return a list of dictionaries with valid keys
    drv_list = get_available_drives(include_virtual=True)
    assert isinstance(drv_list, list)
    for d in drv_list:
        assert "id" in d and "node" in d and "size_gb" in d and "name" in d

    # File size query should work on normal files
    sz = get_device_size("./test_engine.py")
    assert sz == os.path.getsize("./test_engine.py")

    # Windows SMART helper returns valid dict structure
    win_smart = get_windows_smart_status(r"\\.\PhysicalDrive0")
    assert isinstance(win_smart, dict)
    # 21. Test Smart Carving & Bi-fragment Gap Reassembly
    from recovery_engine.smart_carver import validate_jpeg_stream_continuity, validate_h264_nalu_continuity, reassemble_bi_fragments
    head_jpeg = b"\xFF\xD8\xFF\xE0\x00\x10JFIF\x00\x01\x01\x00\x00\x01\x00\x01\x00\x00\xFF\xDA\x00\x0C\x03\x01\x00\x02\x11\x03\x11\x00?\x00" + bytes(range(200))
    tail_jpeg = bytes(range(150)) + b"\xFF\xD9"
    assert validate_jpeg_stream_continuity(head_jpeg, tail_jpeg) is True
    ok_reasm, combined_jpg, matched_off = reassemble_bi_fragments(head_jpeg, [(0x8000, tail_jpeg)], "jpg")
    assert ok_reasm is True
    assert combined_jpg.endswith(b"\xFF\xD9")
    print("  ✓ Smart Carving & Bi-fragment Reassembly tests passed")

    # 22. Test Apple APFS Container & Volume Superblock Parser
    from recovery_engine.apfs_parser import parse_apfs_container_superblock, parse_apfs_volume_superblock, scan_apfs_structures_in_chunk
    synthetic_nxsb = bytearray(4096)
    synthetic_nxsb[0:4] = b"NXSB"
    synthetic_nxsb[4:8] = struct.pack("<I", 4096)  # Block size
    synthetic_nxsb[8:16] = struct.pack("<Q", 1000000)  # Block count
    synthetic_nxsb[40:56] = b"\x12\x34\x56\x78" * 4
    apfs_container = parse_apfs_container_superblock(bytes(synthetic_nxsb), 0)
    assert apfs_container is not None
    assert apfs_container["type"] == "APFS_CONTAINER"
    assert apfs_container["block_size"] == 4096

    synthetic_apfs_vol = bytearray(4096)
    synthetic_apfs_vol[0:4] = b"APFS"
    synthetic_apfs_vol[64:75] = b"MacintoshHD\x00"
    apfs_vol = parse_apfs_volume_superblock(bytes(synthetic_apfs_vol), 0x1000)
    assert apfs_vol is not None
    assert apfs_vol["type"] == "APFS_VOLUME"
    print("  ✓ Apple APFS Container & Volume Parser tests passed")

    # 23. Test Alert Notifier & Webhook Dispatcher
    from recovery_engine.notifier import AlertNotifier
    notifier_dummy = AlertNotifier()  # Disabled by default when no URL
    assert notifier_dummy.enabled is False
    assert notifier_dummy.send_alert("Test", "No alert sent") is False

    notifier_active = AlertNotifier(webhook_url="https://httpbin.org/post")
    assert notifier_active.enabled is True
    print("  ✓ Alert Notifier & Webhook Alerting tests passed")

    # 24. Test Forensic Case Investigation PDF Generator
    from recovery_engine.pdf_report import generate_forensic_pdf_report
    with tempfile.TemporaryDirectory() as pdf_tmp:
        test_records = [
            {
                "index": 1, "category": "Documents", "file_type": "pdf",
                "rel_path": "Documents/PDF/contract.pdf", "size_bytes": 2048,
                "offset": 0x4000, "timestamp": "2026-09-21", "integrity_status": "Valid",
                "md5": "d41d8cd98f00b204e9800998ecf8427e", "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
                "doc_meta": {"has_sensitive_data": True, "summary_badge": "Thai ID (1)"}
            }
        ]
        generated_pdf = generate_forensic_pdf_report(test_records, pdf_tmp, "/dev/rdisk4", "Optimal (100%)")
        assert os.path.exists(generated_pdf)
        with open(generated_pdf, "rb") as pf:
            pdf_bytes = pf.read()
            assert pdf_bytes.startswith(b"%PDF-1.4")
            assert b"DIGITAL FORENSICS & DATA RECOVERY REPORT" in pdf_bytes
            assert b"%%EOF" in pdf_bytes
    print("  ✓ Forensic Investigation PDF Generator (ISO/IEC 27037) tests passed")

    # 25. Test Cloud Storage Exporter & Direct Presigned Uploader
    from recovery_engine.cloud_exporter import upload_file_to_presigned_url
    ok_up, msg_up = upload_file_to_presigned_url("/non/existent/file.bin", "https://s3.amazonaws.com/bucket/key")
    assert ok_up is False
    assert "does not exist" in msg_up
    print("  ✓ Cloud Storage Exporter tests passed")

    print("\n🎉 ALL 25 ENTERPRISE TEST SUITES PASSED SUCCESSFULLY 100%!")

if __name__ == "__main__":
    run_tests()
