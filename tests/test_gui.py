import pytest
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path
import tkinter as tk
from yt_download.gui import DownloaderGUI


@pytest.fixture
def root():
    """Create a Tk root window for testing."""
    root = tk.Tk()
    yield root
    root.destroy()


@pytest.fixture
def gui(root):
    """Create a DownloaderGUI instance for testing."""
    return DownloaderGUI(root)


class TestGUIInitialization:
    def test_window_title(self, gui):
        assert gui.root.title() == "yt-download"

    def test_default_download_type(self, gui):
        assert gui.download_type.get() == "both"

    def test_default_quality(self, gui):
        assert gui.quality_var.get() == "1080"

    def test_default_video_format(self, gui):
        assert gui.video_format_var.get() == "mp4"

    def test_default_audio_format(self, gui):
        assert gui.audio_format_var.get() == "m4a"

    def test_default_destination(self, gui):
        assert "/media/mahmoud/New Volume1/Curriculum/Vidoes" in gui.dest_var.get()


class TestURLValidation:
    def test_empty_url_validation(self, gui):
        gui.url_entry.insert(0, "")
        with patch("tkinter.messagebox.showerror") as mock_error:
            gui.start_download()
            mock_error.assert_called_once()
            assert "Please enter a URL" in mock_error.call_args[0][1]

    def test_invalid_url_validation(self, gui):
        gui.url_entry.insert(0, "not-a-url")
        with patch("tkinter.messagebox.showerror") as mock_error:
            gui.start_download()
            mock_error.assert_called_once()
            assert "Invalid URL" in mock_error.call_args[0][1]

    def test_valid_https_url(self, gui):
        gui.url_entry.insert(0, "https://example.com/video")
        with patch("threading.Thread"):
            gui.start_download()
            # Should not raise error


class TestChooseDestination:
    @patch("tkinter.filedialog.askdirectory")
    def test_choose_destination_updates_path(self, mock_dialog, gui):
        mock_dialog.return_value = "/new/path"
        gui.choose_destination()
        assert gui.dest_var.get() == "/new/path"

    @patch("tkinter.filedialog.askdirectory")
    def test_choose_destination_cancelled(self, mock_dialog, gui):
        original_path = gui.dest_var.get()
        mock_dialog.return_value = ""
        gui.choose_destination()
        assert gui.dest_var.get() == original_path


class TestProgressHook:
    def test_progress_downloading(self, gui):
        d = {
            "status": "downloading",
            "total_bytes": 1000,
            "downloaded_bytes": 500,
            "_speed_str": "1.5MiB/s",
            "_eta_str": "00:10"
        }
        gui.progress_hook(d)
        # Check that progress bar is updated (via after())
        gui.root.update()

    def test_progress_finished(self, gui):
        d = {"status": "finished"}
        gui.progress_hook(d)
        gui.root.update()

    def test_progress_with_missing_bytes(self, gui):
        d = {
            "status": "downloading",
            "total_bytes_estimate": 1000,
            "downloaded_bytes": 200,
            "_speed_str": "N/A",
            "_eta_str": "N/A"
        }
        # Should not raise exception
        gui.progress_hook(d)


class TestDownloadLogic:
    @patch("yt_download.gui.yt_dlp.YoutubeDL")
    @patch("yt_download.gui.shutil.which")
    def test_download_video_only(self, mock_which, mock_ytdl, gui):
        mock_which.return_value = "/usr/bin/ffmpeg"
        mock_ydl_instance = MagicMock()
        mock_ytdl.return_value.__enter__.return_value = mock_ydl_instance

        gui.url_entry.insert(0, "https://example.com/video")
        gui.download_type.set("video")
        gui.download()

        # Should call download once for video only
        assert mock_ydl_instance.download.call_count == 1

    @patch("yt_download.gui.yt_dlp.YoutubeDL")
    @patch("yt_download.gui.shutil.which")
    def test_download_audio_only(self, mock_which, mock_ytdl, gui):
        mock_which.return_value = "/usr/bin/ffmpeg"
        mock_ydl_instance = MagicMock()
        mock_ytdl.return_value.__enter__.return_value = mock_ydl_instance

        gui.url_entry.insert(0, "https://example.com/video")
        gui.download_type.set("audio")
        gui.download()

        # Should call download once for audio only
        assert mock_ydl_instance.download.call_count == 1

    @patch("yt_download.gui.yt_dlp.YoutubeDL")
    @patch("yt_download.gui.shutil.which")
    def test_download_both(self, mock_which, mock_ytdl, gui):
        mock_which.return_value = "/usr/bin/ffmpeg"
        mock_ydl_instance = MagicMock()
        mock_ytdl.return_value.__enter__.return_value = mock_ydl_instance

        gui.url_entry.insert(0, "https://example.com/video")
        gui.download_type.set("both")
        gui.download()

        # Should call download twice (video + audio)
        assert mock_ydl_instance.download.call_count == 2

    @patch("yt_download.gui.yt_dlp.YoutubeDL")
    @patch("yt_download.gui.shutil.which")
    @patch("tkinter.messagebox.showerror")
    def test_download_error_handling(self, mock_error, mock_which, mock_ytdl, gui):
        mock_which.return_value = "/usr/bin/ffmpeg"
        mock_ydl_instance = MagicMock()
        mock_ydl_instance.download.side_effect = Exception("Download failed")
        mock_ytdl.return_value.__enter__.return_value = mock_ydl_instance

        gui.url_entry.insert(0, "https://example.com/video")
        gui.download()

        # Should handle exception and show error
        gui.root.update()
