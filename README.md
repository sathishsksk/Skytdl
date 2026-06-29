# Skytdl

# YouTube Downloader Bot for Koyeb

This is a Telegram bot that downloads videos/audio from YouTube and other platforms, supporting 4K to 144p video and audio with metadata.

[![Deploy to Koyeb](https://www.koyeb.com/static/images/deploy/button.svg)](https://app.koyeb.com/deploy?type=git&repository=github.com/sathishsksk/Skytdl&branch=main&name=skytdl)

## Features

- Full range of video resolutions (2160p → 144p)
- Audio downloads with embedded thumbnail, artist, title, etc.
- Supports YouTube, Instagram, Pixeldrain, KrakenFiles, and direct links
- User settings (quality and send format)
- Progress indication
- Deployable on Koyeb
- Built-in `/health` endpoint for Koyeb health checks

## Deployment on Koyeb

### One-Click Deploy

Click the **Deploy to Koyeb** button above, then set the required environment variables in the Koyeb dashboard.

### Manual Deploy

1. Fork this repository.
2. On [Koyeb](https://app.koyeb.com), create a new app → connect your GitHub repo.
3. Set the required environment variables (see `.env.example`).
4. Koyeb will build using the `Dockerfile` automatically.
5. Set the **health check path** to `/health` and **port** to `8000` in the Koyeb service settings.

## Environment Variables

| Variable | Description |
|----------|-------------|
| APP_ID | Telegram API ID |
| APP_HASH | Telegram API hash |
| BOT_TOKEN | Your bot token |
| OWNER | Admin user IDs (comma-separated) |
| DB_DSN | Database URL (e.g., sqlite:///db.sqlite) |
| AUDIO_FORMAT | Audio output format (m4a, mp3, etc.) |
| PORT | Health check server port (default: `8000`) |
| ... | See `.env.example` for more |

## Health Check

The bot exposes a lightweight HTTP health endpoint used by Koyeb to verify the service is running:

```
GET /health  →  200 OK  {"status": "ok"}
```

This runs automatically in the background when the bot starts — no extra setup needed.

## Usage

Send any YouTube URL to the bot. Use `/settings` to adjust quality and format.
