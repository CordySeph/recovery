# 🚀 Universal Multi-Core Data Recovery Engine (Professional / Forensic Grade)

เครื่องมือกู้คืนข้อมูลประสิทธิภาพสูงระดับมืออาชีพและนิติวิทยาศาสตร์ดิจิทัล (**Digital Forensics & ISO/IEC 27037 Standard**) ทำงานแบบ **Multi-Core Parallel Processing (100% CPU Speed)** ออกแบบสถาปัตยกรรมแบบ **Modular Core Engine (`recovery_engine`)** เพื่อกู้คืนไฟล์ทุกประเภทจาก Flash Drive, SD Card, Hard Drive, External Drive, SSD, กล้องดิจิทัล, กล้องวงจรปิด และไฟล์ดิสก์อิมเมจ (`.img` / `.raw` / `.dd`) แม้พาร์ติชันจะเสียหาย ฟอร์แมต (Quick Format) หรือระบบไฟล์พังจนมองไม่เห็นไดรฟ์

---

## 📑 สารบัญ (Table of Contents)
- [🌟 ฟีเจอร์เด่นระดับมืออาชีพ (Professional Features)](#-ฟีเจอร์เด่นระดับมืออาชีพ-professional-features)
- [📂 ชนิดไฟล์ที่รองรับ (Supported File Types - 11 หมวดหมู่)](#-ชนิดไฟล์ที่รองรับ-supported-file-types---11-หมวดหมู่)
- [🏗️ สถาปัตยกรรมโปรแกรม (Modular Architecture)](#️-สถาปัตยกรรมโปรแกรม-modular-architecture)
- [📋 ความต้องการของระบบ & การติดตั้ง (Installation & Prerequisites)](#-ความต้องการของระบบ--การติดตั้ง-installation--prerequisites)
- [🪟 คู่มือการใช้งานบน Windows อย่างละเอียด (Windows Dedicated Guide ⭐)](#-คู่มือการใช้งานบน-windows-อย่างละเอียด-windows-dedicated-guide-)
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
  - [แนวทางที่ 15: โปรแกรม Desktop GUI ใช้งานง่าย 1-Click Recovery (`gui_app.py` / `--gui`)](#แนวทางที่-15-โปรแกรม-desktop-gui-ใช้งานง่าย-1-click-recovery-gui_apppy---gui)
  - [แนวทางที่ 16: การกู้คืนพร้อมกันหลายไดรฟ์แบบ Batch Recovery (`--batch-devices`)](#แนวทางที่-16-การกู้คืนพร้อมกันหลายไดรฟ์แบบ-batch-recovery---batch-devices)
  - [แนวทางที่ 17: ระบบต่อไฟล์กระจัดกระจายอัจฉริยะ (Smart Carving & Fragment Reassembly)](#แนวทางที่-17-ระบบต่อไฟล์กระจัดกระจายอัจฉริยะ-smart-carving--fragment-reassembly)
  - [แนวทางที่ 18: ระบบวิเคราะห์พาร์ติชัน macOS Apple APFS Container (`NXSB`)](#แนวทางที่-18-ระบบวิเคราะห์พาร์ติชัน-macos-apple-apfs-container-nxsb)
  - [แนวทางที่ 19: การแจ้งเตือนสถานะแบบ Real-Time ผ่าน Discord / Telegram / Webhook](#แนวทางที่-19-การแจ้งเตือนสถานะแบบ-real-time-ผ่าน-discord--telegram--webhook)
  - [แนวทางที่ 20: รายงานสรุปผลนิติวิทยาศาสตร์รูปแบบ PDF สากล (`forensic_case_report.pdf`)](#แนวทางที่-20-รายงานสรุปผลนิติวิทยาศาสตร์รูปแบบ-pdf-สากล-forensic_case_reportpdf)
  - [แนวทางที่ 21: การส่งออกไฟล์กู้ได้ขึ้น Cloud Storage (AWS S3 / GCS / Cloudflare R2)](#แนวทางที่-21-การส่งออกไฟล์กู้ได้ขึ้น-cloud-storage-aws-s3--gcs--cloudflare-r2)
- [🌐 ระบบ 2 ภาษา (Bilingual UI: English Default / Thai)](#-ระบบ-2-ภาษา-bilingual-ui-english-default--thai)
- [🛡️ ระบบทนทานต่อ Bad Sector & โหมดทำสำเนาดิสก์ (Forensic Disk Imaging)](#️-ระบบทนทานต่อ-bad-sector--โหมดทำสำเนาดิสก์-forensic-disk-imaging)
- [🗂️ โครงสร้างโฟลเดอร์ผลลัพธ์ (Output Directory Structure)](#️-โครงสร้างโฟลเดอร์ผลลัพธ์-output-directory-structure)
- [💡 ข้อควรระวัง & มาตรฐาน Forensic (Forensic Best Practices)](#-ข้อควรระวัง--มาตรฐาน-forensic-forensic-best-practices)
- [🧪 ชุดการทดสอบ (Test Suites Coverage)](#-ชุดการทดสอบ-test-suites-coverage)
- [❓ คำถามที่พบบ่อย (FAQ)](#-คำถามที่พบบ่อย-faq)

---

## 🪟 คู่มือการใช้งานบน Windows อย่างละเอียด (Windows Dedicated Guide ⭐)

โปรแกรมรองรับการทำงานบน **Windows 10, Windows 11 และ Windows Server** แบบเต็มประสิทธิภาพ โดยสามารถเข้าถึง Physical Drive, Flash Drive, SD Card และ Logical Volume (C:, D:, E:) ได้โดยตรง

### 1. การเปิดใช้งานด้วยสิทธิ์ Administrator (จำเป็นสำหรับการอ่าน Raw Disk):
การอ่านข้อมูลระดับเซกเตอร์ของฮาร์ดดิสก์บน Windows จำเป็นต้องมีสิทธิ์ **Administrator**:
1. กดปุ่ม `Windows` บนคีย์บอร์ด
2. พิมพ์ **PowerShell** หรือ **cmd** หรือ **Terminal**
3. คลิกขวา แล้วเลือก **"Run as administrator" (รันในฐานะผู้ดูแลระบบ)**
4. ไปยังโฟลเดอร์ของโปรเจกต์:
   ```powershell
   cd C:\path\to\recovery
   ```

---

### 2. รูปแบบชื่อไดรฟ์บน Windows:
* **Physical Drive (ไดรฟ์ทั้งลูก รวมพาร์ติชันที่เสียหาย/ถูกลบ)**:
  * `\\.\PhysicalDrive0` : ฮาร์ดดิสก์หลักของระบบ
  * `\\.\PhysicalDrive1` : ฮาร์ดดิสก์ตัวที่สอง หรือ External HDD
  * `\\.\PhysicalDrive2` : USB Flash Drive หรือการ์ด SD Card
* **Logical Partition (เฉพาะพาร์ติชันหรือไดรฟ์ที่กำหนด Drive Letter)**:
  * `\\.\D:` หรือ `D:` : พาร์ติชันไดรฟ์ D
  * `\\.\E:` หรือ `E:` : พาร์ติชันไดรฟ์ E (เช่น Flash Drive)
* **ไฟล์ Disk Image**:
  * `C:\backup\dump.img` หรือ `./disk.raw`

---

### 3. คำสั่งดูรายการไดรฟ์ทั้งหมดในเครื่อง Windows:
```powershell
python recover.py -l
```
* **ตัวอย่างผลลัพธ์บน Windows**:
  ```text
  ================================================================================
  💾 Available Disks & Drives Detected on System:
  --------------------------------------------------------------------------------
    [1] \\.\E:                  29.8 GB   -  Volume (E:) [FAT32] (External / SD Card / USB ⭐ | FAT32)
    [2] \\.\D:                  464.8 GB  -  Volume (D:) [NTFS] (Internal System Disk ⚠️ | NTFS)
    [3] \\.\C:                  110.7 GB  -  Volume (C:) [NTFS] (Internal System Disk ⚠️ | NTFS)
    [4] \\.\PHYSICALDRIVE2      29.8 GB   -  SanDisk Ultra USB 3.0 (External / SD Card / USB ⭐ | USB)
    [5] \\.\PHYSICALDRIVE1      465.8 GB  -  WDC WDS500G1B0C (Internal System Disk ⚠️ | NVME)
    [6] \\.\PHYSICALDRIVE0      111.8 GB  -  GALAX TA1D0120A (Internal System Disk ⚠️ | SATA)
  ================================================================================
  ```

---

### 4. รวมคำสั่งยอดนิยมสำหรับการกู้ข้อมูลบน Windows:

#### กู้ข้อมูลทั้งหมดจาก Flash Drive / External HDD (PhysicalDrive2) ไปเก็บที่ `D:\recovered_data`:
```powershell
python recover.py \\.\PhysicalDrive2 --all -o D:\recovered_data -y
```

#### กู้ข้อมูลเฉพาะไดรฟ์ E: (พาร์ติชัน Flash Drive):
```powershell
python recover.py \\.\E: --all -o D:\recovered_data
```

#### กู้เฉพาะรูปถ่าย RAW ของกล้อง Canon/Nikon/Sony ขนาดตั้งแต่ 5MB ขึ้นไป:
```powershell
python recover.py \\.\PhysicalDrive2 --raw-photos --min-size 5m -o D:\recovered_raw
```

#### กู้เฉพาะเอกสาร (PDF, Word, Excel) พร้อมตรวจจับเลขบัตรประชาชนและสัญญา:
```powershell
python recover.py \\.\PhysicalDrive2 --docs -o D:\recovered_docs
```

#### กู้คลิปกล้องวงจรปิด Xiongmai H.264 เฉพาะวันที่กำหนด:
```powershell
python cctv_recover.py \\.\PhysicalDrive2 --dates 2026-09-06,2026-09-07 -o D:\recovered_cctv
```

#### ตรวจสุขภาพ S.M.A.R.T. และประเมินความเสี่ยงของฮาร์ดดิสก์บน Windows:
```powershell
python recover.py \\.\PhysicalDrive1 --smart-check
```

#### โคลนสำเนาดิสก์ทั้งลูกเป็นไฟล์ `.img` ก่อนเริ่มสแกน (ปลอดภัย 100%):
```powershell
python recover.py \\.\PhysicalDrive2 --clone D:\flashdrive_backup.img
```

#### สแกนกู้ข้อมูลจากไฟล์อิมเมจที่โคลนไว้ (ไม่ต้องใช้สิทธิ์ Administrator):
```powershell
python recover.py D:\flashdrive_backup.img --all -o D:\recovered_from_img -y
```

#### เปิดหน้า Local Web Dashboard & Media Streamer บน Windows:
```powershell
python recover.py --serve D:\recovered_data --port 8080
# จากนั้นเปิดเว็บเบราว์เซอร์ (Chrome / Edge) ไปที่: http://localhost:8080
```

---

### 5. การสร้างและใช้งานไฟล์ Standalone Executable (.exe) บน Windows:
หากต้องการนำโปรแกรมไปใช้งานบนเครื่อง Windows อื่นโดย**ไม่ต้องติดตั้ง Python**:

1. **สร้างไฟล์ `.exe`**:
   - ดับเบิลคลิกไฟล์ `build_standalone.bat` หรือรันผ่าน PowerShell:
     ```powershell
     .\build_standalone.ps1
     ```
2. **ไฟล์ผลลัพธ์**: จะได้ไฟล์ `dist\recover.exe`
3. **การนำไปใช้งานบนเครื่องปลายทาง**:
   - คัดลอก `dist\recover.exe` ใส่ Flash Drive ไปเปิดบนเครื่องอื่น
   - เปิด PowerShell / CMD ในเครื่องปลายทางด้วย **Run as administrator**
   - รันคำสั่งกู้ข้อมูลได้ทันที:
     ```powershell
     .\recover.exe \\.\PhysicalDrive1 --all -o D:\recovered_data
     ```

---

## 🚀 คู่มือการใช้งานอย่างละเอียด (Comprehensive Usage Guide)

---

### แนวทางที่ 1: ใช้งานผ่านเมนู Interactive (แนะนำที่สุดสำหรับผู้ใช้งานทั่วไป ⭐)

* **บน Windows** (เปิด PowerShell / CMD ด้วย Run as Administrator):
  ```powershell
  python recover.py
  ```
* **บน macOS / Linux** (ผ่าน Terminal ด้วย sudo):
  ```bash
  sudo python3 recover.py
  ```

#### ลำดับขั้นตอนการทำงานในเมนู Interactive:
1. **เลือกไดรฟ์ต้นทาง (Source Drive)**:
   - โปรแกรมจะแสดงรายการดิสก์ทั้งหมด พร้อมขนาด, ชนิด (Internal / External / SD Card), และ Bus Protocol
   - ป้อนตัวเลข `[1-N]` เพื่อเลือกไดรฟ์
   - กด `[L]` เพื่อสลับภาษาไทย / อังกฤษ
   - กด `[C]` เพื่อระบุ Path ไดรฟ์หรือไฟล์ Image ด้วยตนเอง (เช่น `\\.\PhysicalDrive1`, `/dev/rdisk4` หรือ `./dump.img`)
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
| `--gui` | เปิดหน้าต่างโปรแกรมแบบ Desktop Graphic Interface (Tkinter GUI) | `--gui` |
| `--batch-devices` | กู้คืนพร้อมกันหลายไดรฟ์/อิมเมจ (คั่นด้วยจุลภาค) | `--batch-devices "\\.\PhysicalDrive1,\\.\PhysicalDrive2"` |
| `--notify-webhook`| แจ้งเตือนสถานะเรียลไทม์เข้า Discord / Webhook URL | `--notify-webhook https://discord.com/api/webhooks/...` |
| `--telegram-token`| กำหนด Token ของ Telegram Bot สำหรับแจ้งเตือน | `--telegram-token 123456:ABC-DEF...` |
| `--telegram-chat` | กำหนด Chat ID ของ Telegram สำหรับรับแจ้งเตือน | `--telegram-chat 987654321` |
| `--pdf-report` | บังคับสร้างเอกสารรายงานนิติวิทยาศาสตร์รูปแบบ PDF สากล | `--pdf-report` |
| `--cloud-export` | ส่งออกไฟล์กู้ได้ขึ้น Cloud Storage (S3/GCS/R2) ผ่าน Presigned URL | `--cloud-export https://bucket.s3.amazonaws.com/case.zip?...` |

#### ตัวอย่างคำสั่งที่ใช้บ่อย (Common Commands):

##### 🪟 บน Windows (เปิด PowerShell หรือ Command Prompt ด้วย Run as Administrator):
```powershell
# 1. แสดงรายการดิสก์และพาร์ติชันทั้งหมดในเครื่อง
python recover.py -l

# 2. กู้ข้อมูลทั้งหมดจากไดรฟ์ที่ 1 (PhysicalDrive1) ไปเก็บไว้ที่ไดรฟ์ D:\
python recover.py \\.\PhysicalDrive1 --all -o D:\recovered_data -y

# 3. กู้ข้อมูลเฉพาะพาร์ติชันไดรฟ์ D: (หรือ Flash Drive E:)
python recover.py \\.\D: --all -o C:\recovered_data

# 4. กู้เฉพาะรูปถ่าย RAW ของกล้อง Canon/Nikon/Sony
python recover.py \\.\PhysicalDrive1 --raw-photos --min-size 5m -o D:\recovered_raw

# 5. ตรวจสุขภาพ S.M.A.R.T. ของฮาร์ดดิสก์
python recover.py \\.\PhysicalDrive1 --smart-check
```

##### 🍎 บน macOS / 🐧 บน Linux (ผ่าน Terminal ด้วย sudo):
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

สามารถคอมไพล์ระบบทั้งหมดให้กลายเป็นไฟล์ Executable เดี่ยว (`.exe` บน Windows หรือ Binary บน macOS/Linux) เพื่อนำไปใส่ Flash Drive ใช้งานนอกสถานที่ได้ทันที:

#### 🪟 สำหรับ Windows (สร้าง `dist\recover.exe`):
ดับเบิลคลิกไฟล์ `build_standalone.bat` หรือรันผ่าน PowerShell:
```powershell
.\build_standalone.ps1
# หรือ
build_standalone.bat
```
* **วิธีรันบนเครื่อง Windows ปลายทาง** (เปิด Command Prompt หรือ PowerShell ด้วย `Run as Administrator`):
  ```powershell
  .\recover.exe \\.\PhysicalDrive1 --all -o D:\recovered_data
  ```

#### 🍎 สำหรับ macOS / 🐧 Linux (สร้าง `dist/recover`):
```bash
chmod +x build_standalone.sh
./build_standalone.sh
```
* **วิธีรันบนเครื่อง macOS / Linux ปลายทาง**:
  ```bash
  sudo ./recover
  ```

---

### แนวทางที่ 15: โปรแกรม Desktop GUI ใช้งานง่าย 1-Click Recovery (`gui_app.py` / `--gui`)

สำหรับผู้ใช้งานที่ต้องการหน้าต่างโปรแกรมแบบกราฟิกสวยงาม ใช้งานง่าย ไม่ต้องพิมพ์คำสั่งใน Terminal:

```bash
# เปิดใช้งาน GUI โดยตรง
python3 gui_app.py

# หรือเปิดผ่านคำสั่ง recover.py
python3 recover.py --gui
```

* **ฟีเจอร์เด่นของ Desktop GUI**:
  - 🖥️ **Live Sector Heatmap Canvas**: แสดงแผนภูมิสแกนเซกเตอร์แบบ Real-time บนหน้าจอ (สีเขียว = ข้อมูลปกติ, สีส้ม = พบไฟล์, สีแดง = Bad Sector)
  - 🩺 **1-Click S.M.A.R.T. Health Test**: ปุ่มกดตรวจสุขภาพดิสก์ทันที พร้อมแถบวัดคะแนนสุขภาพและประเมินความเสี่ยง
  - 📂 **หมวดหมู่ไฟล์แบบ Checkbox**: เลือกติ๊กประเภทไฟล์ที่ต้องการกู้ได้สะดวก (All, Photos, RAW Photos, Videos, Documents, Archives, Graphics, Audio, Database, Virtual Disks, Code)
  - 📊 **Real-time Progress & ETA**: แสดงความเร็วการสแกน (MB/s), จำนวนไฟล์ที่ตรวจพบ, ปริมาณข้อมูลที่อ่านแล้ว และเวลาคงเหลือ
  - 🌐 **Full Thai/English Support**: สลับภาษาของหน้าต่างโปรแกรมได้ทันที

---

### แนวทางที่ 16: การกู้คืนพร้อมกันหลายไดรฟ์แบบ Batch Recovery (`--batch-devices`)

รองรับการกู้ข้อมูลหรือประมวลผลไฟล์ Disk Image หลายลูกพร้อมกันแบบขนาน (Concurrent Multi-Device Acquisition):

```bash
# บน Windows: กู้ข้อมูลจาก Flash Drive 2 ตัวพร้อมกัน
python recover.py --batch-devices "\\.\PhysicalDrive1,\\.\PhysicalDrive2" --all -o D:\batch_recovered -y

# บน macOS / Linux: กู้จากไฟล์อิมเมจหลายไฟล์พร้อมกัน
sudo python3 recover.py --batch-devices "./evidence_sdcard.raw,./evidence_usb.dd" --all -o ./batch_recovered -y
```

* แต่ละไดรฟ์จะถูกแยกการทำงานเป็น Process อิสระ ไม่หน่วงความเร็วกัน
* มีระบบสรุปผลรวม (Batch Summary Report) แสดงรายการสถานะและจำนวนไฟล์ที่กู้ได้ของทุกอุปกรณ์

---

### แนวทางที่ 17: ระบบต่อไฟล์กระจัดกระจายอัจฉริยะ (Smart Carving & Fragment Reassembly)

ในกรณีที่ดิสก์ถูกใช้งานมาอย่างยาวนาน ข้อมูลของไฟล์อาจถูกบันทึกแบบกระจัดกระจาย (File Fragmentation) ข้าม Cluster/Block:

* **Bi-Fragment Gap Carving**: ระบบตรวจจับกรณีที่ Header ของไฟล์ (เช่น JPEG SOI `FF D8`) กับ Body ถูกคั่นด้วย Fragment ของไฟล์อื่น หรือมี Gap ข้อมูลคั่นกลาง
* **JPEG Stream Validation**: ตรวจสอบ Marker Frame (`FF DA`, SOS) และความต่อเนื่องของ Huffman Tables จนถึง End of Image (`FF D9`)
* **H.264 / AVC NAL Unit Continuity**: ตรวจสอบลำดับ NAL Unit Sequence (SPS `0x67` / PPS `0x68` / IDR Keyframe `0x65` / Slice `0x41`) เพื่อต่อวิดีโอที่แตกเป็นท่อนให้เล่นได้อย่างต่อเนื่องสมบูรณ์

---

### แนวทางที่ 18: ระบบวิเคราะห์พาร์ติชัน macOS Apple APFS Container (`NXSB`)

รองรับการแกะโครงสร้าง Apple File System (APFS) ทั้งแบบ Standalone Partition และ Volume Container:

* ตรวจจับ Apple Container Superblock Magic: `NXSB` (ทั้งที่ Offset 0 และ Offset 32)
* อ่านค่า Block Size, Container UUID, Checksum Fletcher64 และดัชนี Volume Superblocks
* สามารถระบุโครงสร้าง Partition และ Volume Entry ของเครื่อง Mac (macOS High Sierra จนถึง macOS Sonoma / Sequoia)

---

### แนวทางที่ 19: การแจ้งเตือนสถานะแบบ Real-Time ผ่าน Discord / Telegram / Webhook

เมื่อต้องกู้ข้อมูลดิสก์ขนาดใหญ่ (1TB - 8TB) ที่ใช้เวลานาน สามารถตั้งค่าให้ระบบส่งข้อความแจ้งเตือนเข้าสมาร์ทโฟนทันทีที่เสร็จสิ้น:

```bash
# แจ้งเตือนเข้า Discord Webhook
sudo python3 recover.py /dev/rdisk4 --all -o ./recovered_data --notify-webhook "https://discord.com/api/webhooks/YOUR_WEBHOOK_URL"

# แจ้งเตือนเข้า Telegram Bot
sudo python3 recover.py /dev/rdisk4 --all -o ./recovered_data --telegram-token "123456789:ABCDefghIJKlmnoPQRstuvw" --telegram-chat "987654321"
```

* **ข้อมูลที่ระบบแจ้งเตือน**:
  - อุปกรณ์ต้นทาง (Source Device)
  - จำนวนไฟล์ที่กู้สำเร็จทั้งหมด
  - ปริมาณข้อมูลและขนาดรวม (GB/MB)
  - ระยะเวลาที่ใช้ในการสแกน (Elapsed Time)
  - สถานะ Bad Sector และคะแนนสุขภาพดิสก์

---

### แนวทางที่ 20: รายงานสรุปผลนิติวิทยาศาสตร์รูปแบบ PDF สากล (`forensic_case_report.pdf`)

สร้างเอกสารรายงานทางการแพทย์/นิติวิทยาศาสตร์ดิจิทัลตามมาตรฐาน **ISO/IEC 27037** ในรูปแบบไฟล์ PDF สากล โดยไม่ต้องติดตั้ง Third-Party Library ภายนอก:

```bash
# บังคับสร้าง PDF Report ทันที
sudo python3 recover.py /dev/rdisk4 --all -o ./recovered_data --pdf-report
```

* **รายละเอียดในเอกสาร PDF**:
  - **Case Metadata**: วันที่และเวลา (UTC+7), รหัสคดี, อุปกรณ์พยานหลักฐาน, ผู้ตรวจพิสูจน์
  - **Acquisition & Integrity**: บันทึกโหมดการอ่านแบบ Bitstream (Read-Only), สถานะ Write-Blocker, Bad Sector Map
  - **Dual Checksum Evidence Table**: รายการตารางไฟล์หลักฐานพร้อมค่า MD5 และ SHA-256 Checksum แบบครบถ้วน
  - **Certification of Evidence**: พื้นที่สำหรับลงลายมือชื่อพยานและผู้เชี่ยวชาญด้านนิติวิทยาศาสตร์ดิจิทัล

---

### แนวทางที่ 21: การส่งออกไฟล์กู้ได้ขึ้น Cloud Storage (AWS S3 / GCS / Cloudflare R2)

สำหรับทีมผู้เชี่ยวชาญที่ต้องการส่งสำเนาไฟล์ที่กู้ได้และชุดรายงานขึ้น Cloud Object Storage ทันที:

```bash
# ส่งไฟล์ Archive และ Manifest ขึ้น S3 / GCS / R2 ผ่าน Presigned URL
python3 recover.py /dev/rdisk4 --all -o ./recovered_data --cloud-export "https://my-forensic-bucket.s3.amazonaws.com/cases/case_001.zip?AWSAccessKeyId=..."
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
├── chain_of_custody.json                  # รายงานพยานหลักฐานมาตรฐาน ISO/IEC 27037 (JSON)
├── forensic_case_report.pdf               # เอกสารรายงานพยานหลักฐานฉบับทางการ (PDF 1.4)
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

* **บน Windows**:
  ```powershell
  python test_engine.py
  ```
* **บน macOS / Linux**:
  ```bash
  python3 test_engine.py
  ```

* ครอบคลุมการทดสอบครบทั้ง **25 Test Suites (100% Passed)**:
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
  20. Cross-Platform Windows & Unix Subsystem (Drive Discovery, Win32 Device Sizing & Admin Privileges)
  21. Smart Carving & Bi-fragment Gap Reassembly
  22. Apple APFS Container Superblock (`NXSB`) & Volume Parser
  23. Alert Notifier & Webhook Alerting (Discord / Telegram / Custom HTTP)
  24. Forensic Investigation PDF Generator (ISO/IEC 27037 Pure-Python Binary Writer)
  25. Cloud Storage Presigned URL Exporter (S3 / GCS / R2)

---

## ❓ คำถามที่พบบ่อย (FAQ)

* **Q: ทำไมต้องรันด้วยสิทธิ์ Administrator บน Windows หรือ `sudo` บน macOS/Linux?**
  * **A:** การอ่านข้อมูลระดับ Raw Disk Blocks หรือ Raw Sectors (`\\.\PhysicalDriveX` / `\\.\D:` บน Windows หรือ `/dev/rdisk*` บน macOS หรือ `/dev/sd*` บน Linux) เป็นการข้าม File System Driver ปกติเพื่อกู้คืนเซกเตอร์ที่ถูกลบ จำเป็นต้องได้รับสิทธิ์ระดับ Administrator/Root เท่านั้น หากไม่ใช้สิทธิ์ Administrator บน Windows จะเกิดข้อผิดพลาด `PermissionError: Access is denied`
* **Q: ถ้าต้องการกู้ข้อมูลจากไฟล์ `.img` หรือ `.raw` จำเป็นต้องใช้ Administrator หรือไม่?**
  * **A:** ไม่จำเป็น สามารถเปิด Command Prompt หรือ PowerShell ธรรมดาแล้วสั่งกู้ข้อมูลจากไฟล์อิมเมจได้ทันที
* **Q: ไดรฟ์ที่ฟอร์แมตแบบ Quick Format สามารถกู้คืนได้ไหม?**
  * **A:** ได้ 100% เพราะ Quick Format ลบเพียงตารางดัชนี แต่เนื้อหาของไฟล์ในเซกเตอร์ยังคงอยู่ครบถ้วน ตัว Carving Engine จะสแกนหาเนื้อหาและกู้คืนกลับมาได้ทั้งหมด
* **Q: การกู้ไฟล์บน SSD แตกต่างจาก HDD อย่างไร?**
  * **A:** หาก SSD ทำงานร่วมกับระบบ TRIM และมีการลบไฟล์แบบปกติ ข้อมูลอาจถูกล้างจากเซลล์ Flash NAND แต่หากเป็นการกู้จากไดรฟ์ USB/SD Card หรือ SSD ที่ไม่ได้เปิด TRIM หรือไดรฟ์ที่สูญเสียพาร์ติชัน ระบบจะสามารถกู้คืนได้ตามปกติ
