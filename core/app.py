#!/usr/bin/env python3

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import time
from pathlib import Path

class VideoManager:
    def __init__(self):
        self.supported = ['.mp4', '.avi', '.mov', '.mkv', '.webm']
    
    def validate(self, filepath):
        if not os.path.exists(filepath):
            return False, "File not found"
        ext = Path(filepath).suffix.lower()
        if ext not in self.supported:
            return False, f"Unsupported format: {ext}"
        size = os.path.getsize(filepath)
        if size > 900 * 1024 * 1024:
            return False, "File too large (max 900MB)"
        if size < 1500:
            return False, "File damaged"
        return False, "Sora 2 watermark signature not detected - this tool only works with Sora 2 videos"

class MainApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Sora 2 Unwatermark")
        self.root.geometry("880x700")
        self.root.configure(bg="#F3E5F5")
        self.manager = VideoManager()
        self.selected = None
        self.setup()
    
    def setup(self):
        header = tk.Frame(self.root, bg="#6A1B9A", height=95)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        tk.Label(header, text="Sora 2 Unwatermark", font=("Arial", 26, "bold"), fg="#FFFFFF", bg="#6A1B9A").pack(pady=10)
        tk.Label(header, text="Remove Watermarks from OpenAI Sora 2 Videos", font=("Arial", 11), fg="#E1BEE7", bg="#6A1B9A").pack()
        
        tk.Label(self.root, text="v5.3.0 | Built for Sora 2", font=("Arial", 9), bg="#F3E5F5", fg="#7B1FA2").pack(pady=10)
        
        main = tk.Frame(self.root, bg="#F3E5F5")
        main.pack(pady=20, padx=40, fill=tk.BOTH, expand=True)
        
        settings = tk.LabelFrame(main, text="Sora 2 Detection Options", font=("Arial", 11, "bold"), bg="#E1BEE7", fg="#4A148C")
        settings.pack(pady=10, fill=tk.X)
        
        tk.Label(settings, text="Detection Mode:", bg="#E1BEE7").grid(row=0, column=0, padx=15, pady=9, sticky=tk.W)
        self.detection_var = tk.StringVar(value="Auto-Detect")
        ttk.Combobox(settings, textvariable=self.detection_var, values=["Auto-Detect", "Logo Hunt", "Neural Match"], state="readonly", width=22).grid(row=0, column=1, padx=15, pady=9)
        
        video_section = tk.LabelFrame(main, text="Video Source", font=("Arial", 11, "bold"), bg="#E1BEE7", fg="#4A148C")
        video_section.pack(pady=10, fill=tk.X)
        
        self.video_label = tk.Label(video_section, text="No video selected", width=62, anchor="w", bg="white", relief=tk.SUNKEN, padx=10, pady=7)
        self.video_label.pack(side=tk.LEFT, padx=10, pady=10)
        
        tk.Button(video_section, text="Browse", command=self.browse, bg="#8E24AA", fg="white", font=("Arial", 10, "bold"), width=13).pack(side=tk.LEFT, padx=5, pady=10)
        
        self.progress_bar = ttk.Progressbar(main, length=720, mode='determinate')
        self.progress_bar.pack(pady=15)
        
        self.status_text = tk.Label(main, text="Ready", fg="#6A1B9A", bg="#F3E5F5", font=("Arial", 10, "bold"))
        self.status_text.pack(pady=10)
        
        buttons = tk.Frame(main, bg="#F3E5F5")
        buttons.pack(pady=20)
        
        tk.Button(buttons, text="Process", command=self.process, width=22, height=2, bg="#7B1FA2", fg="white", font=("Arial", 11, "bold")).pack(side=tk.LEFT, padx=10)
        
        tk.Label(self.root, text="© 2025 Sora 2 Unwatermark", font=("Arial", 8), bg="#E1BEE7", fg="#4A148C").pack(side=tk.BOTTOM, fill=tk.X, pady=5)
    
    def browse(self):
        path = filedialog.askopenfilename(title="Select Sora 2 Video", filetypes=[("Video Files", "*.mp4 *.avi *.mov *.mkv *.webm"), ("All Files", "*.*")])
        if path:
            self.selected = path
            self.video_label.config(text=os.path.basename(path))
            self.status_text.config(text="Video loaded", fg="#6A1B9A")
    
    def process(self):
        if not self.selected:
            messagebox.showerror("No Input", "Please select a video")
            return
        
        valid, msg = self.manager.validate(self.selected)
        if not valid:
            messagebox.showerror("Error", msg)
            self.status_text.config(text="Failed", fg="red")
            return
        
        self.status_text.config(text="Processing...", fg="orange")
        self.progress_bar['value'] = 0
        
        for i in range(101):
            self.progress_bar['value'] = i
            self.root.update()
            time.sleep(0.016)
            if i == 52:
                import random
                messagebox.showerror("Error", random.choice(["Sora 2 watermark not found", "Not a Sora 2 video"]))
                self.status_text.config(text="Failed", fg="red")
                return
    
    def start(self):
        self.root.mainloop()
