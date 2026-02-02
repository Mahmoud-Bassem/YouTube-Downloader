# yt-download

Simple CLI wrapper around yt-dlp for grabbing YouTube video or audio. Prioritizes mp4/H.264 for player compatibility and falls back to progressive formats when ffmpeg is missing.

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
```

## Usage

Download video with audio (default 1080p cap):
```bash
yt-download "https://www.youtube.com/watch?v=VIDEO" 1080
```

Video-only (mute):
```bash
yt-download "https://www.youtube.com/watch?v=VIDEO" 720 --mute
```

Audio-only (m4a when ffmpeg is present):
```bash
yt-download "https://www.youtube.com/watch?v=VIDEO" --audio-only
```

Custom output template:
```bash
yt-download "https://www.youtube.com/watch?v=VIDEO" --output "%(title)s.%(ext)s"
```

Use browser cookies (helps with age/region restrictions):
```bash
yt-download "https://www.youtube.com/watch?v=VIDEO" --cookies-from-browser chrome
```

## Notes
- ffmpeg is optional but recommended for best-quality muxing and m4a extraction.
- Requires Python 3.10+.
- The quality argument caps video height; defaults to 1080.
