import re

def is_youtube(url):
    return re.search(r"(youtube\.com|youtu\.be)", url, re.I) is not None

def is_instagram(url):
    return "instagram.com" in url

def is_krakenfiles(url):
    return "krakenfiles.com" in url

def is_pixeldrain(url):
    return "pixeldrain.com" in url

def is_direct_link(url):
    return re.match(r"^https?://.*\.[a-zA-Z0-9]{2,}/.*", url) is not None
