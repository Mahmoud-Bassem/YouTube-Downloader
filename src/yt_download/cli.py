import argparse
import shutil
import sys

import yt_dlp


def parse_args(argv: list[str]) -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Download YouTube video or audio with yt-dlp")
    p.add_argument("url")
    p.add_argument("quality", nargs="?", type=int, default=1080, help="max video height")
    p.add_argument("--output", default="%(title)s.%(ext)s", help="output template")
    p.add_argument("--cookies-from-browser", help="e.g. chrome, firefox, brave, chrome:Default")
    p.add_argument("--mute", action="store_true", help="download video without audio")
    p.add_argument("--audio-only", action="store_true", help="download only the audio track")
    p.add_argument("--no-playlist", action="store_true", help="download only the single video")
    return p.parse_args(argv)


def build_format(args: argparse.Namespace, has_ffmpeg: bool) -> str:
    if args.audio_only:
        return "bestaudio[ext=m4a]/bestaudio"

    fmt_video = (
        f"bv*[height<={args.quality}][ext=mp4][vcodec^=avc1]/"
        f"bv*[height<={args.quality}][ext=mp4]/"
        f"bv*[height<={args.quality}]"
    )
    return fmt_video


def build_opts(args: argparse.Namespace, fmt: str, has_ffmpeg: bool) -> dict:
    opts: dict = {
        "format": fmt,
        "outtmpl": args.output,
        "quiet": False,
        "concurrent_fragment_downloads": 1,
    }
    if args.no_playlist:
        opts["noplaylist"] = True
    if has_ffmpeg:
        if args.audio_only:
            opts["postprocessors"] = [
                {"key": "FFmpegExtractAudio", "preferredcodec": "m4a", "preferredquality": "0"}
            ]
        else:
            opts["merge_output_format"] = "mp4"
    if args.cookies_from_browser:
        opts["cookiesfrombrowser"] = (args.cookies_from_browser,)
    return opts


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    has_ffmpeg = shutil.which("ffmpeg") is not None
    fmt = build_format(args, has_ffmpeg)
    opts = build_opts(args, fmt, has_ffmpeg)
    with yt_dlp.YoutubeDL(opts) as ydl:
        return ydl.download([args.url])


__all__ = ["main"]
