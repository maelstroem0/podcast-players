#!/usr/bin/env python3
"""
Fetch YouTube transcript with timestamps and save to transcripts folder.
Auto-generates slug from video title.

Usage:
    python fetch_transcript.py <youtube_url>
    python fetch_transcript.py "https://www.youtube.com/watch?v=ABC123"

Output:
    transcripts/YYYYMMDD_slug.json  - Full transcript with timestamps
    transcripts/YYYYMMDD_slug.txt   - Plain text version (for reading)
"""

import json
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path

from youtube_transcript_api import YouTubeTranscriptApi

SCRIPT_DIR = Path(__file__).parent
ROOT_DIR = SCRIPT_DIR.parent
TRANSCRIPTS_DIR = ROOT_DIR / "transcripts"


def extract_video_id(url: str) -> str:
    """Extract video ID from various YouTube URL formats."""
    patterns = [
        r'(?:v=|/v/|youtu\.be/)([a-zA-Z0-9_-]{11})',
        r'^([a-zA-Z0-9_-]{11})$',
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    raise ValueError(f"Could not extract video ID from: {url}")


def get_video_metadata(video_id: str) -> dict:
    """Fetch video title and upload date using yt-dlp."""
    url = f"https://www.youtube.com/watch?v={video_id}"
    cmd = ["yt-dlp", "--dump-json", "--no-download", url]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        return {
            "title": video_id,
            "upload_date": datetime.now().strftime("%Y%m%d"),
            "channel": "Unknown",
            "duration": 0,
        }

    data = json.loads(result.stdout)
    return {
        "title": data.get("title", video_id),
        "upload_date": data.get("upload_date", datetime.now().strftime("%Y%m%d")),
        "channel": data.get("channel", "Unknown"),
        "duration": data.get("duration", 0),
    }


def slugify(text: str) -> str:
    """Convert text to slug format."""
    text = re.sub(r'\|.*$', '', text)
    text = re.sub(r'\(.*?\)', '', text)
    text = re.sub(r'\[.*?\]', '', text)
    text = text.lower().strip()
    text = re.sub(r'[^a-z0-9\s-]', '', text)
    text = re.sub(r'[\s_]+', '_', text)
    return text[:60].strip('_')


def format_timestamp(seconds: float) -> str:
    """Convert seconds to HH:MM:SS or MM:SS format."""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    if hours > 0:
        return f"{hours}:{minutes:02d}:{secs:02d}"
    return f"{minutes}:{secs:02d}"


def fetch_transcript(url: str) -> tuple[Path, Path, str, dict]:
    """
    Fetch transcript and save to files.
    Returns (json_filepath, txt_filepath, video_url, metadata).
    """
    TRANSCRIPTS_DIR.mkdir(exist_ok=True)

    video_id = extract_video_id(url)
    canonical_url = f"https://www.youtube.com/watch?v={video_id}"

    # Get metadata for title/date
    print(f"Fetching metadata for {video_id}...")
    metadata = get_video_metadata(video_id)

    # Generate slug from title
    slug = slugify(metadata["title"])
    date = metadata["upload_date"][:8]

    print(f"Title: {metadata['title']}")
    print(f"Channel: {metadata['channel']}")
    print(f"Duration: {format_timestamp(metadata['duration'])}")
    print(f"Date: {date}")
    print(f"Slug: {slug}")

    # Fetch transcript
    print("Fetching transcript...")
    ytt = YouTubeTranscriptApi()
    transcript = ytt.fetch(video_id, languages=['en', 'en-US', 'en-GB'])

    # Build segments with timestamps
    segments = []
    for snippet in transcript:
        start = snippet.start
        duration = snippet.duration
        segments.append({
            "start": round(start, 2),
            "end": round(start + duration, 2),
            "duration": round(duration, 2),
            "text": snippet.text,
        })

    # Build full text
    full_text = "\n".join(snippet.text for snippet in transcript)

    # Generate filenames
    base_filename = f"{date}_{slug}"
    json_filepath = TRANSCRIPTS_DIR / f"{base_filename}.json"
    txt_filepath = TRANSCRIPTS_DIR / f"{base_filename}.txt"

    # Save JSON with timestamps
    json_data = {
        "video_id": video_id,
        "url": canonical_url,
        "title": metadata["title"],
        "channel": metadata["channel"],
        "upload_date": date,
        "duration_seconds": metadata["duration"],
        "duration_formatted": format_timestamp(metadata["duration"]),
        "fetched_at": datetime.now().isoformat(),
        "segment_count": len(segments),
        "segments": segments,
        "full_text": full_text,
    }
    json_filepath.write_text(json.dumps(json_data, indent=2), encoding="utf-8")

    # Save plain text version (for easy reading)
    txt_header = f"""Source: {canonical_url}
Title: {metadata['title']}
Channel: {metadata['channel']}
Duration: {format_timestamp(metadata['duration'])}
Date: {date}
Fetched: {datetime.now().isoformat()}

---

"""
    txt_filepath.write_text(txt_header + full_text, encoding="utf-8")

    return json_filepath, txt_filepath, canonical_url, metadata


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    url = sys.argv[1]

    try:
        json_path, txt_path, video_url, metadata = fetch_transcript(url)
        print(f"\n✓ JSON saved: {json_path}")
        print(f"✓ Text saved: {txt_path}")
        print(f"Source URL: {video_url}")
        print(f"Segments: {len(json.loads(json_path.read_text())['segments'])}")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
