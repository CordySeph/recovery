#!/usr/bin/env python3
"""
🚀 Universal Multi-Core Data Recovery Engine (Professional / Forensic Grade)
- High-Performance Multi-Core Parallel File Carver
- S.M.A.R.T. Physical Disk Health Diagnostics & Real-time Thermal Guard
- BitLocker / LUKS / Apple FileVault Encrypted Volume Detector
- Lost & Deleted Partition Table Rebuilder (MBR/GPT/VBR)
- Document Sensitive Data (Thai ID, Credit Cards) & Keyword Inspector
- Video Auto-Repair & `moov` Atom Rebuilder
- FAT/NTFS File System Remnant Parser & Original Filename Recovery
- Built-in Local Web Dashboard & Media Streaming Server
"""

import sys
import os
import argparse
import multiprocessing
import shutil

# Import Core Engine Modules
from recovery_engine.config import DEFAULT_CORES, FILE_CATEGORIES
from recovery_engine.i18n import t, set_language, CURRENT_LANG
from recovery_engine.disk_io import (
    get_available_drives, clone_disk_to_image, is_admin
)
from recovery_engine.scanner import recover_universal
from recovery_engine.smart_checker import evaluate_disk_health, print_health_report
from recovery_engine.crypto_detector import scan_disk_for_encryption
from recovery_engine.partition_rebuilder import scan_disk_partitions, print_partition_report
from recovery_engine.video_repair import repair_video_file
from recovery_engine.remote_exporter import sync_to_remote_sftp
from recovery_engine.web_server import start_dashboard_server

def print_drives_table(drives: list):
    """Render ASCII table of discovered drives."""
    print("=" * 80)
    print(t("drive_list_header"))
    print("-" * 80)
    if not drives:
        print(t("drive_no_found"))
        print("=" * 80)
        return

    for idx, d in enumerate(drives, 1):
        dev_path = d["raw_node"] if sys.platform == "darwin" else d["node"]
        size_str = f"{d['size_gb']:.1f} GB"
        
        tags = []
        if d["is_removable"]:
            tags.append(t("tag_external"))
        elif d["is_internal"]:
            tags.append(t("tag_internal"))
        if d.get("protocol"):
            tags.append(d["protocol"])
        
        tag_str = " | ".join(tags)
        print(f"  [{idx}] {dev_path:<22} {size_str:>9}  -  {d['name']} ({tag_str})")
    print("=" * 80)

def interactive_select_drive() -> str:
    """Interactive loop for user to pick source disk with language toggle."""
    while True:
        drives = get_available_drives()
        print("\n" + "=" * 80)
        print(t("drive_title"))
        print_drives_table(drives)
        print(f"  [L] {t('opt_switch_lang')}")
        print(f"  [C] {t('opt_custom_path')}")
        print(f"  [Q] {t('opt_quit')}")
        print("=" * 80)

        num_drives = len(drives)
        try:
            choice = input(t("prompt_select_drive", n=num_drives)).strip()
        except (KeyboardInterrupt, EOFError):
            print("\n" + t("cancel_msg"))
            sys.exit(0)

        if not choice:
            continue

        choice_lower = choice.lower()

        # Language toggle
        if choice_lower == "l":
            new_lang = "th" if CURRENT_LANG == "en" else "en"
            set_language(new_lang)
            continue

        if choice_lower in ("q", "quit", "exit"):
            print(t("cancel_msg"))
            sys.exit(0)

        if choice_lower in ("c", "custom"):
            try:
                custom_path = input(t("prompt_custom_drive")).strip()
                if custom_path:
                    if sys.platform == "darwin" and custom_path.startswith("/dev/disk"):
                        custom_path = custom_path.replace("/dev/disk", "/dev/rdisk")
                    elif sys.platform == "win32":
                        if len(custom_path) == 2 and custom_path[1] == ":" and custom_path[0].isalpha():
                            custom_path = f"\\\\.\\{custom_path}"
                        elif len(custom_path) == 3 and custom_path[1:] in (":\\", ":/") and custom_path[0].isalpha():
                            custom_path = f"\\\\.\\{custom_path[:2]}"
                    if os.path.exists(custom_path) or (sys.platform == "win32" and custom_path.startswith("\\\\.\\")):
                        return custom_path
                    else:
                        print(f"[!] Path '{custom_path}' does not exist.")
                        continue
            except (KeyboardInterrupt, EOFError):
                sys.exit(0)

        if choice.isdigit():
            idx = int(choice)
            if 1 <= idx <= num_drives:
                selected = drives[idx - 1]
                target_dev = selected["raw_node"] if sys.platform == "darwin" else selected["node"]

                if selected["is_internal"]:
                    print(t("warn_internal", dev=target_dev, name=selected['name']))
                    try:
                        confirm = input(t("confirm_internal")).strip().lower()
                        if confirm not in ("y", "yes"):
                            print("[*] Aborted.")
                            continue
                    except (KeyboardInterrupt, EOFError):
                        sys.exit(0)

                return target_dev

        print("[!] Invalid selection. Please choose a valid number.")

def interactive_select_mode() -> tuple:
    """Prompt user to choose recovery mode (All, Photos, RAW, Videos, Docs, Graphics, Archives, Audio, DB, Virtual Disks, Emails, Code, Clone)."""
    print("\n" + "=" * 80)
    print(t("mode_title"))
    print("=" * 80)
    for i in range(1, 15):
        print(f"  [{i:<2}] {t(f'mode_{i}')}")
    print("=" * 80)

    try:
        ans = input(t("prompt_select_mode")).strip()
    except (KeyboardInterrupt, EOFError):
        print("\n" + t("cancel_msg"))
        sys.exit(0)

    if ans == "2":
        return "recover", {"cctv"}
    elif ans == "3":
        return "recover", FILE_CATEGORIES["images"]
    elif ans == "4":
        return "recover", FILE_CATEGORIES["raw_photos"]
    elif ans == "5":
        return "recover", FILE_CATEGORIES["videos"]
    elif ans == "6":
        return "recover", FILE_CATEGORIES["documents"]
    elif ans == "7":
        return "recover", FILE_CATEGORIES["graphics"]
    elif ans == "8":
        return "recover", FILE_CATEGORIES["archives"]
    elif ans == "9":
        return "recover", FILE_CATEGORIES["audio"]
    elif ans == "10":
        return "recover", FILE_CATEGORIES["database"]
    elif ans == "11":
        return "recover", FILE_CATEGORIES["virtual_disks"]
    elif ans == "12":
        return "recover", FILE_CATEGORIES["emails"]
    elif ans == "13":
        return "recover", FILE_CATEGORIES["code"]
    elif ans == "14":
        return "clone", set()
    else:
        # Default: Universal Mode (All Files)
        return "recover", set().union(*FILE_CATEGORIES.values())

def main():
    if "fork" in multiprocessing.get_all_start_methods():
        try:
            multiprocessing.set_start_method("fork", force=False)
        except (ValueError, RuntimeError):
            pass

    parser = argparse.ArgumentParser(description="Universal Multi-Core Data Recovery Engine (Professional / Forensic Grade)")
    parser.add_argument("device", nargs="?", default=None, help="Drive path (e.g. \\\\.\\PhysicalDrive1, /dev/rdisk4, /dev/sdb, or disk.img)")
    parser.add_argument("-s", "--select", action="store_true", help="Interactively select drive")
    parser.add_argument("-l", "--list-disks", action="store_true", help="List all detected disks and exit")
    parser.add_argument("-o", "--output", default=None, help="Output directory (default: interactive prompt after scan)")
    parser.add_argument("--lang", choices=["th", "en"], default="en", help="Interface language (th: Thai, en: English, default: en)")
    parser.add_argument("--clone", nargs="?", const="default", help="Clone source disk to .img file before recovery")
    parser.add_argument("--smart-check", action="store_true", help="Run standalone S.M.A.R.T. physical disk diagnostics and exit")
    parser.add_argument("--check-crypto", action="store_true", help="Check drive for BitLocker / LUKS / FileVault encrypted volumes and exit")
    parser.add_argument("--scan-partitions", action="store_true", help="Scan and list remnant / lost partition tables and exit")
    parser.add_argument("--serve", nargs="?", const="recovered_all_data", help="Launch local Web Dashboard and media server (default dir: ./recovered_all_data)")
    parser.add_argument("--port", type=int, default=8080, help="Port for local Web Dashboard server (default: 8080)")
    parser.add_argument("--repair-video", type=str, default="", help="Repair corrupted MP4/MOV file")
    parser.add_argument("--ref-video", type=str, default="", help="Reference good MP4/MOV file recorded from same camera")
    parser.add_argument("--sftp-upload", type=str, default="", help="Remote SFTP/rsync destination (e.g. user@server:/path/to/backup)")
    parser.add_argument("--thermal-limit", type=int, default=55, help="Drive temperature limit for auto-throttle in °C (default: 55)")
    parser.add_argument("--all", action="store_true", default=False, help="Recover ALL file types")
    parser.add_argument("--cctv", action="store_true", help="Recover CCTV Xiongmai H.264 only")
    parser.add_argument("--photos", action="store_true", help="Recover photos/images only")
    parser.add_argument("--raw-photos", action="store_true", help="Recover RAW camera photos only (CR2, CR3, NEF, ARW, DNG, TIFF)")
    parser.add_argument("--videos", action="store_true", help="Recover videos only")
    parser.add_argument("--audio", action="store_true", help="Recover audio only (MP3, WAV, FLAC, OGG, M4A)")
    parser.add_argument("--docs", action="store_true", help="Recover documents only")
    parser.add_argument("--graphics", action="store_true", help="Recover graphics/design files only (PSD, AI, EPS, SVG)")
    parser.add_argument("--virtual-disks", action="store_true", help="Recover virtual disks only (VMDK, VHD, VHDX, ISO)")
    parser.add_argument("--emails", action="store_true", help="Recover email files only (EML, PST, MSG)")
    parser.add_argument("--code", action="store_true", help="Recover source code/scripts only (PY, JS, HTML, JSON, CSV, SQL)")
    parser.add_argument("--scan-only", "-n", action="store_true", help="Scan and list files only without extracting/saving")
    parser.add_argument("-y", "--yes", action="store_true", help="Auto-confirm recovery without interactive prompt")
    parser.add_argument("--resume", "-r", action="store_true", help="Resume scanning from last saved checkpoint")
    parser.add_argument("--min-size", type=str, default="", help="Minimum file size filter (e.g. 50k, 1m, 100kb)")
    parser.add_argument("--max-size", type=str, default="", help="Maximum file size filter (e.g. 500m, 2g)")
    parser.add_argument("--no-dedup", action="store_true", help="Disable hash-based duplicate file filtering")
    parser.add_argument("--no-smart", action="store_true", help="Disable pre-scan SMART diagnostics")
    parser.add_argument("--no-fs", action="store_true", help="Disable remnant File System original name recovery")
    parser.add_argument("--no-crypto", action="store_true", help="Disable pre-scan encrypted volume check")
    parser.add_argument("--types", type=str, default="", help="Comma-separated file extensions (e.g. jpg,png,mp4,mp3,pdf,docx,cctv)")
    parser.add_argument("--dates", type=str, default="", help="CCTV Target dates (e.g. 2026-09-06,2026-09-07)")
    parser.add_argument("--gui", action="store_true", help="Launch Modern Native Desktop GUI Application")
    parser.add_argument("--batch-devices", type=str, default="", help="Comma-separated physical drives for concurrent batch recovery")
    parser.add_argument("--notify-webhook", type=str, default="", help="Webhook URL for Discord / generic alert notifications")
    parser.add_argument("--telegram-token", type=str, default="", help="Telegram Bot API Token")
    parser.add_argument("--telegram-chat", type=str, default="", help="Telegram Chat ID")
    parser.add_argument("--cores", type=int, default=DEFAULT_CORES, help=f"CPU cores to use (default: {DEFAULT_CORES})")

    args = parser.parse_args()

    if args.gui:
        try:
            from gui_app import start_gui
            start_gui()
            sys.exit(0)
        except Exception as e:
            print(f"[!] Failed to launch GUI: {e}")
            sys.exit(1)

    if args.batch_devices:
        from recovery_engine.batch_runner import run_batch_recovery
        dev_list = [d.strip() for d in args.batch_devices.split(",") if d.strip()]
        out_base = args.output or "./recovered_batch_data"
        enabled = set().union(*FILE_CATEGORIES.values()) if args.all else FILE_CATEGORIES["images"]
        run_batch_recovery(dev_list, out_base, enabled, cores_per_disk=max(2, args.cores // max(1, len(dev_list))))
        sys.exit(0)

    if args.lang:
        set_language(args.lang)

    # 1. Option: Launch Web Dashboard Server
    if args.serve:
        target_dir = args.serve if args.serve != "recovered_all_data" else (args.output or "./recovered_all_data")
        start_dashboard_server(target_dir, port=args.port)
        sys.exit(0)

    # 2. Option: Video Auto-Repair Tool
    if args.repair_video:
        corrupt_f = args.repair_video
        ref_f = args.ref_video if args.ref_video else None
        base, ext = os.path.splitext(corrupt_f)
        out_f = f"{base}_repaired{ext or '.mp4'}"
        print(f"[*] Attempting video repair on: {corrupt_f}")
        ok, msg = repair_video_file(corrupt_f, out_f, ref_f)
        if ok:
            print(t("repair_video_success", dest=out_f))
            print(f"[*] Note: {msg}")
        else:
            print(t("repair_video_failed", msg=msg))
        sys.exit(0 if ok else 1)

    # 3. Option: Standalone SMART Health Diagnostics
    if args.smart_check:
        target_dev = args.device or interactive_select_drive()
        res = evaluate_disk_health(target_dev)
        print_health_report(res)
        sys.exit(0)

    # 4. Option: Standalone Encryption Check
    if args.check_crypto:
        target_dev = args.device or interactive_select_drive()
        findings = scan_disk_for_encryption(target_dev)
        print("\n" + "=" * 80)
        print("🛡️ ENCRYPTED VOLUME & CONTAINER SCAN REPORT")
        print("=" * 80)
        if not findings:
            print("  ✓ No known encrypted container signatures detected. Drive is in cleartext.")
        else:
            for f in findings:
                print(f"  🚨 [{f['type']}] Offset: 0x{f['offset']:08X} - {f['description']}")
                print(f"     👉 {f['guidance']}")
        print("=" * 80 + "\n")
        sys.exit(0)

    # 5. Option: Standalone Partition Table Scan
    if args.scan_partitions:
        target_dev = args.device or interactive_select_drive()
        parts = scan_disk_partitions(target_dev)
        print_partition_report(parts)
        sys.exit(0)

    # 6. Option: Just list disks
    if args.list_disks:
        drives = get_available_drives(include_virtual=True)
        print_drives_table(drives)
        sys.exit(0)

    # 7. Select Drive
    if args.select or not args.device:
        device_path = interactive_select_drive()
    else:
        device_path = args.device
        if sys.platform == "darwin" and device_path.startswith("/dev/disk") and not device_path.startswith("/dev/rdisk"):
            device_path = device_path.replace("/dev/disk", "/dev/rdisk")
            print(t("auto_raw_device", dev=device_path))
        elif sys.platform == "win32":
            if len(device_path) == 2 and device_path[1] == ":" and device_path[0].isalpha():
                device_path = f"\\\\.\\{device_path}"
            elif len(device_path) == 3 and device_path[1:] in (":\\", ":/") and device_path[0].isalpha():
                device_path = f"\\\\.\\{device_path[:2]}"

    # Check administrator privileges if accessing raw physical/volume devices
    is_raw_dev = (
        (sys.platform == "win32" and device_path.startswith("\\\\.\\")) or
        (sys.platform != "win32" and device_path.startswith("/dev/"))
    )
    if is_raw_dev and not is_admin():
        print("\n" + "=" * 80)
        print(t("permission_error", dev=device_path))
        print(t("sudo_hint"))
        if sys.platform == "win32":
            print("   👉 PowerShell / Command Prompt (Run as Administrator):")
            print(f"      python recover.py {device_path} --all\n")
        else:
            print(f"      sudo python3 recover.py {device_path} --all\n")
        print("=" * 80 + "\n")

    # 8. Handle Clone mode directly
    if args.clone:
        img_out = args.clone if args.clone != "default" else "./disk_dump.img"
        clone_disk_to_image(device_path, img_out)
        sys.exit(0)

    # 9. Determine Mode / Enabled File Types
    mode = "recover"
    if args.types:
        enabled_types = set(t.strip().lower() for t in args.types.split(","))
    elif args.cctv:
        enabled_types = {"cctv"}
    elif args.photos:
        enabled_types = FILE_CATEGORIES["images"]
    elif args.raw_photos:
        enabled_types = FILE_CATEGORIES["raw_photos"]
    elif args.videos:
        enabled_types = FILE_CATEGORIES["videos"]
    elif args.audio:
        enabled_types = FILE_CATEGORIES["audio"]
    elif args.docs:
        enabled_types = FILE_CATEGORIES["documents"]
    elif args.graphics:
        enabled_types = FILE_CATEGORIES["graphics"]
    elif args.virtual_disks:
        enabled_types = FILE_CATEGORIES["virtual_disks"]
    elif args.emails:
        enabled_types = FILE_CATEGORIES["emails"]
    elif args.code:
        enabled_types = FILE_CATEGORIES["code"]
    elif args.all:
        enabled_types = set().union(*FILE_CATEGORIES.values())
    else:
        # Interactive mode selection
        mode, enabled_types = interactive_select_mode()

    if mode == "clone":
        custom_img = input("👉 Enter path for disk image (.img) [Default: ./disk_dump.img]: ").strip()
        if not custom_img:
            custom_img = "./disk_dump.img"
        clone_disk_to_image(device_path, custom_img)
        sys.exit(0)

    target_dates = set(d.strip() for d in args.dates.split(",")) if args.dates else set()
    out_dest = args.output

    recover_universal(
        source_device=device_path,
        output_dir=out_dest,
        enabled_types=enabled_types,
        target_dates=target_dates,
        num_workers=args.cores,
        scan_only=args.scan_only,
        auto_confirm=args.yes,
        resume=args.resume,
        min_size=args.min_size,
        max_size=args.max_size,
        enable_dedup=not args.no_dedup,
        check_smart=not args.no_smart,
        parse_fs=not args.no_fs,
        check_crypto=not args.no_crypto,
        thermal_limit_c=args.thermal_limit,
        webhook_url=args.notify_webhook,
        telegram_token=args.telegram_token,
        telegram_chat_id=args.telegram_chat,
    )

    # If remote SFTP sync requested
    if args.sftp_upload and out_dest and os.path.exists(out_dest):
        print(f"[*] Uploading recovered dataset to remote target: {args.sftp_upload} ...")
        ok_sync, sync_msg = sync_to_remote_sftp(out_dest, args.sftp_upload)
        if ok_sync:
            print(f"🎉 Remote upload succeeded: {args.sftp_upload}")
        else:
            print(f"[!] Remote upload failed: {sync_msg}")

if __name__ == "__main__":
    main()
