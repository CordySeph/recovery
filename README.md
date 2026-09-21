# 🚀 Universal Multi-Core Data Recovery Engine (Professional / Forensic Grade)

เครื่องมือกู้คืนข้อมูลประสิทธิภาพสูงระดับมืออาชีพและนิติวิทยาศาสตร์ดิจิทัล (**Digital Forensics & ISO/IEC 27037 Standard**) ทำงานแบบ **Multi-Core Parallel Processing (100% CPU Speed)** ออกแบบสถาปัตยกรรมแบบ **Modular Core Engine (`recovery_engine`)** เพื่อกู้คืนไฟล์ทุกประเภทจาก Flash Drive, SD Card, Hard Drive, External Drive, SSD, กล้องดิจิทัล, กล้องวงจรปิด และไฟล์ดิสก์อิมเมจ (`.img` / `.raw` / `.dd`) แม้พาร์ติชันจะเสียหาย ฟอร์แมต (Quick Format) หรือระบบไฟล์พังจนมองไม่เห็นไดรฟ์

---

## 📑 สารบัญ (Table of Contents)
- [🌟 ฟีเจอร์เด่นระดับมืออาชีพ (Professional Features)](#-ฟีเจอร์เด่นระดับมืออาชีพ-professional-features)
- [📂 ชนิดไฟล์ที่รองรับ (Supported File Types - 11 หมวดหมู่)](#-ชนิดไฟล์ที่รองรับ-supported-file-types---11-หมวดหมู่)
- [🏗️ สถาปัตยกรรมโปรแกรม (Modular Architecture)](#️-สถาปัตยกรรมโปรแกรม-modular-architecture)
- [📋 ความต้องการของระบบ & การติดตั้ง (Installation & Prerequisites)](#-ความต้องการของระบบ--การติดตั้ง-installation--prerequisites)
- [🚀 คู่มือการใช้งานอย่างละเอียด (Comprehensive Usage Guide)](#-คู่มือการใช้งานอย่างละเอียด-comprehensive-usage-guide)
  - [แนวทางที่ 1: ใช้งานผ่านเมนู Interactive (แนะนำที่สุดสำหรับผู้ใช้งานทั่วไป ⭐)](#แนวทางที่-1-ใช้งานผ่านเมนู-interactive-แนะนำที่สุดสำหรับผู้ใช้งานทั่วไป-)
  - [แนวทางที่ 2: สั่งงานผ่าน Command-Line (CLI Flags สำหรับงานขั้นสูง & สคริปต์อัตโนมัติ)](#แนวทางที่-2-สั่งงานผ่าน-command-line-cli-flags-สำหรับงานขั้นสูง--สคริปต์อัตโนมัติ)
  - [แนวทางที่ 3: ระบบตรวจสุขภาพดิสก์ก่อนสแกน (S.M.A.R.T. Health Diagnostics)](#แนวทางที่-3-ระบบตรวจสุขภาพดิสก์ก่อนสแกน-smart-health-diagnostics)
  - [แนวทางที่ 4: การตรวจจับไดรฟ์ที่เข้ารหัส (BitLocker / LUKS / FileVault Detector)](#แนวทางที่-4-การตรวจจับไดรฟ์ที่เข้ารหัส-bitlocker--luks--filevault-detector)
  - [แนวทางที่ 5: การสแกนกู้ตารางพาร์ติชันเดิม (Partition Table & VBR Rebuilder)](#แนวทางที่-5-การสแกนกู้ตารางพาร์ติชันเดิม-partition-table--vbr-rebuilder)
  - [แนวทางที่ 6: การตรวจสอบข้อมูลสำคัญและเลขบัตร (Sensitive Data & Thai ID Inspector)](#แนวทางที่-6-การตรวจสอบข้อมูลสำคัญและเลขบัตร-sensitive-data--thai-id-inspector)
  - [แนวทางที่ 7: ระบบคุมความร้อนดิสก์อัตโนมัติ (Thermal Guard & Auto-Throttle)](#แนวทางที่-7-ระบบคุมความร้อนดิสก์อัตโนมัติ-thermal-guard--auto-throttle)
  - [แนวทางที่ 8: การซ่อมไฟล์วิดีโอที่เปิดไม่ได้ (Video Auto-Repair & `moov` Rebuilder)](#แนวทางที่-8-การซ่อมไฟล์วิดีโอที่เปิดไม่ได้-video-auto-repair--moov-rebuilder)
  - [แนวทางที่ 9: การกู้ชื่อไฟล์เดิมและโฟลเดอร์เดิม (FAT / NTFS / EXT4 File System Parser)](#แนวทางที่-9-การกู้ชื่อไฟล์เดิมและโฟลเดอร์เดิม-fat--ntfs--ext4-file-system-parser)
  - [แนวทางที่ 10: หน้า Web Dashboard, Live Heatmap & Raw Hex Viewer (`--serve`)](#แนวทางที่-10-หน้า-web-dashboard-live-heatmap--raw-hex-viewer---serve)
  - [แนวทางที่ 11: รายงานนิติวิทยาศาสตร์ ISO/IEC 27037 & Dual Hashing (MD5 + SHA-256)](#แนวทางที่-11-รายงานนิติวิทยาศาสตร์-isoiec-27037--dual-hashing-md5--sha-256)
  - [แนวทางที่ 12: การส่งไฟล์ขึ้น Remote Server / NAS อัตโนมัติ (`--sftp-upload`)](#แนวทางที่-12-การส่งไฟล์ขึ้น-remote-server--nas-อัตโนมัติ---sftp-upload)
  - [แนวทางที่ 13: การกู้ข้อมูลกล้องวงจรปิด Xiongmai H.264 เฉพาะทาง (`cctv_recover.py`)](#แนวทางที่-13-การกู้ข้อมูลกล้องวงจรปิด-xiongmai-h264-เฉพาะทาง-cctv_recoverpy)
  - [แนวทางที่ 14: การนำไปใช้งานบนเครื่องที่ไม่มี Python (Standalone Portable Executable)](#แนวทางที่-14-การนำไปใช้งานบนเครื่องที่ไม่มี-python-standalone-portable-executable)
- [🌐 ระบบ 2 ภาษา (Bilingual UI: English Default / Thai)](#-ระบบ-2-ภาษา-bilingual-ui-english-default--thai)
- [🛡️ ระบบทนทานต่อ Bad Sector & โหมดทำสำเนาดิสก์ (Forensic Disk Imaging)](#️-ระบบทนทานต่อ-bad-sector--โหมดทำสำเนาดิสก์-forensic-disk-imaging)
- [🗂️ โครงสร้างโฟลเดอร์ผลลัพธ์ (Output Directory Structure)](#️-โครงสร้างโฟลเดอร์ผลลัพธ์-output-directory-structure)
- [💡 ข้อควรระวัง & มาตรฐาน Forensic (Forensic Best Practices)](#-ข้อควรระวัง--มาตรฐาน-forensic-forensic-best-practices)
- [🧪 ชุดการทดสอบ (Test Suites Coverage)](#-ชุดการทดสอบ-test-suites-coverage)
- [❓ คำถามที่พบบ่อย (FAQ)](#-คำถามที่พบบ่อย-faq)

---

## 🌟 ฟีเจอร์เด่นระดับมืออาชีพ (Professional Features)

1. **⚡ Multi-Core Parallel Processing (ความเร็วสูงสุด 100% CPU)**:
   - สแกนและสกัดไฟล์พร้อมกันทุกคอร์ CPU ด้วย High-Speed I/O Buffer ขนาด **64 MB** พร้อม Overlap 2MB ป้องกันไฟล์ตกหล่น
2. **⚖️ มาตรฐาน Forensic ISO/IEC 27037 & Dual Hashes (MD5 + SHA-256)**:
   - คำนวณค่า **MD5 และ SHA-256** พร้อมกันแบบ Real-time พร้อมออกรายงานพยานหลักฐานดิจิทัล `chain_of_custody.json` สำหรับใช้ในกระบวนการทางกฎหมาย
3. **🗺️ Visual Disk Sector Heatmap บน Web Dashboard**:
   - แผนที่แสดงความหนาแน่นของเซกเตอร์ดิสก์แบบ Interactive Heatmap บนหน้าเว็บแกลเลอรี
4. **🩺 ระบบตรวจสุขภาพดิสก์ล่วงหน้า (Pre-Scan S.M.A.R.T. Health Diagnostics)**:
   - ตรวจสอบค่าสถานะ S.M.A.R.T. (Reallocated Sectors, Pending Sectors, Temperature, Power-on Hours) และประเมินคะแนนความเสี่ยงของฮาร์ดดิสก์ก่อนเริ่มสแกน ป้องกันมอเตอร์/หัวอ่านพังถาวร
5. **🛡️ ระบบตรวจจับไดรฟ์ที่เข้ารหัส (Encrypted Volume & BitLocker/LUKS Detector)**:
   - ตรวจจับ Header การเข้ารหัส (BitLocker, LUKS v1/v2, Apple FileVault, Encrypted APFS) และแจ้งเตือนก่อนสแกนเพื่อป้องกันการเสียเวลาสแกน Ciphertext
6. **🧩 ระบบค้นหาและกู้ตารางพาร์ติชัน (Lost Partition Table & VBR Rebuilder)**:
   - ค้นหา MBR, GPT Header และ Boot Sector เดิม (NTFS, FAT32, exFAT, APFS, EXT4) เพื่อรายงานตำแหน่งและขนาดพาร์ติชันเดิมที่สูญหาย
7. **🔍 ระบบตรวจจับข้อมูลสำคัญและเลขบัตร (Sensitive Data & Thai ID Inspector)**:
   - สแกนเนื้อหาเอกสารเพื่อค้นหา **เลขบัตรประชาชน 13 หลัก (ตรวจสอบ Checksum จริง)**, หมายเลขบัตรเครดิต (Luhn Algorithm) และคีย์เวิร์ดการเงิน/สัญญา พร้อมติดแท็ก 🚨 Sensitive Data ให้อัตโนมัติ
8. **🌡️ ระบบคุมความร้อนดิสก์อัตโนมัติ (Thermal Guard & Auto-Throttle)**:
   - มอนิเตอร์อุณหภูมิดิสก์ระหว่างสแกน หากเกินเกณฑ์ที่กำหนด (เช่น 55°C) ระบบจะ Auto-Pause พักเครื่อง 20 วินาที เพื่อป้องกันความเสียหายจากความร้อนสะสม
9. **🔬 Interactive Raw Hex Viewer ใน Web Dashboard**:
   - หน้าแดชบอร์ดมีปุ่มคลิกดูเนื้อหาไบนารีระดับ Raw Hex + ASCII Dump ได้ทันทีผ่านเว็บเบราว์เซอร์
10. **☁️ การส่งไฟล์ขึ้น Remote Server / NAS อัตโนมัติ (`--sftp-upload`)**:
    - รองรับการคัดลอก/ซิงค์ชุดข้อมูลที่กู้ได้ตรงไปยัง Server/NAS ผ่าน SFTP/rsync ทันทีที่กู้เสร็จ
11. **🔧 ระบบซ่อมไฟล์วิดีโออัตโนมัติ (Video Auto-Repair & MP4/MOV `moov` Rebuilder)**:
    - ซ่อมแซมไฟล์วิดีโอ MP4 / MOV ที่เปิดเล่นไม่ได้โดยการ Reconstruct โครงสร้าง `moov` atom จาก Reference Video หรือ FastStart Remuxing
12. **🗂️ ระบบกู้ชื่อไฟล์เดิมและโครงสร้างเดิม (FAT / NTFS / EXT4 Remnant Parser)**:
    - สแกนหาตาราง Directory Entries (FAT32/exFAT), $MFT Records (NTFS) และ Linux EXT4 Inode directory blocks เพื่อคืน **"ชื่อไฟล์เดิม (Original Filenames)"**
13. **📷 ระบบกู้ไฟล์ภาพกล้องโปร (RAW Photo Carver with TIFF/EXIF Parser)**:
    - สกัดภาพ RAW จากกล้อง **Canon (.cr2, .cr3), Nikon (.nef), Sony (.arw), Adobe DNG (.dng) และ TIFF** พร้อมดึงข้อมูลรุ่นกล้องและวันที่ถ่ายจริง
14. **🎨 ระบบกู้ไฟล์งานออกแบบ (Graphics & Vector Carver)**:
    - กู้คืนไฟล์ Adobe Photoshop (`.psd`), Illustrator (`.ai`), PostScript (`.eps`) และ Scalable Vector Graphics (`.svg`)
15. **💽 ระบบกู้ไฟล์ดิสก์เสมือน (Virtual Disks & Images)**:
    - รองรับไฟล์ **VMware (.vmdk), Hyper-V (.vhd, .vhdx) และ ISO (.iso)**
16. **✉️ ระบบกู้ไฟล์อีเมล (Email & Mailbox Carver)**:
    - รองรับไฟล์ข้อความ **RFC 822 (.eml) และ Outlook Personal Storage (.pst, .msg)**
17. **💻 ระบบกู้ซอร์สโค้ดและสคริปต์ (Code Carver)**:
    - รองรับไฟล์สคริปต์ **Python (.py), Web (.html), JSON (.json), CSV (.csv) และ SQL (.sql)**
18. **🎵 ระบบกู้ไฟล์เสียงพร้อมอ่าน Metadata (Audio Carver with ID3 / Vorbis Tags)**:
    - กู้คืนไฟล์ **MP3, WAV, FLAC, OGG, M4A, AAC** พร้อมอ่าน ID3v1, ID3v2, Vorbis Comments แล้วแยกโฟลเดอร์ตาม `Audio/<Artist>/<Album>/<Title>.<ext>` อัตโนมัติ
19. **🛡️ ระบบทนทานต่อ Bad Sector อัตโนมัติ (Bad Sector Fault-Tolerance & Auto-Skip)**:
    - สลับไปอ่านละเอียดระดับ 4KB Block อัตโนมัติเมื่อเจอบล็อกเสีย พร้อมบันทึกแผนที่ลงไฟล์ `bad_sectors_map.log`
20. **🧹 ระบบตัดไฟล์ซ้ำอัตโนมัติ (Real-Time Hash-based Deduplication)**:
    - ตรวจจับค่า MD5/SHA-256 Checksum แบบ Real-Time และข้ามการบันทึกไฟล์ที่ซ้ำกัน
21. **⏱️ คำนวณเวลาที่เหลือแบบ Real-Time (Accurate Live ETA & Speed)**:
    - แสดงความเร็วในการอ่านดิสก์ (MB/s) และเวลานับถอยหลังโดยประมาณ
22. **🌐 ระบบ 2 ภาษาในตัว (Bilingual UI Support: English Default / Thai)**:
    - รองรับทั้งภาษาอังกฤษและภาษาไทย สลับภาษาได้ทันทีด้วยปุ่ม `[L]` หรือ Flag `--lang th`

---

## 📂 ชนิดไฟล์ที่รองรับ (Supported File Types - 11 หมวดหมู่)

| หมวดหมู่ | นามสกุลไฟล์ | รายละเอียดโครงสร้าง & การตรวจสอบ |
| :--- | :--- | :--- |
| 📷 **รูปภาพทั่วไป (Images)** | `.jpg`, `.jpeg`, `.png`, `.gif`, `.webp`, `.bmp`, `.heic` | สกัด EXIF DateTime จัดโฟลเดอร์ตามวันจริง |
| 📷 **รูปกล้องโปร (RAW Photos)** | `.cr2`, `.cr3`, `.nef`, `.arw`, `.dng`, `.tiff` | ดึงรุ่นกล้อง Canon/Nikon/Sony/Adobe DNG และวันที่ถ่าย |
| 🎥 **วิดีโอ (Videos)** | `.mp4`, `.mov`, `.avi` | สกัดคอนเทนเนอร์ Atom Header (`ftyp`, `moov`, `mdat`) |
| 📹 **กล้องวงจรปิด (CCTV)** | `.264` / `.mp4` | รองรับชิป Xiongmai H.264 ดึง Timestamp วันเวลาจริง และแปลงเป็น MP4 |
| 🎵 **ไฟล์เสียง (Audio)** | `.mp3`, `.wav`, `.flac`, `.ogg`, `.m4a`, `.aac` | ตรวจสอบ ID3 Tag, Vorbis Comments แยกตามศิลปิน/อัลบั้ม |
| 📄 **เอกสาร (Documents)** | `.pdf`, `.docx`, `.xlsx`, `.pptx`, `.txt` | ตรวจสอบโครงสร้าง, สแกนเลขบัตร ปชช., บัตรเครดิต, สัญญา |
| 🎨 **กราฟิก & เวกเตอร์ (Graphics)** | `.psd`, `.ai`, `.eps`, `.svg` | ตรวจสอบ Photoshop 8BPS Header, Vector Paths |
| 📦 **ไฟล์บีบอัด (Archives)** | `.zip`, `.7z`, `.rar`, `.tar`, `.gz` | ตรวจสอบ Central Directory, Archive Markers, CRC |
| 🗄️ **ฐานข้อมูล (Databases)** | `.sqlite` / `.db` | ไฟล์ฐานข้อมูล SQLite Format 3 ตรวจสอบ B-Tree Integrity |
| 💽 **ดิสก์เสมือน (Virtual Disks)** | `.vmdk`, `.vhd`, `.vhdx`, `.iso` | VMware Sparse, Hyper-V VHDX, ISO 9660 Images |
| ✉️ **อีเมล (Emails)** | `.eml`, `.msg`, `.pst` | RFC 822 Headers, Outlook Personal Storage Tables |
| 💻 **ซอร์สโค้ด (Code)** | `.py`, `.js`, `.html`, `.json`, `.csv`, `.sql` | โครงสร้างสคริปต์, ตารางข้อมูล และฐานข้อมูล SQL |

---

## 🏗️ สถาปัตยกรรมโปรแกรม (Modular Architecture)

```text
re/
├── recover.py                     # [Entry Point] เมนูหลัก, CLI Flags, Web Server & Video Repair
├── cctv_recover.py                # [Entry Point] สคริปต์กู้กล้องวงจรปิดเฉพาะทาง
├── build_standalone.sh            # สคริปต์คอมไพล์เป็น Portable Binary (PyInstaller)
├── test_engine.py                 # ชุดทดสอบ Unit & Functional Test Suite (19 หมวดหมู่)
├── pyproject.toml                 # Packaging configuration (pip install -e .)
├── requirements.txt               # Dependencies documentation
├── .gitignore                     # Git ignore configuration
├── README.md                      # คู่มือการใช้งานฉบับสมบูรณ์
└── recovery_engine/               # [Core Package] แกนกลางระบบกู้ข้อมูล
    ├── __init__.py                # Package Metadata
    ├── config.py                  # ค่าคงที่, Magic Signatures, 11 File Categories
    ├── i18n.py                    # ระบบแปลภาษา 2 ภาษา (EN / TH) และ Safe UTF-8
    ├── disk_io.py                 # ตรวจจับไดรฟ์, Write-Block Check, Resilient Bad Sector Reader, Disk Clone
    ├── deduplicator.py            # ตัวตรวจจับและตัดไฟล์ซ้ำด้วย Dual Hashes (MD5 + SHA-256)
    ├── validators.py              # ตัวตรวจสอบความสมบูรณ์ของโครงสร้างไฟล์แต่ละชนิด
    ├── reporter.py                # ตัวสร้างเว็บแกลเลอรี HTML (Heatmap), CSV และ Chain of Custody JSON
    ├── scanner.py                 # ตัวควบคุมการสแกนและดึงไฟล์แบบ Multi-Core Parallel
    ├── smart_checker.py           # ตัวตรวจสุขภาพดิสก์ S.M.A.R.T. และประเมินความเสี่ยง
    ├── crypto_detector.py         # ตัวตรวจจับไดรฟ์ที่เข้ารหัส (BitLocker, LUKS, FileVault)
    ├── partition_rebuilder.py     # ตัวค้นหาและกู้ตารางพาร์ติชันเดิม (MBR, GPT, VBR)
    ├── doc_inspector.py           # ตัวตรวจจับข้อมูลสำคัญ (เลขบัตร ปชช., บัตรเครดิต, สัญญา)
    ├── thermal_guard.py           # ตัวควบคุมอุณหภูมิดิสก์และพักเครื่องอัตโนมัติ
    ├── remote_exporter.py         # ตัวเชื่อมต่อและส่งไฟล์ขึ้น Remote NAS / SFTP
    ├── video_repair.py            # ตัวซ่อมไฟล์วิดีโอและประกอบ moov atom ใหม่
    ├── fs_parser.py               # ตัวอ่านโครงสร้าง FAT/NTFS/EXT4 เพื่อกู้ชื่อไฟล์เดิม
    ├── web_server.py              # ตัวรัน Local Web Dashboard & Media Streaming Server + Hex API
    └── carvers/                   # โมดูล Carving เจาะจงเฉพาะกลุ่มไฟล์
        ├── __init__.py
        ├── image_carver.py        # สแกนรูปภาพ + สกัดวันที่จาก EXIF Metadata
        ├── raw_carver.py          # สแกนรูปกล้องโปร RAW (CR2/CR3/NEF/ARW/DNG/TIFF)
        ├── video_carver.py        # สแกนวิดีโอ MP4, MOV, AVI และสตรีม CCTV H.264
        ├── audio_carver.py        # สแกนไฟล์เสียง MP3, WAV, FLAC, OGG, M4A + ID3 Tags
        ├── doc_carver.py          # สแกนเอกสาร PDF และ Microsoft Office
        ├── graphics_carver.py     # สแกน Photoshop PSD, Illustrator AI, EPS, SVG
        ├── archive_carver.py      # สแกนไฟล์บีบอัด ZIP, 7Z, RAR, TAR, GZ และ SQLite DB
        ├── virtual_disk_carver.py # สแกนดิสก์เสมือน VMDK, VHD, VHDX, ISO
        ├── email_carver.py        # สแกนอีเมล EML และ Outlook PST
        └── code_carver.py         # สแกนโค้ด Python, HTML, SQL, JSON
```

---

## 📋 ความต้องการของระบบ & การติดตั้ง (Installation & Prerequisites)

* **ระบบปฏิบัติการ**: macOS, Linux (Ubuntu, Debian, Fedora, Arch, CentOS), Windows (ผ่าน WSL2 หรือ Git Bash)
* **Python Version**: Python 3.8 ขึ้นไป (รองรับจนถึง Python 3.14+)
* **Zero Dependencies Required**: ตัว Engine เขียนด้วย Pure Python Standard Library สามารถรันได้ทันทีโดยไม่ต้องติดตั้งไลบรารีภายนอก
* **การติดตั้งเป็น CLI Tool (Optional)**:
  ```bash
  pip install -e .
  # จากนั้นสามารถเรียกใช้งานผ่านคำสั่ง 'universal-recover' และ 'cctv-recover' ได้ทันที
  ```

---

## 🚀 คู่มือการใช้งานอย่างละเอียด (Comprehensive Usage Guide)

---

### แนวทางที่ 1: ใช้งานผ่านเมนู Interactive (แนะนำที่สุดสำหรับผู้ใช้งานทั่วไป ⭐)

เพียงเปิด Terminal และรันคำสั่งหลักด้วยสิทธิ์ `sudo`:

```bash
sudo python3 recover.py
```

#### ลำดับขั้นตอนการทำงานในเมนู Interactive:
1. **เลือกไดรฟ์ต้นทาง (Source Drive)**:
   - โปรแกรมจะแสดงรายการดิสก์ทั้งหมด พร้อมขนาด, ชนิด (Internal / External / SD Card), และ Bus Protocol
   - ป้อนตัวเลข `[1-N]` เพื่อเลือกไดรฟ์
   - กด `[L]` เพื่อสลับภาษาไทย / อังกฤษ
   - กด `[C]` เพื่อระบุ Path ไดรฟ์หรือไฟล์ Image ด้วยตนเอง (เช่น `/dev/rdisk4` หรือ `./dump.img`)
2. **การตรวจสอบอัตโนมัติก่อนสแกน (Pre-Scan Inspection)**:
   - ระบบจะตรวจสุขภาพดิสก์ (S.M.A.R.T. Diagnostics) และแจ้งเตือนทันทีหากพบความเสี่ยงที่หัวอ่าน/มอเตอร์จะพัง
   - ระบบจะตรวจจับโครงสร้างการเข้ารหัส (BitLocker / LUKS / FileVault) และแจ้งเตือนก่อนเริ่มสแกน
3. **เลือกโหมดการกู้ข้อมูล (14 หมวดหมู่)**:
   - `[1]` Universal Recovery (กู้ไฟล์ทุกประเภท)
   - `[2]` CCTV Clips (กล้องวงจรปิด Xiongmai H.264)
   - `[3]` Photos & Images (JPG, PNG, GIF, WEBP, BMP, HEIC)
   - `[4]` Professional RAW Photos (Canon CR2/CR3, Nikon NEF, Sony ARW, Adobe DNG, TIFF)
   - `[5]` Videos (MP4, MOV, AVI, CCTV)
   - `[6]` Documents (PDF, DOCX, XLSX, PPTX, TXT)
   - `[7]` Graphics & Vector Design (PSD, AI, EPS, SVG)
   - `[8]` Archives (ZIP, 7Z, RAR, TAR, GZ)
   - `[9]` Audio & Music (MP3, WAV, FLAC, OGG, M4A, AAC)
   - `[10]` Databases (SQLite DB)
   - `[11]` Virtual Disks & Disk Images (VMDK, VHD, VHDX, ISO)
   - `[12]` Emails & Mailboxes (EML, Outlook PST, MSG)
   - `[13]` Source Code & Scripts (PY, JS, HTML, JSON, CSV, SQL)
   - `[14]` Forensic Disk Clone (ทำสำเนาดิสก์เป็นไฟล์ `.img`)
4. **สแกนเซกเตอร์แบบคู่ขนาน (Multi-Core Processing)**:
   - ระบบแสดงแถบสถานะ: ปริมาณข้อมูลที่สแกนแล้ว (GB), ความเร็วการอ่าน (MB/s), เวลาที่เหลือโดยประมาณ (ETA), และจำนวนไฟล์ที่พบ
5. **เลือกโฟลเดอร์ปลายทาง (Destination Folder)**:
   - โปรแกรมจะแสดงรายการไดรฟ์ที่มีพื้นที่ว่างเพียงพอ และให้เลือกโฟลเดอร์สำหรับบันทึกไฟล์
6. **สกัดไฟล์, ตัดไฟล์ซ้ำ และสร้างรายงานอัตโนมัติ**:
   - บันทึกไฟล์พร้อมคืนชื่อไฟล์เดิม, วันที่ถ่ายจริงจาก EXIF, และสร้างไฟล์รายงาน `recovery_report.csv`, `chain_of_custody.json` และ `gallery.html` ให้ทันที

---

### แนวทางที่ 2: สั่งงานผ่าน Command-Line (CLI Flags สำหรับงานขั้นสูง & สคริปต์อัตโนมัติ)

สามารถระบุพารามิเตอร์ผ่าน Command Line Arguments เพื่อรันงานอัตโนมัติโดยไม่ต้องรอตอบคำถามใน Terminal:

#### ตารางสรุป CLI Flags ทั้งหมด:

| Flag | คำอธิบาย | ตัวอย่างการใช้งาน |
| :--- | :--- | :--- |
| `device` | เส้นทางไดรฟ์หรือไฟล์อิมเมจต้นทาง | `/dev/rdisk4` หรือ `./disk_dump.img` |
| `-o`, `--output` | โฟลเดอร์ปลายทางสำหรับจัดเก็บไฟล์กู้ได้ | `-o /Volumes/BackupDrive/recovered` |
| `--all` | กู้คืนไฟล์ทุกประเภท (Universal Mode) | `--all` |
| `--raw-photos` | กู้เฉพาะรูปกล้องโปร RAW (CR2, NEF, ARW, DNG, TIFF) | `--raw-photos` |
| `--photos` | กู้เฉพาะรูปภาพทั่วไป (JPG, PNG, GIF, WEBP, BMP, HEIC) | `--photos` |
| `--graphics` | กู้เฉพาะไฟล์กราฟิก/งานออกแบบ (PSD, AI, EPS, SVG) | `--graphics` |
| `--videos` | กู้เฉพาะวิดีโอ (MP4, MOV, AVI) | `--videos` |
| `--audio` | กู้เฉพาะไฟล์เสียง (MP3, WAV, FLAC, OGG, M4A, AAC) | `--audio` |
| `--docs` | กู้เฉพาะไฟล์เอกสาร (PDF, DOCX, XLSX, PPTX, TXT) | `--docs` |
| `--virtual-disks` | กู้เฉพาะดิสก์เสมือนและอิมเมจ (VMDK, VHD, VHDX, ISO) | `--virtual-disks` |
| `--emails` | กู้เฉพาะไฟล์อีเมล (EML, PST, MSG) | `--emails` |
| `--code` | กู้เฉพาะซอร์สโค้ดและสคริปต์ (PY, JS, HTML, JSON, SQL) | `--code` |
| `--cctv` | กู้เฉพาะคลิปกล้องวงจรปิด Xiongmai H.264 | `--cctv` |
| `--types` | ระบุนามสกุลไฟล์ที่ต้องการแบบคั่นด้วยจุลภาค | `--types "jpg,png,pdf,docx,psd"` |
| `--min-size` | กรองขนาดไฟล์ขั้นต่ำ (เช่น `50k`, `1m`, `10mb`) | `--min-size 100k` |
| `--max-size` | กรองขนาดไฟล์สูงสุด (เช่น `500m`, `2g`) | `--max-size 500m` |
| `--scan-only`, `-n` | สแกนหาไฟล์และทำสรุปรายการโดยไม่เขียนไฟล์ลงดิสก์ | `--scan-only` |
| `-y`, `--yes` | ยืนยันการกู้ข้อมูลอัตโนมัติ (ข้าม Prompt ถามยืนยัน) | `-y` |
| `--resume`, `-r` | ดำเนินการสแกนต่อจาก Checkpoint เดิมที่ค้างไว้ | `--resume` |
| `--cores` | จำนวน CPU Cores ที่ต้องการใช้ | `--cores 8` |
| `--lang` | สลับภาษาอินเทอร์เฟซ (`th` หรือ `en`) | `--lang th` |
| `--clone` | โคลนดิสก์แบบ Bit-by-Bit เป็นไฟล์อิมเมจก่อนกู้ | `--clone ./disk.img` |
| `--smart-check` | รันการตรวจสุขภาพฮาร์ดดิสก์ S.M.A.R.T. และออกรายงาน | `--smart-check` |
| `--check-crypto` | สแกนหา Header การเข้ารหัส BitLocker/LUKS/FileVault | `--check-crypto` |
| `--scan-partitions` | สแกนหาตารางพาร์ติชันเดิมและ Partition Boot Record | `--scan-partitions` |
| `--serve` | เปิดเว็บเซิร์ฟเวอร์ Local Web Dashboard & Streaming | `--serve ./recovered_data --port 8080` |
| `--repair-video` | ซ่อมแซมไฟล์วิดีโอ MP4 / MOV ที่เปิดเล่นไม่ได้ | `--repair-video corrupt.mp4` |
| `--ref-video` | ระบุไฟล์วิดีโออ้างอิงสำหรับใช้ซ่อมแซม `moov` atom | `--ref-video good_sample.mp4` |
| `--sftp-upload` | ซิงค์ไฟล์กู้ได้ขึ้น Remote SFTP/NAS อัตโนมัติ | `--sftp-upload user@nas:/volume1/backup` |
| `--thermal-limit` | กำหนดอุณหภูมิดิสก์สูงสุด (°C) ก่อนระบบพักเครื่อง | `--thermal-limit 55` |

#### ตัวอย่างคำสั่งที่ใช้บ่อย:

```bash
# 1. กู้ข้อมูลทั้งหมดแบบ Full Auto ไปยัง External Drive
sudo python3 recover.py /dev/rdisk4 --all -o /Volumes/BackupDrive/recovered_data -y

# 2. กู้เฉพาะรูปถ่าย RAW ของกล้อง Canon/Nikon/Sony ที่มีขนาดมากกว่า 5MB
sudo python3 recover.py /dev/rdisk4 --raw-photos --min-size 5m -o ./recovered_raw

# 3. กู้เฉพาะไฟล์งานออกแบบ PSD, AI, Vector
sudo python3 recover.py /dev/rdisk4 --graphics -o ./recovered_design

# 4. สแกนตรวจสอบไฟล์ทั้งหมดโดยยังไม่ต้องเขียนไฟล์ลงเครื่อง (Scan-Only)
sudo python3 recover.py /dev/rdisk4 --all --scan-only

# 5. สแกนต่อจากจุดเดิมหลังเครื่องดับหรือถูกหยุดการทำงาน (Resume)
sudo python3 recover.py /dev/rdisk4 --all --resume -o ./recovered_data
```

---

### แนวทางที่ 3: ระบบตรวจสุขภาพดิสก์ก่อนสแกน (S.M.A.R.T. Health Diagnostics)

เพื่อป้องกันไม่ให้ฮาร์ดดิสก์ที่มีความเสียหายทางกายภาพ (เช่น Bad Sector สะสม, หัวอ่านติดขัด, มอเตอร์ร้อน) เกิดความเสียหายถาวรระหว่างสแกนหนัก สามารถสั่งตรวจเช็กสุขภาพดิสก์แบบ Standalone ได้ทันที:

```bash
sudo python3 recover.py /dev/rdisk4 --smart-check
```

* **ผลลัพธ์ที่ได้**:
  - **Drive Health Score**: คะแนนสุขภาพดิสก์ (0 - 100%)
  - **Failure Risk Level**: ระดับความเสี่ยง (`HEALTHY`, `WARNING`, `CRITICAL`)
  - **Telemetry Data**: Reallocated Sectors, Pending Sectors, Uncorrectable Sectors, อุณหภูมิ และ Power-On Hours
  - **คำแนะนำทาง Forensic**: หากคะแนนอยู่ในระดับ `CRITICAL` ระบบจะแนะนำให้โคลนดิสก์ด้วยคำสั่ง `--clone` ไปยังไฟล์ Image ก่อนเสมอ

---

### แนวทางที่ 4: การตรวจจับไดรฟ์ที่เข้ารหัส (BitLocker / LUKS / FileVault Detector)

ตรวจสอบว่าไดรฟ์เป้าหมายถูกเข้ารหัสไว้หรือไม่ เพื่อไม่ให้เสียเวลาสแกนข้อมูลที่ติดการเข้ารหัส:

```bash
sudo python3 recover.py /dev/rdisk4 --check-crypto
```

* **รองรับการตรวจจับ**:
  - **Microsoft BitLocker** (`-FVE-FS-`, BitLocker To Go)
  - **Linux LUKS v1 / LUKS v2** (`LUKS\xBA\xBE`)
  - **Apple FileVault / Encrypted APFS** (`encx`, Apple CoreStorage)
  - **TrueCrypt / VeraCrypt Volume Headers**

---

### แนวทางที่ 5: การสแกนกู้ตารางพาร์ติชันเดิม (Partition Table & VBR Rebuilder)

กรณีไดรฟ์ถูกฟอร์แมต หรือพาร์ติชันหายจนกลายเป็น Unallocated Space สามารถสแกนหาตารางพาร์ติชันเดิมและ Boot Sector (VBR):

```bash
sudo python3 recover.py /dev/rdisk4 --scan-partitions
```

* **วิเคราะห์โครงสร้าง**:
  - **MBR Partition Table** (Master Boot Record)
  - **GPT Header & Partition Entries** (GUID Partition Table)
  - **Volume Boot Records (VBR)**: NTFS (`NTFS    `), FAT32 (`MSDOS5.0` / `FAT32`), exFAT (`EXFAT   `), Linux EXT4 Superblocks (`0xEF53`), macOS APFS Containers (`NXSB`)

---

### แนวทางที่ 6: การตรวจสอบข้อมูลสำคัญและเลขบัตร (Sensitive Data & Thai ID Inspector)

ระบบมีโมดูลวิเคราะห์เนื้อหาเอกสาร (PDF, DOCX, XLSX, TXT, SQLite) ในตัวแบบอัตโนมัติ:

* **การตรวจจับและยืนยันความถูกต้อง**:
  - **เลขบัตรประชาชนไทย 13 หลัก**: คำนวณสูตร Checksum ทางคณิตศาสตร์จริง (ไม่จับเลขสุ่ม)
  - **หมายเลขบัตรเครดิต 16 หลัก**: คำนวณตรวจสอบด้วย **Luhn Algorithm** (Visa, MasterCard, JCB, Amex)
  - **คีย์เวิร์ดสัญญา/การเงิน**: ตรวจจับคำว่า *สัญญา, เอกสารลับ, ข้อตกลง, ใบเสร็จ, Confidential, Financial Statement*
* **การแสดงผล**:
  - ติดป้ายกำกับสีแดง `🚨 Thai ID (1) • Contract` บนหน้ารายงาน `gallery.html` และระบุลงใน `recovery_report.csv` อัตโนมัติ

---

### แนวทางที่ 7: ระบบคุมความร้อนดิสก์อัตโนมัติ (Thermal Guard & Auto-Throttle)

เมื่อต้องกู้ข้อมูลจาก External HDD หรือ NVMe SSD ความจุสูง (1TB - 16TB) ที่มีความร้อนสะสมต่อเนื่อง:

```bash
# กำหนดอุณหภูมิเพดานสูงสุดที่ 55°C (ค่าเริ่มต้น)
sudo python3 recover.py /dev/rdisk4 --all -o ./recovered_data --thermal-limit 55
```

* **หลักการทำงาน**:
  - ระบบจะอ่านค่าอุณหภูมิจาก S.M.A.R.T. Sensor เป็นระยะ
  - หากอุณหภูมิสูงเกินค่าที่ตั้งไว้ ระบบจะทำการ **Auto-Pause (พัก I/O ชั่วคราว 20 วินาที)** เพื่อให้ดิสก์คลายความร้อน และกลับมาสแกนต่ออัตโนมัติเมื่ออุณหภูมิลดลง

---

### แนวทางที่ 8: การซ่อมไฟล์วิดีโอที่เปิดไม่ได้ (Video Auto-Repair & `moov` Rebuilder)

ไฟล์วิดีโอ MP4 / MOV ที่กู้ได้จากดิสก์ที่เสียหาย มักจะเปิดเล่นไม่ได้เนื่องจาก Header ส่วน `moov` atom ขาดหายหรือเสียหาย สามารถสั่งซ่อมแซมได้ทันที:

```bash
# ซ่อมแซมโดยใช้ไฟล์วิดีโอตัวอย่างที่ดีจากกล้องเดียวกัน (Reference File)
python3 recover.py --repair-video ./broken_video.mp4 --ref-video ./good_sample.mp4
```

* **กระบวนการซ่อมแซม**:
  1. ดึงโครงสร้าง Track Metadata, SPS/PPS Codec parameters จาก Reference Video
  2. กู้คืนและประมวลผลดัชนีภาพจากข้อมูลดิบ `mdat`
  3. ประกอบโครงสร้าง Atom ใหม่พร้อมย้าย `moov` ขึ้นมาไว้ด้านหน้า (FastStart Remuxing) ทำให้เปิดเล่นและสตรีมได้ 100%

---

### แนวทางที่ 9: การกู้ชื่อไฟล์เดิมและโฟลเดอร์เดิม (FAT / NTFS / EXT4 File System Parser)

โปรแกรมผสานการ Carve ระดับ Raw Sector เข้ากับการ Parse ตารางดัชนีของระบบไฟล์เดิม:

* **NTFS**: สแกนหา Master File Table Records (`$MFT` - `FILE`) ดึงชื่อไฟล์ภาษาไทย/Unicode, ขนาดไฟล์เดิม และ Timestamp
* **FAT32 / exFAT**: แกะตาราง Directory Entries และ Long File Name (LFN) Records
* **Linux EXT4**: แกะตาราง Inode Directory Leaf Blocks
* **ผลลัพธ์**: ไฟล์ที่กู้ได้จะถูกตั้งชื่อตามชื่อเดิม เช่น `0001_รายงานงบการเงิน_2026.xlsx` แทนการใช้ชื่อ `file_000001.xlsx`

---

### แนวทางที่ 10: หน้า Web Dashboard, Live Heatmap & Raw Hex Viewer (`--serve`)

เปิดหน้าเว็บแดชบอร์ดเพื่อตรวจสอบ, ค้นหา, สตรีมดูวิดีโอ/เสียง และตรวจดูเนื้อหาไบนารีระดับเซกเตอร์:

```bash
python3 recover.py --serve ./recovered_data --port 8080
```

* เปิดเบราว์เซอร์ไปที่: `http://localhost:8080`
* **ฟีเจอร์ในหน้าเว็บ Dashboard**:
  - 🗺️ **Live Physical Disk Sector Heatmap**: แผนภูมิแสดงตำแหน่งของข้อมูลบนดิสก์จริง (0% - 100%)
  - 🔍 **Instant Search & Filter**: ค้นหาตามชื่อเดิม, ประเภทไฟล์, ช่วงวันที่, ป้าย Sensitive Data, หรือค้นหาด้วยค่า MD5 / SHA-256 Hash
  - 🔬 **Raw Hex Viewer**: คลิกปุ่ม `🔬 Raw Hex View` เพื่อเปิดหน้าต่าง Hex Dump + ASCII View ตรวจดูไบต์ข้อมูลจริงของไฟล์นั้นได้ทันที
  - 🎬 **Built-in Media Players**: สตรีมดูวิดีโอ MP4 / MOV และฟังไฟล์เสียง MP3 / FLAC / WAV พร้อมแสดงรายละเอียด ID3 Tag โดยไม่ต้องโหลดโปรแกรมภายนอก

---

### แนวทางที่ 11: รายงานนิติวิทยาศาสตร์ ISO/IEC 27037 & Dual Hashing (MD5 + SHA-256)

เพื่อรองรับการใช้งานในงานคดีและนิติวิทยาศาสตร์ดิจิทัล ทุกครั้งที่กู้ข้อมูลเสร็จสิ้น โปรแกรมจะสร้างเอกสารสรุปผล 3 ไฟล์:

1. **`chain_of_custody.json`**: บันทึกพยานหลักฐานตามมาตรฐาน **ISO/IEC 27037**:
   ```json
   {
     "standard": "ISO/IEC 27037 Digital Evidence Compliance",
     "case_metadata": {
       "evidence_source": "/dev/rdisk4",
       "acquisition_mode": "Physical / Logical Bitstream Recovery (rb mode)",
       "hash_algorithms": ["MD5", "SHA-256"],
       "timestamp_utc7": "2026-09-21 18:30:00 UTC+7",
       "smart_health_status": "Verified (100%)",
       "total_bytes_scanned": 64000000000,
       "bad_sectors_encountered": 0,
       "total_files_extracted": 1250
     },
     "extracted_files_manifest": [ ... ]
   }
   ```
2. **`recovery_report.csv`**: ตาราง Audit Log สรุป ลำดับ, หมวดหมู่, ชนิดไฟล์, ชื่อเดิม, Offset Hex, ขนาด, วันที่, ข้อมูล Sensitive, ค่า MD5 และค่า **SHA-256 Checksum**
3. **`gallery.html`**: เว็บแกลเลอรีแบบ Standalone ที่สามารถส่งต่อให้ผู้อื่นเปิดดูได้ทันที

---

### แนวทางที่ 12: การส่งไฟล์ขึ้น Remote Server / NAS อัตโนมัติ (`--sftp-upload`)

สำหรับทีมไอทีหรือศูนย์กู้ข้อมูลที่ต้องการส่งข้อมูลที่กู้ได้ตรงไปยัง Backup Server หรือ NAS ทันที:

```bash
sudo python3 recover.py /dev/rdisk4 --all -o ./recovered_data --sftp-upload admin@192.168.1.50:/volume1/forensic_cases/case_001
```

* ระบบจะทำการถ่ายโอนชุดข้อมูลทั้งหมด พร้อมรายงานและ Checksum ไปยังเซิร์ฟเวอร์ปลายทางผ่าน SFTP/rsync อย่างปลอดภัย

---

### แนวทางที่ 13: การกู้ข้อมูลกล้องวงจรปิด Xiongmai H.264 เฉพาะทาง (`cctv_recover.py`)

สำหรับการกู้คืนฮาร์ดดิสก์กล้องวงจรปิด DVR/NVR ที่ใช้ชิป Xiongmai H.264 (ซึ่งมักถูกบันทึกแบบ Raw Stream ไม่มีระบบไฟล์มาตรฐาน):

```bash
# กู้เฉพาะคลิปของวันที่ 6 และ 7 กันยายน 2026 พร้อมแปลงเป็น MP4
sudo python3 cctv_recover.py /dev/rdisk4 --dates 2026-09-06,2026-09-07 -o ./recovered_cctv
```

* **ฟีเจอร์เด่นของ `cctv_recover.py`**:
  - ค้นหา Magic Signature `\x78\x56\x34\x12H264`
  - สกัด Timestamp จริงจาก Frame Header (ปี-เดือน-วัน ชั่วโมง:นาที:วินาที)
  - จัดโครงสร้างโฟลเดอร์ตามวันที่ `Videos/CCTV_Clips/2026-09-06/`
  - แปลง Raw H.264 Stream ให้เป็นไฟล์ `.mp4` พร้อมเปิดดูได้ทันที

---

### แนวทางที่ 14: การนำไปใช้งานบนเครื่องที่ไม่มี Python (Standalone Portable Executable)

สามารถคอมไพล์ระบบทั้งหมดให้กลายเป็นไฟล์ Executable เดี่ยวเพื่อนำไปใส่ Flash Drive ใช้งานนอกสถานที่:

```bash
# 1. รันสคริปต์คอมไพล์
chmod +x build_standalone.sh
./build_standalone.sh
```

* **ผลลัพธ์**: จะได้ไฟล์ไบนารีเดี่ยวที่โฟลเดอร์ `dist/recover`
* **การนำไปใช้งานบนเครื่องปลายทาง**:
  ```bash
  # รันได้ทันทีโดยไม่ต้องติดตั้ง Python หรือไลบรารีใด ๆ เพิ่มเติม!
  sudo ./recover
  ```

---

## 🌐 ระบบ 2 ภาษา (Bilingual UI: English Default / Thai)

โปรแกรมรองรับการแสดงผลทั้งภาษาไทยและภาษาอังกฤษอย่างสมบูรณ์:

* **วิธีสลับภาษาในเมนู Interactive**: กดปุ่ม `[L]` ในหน้าเมนูเลือกไดรฟ์
* **วิธีระบุภาษาผ่าน CLI Flag**:
  ```bash
  sudo python3 recover.py --lang th   # แสดงผลภาษาไทย
  sudo python3 recover.py --lang en   # แสดงผลภาษาอังกฤษ (Default)
  ```

---

## 🛡️ ระบบทนทานต่อ Bad Sector & โหมดทำสำเนาดิสก์ (Forensic Disk Imaging)

### 1. การทำงานเมื่อพบ Bad Sector:
* เมื่อหัวอ่านพบเซกเตอร์ที่เสียหายระหว่างอ่าน Chunk 64MB ตัว Engine จะสลับไปใช้ **4KB Sector Fallback Reader** โดยอัตโนมัติ
* ทำการ Pad เซกเตอร์ที่เสียด้วยไบต์ `\x00` เพื่อรักษาโครงสร้าง Offset ของไฟล์ที่เหลือไม่ให้คลาดเคลื่อน
* บันทึกพิกัดตำแหน่งไบต์ที่เสียหายลงไฟล์ `bad_sectors_map.log`

### 2. โหมดทำสำเนาดิสก์แบบ Bit-by-Bit (Disk Clone):
```bash
# โคลนไดรฟ์เป้าหมายเป็นไฟล์ .img พร้อมคำนวณ SHA-256
sudo python3 recover.py /dev/rdisk4 --clone ./disk_dump.img
```

---

## 🗂️ โครงสร้างโฟลเดอร์ผลลัพธ์ (Output Directory Structure)

เมื่อกระบวนการกู้ข้อมูลเสร็จสมบูรณ์ โฟลเดอร์ปลายทางจะถูกจัดระเบียบตามหมวดหมู่ดังนี้:

```text
recovered_data/
├── Images/
│   ├── JPG/
│   │   ├── 2026-09-15/                    # แยกตามวันที่ถ่ายจริงจาก EXIF
│   │   └── 2026-09-16/
│   ├── PNG/
│   └── HEIC/
├── Raw_Photos/                            # รูปถ่ายกล้องโปร
│   ├── CR2/                               # Canon RAW
│   ├── NEF/                               # Nikon RAW
│   ├── ARW/                               # Sony RAW
│   └── DNG/                               # Adobe Digital Negative
├── Videos/
│   ├── MP4/
│   ├── MOV/
│   └── CCTV_Clips/                        # วิดีโอกล้องวงจรปิด
│       └── 2026-09-06/
│           ├── 2026-09-06_14-30-00_0001.264
│           └── 2026-09-06_14-30-00_0001.mp4  # Companion MP4
├── Audio/                                 # แยกตามโครงสร้าง Artist / Album
│   └── Bodyslam/
│       └── Drive/
│           └── 0001_ความเชื่อ.mp3
├── Documents/
│   ├── PDF/
│   ├── DOCX/
│   └── XLSX/
├── Graphics/                              # ไฟล์กราฟิกและออกแบบ
│   ├── PSD/
│   ├── AI/
│   └── SVG/
├── Archives/
│   ├── ZIP/
│   └── 7Z/
├── Virtual_Disks/                         # ดิสก์เสมือน
│   ├── VMDK/
│   └── ISO/
├── Emails/                                # อีเมล
│   ├── EML/
│   └── PST/
├── Code/                                  # ซอร์สโค้ดและสคริปต์
│   ├── PY/
│   └── SQL/
├── Database/
│   └── SQLITE/
├── recovery_report.csv                    # รายงาน Audit Log พร้อมค่า MD5 + SHA-256
├── chain_of_custody.json                  # รายงานพยานหลักฐานมาตรฐาน ISO/IEC 27037
├── gallery.html                           # หน้าเว็บแกลเลอรี พร้อม Sector Heatmap & Hex Viewer
└── bad_sectors_map.log                    # บันทึกพิกัดเซกเตอร์ที่เสียหาย (ถ้ามี)
```

---

## 💡 ข้อควรระวัง & มาตรฐาน Forensic (Forensic Best Practices)

1. ⚠️ **ห้ามบันทึกไฟล์กู้ได้ลงในไดรฟ์ต้นทางเด็ดขาด (Never Write to Source Drive)**:
   - การบันทึกไฟล์ทับลงในไดรฟ์เดิมจะเขียนทับเซกเตอร์ของไฟล์อื่นที่ยังไม่ได้กู้ ทำให้สูญหายถาวร ให้บันทึกไฟล์ลง External Drive หรือไดรฟ์อื่นเสมอ
2. 🔌 **การใช้ Hardware Write-Blocker**:
   - สำหรับงานพยานหลักฐานศาล แนะนำให้เชื่อมต่อผ่าน Write-Blocker หรือตรวจสอบสถานะผ่านโปรแกรม
3. 💾 **ควรทำ Disk Clone ก่อนเสมอเมื่อพบว่าฮาร์ดดิสก์มีเสียงดังหรือช้าผิดปกติ**:
   - หาก S.M.A.R.T. เตือนระดับ `CRITICAL` ให้ใช้คำสั่ง `--clone` เพื่อดูดข้อมูลออกมาก่อน 1 รอบเสมอ

---

## 🧪 ชุดการทดสอบ (Test Suites Coverage)

สามารถทดสอบความถูกต้องของระบบทั้งหมดได้ด้วยคำสั่ง:

```bash
python3 test_engine.py
```

* ครอบคลุมการทดสอบครบทั้ง **19 Test Suites (100% Passed)**:
  1. `format_eta` & Write-Block Verification
  2. `parse_size_str` Size Parser
  3. `Deduplication` & Dual Hashing (MD5 + SHA-256)
  4. Structural Integrity Validators (PNG, SQLite, MP3, WAV, FLAC)
  5. Audio Carving & ID3 Metadata Parser
  6. Video Auto-Repair & `moov` Atom Rebuilder
  7. S.M.A.R.T. Health Evaluator
  8. File System Metadata Map & Linux EXT4 Parser
  9. Encryption & BitLocker/LUKS Detector
  10. Sensitive Data (Thai ID Checksum, Credit Card Luhn, Keywords) Inspector
  11. Partition Table (MBR) & VBR Scanner
  12. Thermal Guard & Auto-Throttle
  13. Remote Exporter Destination Validator
  14. Professional RAW Photo Carving & Camera Model Parser (Canon/Nikon/Sony/DNG)
  15. Graphics & Vector Design Carvers (PSD, SVG)
  16. Virtual Disk Carvers (VMDK, VHDX, ISO)
  17. Email & Communication Carvers (EML, PST)
  18. Source Code Carvers (HTML, PY, SQL)
  19. Forensic Reporting (CSV, HTML Heatmap Gallery, ISO/IEC 27037 JSON Manifest)

---

## ❓ คำถามที่พบบ่อย (FAQ)

* **Q: ทำไมต้องรันด้วยคำสั่ง `sudo`?**
  * **A:** การอ่านข้อมูลระดับ Raw Disk Blocks (`/dev/rdisk*` บน macOS หรือ `/dev/sd*` บน Linux) จำเป็นต้องได้รับสิทธิ์ระดับ Root หรือ Administrator ของระบบปฏิบัติการ
* **Q: ไดรฟ์ที่ฟอร์แมตแบบ Quick Format สามารถกู้คืนได้ไหม?**
  * **A:** ได้ 100% เพราะ Quick Format ลบเพียงตารางดัชนี แต่เนื้อหาของไฟล์ในเซกเตอร์ยังคงอยู่ครบถ้วน ตัว Carving Engine จะสแกนหาเนื้อหาและกู้คืนกลับมาได้ทั้งหมด
* **Q: การกู้ไฟล์บน SSD แตกต่างจาก HDD อย่างไร?**
  * **A:** หาก SSD ทำงานร่วมกับระบบ TRIM และมีการลบไฟล์แบบปกติ ข้อมูลอาจถูกล้างจากเซลล์ Flash NAND แต่หากเป็นการกู้จากไดรฟ์ USB/SD Card หรือ SSD ที่ไม่ได้เปิด TRIM ระบบจะสามารถกู้คืนได้ตามปกติ
