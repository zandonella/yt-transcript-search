import os
from pathlib import Path
from yt_dlp import YoutubeDL

TRANSCRIPT_DIR = Path("transcripts")
TRANSCRIPT_DIR.mkdir(exist_ok=True)


def download_transcripts_for_videos(playlist_url):
    out_path = Path(TRANSCRIPT_DIR)

    ydl_opts = {
        'skip_download': True,

        'writesubtitles': True,
        'writeautomaticsub': True,
        "subtitleslangs": ["en"],
        'subtitlesformat': 'vtt',

        'outtmpl': str(out_path / "%(uploader)s - %(playlist_title)s/%(title)s [%(id)s].%(ext)s"),

        "yesplaylist": True,

        "quiet": False,
        "no_warnings": True,
        "ignoreerrors": True,
        "retries": 5,
        "sleep_interval": 2,
        "max_sleep_interval": 5,
    }

    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([playlist_url])


if __name__ == "__main__":
    playlist_url = input("Enter the YouTube playlist URL: ").strip()
    stats = download_transcripts_for_videos(playlist_url)
    print("Download complete.")