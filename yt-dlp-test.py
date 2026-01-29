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
        'subtitlesformat': 'json3',

        'outtmpl': str(out_path / "%(playlist_title)s/%(title)s [%(id)s].%(ext)s"),

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
    playlist_url = "https://www.youtube.com/playlist?list=PLlDdLy-1g17ZQlKROSatxk7uGovsBwQ8p"
    stats = download_transcripts_for_videos(playlist_url)
    print("Download complete.")