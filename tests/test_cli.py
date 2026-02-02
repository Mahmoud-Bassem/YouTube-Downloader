import pytest
from unittest.mock import Mock, patch, MagicMock
from yt_download.cli import parse_args, build_format, build_opts, main


class TestParseArgs:
    def test_default_quality(self):
        args = parse_args(["https://example.com/video"])
        assert args.url == "https://example.com/video"
        assert args.quality == 1080
        assert args.audio_only is False
        assert args.mute is False
        assert args.no_playlist is False

    def test_custom_quality(self):
        args = parse_args(["https://example.com/video", "720"])
        assert args.quality == 720

    def test_audio_only_flag(self):
        args = parse_args(["https://example.com/video", "--audio-only"])
        assert args.audio_only is True

    def test_mute_flag(self):
        args = parse_args(["https://example.com/video", "--mute"])
        assert args.mute is True

    def test_no_playlist_flag(self):
        args = parse_args(["https://example.com/video", "--no-playlist"])
        assert args.no_playlist is True

    def test_custom_output(self):
        args = parse_args(["https://example.com/video", "--output", "custom.mp4"])
        assert args.output == "custom.mp4"

    def test_cookies_from_browser(self):
        args = parse_args(["https://example.com/video", "--cookies-from-browser", "chrome"])
        assert args.cookies_from_browser == "chrome"


class TestBuildFormat:
    def test_audio_only_format(self):
        args = Mock(audio_only=True, quality=1080, mute=False)
        fmt = build_format(args, has_ffmpeg=True)
        assert "bestaudio" in fmt

    def test_video_only_format(self):
        args = Mock(audio_only=False, quality=720, mute=False)
        fmt = build_format(args, has_ffmpeg=True)
        assert "bv*[height<=720]" in fmt
        assert "mp4" in fmt

    def test_quality_constraint(self):
        args = Mock(audio_only=False, quality=1080, mute=False)
        fmt = build_format(args, has_ffmpeg=True)
        assert "[height<=1080]" in fmt


class TestBuildOpts:
    def test_basic_options(self):
        args = Mock(
            output="%(title)s.%(ext)s",
            no_playlist=False,
            audio_only=False,
            cookies_from_browser=None
        )
        opts = build_opts(args, "bv*", has_ffmpeg=True)
        assert opts["format"] == "bv*"
        assert opts["outtmpl"] == "%(title)s.%(ext)s"
        assert opts["quiet"] is False

    def test_no_playlist_option(self):
        args = Mock(
            output="test.mp4",
            no_playlist=True,
            audio_only=False,
            cookies_from_browser=None
        )
        opts = build_opts(args, "bv*", has_ffmpeg=True)
        assert opts["noplaylist"] is True

    def test_audio_postprocessor_with_ffmpeg(self):
        args = Mock(
            output="test.m4a",
            no_playlist=False,
            audio_only=True,
            cookies_from_browser=None
        )
        opts = build_opts(args, "bestaudio", has_ffmpeg=True)
        assert "postprocessors" in opts
        assert opts["postprocessors"][0]["key"] == "FFmpegExtractAudio"

    def test_video_merge_format_with_ffmpeg(self):
        args = Mock(
            output="test.mp4",
            no_playlist=False,
            audio_only=False,
            cookies_from_browser=None
        )
        opts = build_opts(args, "bv*", has_ffmpeg=True)
        assert opts["merge_output_format"] == "mp4"

    def test_cookies_from_browser(self):
        args = Mock(
            output="test.mp4",
            no_playlist=False,
            audio_only=False,
            cookies_from_browser="firefox"
        )
        opts = build_opts(args, "bv*", has_ffmpeg=True)
        assert opts["cookiesfrombrowser"] == ("firefox",)


class TestMain:
    @patch("yt_download.cli.yt_dlp.YoutubeDL")
    @patch("yt_download.cli.shutil.which")
    def test_main_success(self, mock_which, mock_ytdl):
        mock_which.return_value = "/usr/bin/ffmpeg"
        mock_ydl_instance = MagicMock()
        mock_ydl_instance.download.return_value = 0
        mock_ytdl.return_value.__enter__.return_value = mock_ydl_instance

        result = main(["https://example.com/video"])
        
        assert result == 0
        mock_ydl_instance.download.assert_called_once_with(["https://example.com/video"])

    @patch("yt_download.cli.yt_dlp.YoutubeDL")
    @patch("yt_download.cli.shutil.which")
    def test_main_no_ffmpeg(self, mock_which, mock_ytdl):
        mock_which.return_value = None
        mock_ydl_instance = MagicMock()
        mock_ydl_instance.download.return_value = 0
        mock_ytdl.return_value.__enter__.return_value = mock_ydl_instance

        result = main(["https://example.com/video", "--audio-only"])
        
        assert result == 0
