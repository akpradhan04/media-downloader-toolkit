"""
Summary:
   This script downloads videos or playlists from YouTube using yt-dlp.

   - Automatically installs yt-dlp if it's not already available.
   - Accepts both single video URLs and playlist URLs.
   - Allows setting a maximum resolution (e.g., 720p).
   - Checks available formats and falls back to the closest lower resolution if needed.
   - Supports downloading a specific range from playlists.
   - Saves videos with organized filenames (and folders for playlists).
   - Can skip errors and optionally run in quiet mode.
"""

import subprocess
import sys

# ===== Self-install yt-dlp if missing =====
try:
    import yt_dlp
except ImportError:
    print("yt-dlp not found. Installing...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "yt-dlp"])
    import yt_dlp
print("yt-dlp is ready\n")


# ===== CONFIGURATION =====
download_list = [
    "https://www.youtube.com/watch?v=VIDEO_ID_1",
    "https://www.youtube.com/playlist?list=PLAYLIST_ID",
]

RESOLUTION = 720
PLAYLIST_START = 1
PLAYLIST_END = None
SKIP_ERRORS = True
QUIET_MODE = False


# ===== FUNCTIONS =====
def is_playlist(url):
    return "playlist" in url or "list=" in url


def get_format(resolution):
    if resolution:
        return f"best[height<={resolution}]"
    return "best"


def check_resolution(url, resolution):
    if not resolution:
        return None

    with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
        info = ydl.extract_info(url, download=False)
        formats = info.get("formats", [])

        available = sorted(
            {f.get("height") for f in formats if f.get("height")}
        )

        print(f"Available: {available}")

        if resolution not in available:
            lower = [r for r in available if r <= resolution]
            if lower:
                chosen = max(lower)
                print(f"Using closest lower: {chosen}p")
                return chosen
            else:
                chosen = max(available)
                print(f"Using best available: {chosen}p")
                return chosen

    return resolution


def download(url):
    print(f"\nProcessing → {url}")

    res = check_resolution(url, RESOLUTION)

    if is_playlist(url):
        ydl_opts = {
            'outtmpl': '%(playlist_title)s/%(playlist_index)s - %(title)s.%(ext)s',
            'format': get_format(res),
            'quiet': QUIET_MODE,
            'ignoreerrors': SKIP_ERRORS,
        }

        if PLAYLIST_START:
            ydl_opts['playliststart'] = PLAYLIST_START
        if PLAYLIST_END:
            ydl_opts['playlistend'] = PLAYLIST_END

    else:
        ydl_opts = {
            'outtmpl': '%(title)s.%(ext)s',
            'format': get_format(res),
            'quiet': QUIET_MODE,
        }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    print("Done")


# ===== MAIN =====
for url in download_list:
    download(url)
