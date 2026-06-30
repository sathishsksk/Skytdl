from engine.generic import YoutubeDownload


class DirectDownload(YoutubeDownload):
    """Plain direct-link files — yt-dlp's generic extractor handles these too."""
    pass
