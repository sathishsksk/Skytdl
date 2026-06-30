# Skytdl

# YouTube Downloader Bot for Koyeb

This is a Telegram bot that downloads videos/audio from YouTube and other platforms, supporting 4K to 144p video and audio with metadata.

[![Deploy to Koyeb](https://www.koyeb.com/static/images/deploy/button.svg)](https://app.koyeb.com/deploy?type=git&repository=github.com/sathishsksk/Skytdl&branch=main&name=skytdl)

## Deployment on Koyeb (One-Click)

Just click the **Deploy to Koyeb** button above. Koyeb reads the `koyeb.yaml` file in this repo and will show you a form asking for these values — **you don't need to know what they mean in advance**, just fill in the four required ones:

| Variable | Required? | What to put |
|----------|-----------|-------------|
| `APP_ID` | ✅ Required | Get from [my.telegram.org](https://my.telegram.org) → API Development Tools |
| `APP_HASH` | ✅ Required | Same page as above |
| `BOT_TOKEN` | ✅ Required | Get from [@BotFather](https://t.me/BotFather) on Telegram |
| `OWNER` | ✅ Required | Your numeric Telegram user ID (get it from [@userinfobot](https://t.me/userinfobot)) — comma-separate if multiple admins |
| `DB_DSN` | Pre-filled | Leave as default (`sqlite:///db.sqlite`) unless using MySQL |
| `AUDIO_FORMAT` | Pre-filled | Leave as default (`m4a`) |
| `TG_NORMAL_MAX_SIZE` | Pre-filled | Max upload size in bytes, default 2GB |
| `FREE_DOWNLOAD` | Pre-filled | Free downloads/user/day, default 3 |
| `ENABLE_FFMPEG` | Pre-filled | Leave as default (`True`) |
| `PORT` | Pre-filled | Leave as default (`8000`) — used by the health check |

After filling the required fields, click **Deploy**. Koyeb builds the Dockerfile, starts the bot, and verifies it's alive via the built-in `/health` endpoint automatically — no extra dashboard configuration needed.

### Manual Deploy (alternative)

1. Fork this repo.
2. On [Koyeb](https://app.koyeb.com), create an app → connect your GitHub fork.
3. Koyeb auto-detects `koyeb.yaml` and prompts for the same variables as above.
4. Deploy.

## Features

- Full range of video resolutions (2160p → 144p)
- Audio downloads with embedded thumbnail, artist, title, etc.
- Supports YouTube, Instagram, Pixeldrain, KrakenFiles, and direct links
- User settings (quality and send format)
- Progress indication
- One-click Koyeb deploy with guided env var setup
- Built-in `/health` endpoint for Koyeb health checks

## Health Check

```
GET /health  →  200 OK  {"status": "ok"}
```

Runs automatically in the background — no setup needed, already wired into `koyeb.yaml`.

## Usage

Send any YouTube URL to the bot. Use `/settings` to adjust quality and format.
