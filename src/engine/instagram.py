from engine.generic import YoutubeDownload


class InstagramDownload(YoutubeDownload):
    """yt-dlp natively supports Instagram, so we reuse the same logic."""
    pass
