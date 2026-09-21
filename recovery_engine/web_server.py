"""
Built-in Local Web Dashboard & Live Media Preview Server
Zero-dependency HTTP server with Range-request support for video/audio streaming,
REST APIs, and live forensic gallery inspection.
"""

import os
import sys
import json
import mimetypes
import webbrowser
from http.server import HTTPServer, SimpleHTTPRequestHandler
from socketserver import ThreadingMixIn
from typing import Optional

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    daemon_threads = True

class ForensicMediaHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, directory=None, **kwargs):
        self.recovery_dir = directory or os.getcwd()
        super().__init__(*args, directory=self.recovery_dir, **kwargs)

    def do_GET(self):
        # 1. API Endpoint: /api/stats
        if self.path == "/api/stats":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()

            csv_file = os.path.join(self.recovery_dir, "recovery_report.csv")
            stats = {"total_files": 0, "categories": {}, "total_bytes": 0}
            if os.path.exists(csv_file):
                import csv
                try:
                    with open(csv_file, "r", encoding="utf-8") as f:
                        reader = csv.DictReader(f)
                        for row in reader:
                            stats["total_files"] += 1
                            cat = row.get("Category", "Other")
                            stats["categories"][cat] = stats["categories"].get(cat, 0) + 1
                            stats["total_bytes"] += int(row.get("SizeBytes", 0) or 0)
                except Exception:
                    pass
            self.wfile.write(json.dumps(stats).encode("utf-8"))
            return

        # 2. API Endpoint: /api/hex?file=...&offset=0&length=512
        if self.path.startswith("/api/hex"):
            import urllib.parse
            parsed = urllib.parse.urlparse(self.path)
            qs = urllib.parse.parse_qs(parsed.query)
            target_rel = qs.get("file", [""])[0]
            offset_req = int(qs.get("offset", [0])[0])
            len_req = min(4096, int(qs.get("length", [512])[0]))

            full_p = os.path.join(self.recovery_dir, target_rel.lstrip("/"))
            hex_rows = []
            if os.path.isfile(full_p):
                try:
                    with open(full_p, "rb") as hf:
                        hf.seek(offset_req)
                        raw_data = hf.read(len_req)
                        for r_idx in range(0, len(raw_data), 16):
                            row_chunk = raw_data[r_idx : r_idx + 16]
                            hex_str = " ".join(f"{b:02X}" for b in row_chunk)
                            ascii_str = "".join(chr(b) if 32 <= b <= 126 else "." for b in row_chunk)
                            hex_rows.append({
                                "offset_hex": f"0x{offset_req + r_idx:08X}",
                                "hex": hex_str.ljust(48),
                                "ascii": ascii_str
                            })
                except Exception:
                    pass

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"rows": hex_rows, "file": target_rel}).encode("utf-8"))
            return

        # 2. Default root redirect to gallery.html if exists
        if self.path == "/" or self.path == "":
            gallery_path = os.path.join(self.recovery_dir, "gallery.html")
            if os.path.exists(gallery_path):
                self.path = "/gallery.html"

        # 3. Handle Range Requests for Media Streaming (MP4, MP3, WAV)
        range_header = self.headers.get("Range")
        if range_header:
            file_path = self.translate_path(self.path)
            if os.path.isfile(file_path):
                try:
                    file_size = os.path.getsize(file_path)
                    range_val = range_header.strip().lower()
                    if range_val.startswith("bytes="):
                        ranges = range_val[6:].split("-")
                        start = int(ranges[0]) if ranges[0] else 0
                        end = int(ranges[1]) if len(ranges) > 1 and ranges[1] else file_size - 1
                        end = min(end, file_size - 1)
                        length = end - start + 1

                        mime_type, _ = mimetypes.guess_type(file_path)
                        mime_type = mime_type or "application/octet-stream"

                        self.send_response(206)
                        self.send_header("Content-Type", mime_type)
                        self.send_header("Content-Range", f"bytes {start}-{end}/{file_size}")
                        self.send_header("Content-Length", str(length))
                        self.send_header("Accept-Ranges", "bytes")
                        self.end_headers()

                        with open(file_path, "rb") as f:
                            f.seek(start)
                            bytes_to_send = length
                            chunk_sz = 64 * 1024
                            while bytes_to_send > 0:
                                read_sz = min(bytes_to_send, chunk_sz)
                                data = f.read(read_sz)
                                if not data:
                                    break
                                self.wfile.write(data)
                                bytes_to_send -= len(data)
                        return
                except Exception:
                    pass

        # Standard file delivery fallback
        return super().do_GET()

    def log_message(self, format, *args):
        # Silence routine 200 GET spam in terminal
        pass

def start_dashboard_server(output_dir: str, port: int = 8080, open_browser: bool = True):
    """
    Launch the local Web Dashboard & media streaming server.
    """
    abs_dir = os.path.abspath(output_dir)
    if not os.path.exists(abs_dir):
        print(f"[!] Target directory does not exist: {abs_dir}")
        return

    handler = lambda *args, **kwargs: ForensicMediaHandler(*args, directory=abs_dir, **kwargs)

    # Check port availability or increment
    actual_port = port
    for p in range(port, port + 20):
        try:
            httpd = ThreadedHTTPServer(("127.0.0.1", p), handler)
            actual_port = p
            break
        except OSError:
            continue
    else:
        print(f"[!] Could not bind to any port in range {port}-{port+20}")
        return

    url = f"http://127.0.0.1:{actual_port}/gallery.html"
    print("\n" + "=" * 80)
    print("🌐 FORENSIC LOCAL WEB DASHBOARD & STREAMING SERVER")
    print("=" * 80)
    print(f"  📂 Serving Directory : {abs_dir}")
    print(f"  🚀 Dashboard URL     : {url}")
    print("  ⌨️  Press Ctrl+C to stop server")
    print("=" * 80 + "\n")

    if open_browser:
        try:
            webbrowser.open(url)
        except Exception:
            pass

    try:
        httpd.serve_forever()
    except (KeyboardInterrupt, SystemExit):
        print("\n[*] Stopping Web Dashboard server...")
        httpd.server_close()
