import time
from pathlib import Path
from yt_dlp import YoutubeDL

TRANSCRIPT_DIR = Path("transcripts")

def download_transcripts_for_videos(playlist_url):
    out_path = Path(TRANSCRIPT_DIR)

    ydl_opts = {
        "skip_download": True,
        "writesubtitles": True,
        "writeautomaticsub": True,
        "subtitleslangs": ["en"],
        "subtitlesformat": "vtt",
        "outtmpl": str(out_path / "%(title)s [%(id)s].%(ext)s"),
        "yesplaylist": True,
        "quiet": False,
        "no_warnings": True,
        "ignoreerrors": True,
        "retries": 5,
        "sleep_interval": 3,
        "max_sleep_interval": 7,
    }

    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([playlist_url])


if __name__ == "__main__":
    directory = input("Enter a directory to save transcripts: ").strip()
    if directory:
        TRANSCRIPT_DIR = Path(directory)
        TRANSCRIPT_DIR.mkdir(exist_ok=True)
    playlist_url = input("Enter the YouTube playlist URL: ").strip()
    start_time = time.time()
    stats = download_transcripts_for_videos(playlist_url)
    end_time = time.time()
    elapsed_time = end_time - start_time
    print("Download complete.")
    print(f"Elapsed time: {elapsed_time:.2f} seconds")
