#!/usr/bin/env python3
# coding: utf-8
import logging
import os
import sys
from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery
from config import APP_ID, APP_HASH, BOT_TOKEN, OWNER
from config.constant import BotText
from database.model import init_user, get_quality_settings, get_format_settings, set_user_settings
from engine.generic import YoutubeDownload
from engine.direct import DirectDownload
from engine.instagram import InstagramDownload
from engine.krakenfiles import KrakenFilesDownload
from engine.pixeldrain import PixelDrainDownload
from utils import is_youtube, is_instagram, is_krakenfiles, is_pixeldrain, is_direct_link
from health import start_health_server

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Client("ytdlbot", api_id=APP_ID, api_hash=APP_HASH, bot_token=BOT_TOKEN)

# ---- Start command ----
@app.on_message(filters.command("start"))
async def start_command(client: Client, message: Message):
    await message.reply_text(BotText.start, parse_mode=enums.ParseMode.MARKDOWN)

# ---- Help command ----
@app.on_message(filters.command("help"))
async def help_command(client: Client, message: Message):
    await message.reply_text(BotText.help, parse_mode=enums.ParseMode.MARKDOWN)

# ---- About command ----
@app.on_message(filters.command("about"))
async def about_command(client: Client, message: Message):
    await message.reply_text(BotText.about, parse_mode=enums.ParseMode.MARKDOWN)

# ---- Settings command ----
@app.on_message(filters.command("settings"))
async def settings_handler(client: Client, message: Message):
    chat_id = message.chat.id
    init_user(chat_id)
    await client.send_chat_action(chat_id, enums.ChatAction.TYPING)

    # Quality buttons (8 resolutions + audio)
    quality_buttons = [
        InlineKeyboardButton("📺 2160p", callback_data="2160p"),
        InlineKeyboardButton("📺 1440p", callback_data="1440p"),
        InlineKeyboardButton("📺 1080p", callback_data="1080p"),
        InlineKeyboardButton("📺 720p",  callback_data="720p"),
        InlineKeyboardButton("📺 480p",  callback_data="480p"),
        InlineKeyboardButton("📺 360p",  callback_data="360p"),
        InlineKeyboardButton("📺 240p",  callback_data="240p"),
        InlineKeyboardButton("📺 144p",  callback_data="144p"),
        InlineKeyboardButton("🎵 Audio", callback_data="audio"),
    ]
    # Arrange into rows of 3
    markup_rows = [quality_buttons[i:i+3] for i in range(0, len(quality_buttons), 3)]

    # Send-as buttons
    format_buttons = [
        InlineKeyboardButton("📄 Document", callback_data="document"),
        InlineKeyboardButton("🎬 Video",    callback_data="video"),
        InlineKeyboardButton("🎵 Audio",    callback_data="audio"),
    ]
    markup_rows.append(format_buttons)

    markup = InlineKeyboardMarkup(markup_rows)
    quality = get_quality_settings(chat_id)
    send_type = get_format_settings(chat_id)
    await client.send_message(
        chat_id,
        BotText.settings.format(quality, send_type),
        reply_markup=markup,
        parse_mode=enums.ParseMode.MARKDOWN
    )

# ---- Callback queries ----
@app.on_callback_query()
async def callback_handler(client: Client, callback_query: CallbackQuery):
    chat_id = callback_query.message.chat.id
    data = callback_query.data
    logger.info("Callback data: %s from %s", data, chat_id)

    # Quality selection
    if data in ["2160p", "1440p", "1080p", "720p", "480p", "360p", "240p", "144p", "audio"]:
        set_user_settings(chat_id, "quality", data)
        await callback_query.answer(f"✅ Quality set to {data}")
        # Update the settings message
        await settings_handler(client, callback_query.message)

    # Format selection
    elif data in ["document", "video", "audio"]:
        set_user_settings(chat_id, "format", data)
        await callback_query.answer(f"✅ Send as {data}")
        await settings_handler(client, callback_query.message)

    else:
        await callback_query.answer("Unknown option")

# ---- Handle URLs ----
@app.on_message(filters.text & ~filters.command([]))
async def handle_url(client: Client, message: Message):
    chat_id = message.chat.id
    url = message.text.strip()
    init_user(chat_id)

    # Choose appropriate downloader
    if is_youtube(url):
        downloader = YoutubeDownload(chat_id, url, client)
    elif is_instagram(url):
        downloader = InstagramDownload(chat_id, url, client)
    elif is_krakenfiles(url):
        downloader = KrakenFilesDownload(chat_id, url, client)
    elif is_pixeldrain(url):
        downloader = PixelDrainDownload(chat_id, url, client)
    elif is_direct_link(url):
        downloader = DirectDownload(chat_id, url, client)
    else:
        await message.reply_text("❌ Unsupported URL or platform.")
        return

    # Start download
    await downloader.start()

if __name__ == "__main__":
    start_health_server()   # ← Koyeb health check (runs in background thread)
    app.run()
