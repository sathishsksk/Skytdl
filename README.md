# Skytdl

# YouTube Downloader Bot for Koyeb

This is a Telegram bot that downloads videos/audio from YouTube and other platforms, supporting 4K to 144p video and audio with metadata.

## Features

- Full range of video resolutions (2160p → 144p)
- Audio downloads with embedded thumbnail, artist, title, etc.
- Supports YouTube, Instagram, Pixeldrain, KrakenFiles, and direct links
- User settings (quality and send format)
- Progress indication
- Deployable on Koyeb

## Deployment on Koyeb

1. Fork/clone this repository.
2. On Koyeb, create a new app and connect your GitHub repo.
3. Set the required environment variables (see `.env.example`).
4. Deploy with the Dockerfile.

## Environment Variables

| Variable | Description |
|----------|-------------|
| APP_ID | Telegram API ID |
| APP_HASH | Telegram API hash |
| BOT_TOKEN | Your bot token |
| OWNER | Admin user IDs (comma-separated) |
| DB_DSN | Database URL (e.g., sqlite:///db.sqlite) |
| AUDIO_FORMAT | Audio output format (m4a, mp3, etc.) |
| ... | See `.env.example` for more |

## Usage

Send any YouTube URL to the bot. Use `/settings` to adjust quality and format.
