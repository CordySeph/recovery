#!/usr/bin/env python3
"""
High-Performance Multi-Core CCTV Data Recovery & Extraction Tool (Xiongmai H.264)
- Specialized CCTV DVR / NVR Recovery Engine
- Uses ALL available CPU Cores for parallel decoding, indexing, extraction, and MP4 remuxing.
"""

import sys
import os
import argparse
import multiprocessing
import shutil
from typing import Set

from recovery_engine.config import DEFAULT_CORES
from recovery_engine.i18n import t, set_language, CURRENT_LANG
from recovery_engine.disk_io import get_available_drives, is_admin
from recovery_engine.scanner import recover_universal

def print_drives_table(drives: list):
    print("=" * 80)
    print("💾 " + t("drive_list_header"))
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
    while True:
        drives = get_available_drives()
        print("\n" + "=" * 80)
        print("🔍 CCTV " + t("drive_title"))
        print_drives_table(drives)
        print(f"  [L] {t('opt_switch_lang')}")
        print(f"  [C] {t('opt_custom_path')}")
        print(f"  [Q] {t('opt_quit')}")
        print("=" * 80)

        try:
            choice = input(t("prompt_select_drive", n=len(drives))).strip()
        except (KeyboardInterrupt, EOFError):
            print("\n" + t("cancel_msg"))
            sys.exit(0)

        if not choice:
            continue

        choice_lower = choice.lower()
        if choice_lower == "l":
            new_lang = "th" if CURRENT_LANG == "en" else "en"
            set_language(new_lang)
            continue

        if choice_lower in ("q", "quit"):
            print(t("cancel_msg"))
            sys.exit(0)

        if choice_lower in ("c", "custom"):
            custom = input(t("prompt_custom_drive")).strip()
            if custom:
                if sys.platform == "darwin" and custom.startswith("/dev/disk"):
                    custom = custom.replace("/dev/disk", "/dev/rdisk")
                elif sys.platform == "win32":
                    if len(custom) == 2 and custom[1] == ":" and custom[0].isalpha():
                        custom = f"\\\\.\\{custom}"
                    elif len(custom) == 3 and custom[1:] in (":\\", ":/") and custom[0].isalpha():
                        custom = f"\\\\.\\{custom[:2]}"
                if os.path.exists(custom) or (sys.platform == "win32" and custom.startswith("\\\\.\\")):
                    return custom
            continue

        if choice.isdigit():
            idx = int(choice)
            if 1 <= idx <= len(drives):
                sel = drives[idx - 1]
                return sel["raw_node"] if sys.platform == "darwin" else sel["node"]

def main():
    if "fork" in multiprocessing.get_all_start_methods():
        try:
            multiprocessing.set_start_method("fork", force=False)
        except (ValueError, RuntimeError):
            pass

    parser = argparse.ArgumentParser(description="Multi-Core CCTV Data Recovery Engine (Xiongmai H.264)")
    parser.add_argument("device", nargs="?", default=None, help="Drive path (e.g. \\\\.\\PhysicalDrive1, /dev/rdisk4, /dev/sdb, or disk.img)")
    parser.add_argument("-s", "--select", action="store_true", help="Interactively select drive")
    parser.add_argument("-l", "--list-disks", action="store_true", help="List all detected disks and exit")
    parser.add_argument("-o", "--output", default="./recovered_all_cctv", help="Output directory")
    parser.add_argument("--lang", choices=["th", "en"], default="en", help="Interface language (th: Thai, en: English, default: en)")
    parser.add_argument("-y", "--yes", action="store_true", help="Auto-confirm recovery without interactive prompt")
    parser.add_argument("--all", action="store_true", default=True, help="Extract ALL clips from all dates")
    parser.add_argument("--dates", type=str, default="", help="Specific dates comma-separated (e.g. 2026-09-06,2026-09-07)")
    parser.add_argument("--cores", type=int, default=DEFAULT_CORES, help=f"Number of CPU cores (default: {DEFAULT_CORES})")

    args = parser.parse_args()

    if args.lang:
        set_language(args.lang)

    if args.list_disks:
        drives = get_available_drives(include_virtual=True)
        print_drives_table(drives)
        sys.exit(0)

    if args.select or not args.device:
        device_path = interactive_select_drive()
    else:
        device_path = args.device
        if sys.platform == "darwin" and device_path.startswith("/dev/disk") and not device_path.startswith("/dev/rdisk"):
            device_path = device_path.replace("/dev/disk", "/dev/rdisk")
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
            print(f"      python cctv_recover.py {device_path} --dates {args.dates or '2026-09-06'}\n")
        else:
            print(f"      sudo python3 cctv_recover.py {device_path} --dates {args.dates or '2026-09-06'}\n")
        print("=" * 80 + "\n")

    target_dates = set(d.strip() for d in args.dates.split(",")) if args.dates else set()

    recover_universal(
        source_device=device_path,
        output_dir=args.output,
        enabled_types={"cctv"},
        target_dates=target_dates,
        num_workers=args.cores,
        auto_confirm=args.yes
    )

if __name__ == "__main__":
    main()
