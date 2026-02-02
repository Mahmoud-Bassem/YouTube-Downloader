# yt-download

A user-friendly YouTube downloader with both command-line (CLI) and graphical (GUI) interfaces. Download videos, audio, or both with customizable quality and format options.

## ✨ Features

- 🖥️ **GUI Application**: Easy-to-use graphical interface with real-time progress tracking
- ⚡ **CLI Tool**: Fast command-line interface for power users
- 🎬 **Video Downloads**: Choose quality from 360p to 2160p (4K)
- 🎵 **Audio Downloads**: Extract audio in m4a, mp3, wav, or aac formats
- 📦 **Flexible Output**: Download video-only, audio-only, or both separately
- 📊 **Progress Tracking**: Real-time download speed and ETA display
- 🎯 **Format Selection**: Choose from mp4, mkv, webm, or avi for videos
- 🔗 **Smart URLs**: Supports both individual videos and playlist URLs

## 🚀 Quick Start

### Installation

1. **Clone or download this repository**
2. **Install dependencies:**
   ```bash
   pip install .
   ```
3. **(Optional but recommended) Install ffmpeg:**
   ```bash
   # Ubuntu/Debian
   sudo apt install ffmpeg
   
   # macOS with Homebrew
   brew install ffmpeg
   ```

### Launch the GUI

The easiest way to get started:

```bash
python -m yt_download.gui
```

Or if installed:
```bash
yt-download-gui
```

## 📖 How to Use the GUI

### Step 1: Paste Your Video URL
- Copy any YouTube video or playlist URL
- Examples:
  - Single video: `https://www.youtube.com/watch?v=VIDEO_ID`
  - Video from playlist: `https://www.youtube.com/watch?v=VIDEO_ID&list=PLAYLIST_ID`
  - Playlist URL: `https://www.youtube.com/playlist?list=PLAYLIST_ID`
- Paste it into the "Video URL" field

> **Note:** For playlist URLs, only the first/specific video will be downloaded (single video mode)

### Step 2: Choose What to Download
Select one of three options:
- **Video Only** - Downloads just the video (no audio track)
- **Audio Only** - Extracts only the audio
- **Both** (default) - Downloads separate video and audio files

### Step 3: Select Quality & Format

**Video Quality:** Choose from 360p, 480p, 720p, 1080p, 1440p, or 2160p (4K)
- Higher quality = larger file size
- Default: 1080p

**Video Format:** mp4 (recommended), mkv, webm, or avi
- mp4 works on most devices

**Audio Format:** m4a (recommended), mp3, wav, or aac
- m4a: Best quality, smaller file
- mp3: Universal compatibility
- wav: Uncompressed, large file
- aac: Modern, efficient

### Step 4: Choose Download Location

**Default location:** `/media/mahmoud/New Volume1/Curriculum/Vidoes`

**To change the default:**
1. Open `src/yt_download/gui.py` in a text editor
2. Find this line (around line 66):
   ```python
   self.dest_var = tk.StringVar(value="/media/mahmoud/New Volume1/Curriculum/Vidoes")
   ```
3. Change the path to your preferred location:
   ```python
   self.dest_var = tk.StringVar(value="/home/yourname/Downloads")
   ```

**To change for one download:**
- Click the **Browse** button
- Select your desired folder

### Step 5: Download!
- Click the green **Download** button
- Watch the progress bar and speed/ETA info
- Files will be saved as:
  - Video: `Video Title.mp4` (or chosen format)
  - Audio: `Video Title_audio.m4a` (or chosen format)

## 💻 Command Line Usage (Advanced)

### Basic Examples

Download video at 1080p (default, video-only):
```bash
yt-download "https://www.youtube.com/watch?v=VIDEO_ID"
```

Download at specific quality:
```bash
yt-download "https://www.youtube.com/watch?v=VIDEO_ID" 720
```

Extract audio only:
```bash
yt-download "https://www.youtube.com/watch?v=VIDEO_ID" --audio-only
```

Custom output location:
```bash
yt-download "https://www.youtube.com/watch?v=VIDEO_ID" --output "/path/to/folder/%(title)s.%(ext)s"
```

Download only video, no audio:
```bash
yt-download "https://www.youtube.com/watch?v=VIDEO_ID" --mute
```

Use browser cookies (for age-restricted or region-locked videos):
```bash
yt-download "https://www.youtube.com/watch?v=VIDEO_ID" --cookies-from-browser chrome
```

Download specific video from playlist (ignore rest of playlist):
```bash
yt-download "https://www.youtube.com/watch?v=VIDEO_ID&list=PLAYLIST" --no-playlist
```

### All CLI Options

```bash
yt-download --help
```

## 📋 Requirements

- **Python 3.10 or newer**
- **yt-dlp** (installed automatically)
- **ffmpeg** (optional but highly recommended)
  - Required for: audio extraction, format conversion, video/audio merging
  - Without it: downloads may be video-only or lower quality
- **Tkinter** (for GUI, usually included with Python)

### Check if ffmpeg is installed:
```bash
ffmpeg -version
```

## ⚙️ Configuration

### Change Default Download Path (GUI)

Edit `src/yt_download/gui.py`, line ~66:
```python
self.dest_var = tk.StringVar(value="YOUR_PATH_HERE")
```

### Change Default Quality (GUI)

Edit `src/yt_download/gui.py`, line ~38:
```python
self.quality_var = tk.StringVar(value="720")  # Change from "1080"
```

### Change Default Formats (GUI)

Edit `src/yt_download/gui.py`:
- Video format (line ~45): `self.video_format_var = tk.StringVar(value="mkv")`
- Audio format (line ~52): `self.audio_format_var = tk.StringVar(value="mp3")`

## 🧪 Running Tests

```bash
pytest tests/ -v
```

## ❓ Troubleshooting

**"No module named tkinter"**
```bash
# Ubuntu/Debian
sudo apt install python3-tk

# macOS (use system Python or install via Homebrew)
brew install python-tk
```

**"command not found: ffmpeg"**
- Install ffmpeg (see Installation section)
- Downloads will still work but with limited format options

**Download fails with "Invalid URL"**
- Ensure URL starts with `http://` or `https://`
- Check that the video is public and available

**Video has no audio**
- Install ffmpeg for proper audio/video merging
- Or select "Both" to download separate files

## 📝 Notes

- Video format selection is best-effort; yt-dlp may substitute if exact format unavailable
- Audio codec conversion (mp3, wav, aac) requires ffmpeg
- GUI always downloads single videos (no full playlist support)
- CLI supports playlist downloads when `--no-playlist` is not used
- Downloaded files use the video title as filename

## 📄 License

See LICENSE file for details.
