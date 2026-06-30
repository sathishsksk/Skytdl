#!/usr/bin/env python3
# coding: utf-8
import logging
import os
from pathlib import Path
import yt_dlp
from config import AUDIO_FORMAT
from utils import is_youtube
from database.model import get_format_settings, get_quality_settings
from engine.base import BaseDownloader

# Resolution mapping (from 4K to 144p)
RESOLUTION_MAP = {
    "2160p": 2160,
    "1440p": 1440,
    "1080p": 1080,
    "720p": 720,
    "480p": 480,
    "360p": 360,
    "240p": 240,
    "144p": 144,
}

def match_filter(info_dict):
    if info_dict.get("is_live"):
        raise NotImplementedError("Skipping live video")
    return None

class YoutubeDownload(BaseDownloader):
    @staticmethod
    def get_format(resolution: int):
        """Generate yt-dlp format selectors for a given height."""
        return [
            f"bestvideo[ext=mp4][height={resolution}]+bestaudio[ext=m4a]",
            f"bestvideo[vcodec^=avc][height={resolution}]+bestaudio[acodec^=mp4a]/best[vcodec^=avc]/best",
        ]

    def _setup_formats(self) -> list:
        if not is_youtube(self._url):
            return [None]

        quality = get_quality_settings(self._chat_id)      # e.g., "2160p", "1080p", "audio"
        send_type = get_format_settings(self._chat_id)     # "video", "audio", "document"

        formats = []
        defaults = [
            "bestvideo[ext=mp4][vcodec!*=av01][vcodec!*=vp09]+bestaudio[ext=m4a]/bestvideo+bestaudio",
            "bestvideo[vcodec^=avc]+bestaudio[acodec^=mp4a]/best[vcodec^=avc]/best",
            None,
        ]
        audio_ext = AUDIO_FORMAT or "m4a"

        # ---- Audio mode ----
        if quality == "audio":
            formats.append(f"bestaudio[ext={audio_ext}]")
            formats.extend(defaults)
            return formats

        # ---- Video mode ----
        if quality in RESOLUTION_MAP:
            res = RESOLUTION_MAP[quality]
            formats.extend(self.get_format(res))
        else:
            # Fallback to 1080p if unknown quality
            formats.extend(self.get_format(1080))

        # Append default selectors as fallback (if not already the highest)
        if quality != "2160p":
            formats.extend(defaults)

        return formats

    def _download(self, formats) -> list:
        output = Path(self._tempdir.name, "%(title).70s.%(ext)s").as_posix()
        ydl_opts = {
            "progress_hooks": [lambda d: self.download_hook(d)],
            "outtmpl": output,
            "restrictfilenames": False,
            "quiet": True,
            "match_filter": match_filter,
            "concurrent_fragments": 16,
            "buffersize": 4194304,
            "retries": 6,
            "fragment_retries": 6,
            "skip_unavailable_fragments": True,
            "embed_metadata": True,       # Embed all metadata
            "embed_thumbnail": True,      # Embed thumbnail into audio
            "writethumbnail": False,
        }

        # YouTube-specific cookies / PO Token
        if is_youtube(self._url):
            # cookiesfrombrowser only makes sense if you actually run a
            # real browser profile inside the container (rare on Koyeb,
            # which is headless). Skip silently if BROWSERS is unset.
            if browsers := os.getenv("BROWSERS"):
                # NOTE: cookiesfrombrowser expects ONE browser as a tuple
                # (browser, profile, keyring, container) — NOT a list of
                # multiple browser names. Passing "chrome,firefox" made
                # yt-dlp treat "firefox" as a *profile name* inside
                # Chrome's config dir, which doesn't exist → crash.
                # Use only the first browser listed.
                browser_name = browsers.split(",")[0].strip()
                if browser_name:
                    ydl_opts["cookiesfrombrowser"] = (browser_name,)

            if os.path.isfile("youtube-cookies.txt") and os.path.getsize("youtube-cookies.txt") > 100:
                ydl_opts["cookiefile"] = "youtube-cookies.txt"
            if potoken := os.getenv("POTOKEN"):
                ydl_opts["extractor_args"] = {
                    "youtube": ["player-client=web,default", f"po_token=web+{potoken}"]
                }

        # Google Drive special handling
        if self._url.startswith("https://drive.google.com"):
            formats = ["source"] + formats

        files = None
        for f in formats:
            ydl_opts["format"] = f
            logging.info("yt-dlp options: %s", ydl_opts)
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([self._url])
                files = list(Path(self._tempdir.name).glob("*"))
                break
        return files

    def _start(self, formats=None):
        default_formats = self._setup_formats()
        if formats is not None:
            default_formats = formats + self._setup_formats()
        self._download(default_formats)
