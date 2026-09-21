"""
Forensic Audit Report Generator (CSV, JSON Chain of Custody) & Interactive Visual Web Gallery (HTML)
Supports Media Preview (Images, RAW Photos, MP4/MOV, CCTV H.264, Audio Streams),
ID3/EXIF Metadata, S.M.A.R.T. Health Status, Sensitive Data & Keywords Inspector,
Disk Sector Heatmap Visualizer, and Built-in Interactive Raw Hex Viewer.
"""

import os
import csv
import json
import html
import datetime
from typing import List, Dict, Optional
from recovery_engine.i18n import CURRENT_LANG

def generate_csv_report(recovered_records: List[Dict], output_dir: str) -> str:
    """
    Generate forensic audit CSV report with dual hashes (MD5 & SHA-256).
    """
    csv_path = os.path.join(output_dir, "recovery_report.csv")
    fieldnames = [
        "Index",
        "Category",
        "FileType",
        "OriginalFilename",
        "RelativePath",
        "SizeBytes",
        "SizeMB",
        "DiskOffsetHex",
        "Timestamp",
        "IntegrityStatus",
        "SensitiveData",
        "MatchedKeywords",
        "MD5Checksum",
        "SHA256Checksum",
    ]

    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for rec in recovered_records:
            doc_meta = rec.get("doc_meta", {})
            sens_badge = doc_meta.get("summary_badge", "")
            kw_str = ", ".join(doc_meta.get("keywords_matched", []))

            writer.writerow({
                "Index": rec.get("index", ""),
                "Category": rec.get("category", ""),
                "FileType": rec.get("file_type", "").upper(),
                "OriginalFilename": rec.get("original_name", ""),
                "RelativePath": rec.get("rel_path", ""),
                "SizeBytes": rec.get("size_bytes", 0),
                "SizeMB": f"{rec.get('size_bytes', 0) / (1024 * 1024):.2f}",
                "DiskOffsetHex": f"0x{rec.get('offset', 0):010X}",
                "Timestamp": rec.get("timestamp", ""),
                "IntegrityStatus": rec.get("integrity_status", ""),
                "SensitiveData": sens_badge,
                "MatchedKeywords": kw_str,
                "MD5Checksum": rec.get("md5", ""),
                "SHA256Checksum": rec.get("sha256", ""),
            })
    return csv_path

def generate_chain_of_custody_manifest(
    recovered_records: List[Dict],
    output_dir: str,
    source_device: str,
    total_scanned_bytes: int = 0,
    bad_sectors_count: int = 0,
    smart_status: Optional[str] = None
) -> str:
    """
    Generate ISO/IEC 27037 compliant Forensic Chain of Custody JSON manifest.
    """
    manifest_path = os.path.join(output_dir, "chain_of_custody.json")
    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC+7")

    total_size = sum(rec.get("size_bytes", 0) for rec in recovered_records)
    categories_count = {}
    for r in recovered_records:
        cat = r.get("category", "other")
        categories_count[cat] = categories_count.get(cat, 0) + 1

    manifest = {
        "standard": "ISO/IEC 27037 Digital Evidence Compliance",
        "case_metadata": {
            "evidence_source": source_device,
            "acquisition_mode": "Physical / Logical Bitstream Recovery (rb mode)",
            "hash_algorithms": ["MD5", "SHA-256"],
            "timestamp_utc7": now_str,
            "smart_health_status": smart_status or "Not Available",
            "total_bytes_scanned": total_scanned_bytes,
            "bad_sectors_encountered": bad_sectors_count,
            "total_files_extracted": len(recovered_records),
            "total_extracted_bytes": total_size,
            "category_breakdown": categories_count,
        },
        "extracted_files_manifest": [
            {
                "index": r.get("index"),
                "filename": os.path.basename(r.get("rel_path", "")),
                "original_name": r.get("original_name", ""),
                "relative_path": r.get("rel_path", ""),
                "category": r.get("category", ""),
                "file_type": r.get("file_type", "").upper(),
                "size_bytes": r.get("size_bytes", 0),
                "offset_hex": f"0x{r.get('offset', 0):010X}",
                "timestamp": r.get("timestamp", ""),
                "integrity_status": r.get("integrity_status", "Valid"),
                "sensitive_data": r.get("doc_meta", {}).get("summary_badge", ""),
                "md5": r.get("md5", ""),
                "sha256": r.get("sha256", "")
            }
            for r in recovered_records
        ]
    }

    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)

    return manifest_path

def generate_gallery_html(
    recovered_records: List[Dict],
    output_dir: str,
    title: str = "Forensic Data Recovery Gallery",
    smart_status: Optional[str] = None,
    total_disk_size: int = 0
) -> str:
    """
    Generate an interactive standalone HTML gallery with embedded media players,
    live search filter, category tabs, disk sector heatmap visualizer,
    ID3 audio inspector, sensitive data indicators, and interactive Hex Dump inspector.
    """
    html_path = os.path.join(output_dir, "gallery.html")

    # Group counts
    categories = {}
    for rec in recovered_records:
        cat = rec.get("category", "Other")
        categories[cat] = categories.get(cat, 0) + 1

    cards_html = []
    for rec in recovered_records:
        cat = rec.get("category", "Other")
        ft = rec.get("file_type", "").lower()
        rel_path = rec.get("rel_path", "")
        size_mb = rec.get("size_bytes", 0) / (1024 * 1024)
        offset_hex = f"0x{rec.get('offset', 0):010X}"
        ts = rec.get("timestamp", "-")
        md5_val = rec.get("md5", "-")
        sha256_val = rec.get("sha256", "-")
        status = rec.get("integrity_status", "Valid")
        fname = os.path.basename(rel_path)
        orig_name = rec.get("original_name", "")
        audio_meta = rec.get("audio_meta", {})
        doc_meta = rec.get("doc_meta", {})
        raw_meta = rec.get("meta", {})

        preview_html = ""
        if ft in ("jpg", "jpeg", "png", "gif", "webp", "bmp"):
            preview_html = f'<img src="{html.escape(rel_path)}" alt="{html.escape(fname)}" loading="lazy" class="card-thumb" onclick="openLightbox(\'{html.escape(rel_path)}\', \'{html.escape(fname)}\')"/>'
        elif ft in ("cr2", "cr3", "nef", "arw", "dng", "tiff"):
            cam_str = f"{raw_meta.get('make', '')} {raw_meta.get('model', '')}".strip() or "RAW Photo"
            preview_html = f'<div class="card-icon">📷<br><span style="font-size:11px;color:#58a6ff;font-weight:bold;">{html.escape(cam_str)}</span></div>'
        elif ft in ("psd", "ai", "eps", "svg"):
            preview_html = f'<div class="card-icon">🎨<br><span style="font-size:12px;color:#888;">{ft.upper()} Design</span></div>'
        elif ft in ("mp4", "mov"):
            preview_html = f'''
            <video controls preload="metadata" class="card-video">
                <source src="{html.escape(rel_path)}" type="video/mp4">
                Your browser does not support video playback.
            </video>'''
        elif ft == "cctv":
            mp4_cand = rel_path.replace(".264", ".mp4")
            if os.path.exists(os.path.join(output_dir, mp4_cand)):
                preview_html = f'''
                <video controls preload="metadata" class="card-video">
                    <source src="{html.escape(mp4_cand)}" type="video/mp4">
                    Your browser does not support video playback.
                </video>'''
            else:
                preview_html = f'<div class="card-icon">📹<br><span style="font-size:12px;color:#888;">Raw H.264 Stream</span></div>'
        elif ft in ("mp3", "wav", "flac", "ogg", "m4a", "aac"):
            preview_html = f'''
            <div class="card-icon" style="padding:10px 0;">🎵</div>
            <audio controls style="width:90%;margin-bottom:8px;">
                <source src="{html.escape(rel_path)}">
            </audio>'''
        elif ft == "pdf":
            preview_html = f'<div class="card-icon">📄<br><span style="font-size:12px;color:#888;">PDF Document</span></div>'
        elif ft in ("docx", "xlsx", "pptx", "txt"):
            preview_html = f'<div class="card-icon">📑<br><span style="font-size:12px;color:#888;">Document ({ft.upper()})</span></div>'
        elif ft in ("zip", "7z", "rar", "tar", "gz"):
            preview_html = f'<div class="card-icon">📦<br><span style="font-size:12px;color:#888;">Archive</span></div>'
        elif ft in ("sqlite", "db"):
            preview_html = f'<div class="card-icon">🗄️<br><span style="font-size:12px;color:#888;">SQLite DB</span></div>'
        elif ft in ("vmdk", "vhd", "vhdx", "iso"):
            preview_html = f'<div class="card-icon">💽<br><span style="font-size:12px;color:#888;">Virtual Disk ({ft.upper()})</span></div>'
        elif ft in ("eml", "msg", "pst"):
            preview_html = f'<div class="card-icon">✉️<br><span style="font-size:12px;color:#888;">Email / Mailbox</span></div>'
        elif ft in ("py", "js", "html", "json", "csv", "sql"):
            preview_html = f'<div class="card-icon">💻<br><span style="font-size:12px;color:#888;">Code ({ft.upper()})</span></div>'
        else:
            preview_html = f'<div class="card-icon">💾<br><span style="font-size:12px;color:#888;">{ft.upper()}</span></div>'

        # Optional audio extra meta lines
        audio_lines = ""
        if audio_meta:
            art = audio_meta.get("artist")
            tit = audio_meta.get("title")
            if art or tit:
                audio_lines = f'<div><b>Track:</b> {html.escape(tit or "-")} | <b>Artist:</b> {html.escape(art or "-")}</div>'

        # Sensitive data badge
        sensitive_badge_html = ""
        if doc_meta.get("has_sensitive_data"):
            badge_text = doc_meta.get("summary_badge") or "Sensitive Data"
            sensitive_badge_html = f'<div style="background:#da3633;color:#fff;padding:2px 8px;border-radius:10px;font-size:11px;align-self:flex-start;font-weight:bold;">🚨 {html.escape(badge_text)}</div>'

        orig_badge = f'<div style="color:#58a6ff;font-size:12px;word-break:break-all;"><b>Original:</b> {html.escape(orig_name)}</div>' if orig_name else ''

        card = f'''
        <div class="gallery-card" data-category="{html.escape(cat)}" data-name="{html.escape(fname.lower())} {html.escape(orig_name.lower())}" data-hash="{html.escape(md5_val)} {html.escape(sha256_val)}">
            <div class="card-media">
                {preview_html}
            </div>
            <div class="card-body">
                <div class="card-title" title="{html.escape(fname)}"><a href="{html.escape(rel_path)}" target="_blank">{html.escape(fname)}</a></div>
                <div style="display:flex;gap:6px;flex-wrap:wrap;">
                    <div class="card-badge">{html.escape(cat)} • {ft.upper()}</div>
                    {sensitive_badge_html}
                </div>
                {orig_badge}
                <div class="card-meta">
                    <div><b>Size:</b> {size_mb:.2f} MB</div>
                    <div><b>Offset:</b> <code>{offset_hex}</code></div>
                    <div><b>Date:</b> {html.escape(ts)}</div>
                    {audio_lines}
                    <div><b>Status:</b> <span style="color:#4caf50;">{html.escape(status)}</span></div>
                    <div class="hash-text" title="MD5: {html.escape(md5_val)}&#10;SHA-256: {html.escape(sha256_val)}"><b>MD5:</b> {html.escape(md5_val[:16])}...</div>
                </div>
                <button class="hex-btn" onclick="openHexModal('{html.escape(rel_path)}', '{html.escape(fname)}')">🔬 Raw Hex View</button>
            </div>
        </div>
        '''
        cards_html.append(card)

    filter_buttons = ['<button class="filter-btn active" onclick="filterCategory(\'all\', this)">All (' + str(len(recovered_records)) + ')</button>']
    for cat, count in sorted(categories.items()):
        filter_buttons.append(f'<button class="filter-btn" onclick="filterCategory(\'{html.escape(cat)}\', this)">{html.escape(cat)} ({count})</button>')

    smart_badge = f'<span style="background:#238636;color:#fff;padding:3px 8px;border-radius:12px;font-size:12px;margin-left:8px;">SMART: {html.escape(smart_status)}</span>' if smart_status else ''

    # Generate Sector Heatmap blocks (100 block segments)
    heatmap_blocks_html = []
    max_offset = max([r.get("offset", 0) for r in recovered_records] or [1])
    target_max = total_disk_size if total_disk_size > 0 else max(max_offset, 1024*1024)

    block_density = [0] * 100
    for r in recovered_records:
        off = r.get("offset", 0)
        bucket = min(99, max(0, int((off / target_max) * 100)))
        block_density[bucket] += 1

    for b_idx, count in enumerate(block_density):
        if count == 0:
            color = "#21262d"
            title_tip = f"Sector Range {b_idx}% - Empty / Scanned"
        elif count < 5:
            color = "#1f6feb"
            title_tip = f"Sector Range {b_idx}% - {count} files recovered"
        elif count < 15:
            color = "#238636"
            title_tip = f"Sector Range {b_idx}% - {count} files recovered (Medium Density)"
        else:
            color = "#e3b341"
            title_tip = f"Sector Range {b_idx}% - {count} files recovered (High Cluster)"

        heatmap_blocks_html.append(f'<div class="heatmap-cell" style="background:{color};" title="{title_tip}"></div>')

    full_html = f'''<!DOCTYPE html>
<html lang="{CURRENT_LANG}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{html.escape(title)}</title>
    <style>
        :root {{
            --bg-color: #0d1117;
            --surface-color: #161b22;
            --card-bg: #21262d;
            --border-color: #30363d;
            --text-primary: #c9d1d9;
            --text-secondary: #8b949e;
            --accent: #58a6ff;
            --accent-hover: #1f6feb;
        }}
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{
            background-color: var(--bg-color);
            color: var(--text-primary);
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            padding: 24px;
        }}
        header {{
            text-align: center;
            margin-bottom: 24px;
            padding-bottom: 20px;
            border-bottom: 1px solid var(--border-color);
        }}
        h1 {{ font-size: 26px; color: #58a6ff; margin-bottom: 8px; }}
        .header-stats {{
            font-size: 14px;
            color: var(--text-secondary);
        }}
        .heatmap-container {{
            background: var(--surface-color);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            padding: 16px;
            margin-bottom: 24px;
        }}
        .heatmap-title {{
            font-size: 14px;
            font-weight: bold;
            color: var(--text-primary);
            margin-bottom: 10px;
            display: flex;
            justify-content: space-between;
        }}
        .heatmap-grid {{
            display: grid;
            grid-template-columns: repeat(50, 1fr);
            gap: 3px;
        }}
        .heatmap-cell {{
            height: 12px;
            border-radius: 2px;
            cursor: pointer;
            transition: transform 0.1s;
        }}
        .heatmap-cell:hover {{
            transform: scale(1.4);
            z-index: 10;
        }}
        .controls {{
            display: flex;
            flex-wrap: wrap;
            gap: 12px;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 24px;
            background: var(--surface-color);
            padding: 16px;
            border-radius: 8px;
            border: 1px solid var(--border-color);
        }}
        .search-box {{
            flex: 1;
            min-width: 250px;
            padding: 10px 14px;
            background: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 6px;
            color: var(--text-primary);
            font-size: 14px;
        }}
        .search-box:focus {{
            outline: none;
            border-color: var(--accent);
        }}
        .filter-group {{
            display: flex;
            flex-wrap: wrap;
            gap: 6px;
        }}
        .filter-btn {{
            background: var(--card-bg);
            border: 1px solid var(--border-color);
            color: var(--text-secondary);
            padding: 6px 12px;
            border-radius: 6px;
            cursor: pointer;
            font-size: 13px;
            transition: 0.2s;
        }}
        .filter-btn:hover, .filter-btn.active {{
            background: var(--accent);
            color: #fff;
            border-color: var(--accent);
        }}
        .gallery-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
            gap: 20px;
        }}
        .gallery-card {{
            background: var(--surface-color);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            overflow: hidden;
            display: flex;
            flex-direction: column;
            transition: transform 0.2s, box-shadow 0.2s;
        }}
        .gallery-card:hover {{
            transform: translateY(-4px);
            box-shadow: 0 8px 24px rgba(0,0,0,0.5);
            border-color: #58a6ff;
        }}
        .card-media {{
            height: 180px;
            background: #0d1117;
            display: flex;
            align-items: center;
            justify-content: center;
            overflow: hidden;
        }}
        .card-thumb {{
            width: 100%;
            height: 100%;
            object-fit: cover;
            cursor: pointer;
        }}
        .card-video {{
            width: 100%;
            height: 100%;
            background: #000;
        }}
        .card-icon {{
            font-size: 44px;
            text-align: center;
        }}
        .card-body {{
            padding: 14px;
            display: flex;
            flex-direction: column;
            gap: 8px;
            flex: 1;
        }}
        .card-title {{
            font-size: 14px;
            font-weight: 600;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }}
        .card-title a {{
            color: var(--accent);
            text-decoration: none;
        }}
        .card-title a:hover {{ text-decoration: underline; }}
        .card-badge {{
            display: inline-block;
            background: #238636;
            color: #fff;
            font-size: 11px;
            font-weight: 600;
            padding: 2px 8px;
            border-radius: 12px;
            align-self: flex-start;
        }}
        .card-meta {{
            font-size: 12px;
            color: var(--text-secondary);
            display: flex;
            flex-direction: column;
            gap: 4px;
        }}
        .hash-text {{
            font-family: monospace;
            font-size: 11px;
        }}
        .hex-btn {{
            margin-top: 8px;
            background: #21262d;
            border: 1px solid #30363d;
            color: #58a6ff;
            padding: 6px;
            border-radius: 5px;
            cursor: pointer;
            font-size: 11px;
            transition: 0.2s;
        }}
        .hex-btn:hover {{
            background: #30363d;
            color: #79c0ff;
        }}
        /* Modals */
        #lightbox, #hexModal {{
            display: none;
            position: fixed;
            z-index: 1000;
            left: 0; top: 0; width: 100%; height: 100%;
            background: rgba(0,0,0,0.9);
            align-items: center;
            justify-content: center;
            flex-direction: column;
        }}
        #hexModalBox {{
            width: 80%;
            max-width: 900px;
            background: #161b22;
            border: 1px solid #30363d;
            border-radius: 8px;
            padding: 20px;
            color: #c9d1d9;
            font-family: monospace;
            display: flex;
            flex-direction: column;
            max-height: 85vh;
        }}
        #hexModalContent {{
            background: #0d1117;
            padding: 14px;
            border-radius: 6px;
            overflow-y: auto;
            white-space: pre;
            font-size: 12px;
            line-height: 1.5;
            flex: 1;
            margin-top: 10px;
        }}
        .modal-close {{
            align-self: flex-end;
            color: #8b949e;
            font-size: 24px;
            cursor: pointer;
        }}
        .modal-close:hover {{ color: #fff; }}
    </style>
</head>
<body>
    <header>
        <h1>🚀 {html.escape(title)}</h1>
        <div class="header-stats">
            Total Recovered Files: <b>{len(recovered_records)}</b> | 
            Audit Reports: <a href="recovery_report.csv" style="color:var(--accent);">recovery_report.csv</a> &bull; 
            <a href="chain_of_custody.json" style="color:var(--accent);">chain_of_custody.json (ISO/IEC 27037)</a>
            {smart_badge}
        </div>
    </header>

    <div class="heatmap-container">
        <div class="heatmap-title">
            <span>🗺️ Physical Disk Sector Heatmap (0% &rarr; 100%)</span>
            <span style="font-size:12px;color:var(--text-secondary);">Dark: Empty/Scanned | Blue/Green: File Clusters | Yellow: High Density</span>
        </div>
        <div class="heatmap-grid">
            {''.join(heatmap_blocks_html)}
        </div>
    </div>

    <div class="controls">
        <input type="text" id="searchBox" class="search-box" placeholder="🔍 Search file name, original name, artist, sensitive data, MD5 / SHA-256 hash..." onkeyup="filterCards()">
        <div class="filter-group">
            {''.join(filter_buttons)}
        </div>
    </div>

    <div class="gallery-grid" id="galleryGrid">
        {''.join(cards_html)}
    </div>

    <div id="lightbox" onclick="closeLightbox()">
        <span style="position:absolute;top:20px;right:30px;color:#fff;font-size:36px;cursor:pointer;">&times;</span>
        <img id="lightbox-img" src="" alt="" style="max-width:90%;max-height:85%;border-radius:4px;">
        <div id="lightbox-caption" style="color:#fff;margin-top:10px;"></div>
    </div>

    <div id="hexModal">
        <div id="hexModalBox">
            <div style="display:flex;justify-content:space-between;align-items:center;">
                <h3 id="hexModalTitle" style="color:#58a6ff;font-size:16px;">🔬 Raw Hex Viewer</h3>
                <span class="modal-close" onclick="closeHexModal()">&times;</span>
            </div>
            <div id="hexModalContent">Loading binary stream...</div>
        </div>
    </div>

    <script>
        let currentCategory = 'all';

        function filterCategory(cat, btn) {{
            currentCategory = cat;
            document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            filterCards();
        }}

        function filterCards() {{
            const query = document.getElementById('searchBox').value.toLowerCase().trim();
            const cards = document.querySelectorAll('.gallery-card');

            cards.forEach(card => {{
                const cat = card.getAttribute('data-category');
                const name = card.getAttribute('data-name');
                const hash = card.getAttribute('data-hash').toLowerCase();

                const matchesCat = (currentCategory === 'all' || cat === currentCategory);
                const matchesQuery = (!query || name.includes(query) || hash.includes(query));

                if (matchesCat && matchesQuery) {{
                    card.style.display = 'flex';
                }} else {{
                    card.style.display = 'none';
                }}
            }});
        }}

        function openLightbox(src, caption) {{
            document.getElementById('lightbox-img').src = src;
            document.getElementById('lightbox-caption').innerText = caption;
            document.getElementById('lightbox').style.display = 'flex';
        }}

        function closeLightbox() {{
            document.getElementById('lightbox').style.display = 'none';
        }}

        function openHexModal(filePath, fileName) {{
            document.getElementById('hexModalTitle').innerText = '🔬 Raw Hex View: ' + fileName;
            document.getElementById('hexModalContent').innerText = 'Fetching hex stream from server...';
            document.getElementById('hexModal').style.display = 'flex';

            fetch('/api/hex?file=' + encodeURIComponent(filePath) + '&length=1024')
                .then(r => r.json())
                .then(data => {{
                    if (data && data.rows && data.rows.length > 0) {{
                        let out = 'Offset (Hex)  00 01 02 03 04 05 06 07 08 09 0A 0B 0C 0D 0E 0F  ASCII\\n';
                        out += '-----------------------------------------------------------------------\\n';
                        data.rows.forEach(r => {{
                            out += r.offset_hex + '  ' + r.hex + '  |' + r.ascii + '|\\n';
                        }});
                        document.getElementById('hexModalContent').innerText = out;
                    }} else {{
                        document.getElementById('hexModalContent').innerText = '[!] Hex API only active when dashboard is started with --serve';
                    }}
                }})
                .catch(e => {{
                    document.getElementById('hexModalContent').innerText = '[!] Launch with "python3 recover.py --serve" to inspect live Hex bytes.';
                }});
        }}

        function closeHexModal() {{
            document.getElementById('hexModal').style.display = 'none';
        }}
    </script>
</body>
</html>'''

    with open(html_path, "w", encoding="utf-8") as f:
        f.write(full_html)

    return html_path
