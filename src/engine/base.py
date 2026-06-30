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
        self._chat_id = chat_id
        self._url = url
        self._client = client
        self._tempdir = tempfile.TemporaryDirectory(dir=TMPFILE_PATH)
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
            if self.filename and os.path.exists(self.filename):
                self.filesize = os.path.getsize(self.filename)

    async def start(self):
        await self._client.send_chat_action(self._chat_id, ChatAction.UPLOAD_DOCUMENT)
        try:
            self._start()
        except Exception as e:
            logging.exception("Download failed")
            await self._client.send_message(self._chat_id, BotText.error.format(error=str(e)))
        finally:
            await self._upload()

    def _start(self, formats=None):
        raise NotImplementedError

    async def _upload(self):
        """Upload every file found in the temp dir, then clean up."""
        try:
            files = list(Path(self._tempdir.name).glob("*"))
            for f in files:
                try:
                    await self._client.send_document(self._chat_id, str(f))
                except RPCError as e:
                    logging.exception("Upload failed for %s", f)
                    await self._client.send_message(
                        self._chat_id, BotText.error.format(error=str(e))
                    )
        finally:
            self._tempdir.cleanup()
