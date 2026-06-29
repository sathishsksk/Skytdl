import logging
import tempfile
import os
from pathlib import Path
from pyrogram.enums import ChatAction
from pyrogram.errors import RPCError
from config import TG_NORMAL_MAX_SIZE, TMPFILE_PATH
from config.constant import BotText

class BaseDownloader:
    def __init__(self, chat_id, url, client):
        self.chat_id = chat_id
        self.url = url
        self.client = client
        self.tempdir = tempfile.TemporaryDirectory(dir=TMPFILE_PATH)
        self.filename = None
        self.filesize = 0
        self.progress = 0
        self.speed = ""
        self.elapsed = ""

    def download_hook(self, d):
        if d['status'] == 'downloading':
            self.progress = d.get('_percent_str', '0%').strip()
            self.speed = d.get('_speed_str', 'N/A').strip()
            self.elapsed = d.get('_eta_str', 'N/A').strip()
        elif d['status'] == 'finished':
            self.filename = d.get('filename', '')
            self.filesize = os.path.getsize(self.filename)

    async def start(self):
        await self.client.send_chat_action(self.chat_id, ChatAction.UPLOAD_DOCUMENT)
        # Override _start in subclasses
        self._start()

    def _start(self, formats=None):
        raise NotImplementedError

    def _upload(self):
        # Implementation to upload file(s) from tempdir
        pass
