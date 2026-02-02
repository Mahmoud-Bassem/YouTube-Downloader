# yt-download

Simple CLI and GUI wrapper around yt-dlp for downloading YouTube videos and audio.

## Features

- **CLI**: Fast command-line downloads with customizable options
- **GUI**: User-friendly Tkinter interface with progress tracking
- Video and audio format selection (mp4, mkv, webm, avi for video; m4a, mp3, wav, aac for audio)
- Quality selection (360p-2160p)
- Download video-only, audio-only, or both
- Real-time progress bar and speed/ETA display

## Install

### Pip (in a venv)
```bash
pip install .
```

### Pipx (isolated)
```bash
pipx install .
```

### From source without installing
```bash
python -m yt_download --help
python -m yt_download.gui
```

## Usage

### CLI

Download single video (1080p, video-only):
```bash
yt-download "https://www.youtube.com/watch?v=VIDEO_ID"
```

Download with specific quality:
```bash
yt-download "https://www.youtube.com/watch?v=VIDEO_ID" 720
```

Audio-only (requires ffmpeg):
```bash
yt-download "https://www.youtube.com/watch?v=VIDEO_ID" --audio-only
```

Download just the video, no audio:
```bash
yt-download "https://www.youtube.com/watch?v=VIDEO_ID" --mute
```

Custom output location and name:
```bash
yt-download "https://www.youtube.com/watch?v=VIDEO_ID" --output "/path/to/%(title)s.%(ext)s"
```

Use browser cookies (for age/region restrictions):
```bash
yt-download "https://www.youtube.com/watch?v=VIDEO_ID" --cookies-from-browser chrome
```

### GUI

Launch the GUI:
```bash
python -m yt_download.gui
```
or if installed:
```bash
yt-download-gui
```

Select download type, quality, format, and destination folder. Progress bar shows real-time stats.

## Requirements

- Python 3.10+
- yt-dlp
- ffmpeg (optional, recommended for best quality)
- Tkinter (included with most Python distributions)

## Notes

- ffmpeg is optional but strongly recommended for quality video/audio extraction and codec conversion.
- GUI defaults to `~/Downloads` as destination.
- Video format selection is best-effort; yt-dlp may substitute if exact format unavailable.
- Audio codec conversion requires ffmpeg.

- Requires Python 3.10+.
- The quality argument caps video height; defaults to 1080.
