import json
import os
from pathlib import Path

TRANSCRIPT_DIR = Path("transcripts")
PLAYLIST_ID = "PLlDdLy-1g17aiMmEw63_K4Gf-gq_0AJhI"

transcripts = os.listdir(TRANSCRIPT_DIR / PLAYLIST_ID)

for transcript_file in transcripts:
    print(f"Transcript file: {transcript_file}\n")
    with open(TRANSCRIPT_DIR / PLAYLIST_ID / transcript_file, "r", encoding="utf-8") as f:
        transcript_data = json.load(f)
        
        for i, entry in enumerate(transcript_data):
            if i >= 5:
                break
            print(f"{entry['start']}: {entry['text']}, (duration: {entry.get('duration', 'N/A')})")