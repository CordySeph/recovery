"""
Internationalization (i18n) & Bilingual UI System (English / Thai)
"""

import sys

# Safe UTF-8 Terminal Encoding Setup
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
if hasattr(sys.stderr, "reconfigure"):
    try:
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

CURRENT_LANG = "en"

STRINGS = {
    "en": {
        "app_title": "🚀 UNIVERSAL MULTI-CORE DATA RECOVERY ENGINE (PROFESSIONAL)",
        "app_desc": "High-Performance Multi-Core Parallel Data Recovery Tool",
        "source_label": "Source Device          : ",
        "cores_label": "CPU Cores Allocated    : ",
        "types_label": "Target File Types      : ",
        "dest_label": "Output Directory       : ",
        "drive_title": "🔍 Drive Selection Menu (Data Recovery Engine)",
        "drive_list_header": "💾 Available Disks & Drives Detected on System:",
        "drive_no_found": "  [!] No connected drives detected",
        "tag_external": "External / SD Card / USB ⭐ Recommended",
        "tag_internal": "Internal System Disk ⚠️",
        "opt_custom_path": "Specify custom Drive or Image file path (Custom Path / File)",
        "opt_switch_lang": "Switch Language / สลับภาษา (TH / EN)",
        "opt_quit": "Cancel / Exit program (Quit)",
        "prompt_select_drive": "👉 Select Drive (Enter 1-{n}, L, C or Q): ",
        "prompt_custom_drive": "👉 Enter Path of Drive or Image file (e.g. \\\\.\\PhysicalDrive1, /dev/rdisk4, or backup.img): ",
        "warn_internal": "\n⚠️  Warning: You selected '{dev}' ({name}) which is the Internal System Disk",
        "confirm_internal": "❓ Are you sure you want to scan this drive? (y/N): ",
        "mode_title": "🎯 Select Recovery / Imaging Mode:",
        "mode_1": "🌟 Recover All Files (Universal Mode: Images, RAW, Videos, Docs, Archives, Virtual Disks, Code, CCTV, etc.)",
        "mode_2": "📹 Recover CCTV Clips (Xiongmai H.264 & Auto-Remux to MP4)",
        "mode_3": "🖼️  Recover Photos & Images Only (JPG, PNG, GIF, WEBP, BMP, HEIC)",
        "mode_4": "📷 Recover Professional Camera RAW Photos (CR2, CR3, NEF, ARW, DNG, TIFF)",
        "mode_5": "🎬 Recover Videos Only (MP4, MOV, AVI, CCTV)",
        "mode_6": "📄 Recover Documents Only (PDF, DOCX, XLSX, PPTX, TXT)",
        "mode_7": "🎨 Recover Graphics & Vector Design (PSD, AI, EPS, SVG)",
        "mode_8": "📦 Recover Archives Only (ZIP, 7Z, RAR, TAR, GZ)",
        "mode_9": "🎵 Recover Audio Only (MP3, WAV, FLAC, OGG, M4A, AAC)",
        "mode_10": "🗄️  Recover Databases (SQLite)",
        "mode_11": "💽 Recover Virtual Disks & Images (VMDK, VHD, VHDX, ISO)",
        "mode_12": "✉️  Recover Emails & Mailboxes (EML, PST, MSG)",
        "mode_13": "💻 Recover Source Code & Scripts (PY, JS, HTML, JSON, CSV, SQL)",
        "mode_14": "🛡️  Disk Imaging Mode (Clone Disk to .img File before recovery)",
        "prompt_select_mode": "👉 Select Mode (1-14) [Default 1]: ",
        "dest_title": "📁 Select Output Destination Drive / Directory:",
        "tag_default_dest": "Default Folder",
        "tag_desktop": "Desktop",
        "tag_external_dest": "External Drive ⭐ Recommended",
        "opt_custom_dest": "Specify custom folder / drive path (Custom Destination)",
        "prompt_select_dest": "👉 Select Destination (1-{n}, C or Q) [Default 1]: ",
        "prompt_custom_dest": "👉 Enter Path of target folder/drive: ",
        "free_space": "Free Space",
        "scanning_start": "[*] Starting sector scan with {mb} MB High-Speed I/O Buffer...\n",
        "scan_progress": "Scanned",
        "speed": "Speed",
        "eta": "ETA",
        "found_files": "Files Found",
        "scan_completed": "🎉 Disk scan completed in {elapsed:.1f}s! Total files detected: {total}",
        "no_files_found": "[!] No files found matching selected criteria",
        "scan_only_done": "\n[*] Scan completed (Scan-Only Mode: No files were written to disk)",
        "confirm_recover": "❓ Detected {total} files. Start data recovery process? [Y/n]: ",
        "extracting": "\n[🎯] Extracting, validating integrity, and saving {total} files to CPU {cores} Workers...",
        "all_done": "🎉 Recovery completed successfully for {total} files!",
        "out_folder": "📁 Output Folder       : ",
        "out_gallery": "🖼️  Visual Gallery      : ",
        "out_report": "📑 Audit CSV Report    : ",
        "out_bad_sectors": "🛡️  Bad Sectors Map Log : ",
        "out_dedup_stat": "🧹 Deduplication Saved : {count} duplicate files omitted",
        "permission_error": "[!] ERROR: Administrator / Root privileges required to access {dev}",
        "sudo_hint": "👉 Please run the command again with elevated privileges (Administrator / sudo):",
        "clone_title": "🛡️ DISK IMAGING & RAW CLONE ENGINE (BIT-BY-BIT DUMP)",
        "clone_source": "[*] Source Device : ",
        "clone_dest": "[*] Target Image  : ",
        "clone_progress": "Copied",
        "clone_rem_time": "Time Left",
        "clone_done": "🎉 Disk cloned successfully in {elapsed:.1f}s!",
        "clone_hint": "👉 You can now safely recover data from this image file:",
        "checkpoint_found": "[⚡] Checkpoint found at position {gb:.2f} GB ({count} files detected)",
        "checkpoint_resume_prompt": "👉 Resume scanning from last checkpoint? [Y/n]: ",
        "resume_continuing": "[*] Resuming scan from byte offset: {bytes} ({gb:.2f} GB)\n",
        "cancel_msg": "[*] Operation cancelled.",
        "auto_raw_device": "[*] Normalized path to Raw Character Device: {dev}",
        "bad_sector_detected": "\n[⚠️] Bad sector / Read error at offset {offset_hex}. Auto-skipping damaged block safely...",
        "smart_title": "🩺 S.M.A.R.T. Drive Health Diagnostics",
        "smart_score_label": "Drive Health Score       : {score}/100 ({grade})",
        "smart_risk_label": "Drive Failure Risk       : [{risk}]",
        "smart_warn_critical": "⚠️  CRITICAL: Physical drive hardware has severe damage! Recommend cloning with --clone before scanning.",
        "fs_parsing_msg": "[*] Scanning remnant FAT/NTFS File System structures for original filenames...",
        "fs_found_msg": "[*] Indexed {count} original filenames from File System metadata.",
        "server_started_msg": "🌐 Local Web Dashboard active at http://localhost:{port}/gallery.html",
        "repair_video_success": "🎉 Successfully repaired video container: {dest}",
        "repair_video_failed": "[!] Failed to repair video: {msg}",
        "crypto_detected_warn": "🚨 WARNING: Detected encrypted volume headers ({types}) on target device!",
        "crypto_detected_advice": "👉 Raw carving on encrypted volumes yields ciphertext. Please decrypt/mount volume first.",
        "thermal_alert_msg": "🌡️ Thermal Guard: Drive reached {temp}°C (Exceeds {max}°C). Cooling down...",
        "partition_scan_done": "🧩 Partition scan found {count} lost/deleted volumes.",
        "sensitive_data_found_msg": "🚨 Detected {count} files containing sensitive personal/financial data.",
    },
    "th": {
        "app_title": "🚀 UNIVERSAL MULTI-CORE DATA RECOVERY ENGINE (PROFESSIONAL)",
        "app_desc": "เครื่องมือกู้คืนข้อมูลประสิทธิภาพสูง รองรับทุกไฟล์และกล้องวงจรปิด",
        "source_label": "แหล่งข้อมูล (Source)     : ",
        "cores_label": "จำนวน CPU Cores ที่ใช้งาน : ",
        "types_label": "ประเภทไฟล์ที่ค้นหา         : ",
        "dest_label": "โฟลเดอร์ปลายทาง (Output)   : ",
        "drive_title": "🔍 ระบบเลือก Drive สำหรับกู้ข้อมูล (Data Recovery Engine)",
        "drive_list_header": "💾 รายการ Drive / ดิสก์ทั้งหมดที่ตรวจพบในเครื่อง:",
        "drive_no_found": "  [!] ไม่พบ Drive ที่เชื่อมต่ออยู่",
        "tag_external": "External / SD Card / USB ⭐ แนะนำ",
        "tag_internal": "Internal System Disk ⚠️",
        "opt_custom_path": "ระบุเส้นทาง Drive หรือไฟล์ Image ด้วยตนเอง (Custom Path / File)",
        "opt_switch_lang": "Switch Language / สลับภาษา (EN / TH)",
        "opt_quit": "ยกเลิก / ออกจากโปรแกรม (Quit)",
        "prompt_select_drive": "👉 กรุณาเลือก Drive (ระบุหมายเลข 1-{n}, L, C หรือ Q): ",
        "prompt_custom_drive": "👉 ป้อน Path ของ Drive หรือ Image file (เช่น \\\\.\\PhysicalDrive1, /dev/rdisk4 หรือ backup.img): ",
        "warn_internal": "\n⚠️  คำเตือน: คุณเลือก '{dev}' ({name}) ซึ่งเป็น Internal System Disk",
        "confirm_internal": "❓ คุณแน่ใจหรือไม่ว่าต้องการสแกนกู้ข้อมูลจากไดรฟ์นี้? (y/N): ",
        "mode_title": "🎯 เลือกโหมดการทำงาน (Recovery / Imaging Mode):",
        "mode_1": "🌟 กู้ข้อมูลทุกอย่าง (Universal Mode: รูปภาพ, RAW Photos, วิดีโอ, เอกสาร, กราฟิก, Virtual Disks, โค้ด, CCTV ฯลฯ)",
        "mode_2": "📹 กู้เฉพาะคลิปกล้องวงจรปิด (CCTV Mode: Xiongmai H.264 & แปลงเป็น MP4)",
        "mode_3": "🖼️  กู้เฉพาะรูปภาพทั่วไป (Photos: JPG, PNG, GIF, WEBP, BMP, HEIC)",
        "mode_4": "📷 กู้เฉพาะรูปกล้องโปร / RAW Photos (CR2, CR3, NEF, ARW, DNG, TIFF)",
        "mode_5": "🎬 กู้เฉพาะวิดีโอ (Videos: MP4, MOV, AVI, CCTV)",
        "mode_6": "📄 กู้เฉพาะเอกสาร (Documents: PDF, DOCX, XLSX, PPTX, TXT)",
        "mode_7": "🎨 กู้เฉพาะไฟล์กราฟิก & ออกแบบ (Design: PSD, AI, EPS, SVG)",
        "mode_8": "📦 กู้เฉพาะไฟล์บีบอัด (Archives: ZIP, 7Z, RAR, TAR, GZ)",
        "mode_9": "🎵 กู้เฉพาะไฟล์เสียง (Audio: MP3, WAV, FLAC, OGG, M4A, AAC)",
        "mode_10": "🗄️  กู้ฐานข้อมูล (Databases: SQLite)",
        "mode_11": "💽 กู้ไฟล์ Virtual Disks & Disk Images (VMDK, VHD, VHDX, ISO)",
        "mode_12": "✉️  กู้ไฟล์อีเมลและกล่องข้อความ (Emails: EML, PST, MSG)",
        "mode_13": "💻 กู้ซอร์สโค้ดและสคริปต์ (Code: PY, JS, HTML, JSON, CSV, SQL)",
        "mode_14": "🛡️  โหมดทำสำเนาดิสก์ (Clone Disk to .img File ก่อนกู้ข้อมูล)",
        "prompt_select_mode": "👉 เลือกโหมด (1-14) [ค่าเริ่มต้น 1]: ",
        "dest_title": "📁 เลือก Drive / โฟลเดอร์ปลายทางสำหรับบันทึกไฟล์ที่กู้ได้ (Output Destination):",
        "tag_default_dest": "โฟลเดอร์เริ่มต้น",
        "tag_desktop": "Desktop",
        "tag_external_dest": "External Drive ⭐ แนะนำ",
        "opt_custom_dest": "ระบุเส้นทางโฟลเดอร์หรือไดรฟ์ปลายทางด้วยตนเอง (Custom Destination)",
        "prompt_select_dest": "👉 เลือกตำแหน่งบันทึกข้อมูล (1-{n}, C หรือ Q) [ค่าเริ่มต้น 1]: ",
        "prompt_custom_dest": "👉 ป้อน Path ของโฟลเดอร์/Drive ปลายทางที่ต้องการบันทึก: ",
        "free_space": "พื้นที่ว่าง",
        "scanning_start": "[*] เริ่มสแกนเซกเตอร์ดิสก์ด้วย High-Speed I/O Buffer ขนาด {mb} MB...\n",
        "scan_progress": "สแกนแล้ว",
        "speed": "ความเร็ว",
        "eta": "เวลาที่เหลือ",
        "found_files": "ตรวจพบไฟล์",
        "scan_completed": "🎉 สแกนดิสก์เสร็จสิ้นในเวลา {elapsed:.1f} วินาที! ตรวจพบไฟล์ทั้งหมด: {total} ไฟล์",
        "no_files_found": "[!] ไม่พบข้อมูลไฟล์ตรงกับเงื่อนไขที่เลือก",
        "scan_only_done": "\n[*] สแกนเสร็จสิ้น (โหมด Scan-Only: ไม่มีการบันทึกไฟล์ลงเครื่อง)",
        "confirm_recover": "❓ ตรวจพบ {total} ไฟล์ ต้องการเริ่มขั้นตอนกู้ข้อมูลหรือไม่? [Y/n]: ",
        "extracting": "\n[🎯] กำลังสกัด ตรวจสอบความสมบูรณ์ และบันทึก {total} ไฟล์ ไปยัง CPU {cores} Workers...",
        "all_done": "🎉 กู้ข้อมูลและบันทึกไฟล์ทั้งหมดเสร็จสิ้นสมบูรณ์ {total} ไฟล์!",
        "out_folder": "📁 โฟลเดอร์ที่เก็บไฟล์       : ",
        "out_gallery": "🖼️  หน้าเว็บแกลเลอรี         : ",
        "out_report": "📑 รายงาน Audit CSV        : ",
        "out_bad_sectors": "🛡️  บันทึก Bad Sector Map  : ",
        "out_dedup_stat": "🧹 ตัดไฟล์ซ้ำ (Deduplication) : ลดไฟล์ซ้ำไป {count} ไฟล์",
        "permission_error": "[!] ERROR: ต้องการสิทธิ์ Administrator หรือ root (sudo) ในการเข้าถึง {dev}",
        "sudo_hint": "👉 กรุณารันคำสั่งใหม่อีกครั้งด้วยสิทธิ์ Administrator หรือ sudo:",
        "clone_title": "🛡️ DISK IMAGING & RAW CLONE ENGINE (BIT-BY-BIT DUMP)",
        "clone_source": "[*] ไดรฟ์ต้นทาง (Source)     : ",
        "clone_dest": "[*] ไฟล์ปลายทาง (Image File) : ",
        "clone_progress": "คัดลอกแล้ว",
        "clone_rem_time": "เหลือเวลา",
        "clone_done": "🎉 สำเนาดิสก์เสร็จสมบูรณ์ในเวลา {elapsed:.1f} วินาที!",
        "clone_hint": "👉 คุณสามารถสั่งกู้ข้อมูลจากไฟล์อิมเมจนี้ได้อย่างปลอดภัยทันที:",
        "checkpoint_found": "[⚡] ตรวจพบบันทึกการสแกนเดิมที่ตำแหน่ง {gb:.2f} GB (พบ {count} ไฟล์)",
        "checkpoint_resume_prompt": "👉 ต้องการสแกนต่อจากจุดเดิมหรือไม่? [Y/n]: ",
        "resume_continuing": "[*] ดำเนินการสแกนต่อจากไบต์ที่: {bytes} ({gb:.2f} GB)\n",
        "cancel_msg": "[*] ยกเลิกการทำงานเรียบร้อย",
        "auto_raw_device": "[*] ปรับเส้นทางเป็น Raw Device อัตโนมัติเพื่อความเร็วสูงสุด: {dev}",
        "bad_sector_detected": "\n[⚠️] ตรวจพบ Bad Sector / อ่านดิสก์ขัดข้องที่ Offset {offset_hex} ระบบกำลังข้ามจุดเสียหายให้อัตโนมัติ...",
        "smart_title": "🩺 รายงานตรวจสุขภาพดิสก์ S.M.A.R.T. Health Diagnostics",
        "smart_score_label": "คะแนนสุขภาพดิสก์           : {score}/100 ({grade})",
        "smart_risk_label": "ระดับความเสี่ยงของดิสก์      : [{risk}]",
        "smart_warn_critical": "⚠️  เตือนระดับวิกฤต: ฮาร์ดดิสก์มีความเสียหายทางกายภาพสูง! แนะนำให้โคลนด้วยคำสั่ง --clone ก่อนสแกน",
        "fs_parsing_msg": "[*] กำลังสแกนหาโครงสร้าง FAT/NTFS เพื่อกู้ชื่อไฟล์เดิมและโฟลเดอร์เดิม...",
        "fs_found_msg": "[*] ทำดัชนีชื่อไฟล์เดิมสำเร็จ {count} ไฟล์ จากโครงสร้าง File System",
        "server_started_msg": "🌐 เปิดหน้า Local Web Dashboard สำเร็จที่ http://localhost:{port}/gallery.html",
        "repair_video_success": "🎉 ซ่อมแซมโครงสร้างวิดีโอสำเร็จ: {dest}",
        "repair_video_failed": "[!] ซ่อมแซมวิดีโอไม่สำเร็จ: {msg}",
        "crypto_detected_warn": "🚨 แจ้งเตือน: ตรวจพบโครงสร้างพาร์ติชันที่ถูกเข้ารหัส ({types}) บนไดรฟ์เป้าหมาย!",
        "crypto_detected_advice": "👉 การสแกนแบบ Raw บนไดรฟ์ที่เข้ารหัสจะได้ข้อมูลสุ่ม แนะนำให้ปลดล็อค (Mount/Decrypt) ก่อนสแกน",
        "thermal_alert_msg": "🌡️ ระบบคุมความร้อน: อุณหภูมิดิสก์แตะ {temp}°C (เกินเกณฑ์ {max}°C) กำลังพักลดความร้อน...",
        "partition_scan_done": "🧩 สแกนพบพาร์ติชันที่หลงเหลือ/ถูกลบจำนวน {count} พาร์ติชัน",
        "sensitive_data_found_msg": "🚨 ตรวจพบ {count} ไฟล์ที่มีข้อมูลส่วนบุคคลหรือเอกสารสำคัญ (เลขบัตร/สัญญา/การเงิน)",
    }
}

def t(key: str, **kwargs) -> str:
    """Translate string key with interpolation."""
    lang_dict = STRINGS.get(CURRENT_LANG, STRINGS["en"])
    text = lang_dict.get(key, STRINGS["en"].get(key, key))
    if kwargs:
        try:
            return text.format(**kwargs)
        except Exception:
            return text
    return text

def set_language(lang: str):
    """Set global language (en or th)."""
    global CURRENT_LANG
    if lang and lang.lower() in ("th", "thai"):
        CURRENT_LANG = "th"
    elif lang and lang.lower() in ("en", "english"):
        CURRENT_LANG = "en"
