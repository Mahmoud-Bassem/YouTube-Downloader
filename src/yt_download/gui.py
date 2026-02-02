import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import threading
from pathlib import Path
import shutil

import yt_dlp


class DownloaderGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("yt-download")
        self.root.geometry("600x500")
        self.root.resizable(False, False)

        # URL input
        tk.Label(root, text="Video URL:").grid(row=0, column=0, sticky="w", padx=10, pady=10)
        self.url_entry = tk.Entry(root, width=50)
        self.url_entry.grid(row=0, column=1, padx=10, pady=10)

        # Download type
        tk.Label(root, text="Download:").grid(row=1, column=0, sticky="w", padx=10, pady=10)
        self.download_type = tk.StringVar(value="both")
        tk.Radiobutton(root, text="Video Only", variable=self.download_type, value="video").grid(
            row=1, column=1, sticky="w"
        )
        tk.Radiobutton(root, text="Audio Only", variable=self.download_type, value="audio").grid(
            row=1, column=1, sticky="w", padx=110
        )
        tk.Radiobutton(root, text="Both", variable=self.download_type, value="both").grid(
            row=1, column=1, sticky="w", padx=220
        )

        # Quality (for video)
        tk.Label(root, text="Video Quality:").grid(row=2, column=0, sticky="w", padx=10, pady=10)
        self.quality_var = tk.StringVar(value="1080")
        tk.OptionMenu(root, self.quality_var, "360", "480", "720", "1080", "1440", "2160").grid(
            row=2, column=1, sticky="w", padx=10
        )

        # Video format
        tk.Label(root, text="Video Format:").grid(row=3, column=0, sticky="w", padx=10, pady=10)
        self.video_format_var = tk.StringVar(value="mp4")
        tk.OptionMenu(root, self.video_format_var, "mp4", "mkv", "webm", "avi").grid(
            row=3, column=1, sticky="w", padx=10
        )

        # Audio format
        tk.Label(root, text="Audio Format:").grid(row=4, column=0, sticky="w", padx=10, pady=10)
        self.audio_format_var = tk.StringVar(value="m4a")
        tk.OptionMenu(root, self.audio_format_var, "m4a", "mp3", "wav", "aac").grid(
            row=4, column=1, sticky="w", padx=10
        )

        # Destination
        tk.Label(root, text="Save to:").grid(row=5, column=0, sticky="nw", padx=10, pady=10)
        
        dest_frame = tk.Frame(root)
        dest_frame.grid(row=5, column=1, sticky="w", padx=10, pady=10)
        
        self.dest_var = tk.StringVar(value="/media/mahmoud/New Volume1/Curriculum/Vidoes")
        self.dest_label = tk.Label(dest_frame, text=self.dest_var.get(), wraplength=350, justify="left", anchor="w")
        self.dest_label.pack(anchor="w")
        
        tk.Button(dest_frame, text="Browse", command=self.choose_destination).pack(anchor="w", pady=(5, 0))

        # Download button
        self.download_btn = tk.Button(root, text="Download", command=self.start_download, bg="green", fg="white", font=("Arial", 12, "bold"))
        self.download_btn.grid(row=6, column=0, columnspan=2, pady=15, sticky="ew", padx=10)

        # Progress bar
        self.progress = ttk.Progressbar(root, mode="determinate", maximum=100)
        self.progress.grid(row=7, column=0, columnspan=2, sticky="ew", padx=10, pady=5)

        # Status
        self.status_var = tk.StringVar(value="Ready")
        self.status_label = tk.Label(root, textvariable=self.status_var, wraplength=500, justify="left")
        self.status_label.grid(row=8, column=0, columnspan=2, padx=10, pady=10)

    def choose_destination(self) -> None:
        folder = filedialog.askdirectory(initialdir=self.dest_var.get())
        if folder:
            self.dest_var.set(folder)
            self.dest_label.config(text=folder)

    def start_download(self) -> None:
        url = self.url_entry.get().strip()
        if not url:
            messagebox.showerror("Error", "Please enter a URL")
            return
        if not (url.startswith("http://") or url.startswith("https://")):
            messagebox.showerror("Error", "Invalid URL. Must start with http:// or https://")
            return

        self.download_btn.config(state="disabled")
        self.progress["value"] = 0
        self.status_var.set("Starting download...")
        threading.Thread(target=self.download, daemon=True).start()

    def progress_hook(self, d: dict) -> None:
        """Progress callback for yt-dlp."""
        if d["status"] == "downloading":
            try:
                total = d.get("total_bytes") or d.get("total_bytes_estimate", 1)
                current = d.get("downloaded_bytes", 0)
                percent = (current / total * 100) if total > 0 else 0
                
                def update():
                    self.progress["value"] = min(percent, 99)
                    speed = d.get("_speed_str", "N/A")
                    eta = d.get("_eta_str", "N/A")
                    self.status_var.set(f"Downloading... {percent:.1f}% | Speed: {speed} | ETA: {eta}")
                
                self.root.after(0, update)
            except (ValueError, KeyError, ZeroDivisionError):
                pass
        elif d["status"] == "finished":
            def finish():
                self.progress["value"] = 100
                self.status_var.set("Processing...")
            self.root.after(0, finish)

    def download(self) -> None:
        try:
            url = self.url_entry.get().strip()
            dest = self.dest_var.get()
            dtype = self.download_type.get()
            quality = int(self.quality_var.get())
            video_fmt_ext = self.video_format_var.get()
            audio_fmt_ext = self.audio_format_var.get()

            has_ffmpeg = shutil.which("ffmpeg") is not None

            # Build video format with extension constraint
            video_fmt = (
                f"bv*[height<={quality}][ext={video_fmt_ext}][vcodec^=avc1]/"
                f"bv*[height<={quality}][ext={video_fmt_ext}]/"
                f"bv*[height<={quality}]"
            )

            # Build audio format with extension constraint
            audio_fmt = f"bestaudio[ext={audio_fmt_ext}]/bestaudio"

            # Download video if requested
            if dtype in ("video", "both"):
                self.status_var.set("Downloading video...")
                video_opts = {
                    "format": video_fmt,
                    "outtmpl": str(Path(dest) / f"%(title)s.{video_fmt_ext}"),
                    "quiet": True,
                    "no_warnings": True,
                    "progress_hooks": [self.progress_hook],
                    "noplaylist": True,
                }
                if has_ffmpeg:
                    video_opts["merge_output_format"] = video_fmt_ext

                with yt_dlp.YoutubeDL(video_opts) as ydl:
                    ydl.download([url])

            # Download audio if requested
            if dtype in ("audio", "both"):
                self.progress["value"] = 0
                self.status_var.set("Downloading audio...")
                audio_opts = {
                    "format": audio_fmt,
                    "outtmpl": str(Path(dest) / f"%(title)s_audio.{audio_fmt_ext}"),
                    "quiet": True,
                    "no_warnings": True,
                    "progress_hooks": [self.progress_hook],
                    "noplaylist": True,
                }
                if has_ffmpeg and audio_fmt_ext != "m4a":
                    audio_opts["postprocessors"] = [
                        {"key": "FFmpegExtractAudio", "preferredcodec": audio_fmt_ext, "preferredquality": "0"}
                    ]

                with yt_dlp.YoutubeDL(audio_opts) as ydl:
                    ydl.download([url])

            self.root.after(0, lambda: self.progress.config(value=100))
            msg = "Download completed!"
            if dtype == "video":
                msg = "Video download completed!"
            elif dtype == "audio":
                msg = "Audio download completed!"
            self.root.after(0, lambda: self.status_var.set(f"✓ {msg}"))
            self.root.after(0, lambda: messagebox.showinfo("Success", f"{msg}\nSaved to:\n{dest}"))
        except Exception as e:
            self.root.after(0, lambda: self.status_var.set(f"✗ Error: {str(e)}"))
            self.root.after(0, lambda: messagebox.showerror("Error", str(e)))
        finally:
            self.root.after(0, lambda: self.download_btn.config(state="normal"))


def main():
    root = tk.Tk()
    gui = DownloaderGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
