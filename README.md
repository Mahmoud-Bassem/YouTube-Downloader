# YouTube Downloader

Download YouTube videos and audio via GUI or CLI.

## Install

```bash
pip install .
```

**Recommended:** Install ffmpeg for format conversion
```bash
sudo apt install ffmpeg  # Ubuntu/Debian
brew install ffmpeg      # macOS
```

## GUI (Easiest)

```bash
python -m yt_download.gui
```

1. Paste YouTube URL
2. Choose: Video Only / Audio Only / Both
3. Select quality (360p-2160p) and format
4. Click Download

**Change default save path:** Edit `src/yt_download/gui.py` line 66:
```python
self.dest_var = tk.StringVar(value="/your/path/here")
```

## CLI

```bash
# Default (1080p video-only)
yt-download "URL"

# Specific quality
yt-download "URL" 720

# Audio only
yt-download "URL" --audio-only

# Custom output
yt-download "URL" --output "/path/%(title)s.%(ext)s"

# All options
yt-download --help
```

## Features

- Video: mp4, mkv, webm, avi | 360p-2160p
- Audio: m4a, mp3, wav, aac
- Progress bar with speed/ETA
- Single video download (playlists: only specific video from URL)

## Tests

```bash
pytest tests/ -v
```

## Troubleshooting

**No tkinter:** `sudo apt install python3-tk`  
**No ffmpeg:** Install ffmpeg (see above)  
**URL error:** Must start with http:// or https://

Requires Python 3.10+
