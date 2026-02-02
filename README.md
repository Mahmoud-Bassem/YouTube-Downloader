# YouTube Downloader

Download YouTube videos and audio with a simple GUI.

## Setup

```bash
pip install .
sudo apt install ffmpeg  # Ubuntu/Debian
```

## Use Case: Download a Music Video as Audio

1. **Launch the app:**
   ```bash
   python -m yt_download.gui
   ```

2. **Paste the YouTube URL:**
   - Go to YouTube, find a music video
   - Copy the URL (e.g., `https://www.youtube.com/watch?v=...`)
   - Paste into the "Video URL" field

3. **Choose what to download:**
   - Select **Audio Only**

4. **Pick audio quality:**
   - **Audio Format:** m4a (best quality, small file)
   - *(Optional) Video Quality setting is disabled since you chose audio-only*

5. **Set where to save:**
   - Click **Browse** to choose a folder
   - Or use the default path

6. **Download:**
   - Click the green **Download** button
   - Watch the progress bar
   - File saves as: `Video Title_audio.m4a`

## Requires

- Python 3.10+
- ffmpeg (for format conversion)

