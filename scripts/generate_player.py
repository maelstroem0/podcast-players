#!/usr/bin/env python3
"""
Generate self-contained HTML player from excerpts JSON.

Usage:
    python generate_player.py excerpts/YYYYMMDD_slug.json
    python generate_player.py excerpts/YYYYMMDD_slug.json --output players/custom.html

Output:
    players/YYYYMMDD_slug.html  - Self-contained excerpt player
"""

import json
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
ROOT_DIR = SCRIPT_DIR.parent
TEMPLATES_DIR = ROOT_DIR / "templates"
PLAYERS_DIR = ROOT_DIR / "players"
TRANSCRIPTS_DIR = ROOT_DIR / "transcripts"


def format_duration(seconds: int) -> str:
    """Convert seconds to M:SS format."""
    minutes = seconds // 60
    secs = seconds % 60
    return f"{minutes}:{secs:02d}"


def extract_transcript_text(segments: list, start: float, end: float) -> str:
    """Extract transcript text for a given time range."""
    texts = []
    for seg in segments:
        # Include segment if it overlaps with our range
        if seg["start"] < end and seg["end"] > start:
            texts.append(seg["text"])

    # Join and format speaker changes (>> indicates new speaker)
    raw_text = " ".join(texts)
    # Add line breaks before speaker indicators
    formatted = raw_text.replace(" >> ", "<br><br><strong>›</strong> ")
    formatted = formatted.replace(">> ", "<strong>›</strong> ")
    return formatted


def load_transcript(excerpts_file: Path, transcript_file: str = None) -> list:
    """Load transcript segments from corresponding transcript JSON.

    Args:
        excerpts_file: Path to excerpts JSON (used to derive default transcript name)
        transcript_file: Optional explicit transcript filename (without path)
    """
    if transcript_file:
        transcript_path = TRANSCRIPTS_DIR / transcript_file
    else:
        # Default: same name as excerpts file
        transcript_path = TRANSCRIPTS_DIR / excerpts_file.name

    if transcript_path.exists():
        data = json.loads(transcript_path.read_text())
        return data.get("segments", [])

    # Try to find a transcript that starts with the same date prefix
    date_prefix = excerpts_file.stem.split("_")[0]  # e.g., "20260104"
    for f in TRANSCRIPTS_DIR.glob(f"{date_prefix}_*.json"):
        data = json.loads(f.read_text())
        if "segments" in data:
            return data.get("segments", [])

    return []


def generate_player(excerpts_path: str, output_path: str = None) -> Path:
    """Generate HTML player from excerpts JSON."""
    excerpts_file = Path(excerpts_path)

    if not excerpts_file.exists():
        raise FileNotFoundError(f"Excerpts file not found: {excerpts_path}")

    # Load excerpts
    data = json.loads(excerpts_file.read_text())

    # Load transcript and add text to each excerpt
    transcript_file = data.get("transcript_file")  # Optional explicit transcript filename
    transcript_segments = load_transcript(excerpts_file, transcript_file)
    if transcript_segments:
        for exc in data["excerpts"]:
            exc["transcript"] = extract_transcript_text(
                transcript_segments, exc["start"], exc["end"]
            )
    
    # Determine output path
    if output_path:
        out_file = Path(output_path)
    else:
        PLAYERS_DIR.mkdir(exist_ok=True)
        out_file = PLAYERS_DIR / excerpts_file.name.replace('.json', '.html')
    
    # Load template
    template_file = TEMPLATES_DIR / "player_template.html"
    if not template_file.exists():
        raise FileNotFoundError(f"Template not found: {template_file}")
    
    template = template_file.read_text()
    
    # Calculate total excerpt duration
    total_excerpt_duration = sum(e["duration"] for e in data["excerpts"])
    
    # Build excerpt list HTML
    excerpt_items = []
    for i, exc in enumerate(data["excerpts"]):
        duration_str = format_duration(exc["duration"])
        insight = exc.get("insight", "")
        excerpt_items.append(
            f'<div class="excerpt-item" data-index="{i}" onclick="playExcerpt({i})">'
            f'<span class="excerpt-num">{i + 1}</span>'
            f'<div class="excerpt-content">'
            f'<div class="excerpt-label">{exc["label"]}</div>'
            f'<div class="excerpt-insight">{insight}</div>'
            f'</div>'
            f'<span class="excerpt-duration">{duration_str}</span>'
            f'</div>'
        )
    excerpt_list_html = "\n                ".join(excerpt_items)
    
    # Build excerpts JSON for JavaScript
    excerpts_js = json.dumps(data["excerpts"], indent=2)
    
    # Replace placeholders in template
    html = template
    html = html.replace("{{VIDEO_ID}}", data["video_id"])
    html = html.replace("{{VIDEO_TITLE}}", data["title"])
    html = html.replace("{{CHANNEL}}", data.get("channel", ""))
    html = html.replace("{{TOTAL_DURATION}}", format_duration(data["total_duration"]))
    html = html.replace("{{EXCERPT_DURATION}}", format_duration(total_excerpt_duration))
    html = html.replace("{{EXCERPT_COUNT}}", str(len(data["excerpts"])))
    html = html.replace("{{EXCERPT_PERCENT}}", str(round(total_excerpt_duration / data["total_duration"] * 100)))
    html = html.replace("{{EXCERPT_LIST}}", excerpt_list_html)
    html = html.replace("{{EXCERPTS_JSON}}", excerpts_js)
    html = html.replace("{{PDF_LINK}}", data.get("pdf_link", ""))
    
    # Write output
    out_file.parent.mkdir(exist_ok=True)
    out_file.write_text(html, encoding="utf-8")
    
    return out_file


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    
    excerpts_path = sys.argv[1]
    output_path = None
    
    if len(sys.argv) >= 4 and sys.argv[2] == "--output":
        output_path = sys.argv[3]
    
    try:
        out_file = generate_player(excerpts_path, output_path)
        print(f"✓ Player generated: {out_file}")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
