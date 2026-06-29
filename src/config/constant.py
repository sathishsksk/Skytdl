class BotText:
    start = """
🎬 **YouTube Downloader Bot** 🎬

Send me a YouTube link (or any link supported by yt-dlp) and I'll download it for you!
I support **4K to 144p video** and **audio with full metadata** (thumbnail, artist, title, etc.).

📌 Use /settings to adjust quality and output format
📌 Use /help for assistance
📌 Use /about to learn more

Join https://t.me/ytdlbot0 for updates.
"""

    help = """
📖 **Help**

1️⃣ Send a YouTube / any yt-dlp supported URL directly.
2️⃣ For special links (Instagram, Pixeldrain, KrakenFiles) use `/spdl {URL}`.
3️⃣ Adjust settings: /settings
4️⃣ View stats: /stats
5️⃣ Buy quota (if VIP enabled): /buy

💡 If the bot is unresponsive, please wait or join https://t.me/ytdlbot0
🔗 Source: https://github.com/tgbot-collection/ytdlbot
"""

    about = """
🤖 **YouTube Downloader**

Developed by @BennyThink
Open source: https://github.com/tgbot-collection/ytdlbot

✨ Features:
• Supports 4K → 144p full range of resolutions
• Audio downloads with embedded metadata (thumbnail, artist, album, etc.)
• Fast download & upload with progress indicator
• Caching (same video downloaded once)
"""

    settings = """
⚙️ **Current Settings**

Video quality: `{}`
Send as: `{}`

Choose below:
• Quality: 2160p / 1440p / 1080p / 720p / 480p / 360p / 240p / 144p / Audio
• Send as: Document / Video / Audio
"""

    progress = """
⏳ **Processing...**

📥 Downloading: `{filename}`
📊 Progress: `{percent}%`
⚡ Speed: `{speed}`
⏱️ Elapsed: `{elapsed}`
"""

    success = """
✅ **Download complete!**

📁 File: `{filename}`
📦 Size: `{size}`
🎞️ Resolution: `{resolution}`
🎵 Audio: `{audio_info}`

Uploading to Telegram, please wait...
"""

    error = """
❌ **Error**

`{error}`

Please check the URL or try again later.
If the problem persists, join https://t.me/ytdlbot0 for support.
"""
