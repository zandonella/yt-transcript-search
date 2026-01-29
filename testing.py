import json
import os
import time
import random
from pathlib import Path
from youtube_transcript_api import (
    YouTubeTranscriptApi,
    TranscriptsDisabled,
    NoTranscriptFound,
    CouldNotRetrieveTranscript,
)
from youtube_transcript_api.formatters import JSONFormatter

from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("YOUTUBE_API_KEY")


TRANSCRIPT_DIR = Path("transcripts")
PLAYLIST_ID = "PLlDdLy-1g17aiMmEw63_K4Gf-gq_0AJhI"
TRANSCRIPT_DIR.mkdir(exist_ok=True)
(TRANSCRIPT_DIR / PLAYLIST_ID).mkdir(exist_ok=True)





from googleapiclient.discovery import build
youtube = build('youtube', 'v3', developerKey=api_key)

list_request = youtube.playlistItems().list(
    part='snippet,contentDetails',
    maxResults=1,
    playlistId=PLAYLIST_ID
)

response = list_request.execute()

ids_to_download = []

while response:
    for item in response['items']:
        video_id = item['contentDetails']['videoId']
        ids_to_download.append(video_id)

    if len(ids_to_download) >= 25:
        break
    
    list_request = youtube.playlistItems().list_next(
        previous_request=list_request,
        previous_response=response
    )
    
    if list_request is None:
        break
    
    response = list_request.execute()

print(ids_to_download)

yt_transcript_api = YouTubeTranscriptApi()

def download_and_cache_transcript(video_id):
    output_file = TRANSCRIPT_DIR / PLAYLIST_ID / f"{video_id}.json"
    if output_file.exists():
        print(f"Transcript for {video_id} already exists. Skipping download.")
        return
    
    try:
        transcript = yt_transcript_api.fetch(video_id)

        with open(output_file, "w", encoding="utf-8") as json_file:
            formatter = JSONFormatter()
            json_formatted = formatter.format_transcript(transcript)
            json.dump(json.loads(json_formatted), json_file, indent=4)
            
        print(f"Downloaded transcript for {video_id}")

        return transcript
    
    except (TranscriptsDisabled, NoTranscriptFound) as e:
        print(f"No transcript available for {video_id}: {e}")
    except CouldNotRetrieveTranscript as e:
        print(f"Could not retrieve transcript for {video_id}: {e}")
    except Exception as e:
        print(f"An unexpected error occurred for {video_id}: {e}")
    
    finally:
        time.sleep(random.uniform(5, 10))  # Sleep between 5 to 10 seconds

def download_transcripts_for_videos(video_ids):
    results = {
        "success": [],
        "failed": []
    }

    for i, video_id in enumerate(video_ids):
        print(f"[{i + 1}/{len(video_ids)}] Fetching transcript for {video_id}...")
        transcript = download_and_cache_transcript(video_id)

        if transcript:
            results["success"].append(video_id)
        else:
            results["failed"].append(video_id)

    return results

if __name__ == "__main__":
    stats = download_transcripts_for_videos(ids_to_download)
    print("Download complete.")
    print(f"Successful downloads: {len(stats['success'])}")
    print(f"Failed downloads: {len(stats['failed'])}")