import os
from dotenv import load_dotenv

load_dotenv()

APP_ID = int(os.getenv("APP_ID", 0))
APP_HASH = os.getenv("APP_HASH", "")
BOT_TOKEN = os.getenv("BOT_TOKEN", "")
OWNER = [int(x) for x in os.getenv("OWNER", "").split(",") if x]

DB_DSN = os.getenv("DB_DSN", "sqlite:///db.sqlite")
REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_DB = int(os.getenv("REDIS_DB", 0))

AUDIO_FORMAT = os.getenv("AUDIO_FORMAT", "m4a")
TG_NORMAL_MAX_SIZE = int(os.getenv("TG_NORMAL_MAX_SIZE", 2000000000))
FREE_DOWNLOAD = int(os.getenv("FREE_DOWNLOAD", 3))
ENABLE_FFMPEG = os.getenv("ENABLE_FFMPEG", "True").lower() == "true"

TMPFILE_PATH = os.getenv("TMPFILE_PATH", "/app/tmp")
