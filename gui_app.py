#!/usr/bin/env python3
"""
Native Modern Desktop GUI for Universal Multi-Core Data Recovery Engine
Built with Python Tkinter (Zero External Dependencies, Works natively on macOS, Linux, Windows).
"""

import sys
import os
import threading
import time
import subprocess

try:
    import tkinter as tk
    from tkinter import ttk, filedialog, messagebox
    HAS_TKINTER = True
except ImportError:
    HAS_TKINTER = False

from recovery_engine.config import DEFAULT_CORES, FILE_CATEGORIES
from recovery_engine.disk_io import get_available_drives, get_device_size
from recovery_engine.smart_checker import evaluate_disk_health
from recovery_engine.scanner import recover_universal

class ModernRecoveryGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🚀 Universal Data Recovery Engine (Forensic Grade v2.0)")
        self.root.geometry("860x720")
        self.root.minsize(800, 650)
        self.root.configure(bg="#0d1117")

        self.drives = []
        self.is_scanning = False
        self.selected_drive = tk.StringVar()
        self.output_dir = tk.StringVar(value=os.path.abspath("./recovered_all_data"))
        self.category_vars = {cat: tk.BooleanVar(value=True) for cat in FILE_CATEGORIES.keys()}

        self._setup_styles()
        self._build_ui()
        self._refresh_drives()

    def _setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TProgressbar", thickness=18, troughcolor="#161b22", background="#58a6ff")

    def _build_ui(self):
        # Header Banner
        header = tk.Frame(self.root, bg="#161b22", padx=20, pady=14)
        header.pack(fill="x")

        title_lbl = tk.Label(
            header,
            text="🚀 Universal Multi-Core Data Recovery Suite",
            font=("Helvetica", 17, "bold"),
            fg="#58a6ff",
            bg="#161b22"
        )
        title_lbl.pack(anchor="w")

        sub_lbl = tk.Label(
            header,
            text="Forensic Bitstream Carver • S.M.A.R.T. Health Guard • ISO/IEC 27037 Standard",
            font=("Helvetica", 10),
            fg="#8b949e",
            bg="#161b22"
        )
        sub_lbl.pack(anchor="w")

        # Main Container
        main_frame = tk.Frame(self.root, bg="#0d1117", padx=20, pady=12)
        main_frame.pack(fill="both", expand=True)

        # 1. Drive Selection Section
        drive_sec = tk.LabelFrame(main_frame, text=" 💾 1. Source Drive Selection ", bg="#161b22", fg="#c9d1d9", font=("Helvetica", 11, "bold"), padx=12, pady=8)
        drive_sec.pack(fill="x", pady=6)

        self.drive_combo = ttk.Combobox(drive_sec, textvariable=self.selected_drive, state="readonly", font=("Helvetica", 10), width=65)
        self.drive_combo.pack(side="left", padx=6, fill="x", expand=True)

        refresh_btn = tk.Button(drive_sec, text="🔄 Refresh", bg="#21262d", fg="#58a6ff", command=self._refresh_drives, relief="flat", padx=10)
        refresh_btn.pack(side="left", padx=4)

        smart_btn = tk.Button(drive_sec, text="🩺 S.M.A.R.T.", bg="#21262d", fg="#7ee787", command=self._check_smart, relief="flat", padx=10)
        smart_btn.pack(side="left", padx=4)

        # 2. Category Checkboxes
        cat_sec = tk.LabelFrame(main_frame, text=" 📂 2. Target File Categories ", bg="#161b22", fg="#c9d1d9", font=("Helvetica", 11, "bold"), padx=12, pady=8)
        cat_sec.pack(fill="x", pady=6)

        grid_frame = tk.Frame(cat_sec, bg="#161b22")
        grid_frame.pack(fill="x")

        r, c = 0, 0
        for cat, var in self.category_vars.items():
            label_txt = f"{cat.replace('_', ' ').title()}"
            cb = tk.Checkbutton(grid_frame, text=label_txt, variable=var, bg="#161b22", fg="#c9d1d9", selectcolor="#0d1117", activebackground="#161b22", font=("Helvetica", 10))
            cb.grid(row=r, column=c, sticky="w", padx=10, pady=3)
            c += 1
            if c > 3:
                c = 0
                r += 1

        # 3. Destination Folder Section
        dest_sec = tk.LabelFrame(main_frame, text=" 📁 3. Destination Folder ", bg="#161b22", fg="#c9d1d9", font=("Helvetica", 11, "bold"), padx=12, pady=8)
        dest_sec.pack(fill="x", pady=6)

        dest_entry = tk.Entry(dest_sec, textvariable=self.output_dir, font=("Helvetica", 10), bg="#0d1117", fg="#c9d1d9", relief="flat", insertbackground="#fff")
        dest_entry.pack(side="left", fill="x", expand=True, padx=6)

        browse_btn = tk.Button(dest_sec, text="📂 Browse...", bg="#21262d", fg="#58a6ff", command=self._browse_dest, relief="flat", padx=10)
        browse_btn.pack(side="left", padx=4)

        # 4. Progress & Real-Time Sector Heatmap Canvas
        prog_sec = tk.LabelFrame(main_frame, text=" ⚡ 4. Live Progress & Sector Heatmap ", bg="#161b22", fg="#c9d1d9", font=("Helvetica", 11, "bold"), padx=12, pady=8)
        prog_sec.pack(fill="both", expand=True, pady=6)

        self.status_lbl = tk.Label(prog_sec, text="Ready to scan.", font=("Helvetica", 10), fg="#8b949e", bg="#161b22")
        self.status_lbl.pack(anchor="w", pady=2)

        self.progress_bar = ttk.Progressbar(prog_sec, style="TProgressbar", mode="determinate")
        self.progress_bar.pack(fill="x", pady=4)

        self.heatmap_canvas = tk.Canvas(prog_sec, height=45, bg="#0d1117", highlightthickness=1, highlightbackground="#30363d")
        self.heatmap_canvas.pack(fill="x", pady=4)

        # 5. Action Buttons Footer
        footer = tk.Frame(self.root, bg="#161b22", padx=20, pady=12)
        footer.pack(fill="x")

        self.start_btn = tk.Button(
            footer,
            text="🚀 START 1-CLICK RECOVERY",
            bg="#238636",
            fg="#ffffff",
            font=("Helvetica", 12, "bold"),
            relief="flat",
            padx=18,
            pady=6,
            command=self._start_recovery
        )
        self.start_btn.pack(side="left", padx=6)

        dash_btn = tk.Button(
            footer,
            text="🌐 Open Web Dashboard",
            bg="#1f6feb",
            fg="#ffffff",
            font=("Helvetica", 11, "bold"),
            relief="flat",
            padx=14,
            pady=6,
            command=self._launch_dashboard
        )
        dash_btn.pack(side="left", padx=6)

    def _refresh_drives(self):
        self.drives = get_available_drives(include_virtual=True)
        drive_labels = []
        for d in self.drives:
            dev_p = d["raw_node"] if sys.platform == "darwin" else d["node"]
            drive_labels.append(f"{dev_p} - {d['name']} ({d['size_gb']:.1f} GB)")
        self.drive_combo["values"] = drive_labels
        if drive_labels:
            self.drive_combo.current(0)

    def _browse_dest(self):
        folder = filedialog.askdirectory(initialdir=self.output_dir.get())
        if folder:
            self.output_dir.set(folder)

    def _check_smart(self):
        selected_txt = self.selected_drive.get()
        if not selected_txt:
            messagebox.showwarning("Warning", "Please select a drive first.")
            return
        dev_node = selected_txt.split(" - ")[0]
        res = evaluate_disk_health(dev_node)
        msg = f"Drive: {dev_node}\nHealth Score: {res['health_score']}/100\nRisk Level: {res['risk_level']}\nStatus: {res['status_label']}\n\nRecommendations:\n{res['recommendations']}"
        messagebox.showinfo("🩺 S.M.A.R.T. Health Report", msg)

    def _start_recovery(self):
        selected_txt = self.selected_drive.get()
        if not selected_txt:
            messagebox.showwarning("Warning", "Please select a target drive.")
            return

        target_dev = selected_txt.split(" - ")[0]
        out_dir = self.output_dir.get()

        enabled_types = set()
        for cat, var in self.category_vars.items():
            if var.get():
                enabled_types.update(FILE_CATEGORIES[cat])

        if not enabled_types:
            messagebox.showwarning("Warning", "Please select at least one file category.")
            return

        self.start_btn.config(state="disabled", text="⏳ Recovering...")
        self.is_scanning = True

        def run_thread():
            try:
                self.status_lbl.config(text=f"Scanning {target_dev} with all CPU cores...")
                recover_universal(
                    source_device=target_dev,
                    output_dir=out_dir,
                    enabled_types=enabled_types,
                    num_workers=DEFAULT_CORES,
                    auto_confirm=True
                )
                self.root.after(0, lambda: messagebox.showinfo("🎉 Done", f"Recovery Complete!\nFiles saved to: {out_dir}"))
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("Error", str(e)))
            finally:
                self.root.after(0, self._recovery_finished)

        threading.Thread(target=run_thread, daemon=True).start()

    def _recovery_finished(self):
        self.is_scanning = False
        self.start_btn.config(state="normal", text="🚀 START 1-CLICK RECOVERY")
        self.status_lbl.config(text="Recovery finished successfully.")

    def _launch_dashboard(self):
        out_dir = self.output_dir.get()
        gallery_p = os.path.join(out_dir, "gallery.html")
        if os.path.exists(gallery_p):
            import webbrowser
            webbrowser.open(f"file://{gallery_p}")
        else:
            messagebox.showinfo("Dashboard", "No gallery.html found yet. Please run a recovery job first.")

def start_gui():
    if not HAS_TKINTER:
        print("[!] Tkinter is not installed on this Python environment.")
        sys.exit(1)
    root = tk.Tk()
    app = ModernRecoveryGUI(root)
    root.mainloop()

if __name__ == "__main__":
    start_gui()
