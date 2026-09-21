"""
Multi-Core Parallel Chunk Scanner & Extraction Orchestrator
Integrated with:
- Specialized Image, Video, Audio, Document, Archive, and SQLite Carvers
- File System Metadata & Original Filename Recovery (FAT/NTFS)
- Pre-Scan S.M.A.R.T. Health Diagnostic Pre-Check
- Real-Time Thermal Guard & Auto-Throttle
- BitLocker / LUKS / FileVault Encryption Detection
- Document Sensitive Data (Thai ID, Credit Cards, Keywords) Inspector
- ID3 / EXIF / CCTV Metadata Sorters
- Real-time Hash Deduplicator & Forensic Reporter
"""

import sys
import os
import time
import json
import datetime
from concurrent.futures import ProcessPoolExecutor, as_completed
from typing import List, Dict, Set, Tuple, Optional

from recovery_engine.config import (
    CHUNK_SIZE, OVERLAP_SIZE, DEFAULT_CORES, FILE_CATEGORIES,
    parse_size_str
)
from recovery_engine.i18n import t
from recovery_engine.disk_io import (
    get_device_size, format_eta, ResilientDiskReader
)
from recovery_engine.validators import validate_file_integrity
from recovery_engine.deduplicator import HashDeduplicator
from recovery_engine.reporter import generate_csv_report, generate_gallery_html, generate_chain_of_custody_manifest
from recovery_engine.carvers.image_carver import scan_images_in_chunk, extract_exif_date
from recovery_engine.carvers.video_carver import scan_videos_in_chunk, convert_h264_to_mp4
from recovery_engine.carvers.audio_carver import scan_audio_in_chunk, extract_audio_metadata
from recovery_engine.carvers.doc_carver import scan_documents_in_chunk
from recovery_engine.carvers.archive_carver import scan_archives_and_db_in_chunk
from recovery_engine.carvers.raw_carver import scan_raw_photos_in_chunk
from recovery_engine.carvers.graphics_carver import scan_graphics_in_chunk
from recovery_engine.carvers.virtual_disk_carver import scan_virtual_disks_in_chunk
from recovery_engine.carvers.email_carver import scan_emails_in_chunk
from recovery_engine.carvers.code_carver import scan_code_in_chunk
from recovery_engine.smart_checker import evaluate_disk_health, print_health_report
from recovery_engine.fs_parser import scan_filesystem_structures_in_chunk, FileSystemMetadataMap
from recovery_engine.crypto_detector import scan_disk_for_encryption
from recovery_engine.doc_inspector import inspect_document_payload
from recovery_engine.thermal_guard import ThermalGuard

def scan_chunk_worker(task_args: Tuple[bytes, int, Set[str], Set[str]]) -> Tuple[List[Dict], List[Dict]]:
    """
    Worker function executed in parallel across CPU cores to scan a 64MB chunk.
    Returns (detected_files, detected_fs_structures).
    """
    chunk, base_offset, enabled_types, target_dates = task_args
    detected_files = []
    fs_structures = []

    # 1. Images
    img_types = FILE_CATEGORIES["images"].intersection(enabled_types)
    if img_types:
        for item in scan_images_in_chunk(chunk, base_offset):
            if item["file_type"] in img_types:
                detected_files.append(item)

    # 2. RAW Photos (CR2, CR3, NEF, ARW, DNG, TIFF)
    raw_types = FILE_CATEGORIES["raw_photos"].intersection(enabled_types)
    if raw_types:
        for item in scan_raw_photos_in_chunk(chunk, base_offset):
            if item["file_type"] in raw_types:
                detected_files.append(item)

    # 3. Videos & CCTV
    vid_types = FILE_CATEGORIES["videos"].intersection(enabled_types)
    if vid_types:
        for item in scan_videos_in_chunk(chunk, base_offset):
            ft = item["file_type"]
            if ft in vid_types:
                if ft == "cctv" and target_dates:
                    ts = item.get("datetime_obj")
                    if ts and ts.strftime("%Y-%m-%d") not in target_dates:
                        continue
                detected_files.append(item)

    # 4. Audio Streams (MP3, WAV, FLAC, OGG, M4A)
    aud_types = FILE_CATEGORIES["audio"].intersection(enabled_types)
    if aud_types:
        for item in scan_audio_in_chunk(chunk, base_offset):
            if item["file_type"] in aud_types:
                detected_files.append(item)

    # 5. Documents
    doc_types = FILE_CATEGORIES["documents"].intersection(enabled_types)
    if doc_types:
        for item in scan_documents_in_chunk(chunk, base_offset):
            if item["file_type"] in doc_types:
                detected_files.append(item)

    # 6. Graphics & Vector Design (PSD, AI, EPS, SVG)
    graph_types = FILE_CATEGORIES["graphics"].intersection(enabled_types)
    if graph_types:
        for item in scan_graphics_in_chunk(chunk, base_offset):
            if item["file_type"] in graph_types:
                detected_files.append(item)

    # 7. Archives & DB
    other_types = (FILE_CATEGORIES["archives"] | FILE_CATEGORIES["database"]).intersection(enabled_types)
    if other_types:
        for item in scan_archives_and_db_in_chunk(chunk, base_offset):
            if item["file_type"] in other_types:
                detected_files.append(item)

    # 8. Virtual Disks (VMDK, VHD, VHDX, ISO)
    vdisk_types = FILE_CATEGORIES["virtual_disks"].intersection(enabled_types)
    if vdisk_types:
        for item in scan_virtual_disks_in_chunk(chunk, base_offset):
            if item["file_type"] in vdisk_types:
                detected_files.append(item)

    # 9. Emails (EML, PST, MSG)
    email_types = FILE_CATEGORIES["emails"].intersection(enabled_types)
    if email_types:
        for item in scan_emails_in_chunk(chunk, base_offset):
            if item["file_type"] in email_types:
                detected_files.append(item)

    # 10. Code & Structured Data (PY, JS, HTML, JSON, CSV, SQL)
    code_types = FILE_CATEGORIES["code"].intersection(enabled_types)
    if code_types:
        for item in scan_code_in_chunk(chunk, base_offset):
            if item["file_type"] in code_types:
                detected_files.append(item)

    # 11. File System Remnants (FAT Directory entries, NTFS MFT, EXT4 Inodes)
    try:
        fs_structures = scan_filesystem_structures_in_chunk(chunk, base_offset)
    except Exception:
        fs_structures = []

    return detected_files, fs_structures

def worker_extract_file(task_data: Tuple) -> Dict:
    """
    Worker function to extract, validate, deduplicate, inspect sensitive data, and write a single file.
    """
    (
        source_device, offset, file_type, category, est_size,
        file_idx, total_files, output_dir, timestamp, min_size_bytes, max_size_bytes,
        original_name
    ) = task_data

    rel_path = ""
    status = "Valid"
    size_bytes = 0
    md5_hash = ""
    exif_date = None
    audio_meta = {}
    doc_meta = {}

    try:
        with open(source_device, "rb") as disk:
            disk.seek(offset)
            data = disk.read(est_size)
            size_bytes = len(data)

            # Apply size constraints
            if min_size_bytes > 0 and size_bytes < min_size_bytes:
                return {"valid": False, "reason": "Below min-size", "index": file_idx}
            if max_size_bytes > 0 and size_bytes > max_size_bytes:
                return {"valid": False, "reason": "Above max-size", "index": file_idx}

            # Structural validation
            is_valid, status_msg = validate_file_integrity(file_type, data)
            status = status_msg

            # Sensitive Data & Keyword Inspection
            if category in ("Documents", "Database") or file_type in ("txt", "pdf", "docx", "xlsx", "pptx", "sqlite", "db"):
                doc_meta = inspect_document_payload(data, file_type)

            # Directory sorting
            cat_dir = os.path.join(output_dir, category, file_type.upper())
            
            # Check EXIF for images
            if file_type.lower() in ("jpg", "jpeg"):
                exif_date = extract_exif_date(data)
                if exif_date:
                    cat_dir = os.path.join(cat_dir, exif_date)
                    timestamp = exif_date

            # Check Audio ID3 / Vorbis Metadata
            if category == "Audio":
                audio_meta = extract_audio_metadata(data, file_type)
                artist = audio_meta.get("artist", "").strip()
                album = audio_meta.get("album", "").strip()
                if artist:
                    safe_artist = "".join(c for c in artist if c.isalnum() or c in (" ", "-", "_")).strip()[:40]
                    cat_dir = os.path.join(output_dir, "Audio", safe_artist)
                    if album:
                        safe_album = "".join(c for c in album if c.isalnum() or c in (" ", "-", "_")).strip()[:40]
                        cat_dir = os.path.join(cat_dir, safe_album)

            # Check CCTV dates
            if file_type == "cctv" and timestamp:
                day_folder = timestamp.split(" ")[0]
                cat_dir = os.path.join(output_dir, "Videos", "CCTV_Clips", day_folder)

            os.makedirs(cat_dir, exist_ok=True)

            # Output filename
            if original_name:
                safe_orig = "".join(c for c in original_name if c.isalnum() or c in (" ", "-", "_", ".")).strip()
                out_name = f"{file_idx:04d}_{safe_orig}" if safe_orig else f"file_{file_idx:06d}.{file_type}"
                file_dest = os.path.join(cat_dir, out_name)
                with open(file_dest, "wb") as f_out:
                    f_out.write(data)
                rel_path = os.path.relpath(file_dest, output_dir)
            elif file_type == "cctv":
                time_part = timestamp.replace(" ", "_").replace(":", "-") if timestamp else f"clip_{file_idx:06d}"
                out_name = f"{time_part}_{file_idx:04d}.264"
                file_dest = os.path.join(cat_dir, out_name)
                with open(file_dest, "wb") as f_out:
                    f_out.write(data)
                
                # Companion MP4
                mp4_dest = file_dest.replace(".264", ".mp4")
                convert_h264_to_mp4(file_dest, mp4_dest)
                rel_path = os.path.relpath(file_dest, output_dir)
            elif category == "Audio" and audio_meta.get("title"):
                safe_title = "".join(c for c in audio_meta["title"] if c.isalnum() or c in (" ", "-", "_")).strip()[:50]
                out_name = f"{safe_title}_{file_idx:04d}.{file_type}"
                file_dest = os.path.join(cat_dir, out_name)
                with open(file_dest, "wb") as f_out:
                    f_out.write(data)
                rel_path = os.path.relpath(file_dest, output_dir)
            else:
                out_name = f"file_{file_idx:06d}.{file_type}"
                file_dest = os.path.join(cat_dir, out_name)
                with open(file_dest, "wb") as f_out:
                    f_out.write(data)
                rel_path = os.path.relpath(file_dest, output_dir)

            import hashlib
            md5_hash = hashlib.md5(data).hexdigest()
            sha256_hash = hashlib.sha256(data).hexdigest()

    except Exception as e:
        status = f"Error: {e}"

    return {
        "valid": True,
        "index": file_idx,
        "total": total_files,
        "category": category,
        "file_type": file_type,
        "offset": offset,
        "size_bytes": size_bytes,
        "timestamp": timestamp or (exif_date or "-"),
        "integrity_status": status,
        "md5": md5_hash,
        "sha256": sha256_hash,
        "rel_path": rel_path,
        "original_name": original_name,
        "audio_meta": audio_meta,
        "doc_meta": doc_meta,
    }

def recover_universal(
    source_device: str,
    output_dir: Optional[str] = None,
    enabled_types: Set[str] = None,
    target_dates: Set[str] = None,
    num_workers: int = DEFAULT_CORES,
    scan_only: bool = False,
    auto_confirm: bool = False,
    resume: bool = False,
    min_size: str = "",
    max_size: str = "",
    enable_dedup: bool = True,
    check_smart: bool = True,
    parse_fs: bool = True,
    check_crypto: bool = True,
    thermal_limit_c: int = 55,
):
    """
    Universal Multi-Core Data Recovery Engine Main Workflow.
    """
    from recovery_engine.disk_io import interactive_select_destination

    target_dates = target_dates or set()
    min_size_bytes = parse_size_str(min_size)
    max_size_bytes = parse_size_str(max_size)

    # 1. Pre-Scan Encryption Header Check
    if check_crypto and os.path.exists(source_device):
        crypto_findings = scan_disk_for_encryption(source_device)
        if crypto_findings:
            types_str = ", ".join(set(c["type"] for c in crypto_findings))
            print("\n" + "=" * 80)
            print(t("crypto_detected_warn", types=types_str))
            print(t("crypto_detected_advice"))
            print("=" * 80)
            if not auto_confirm:
                try:
                    ans = input("❓ Do you still wish to proceed with raw carve? (y/N): ").strip().lower()
                    if ans not in ("y", "yes"):
                        print("[*] Aborted for data safety.")
                        return
                except (KeyboardInterrupt, EOFError):
                    return

    # 2. Pre-Scan S.M.A.R.T. Health Diagnostic Check
    health_res = None
    if check_smart and os.path.exists(source_device):
        health_res = evaluate_disk_health(source_device)
        print_health_report(health_res)
        if health_res["risk_level"] == "CRITICAL" and not auto_confirm:
            print(t("smart_warn_critical"))
            try:
                ans = input("❓ Do you still wish to proceed with direct scan? (y/N): ").strip().lower()
                if ans not in ("y", "yes"):
                    print("[*] Aborted for drive safety. Please clone first with --clone.")
                    return
            except (KeyboardInterrupt, EOFError):
                return

    total_size = get_device_size(source_device)
    total_gb = total_size / (1024 ** 3) if total_size else 0

    print("\n" + "=" * 80)
    print(t("app_title"))
    print(t("app_desc"))
    print("=" * 80)
    print(f"{t('source_label')}{source_device} ({total_gb:.1f} GB)")
    print(f"{t('cores_label')}{num_workers} Parallel Workers")
    print(f"{t('types_label')}{', '.join(sorted(enabled_types))}")
    if output_dir:
        print(f"{t('dest_label')}{os.path.abspath(output_dir)}")
    if min_size_bytes or max_size_bytes:
        print(f"[*] Size Constraints      : Min={min_size or 'None'}, Max={max_size or 'None'}")
    print("=" * 80 + "\n")

    checkpoint_dir = output_dir or "./recovered_all_data"
    os.makedirs(checkpoint_dir, exist_ok=True)
    checkpoint_file = os.path.join(checkpoint_dir, ".recovery_checkpoint.json")

    scanned_files: List[Dict] = []
    fs_meta_map = FileSystemMetadataMap()
    start_offset = 0

    # Handle checkpoint resume
    if resume and os.path.exists(checkpoint_file):
        try:
            with open(checkpoint_file, "r", encoding="utf-8") as f:
                cp = json.load(f)
                start_offset = cp.get("last_offset", 0)
                scanned_files = cp.get("scanned_files", [])
                print(t("checkpoint_found", gb=start_offset / (1024**3), count=len(scanned_files)))
                print(t("resume_continuing", bytes=start_offset, gb=start_offset / (1024**3)))
        except Exception:
            start_offset = 0

    reader = ResilientDiskReader(source_device, log_dir=output_dir or ".")
    thermal_guard = ThermalGuard(source_device, max_temp_c=thermal_limit_c)
    print(t("scanning_start", mb=CHUNK_SIZE // (1024 * 1024)))

    start_time = time.time()
    current_offset = start_offset
    last_checkpoint_time = time.time()

    try:
        with open(source_device, "rb") as disk, ProcessPoolExecutor(max_workers=num_workers) as executor:
            pending_futures = {}

            while True:
                # Thermal Guard Check
                thermal_guard.check_and_throttle_if_hot()

                chunk, read_len = reader.read_chunk_safe(disk, current_offset, CHUNK_SIZE + OVERLAP_SIZE)
                if not chunk or read_len == 0:
                    break

                future = executor.submit(scan_chunk_worker, (chunk, current_offset, enabled_types, target_dates))
                pending_futures[future] = (current_offset, read_len)

                current_offset += CHUNK_SIZE

                # Process completed futures
                if len(pending_futures) >= num_workers * 2:
                    for f in list(pending_futures.keys()):
                        if f.done():
                            found_files, found_fs = f.result()
                            scanned_files.extend(found_files)
                            for fs_item in found_fs:
                                fs_meta_map.add_record(
                                    fs_item.get("offset", 0),
                                    fs_item.get("filename", ""),
                                    fs_item.get("path", ""),
                                    fs_item.get("size", 0),
                                    fs_item.get("timestamp", "")
                                )
                            del pending_futures[f]

                # Progress & Live ETA calculation
                elapsed = time.time() - start_time
                scanned_bytes = current_offset - start_offset
                speed_mb = (scanned_bytes / (1024 * 1024)) / elapsed if elapsed > 0 else 0
                
                eta_str = "--:--"
                if total_size > 0:
                    pct = min(100.0, (current_offset / total_size) * 100)
                    rem_bytes = max(0, total_size - current_offset)
                    eta_sec = rem_bytes / (speed_mb * 1024 * 1024) if speed_mb > 0 else 0
                    eta_str = format_eta(eta_sec)
                    sys.stdout.write(
                        f"\r[⚡] {t('scan_progress')}: {current_offset / (1024**3):6.2f} GB ({pct:5.1f}%) | "
                        f"{t('speed')}: {speed_mb:5.1f} MB/s | {t('eta')}: {eta_str} | "
                        f"{t('found_files')}: {len(scanned_files):5d} "
                    )
                else:
                    sys.stdout.write(
                        f"\r[⚡] {t('scan_progress')}: {current_offset / (1024**3):6.2f} GB | "
                        f"{t('speed')}: {speed_mb:5.1f} MB/s | {t('found_files')}: {len(scanned_files):5d} "
                    )
                sys.stdout.flush()

                # Periodic Checkpoint Saving every 30 seconds
                if time.time() - last_checkpoint_time > 30:
                    try:
                        with open(checkpoint_file, "w", encoding="utf-8") as cp_f:
                            json.dump({"last_offset": current_offset, "scanned_files": scanned_files}, cp_f)
                        last_checkpoint_time = time.time()
                    except Exception:
                        pass

            # Gather remaining futures
            for f in as_completed(pending_futures.keys()):
                found_files, found_fs = f.result()
                scanned_files.extend(found_files)
                for fs_item in found_fs:
                    fs_meta_map.add_record(
                        fs_item.get("offset", 0),
                        fs_item.get("filename", ""),
                        fs_item.get("path", ""),
                        fs_item.get("size", 0),
                        fs_item.get("timestamp", "")
                    )

        total_elapsed = time.time() - start_time
        print(f"\n\n" + t("scan_completed", elapsed=total_elapsed, total=len(scanned_files)))

        if fs_meta_map.records_found > 0:
            print(t("fs_found_msg", count=fs_meta_map.records_found))

        # Summary breakdown by file type
        type_counts = {}
        for item in scanned_files:
            ft = item["file_type"].upper()
            type_counts[ft] = type_counts.get(ft, 0) + 1

        for ft, count in sorted(type_counts.items()):
            print(f"  📁 {ft:<12}: {count:>6d} files")

        if not scanned_files:
            print("\n" + t("no_files_found"))
            return

        if scan_only:
            print(t("scan_only_done"))
            return

        # Extraction confirmation
        if not auto_confirm:
            try:
                ans = input("\n" + t("confirm_recover", total=len(scanned_files))).strip().lower()
                if ans and ans not in ("y", "yes"):
                    print(t("cancel_msg"))
                    return
            except (KeyboardInterrupt, EOFError):
                print("\n" + t("cancel_msg"))
                return

        # Determine destination folder (if not specified via CLI)
        if not output_dir:
            output_dir = interactive_select_destination(default_dest="./recovered_all_data")
        os.makedirs(output_dir, exist_ok=True)

        # Phase 2: Parallel Extraction, Integrity Validation & Deduplication
        print(t("extracting", total=len(scanned_files), cores=num_workers))
        
        deduplicator = HashDeduplicator(enabled=enable_dedup)
        tasks = []
        for idx, item in enumerate(scanned_files, 1):
            orig_meta = fs_meta_map.match_carved_file(item["offset"], item["file_type"], item["size_bytes"])
            orig_name = orig_meta.get("filename", "") if orig_meta else ""

            tasks.append((
                source_device,
                item["offset"],
                item["file_type"],
                item["category"],
                item["size_bytes"],
                idx,
                len(scanned_files),
                output_dir,
                item.get("timestamp", ""),
                min_size_bytes,
                max_size_bytes,
                orig_name
            ))

        extracted_records = []
        with ProcessPoolExecutor(max_workers=num_workers) as executor:
            futures = [executor.submit(worker_extract_file, t_data) for t_data in tasks]
            completed_count = 0

            for f in as_completed(futures):
                res = f.result()
                completed_count += 1
                if not res.get("valid", True):
                    continue

                # Deduplication check
                is_unique, md5_val = deduplicator.check_and_register(res.get("md5", "").encode("utf-8"))
                if not is_unique:
                    try:
                        dup_path = os.path.join(output_dir, res.get("rel_path", ""))
                        if os.path.exists(dup_path):
                            os.remove(dup_path)
                    except Exception:
                        pass
                    continue

                extracted_records.append(res)
                size_mb = res.get("size_bytes", 0) / (1024 * 1024)
                sys.stdout.write(
                    f"\r  [+] [{completed_count:05d}/{len(scanned_files):05d}] {res.get('file_type','').upper():<5} "
                    f"({size_mb:5.1f} MB) -> {res.get('rel_path', '')} "
                )
                sys.stdout.flush()

        print("\n\n" + "=" * 80)
        print(t("all_done", total=len(extracted_records)))
        print("=" * 80)

        # Count sensitive files
        sens_count = sum(1 for r in extracted_records if r.get("doc_meta", {}).get("has_sensitive_data"))
        if sens_count > 0:
            print(t("sensitive_data_found_msg", count=sens_count))

        # Generate Reports
        smart_str = f"{health_res['status_label']} ({health_res['health_score']}%)" if health_res else None
        csv_path = generate_csv_report(extracted_records, output_dir)
        html_path = generate_gallery_html(extracted_records, output_dir, smart_status=smart_str, total_disk_size=total_size)
        manifest_path = generate_chain_of_custody_manifest(
            extracted_records,
            output_dir,
            source_device=source_device,
            total_scanned_bytes=current_offset,
            bad_sectors_count=len(reader.bad_sectors),
            smart_status=smart_str
        )

        print(f"{t('out_folder')}{os.path.abspath(output_dir)}")
        print(f"{t('out_gallery')}{os.path.abspath(html_path)}")
        print(f"{t('out_report')}{os.path.abspath(csv_path)}")
        print(f"[*] Forensic Manifest (ISO 27037)  : {os.path.abspath(manifest_path)}")
        if deduplicator.duplicate_count > 0:
            print(t("out_dedup_stat", count=deduplicator.duplicate_count))
        if reader.bad_sectors:
            print(f"{t('out_bad_sectors')}{os.path.abspath(reader.bad_sector_log_file)}")
        print("=" * 80 + "\n")

        # Clean up checkpoint upon complete recovery
        if os.path.exists(checkpoint_file):
            try:
                os.remove(checkpoint_file)
            except Exception:
                pass

    except PermissionError:
        print(f"\n" + t("permission_error", dev=source_device))
        print(f"{t('sudo_hint')} sudo python3 {os.path.abspath(__file__)} {source_device} --all")
    except Exception as e:
        print(f"\n[!] Error: {e}")
