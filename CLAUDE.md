# Podcast Transcript → Alpha Agent SOP
Repeatable steps for podcast analysis. Input: YouTube URL or raw transcript.

---

## Environment Setup

```
Working dir: /Users/adham/Claude-sandbox/Podcasts/
├── scripts/
│   ├── fetch_transcript.py   # YouTube transcript fetcher (with timestamps)
│   └── generate_player.py    # Excerpt player generator (extracts transcript text)
├── templates/
│   └── player_template.html  # Player HTML template (2-column layout)
├── podcast_analysis_framework.md # Analysis template
├── styles/report.css             # MAELSTROEM PDF styling
├── transcripts/                  # Raw transcripts (.json + .txt)
├── analyses/                     # Markdown analyses
├── excerpts/                     # Excerpt definitions (JSON)
├── players/                      # Generated HTML players
├── pdfs/                         # Final PDFs
└── tmp/                          # Intermediate HTML
```

### GitHub Pages Hosting
- **Repo:** https://github.com/maelstroem0/podcast-players
- **Base URL:** https://maelstroem0.github.io/podcast-players/
- Players and PDFs are auto-hosted after `git push`

### macOS Dependencies
- **pango**: installed via homebrew at `/opt/homebrew/lib/`
- **Fix**: prefix weasyprint commands with `DYLD_LIBRARY_PATH=/opt/homebrew/lib`

---

## Quick Pipeline (for new podcast)

```bash
# 1) Fetch transcript
python scripts/fetch_transcript.py "https://www.youtube.com/watch?v=VIDEO_ID"

# 2) Read transcript and write analysis (manually or via Claude)
# Output: analyses/YYYYMMDD_slug.md

# 3) Create excerpts JSON with pm_takeaway field
# Output: excerpts/YYYYMMDD_slug.json

# 4) Generate player + PDF
SLUG="YYYYMMDD_slug"
python scripts/generate_player.py excerpts/${SLUG}.json && \
pandoc analyses/${SLUG}.md -s --css=styles/report.css -o tmp/${SLUG}.html && \
DYLD_LIBRARY_PATH=/opt/homebrew/lib weasyprint --base-url . tmp/${SLUG}.html pdfs/${SLUG}.pdf

# 5) Push to GitHub Pages
git add players/ pdfs/ analyses/ excerpts/ && git commit -m "Add ${SLUG}" && git push
```

---

## 1) Fetch Transcript

```bash
python scripts/fetch_transcript.py <youtube_url>
```

**Output:**
- `transcripts/YYYYMMDD_slug.json` — Full transcript with timestamps
- `transcripts/YYYYMMDD_slug.txt` — Plain text version

---

## 2) Analyze

- **Read FULL transcript.** No truncation.
- Use `podcast_analysis_framework.md` template
- Output: `analyses/YYYYMMDD_slug.md`

### Speaker Bio (Required)

Add a **Speaker Bio** section immediately after the header block (before Executive Summary):

```markdown
## Speaker Bio

**[Name]** is [role] at [firm]. [1-2 sentences on background/credentials]. [Optional: notable calls or track record].
```

**Process:**
1. Check if transcript intro sufficiently covers speaker background
2. If not, **websearch** `"[Speaker Name]" [firm] bio` to gather credentials
3. Keep bio to 2-3 sentences max — focus on relevance to topic

**Example:**
```markdown
## Speaker Bio

**Alan Dunne** is founder of Archive Capital, an advisory firm focused on alternative investments. Former head of portfolio construction at Abbey Capital with 20+ years in macro/CTA allocation. Author of research on regime-adaptive portfolios.
```

### Key Formatting Rules

| Element | Format |
|---------|--------|
| Player link | `**⏱️ 5-Minute Version:** [Watch Key Excerpts](https://maelstroem0.github.io/podcast-players/players/YYYYMMDD_slug.html)` |
| Source link | `*Source: [Channel Name (YouTube)](URL)*` |
| Key Quotes | `1. > "quote"` with **BLANK LINE** between each |
| Top 3 Ideas | **BLANK LINE** after header, **BLANK LINE** between items |

#### ⚠️ CRITICAL: Blank Line Examples

**Key Quotes** — MUST have empty line between each quote:
```markdown
## Key Quotes

1. > "First quote here."

2. > "Second quote here."

3. > "Third quote here."
```

**Top 3 Ideas** — MUST have empty line after header AND between items:
```markdown
**Top 3 Investable Ideas:**

1) **First idea** — details here

2) **Second idea** — details here

3) **Third idea** — details here
```

❌ **WRONG** (no blank lines):
```markdown
1. > "Quote one."
2. > "Quote two."
```

---

## 3) Create Excerpts JSON

Create `excerpts/YYYYMMDD_slug.json` with this structure:

```json
{
  "video_id": "ABC123xyz",
  "url": "https://www.youtube.com/watch?v=ABC123xyz",
  "title": "Speaker Name: Key Phrase",
  "channel": "Channel Name",
  "total_duration": 7200,
  "pdf_link": "../pdfs/YYYYMMDD_slug.pdf",
  "excerpts": [
    {
      "id": 1,
      "start": 342,
      "end": 398,
      "duration": 56,
      "label": "Short title for this excerpt",
      "insight": "What the speaker is saying (descriptive)",
      "pm_takeaway": "Why it matters for PMs—actionable insight"
    }
  ]
}
```

### Excerpt Fields

| Field | Purpose | Example |
|-------|---------|---------|
| `label` | Short title shown in list | "Bitcoin is digital store of value" |
| `insight` | Descriptive summary (shown in excerpt list subtext) | "BTC competes with $500-800T fiat stores, not just gold" |
| `pm_takeaway` | Actionable PM insight (shown in PM Takeaway panel) | "BUY BTC. Size against fiat TAM ($500-800T), not gold. This is a 10x not 2x." |

#### ⚠️ PM Takeaway Style Guide

PM Takeaways must be **opinionated and actionable**—not generic observations.

✅ **GOOD** (specific, actionable, opinionated):
- "BUY SOFR. Market underpricing cuts by 50-75bps."
- "STEEPENERS NOW. Buy 10Y puts, stay long front-end."
- "Underweight hyperscalers—own semis over software."
- "Gold is a PASS at these levels. Too elevated to chase."

❌ **BAD** (generic, passive, no trade):
- "Consider defensive positioning"
- "AI concentration risk is real"
- "Prepare for non-parallel curve moves"
- "Market underpricing cuts"

**Rules:**
1. Start with action verb or trade direction (BUY, SELL, FADE, AVOID, PASS)
2. Include specific instrument/asset when possible
3. State conviction level if speaker did ("highest conviction call")
4. Include target levels if mentioned

### Excerpt Selection Rules
- **Total duration:** 4-5 minutes (240-300 seconds)
- **Per excerpt:** 30-75 seconds
- **Count:** 5-8 excerpts
- **Content:** Map to Key Quotes and Investable Insights

### Finding Timestamps
1. Search transcript JSON `segments` array for key quote text
2. Note the `start` time of matching segment
3. Extend `end` time to capture full thought (30-60s)

**Note:** Transcript filenames may differ from excerpt filenames (e.g., `20260104_ds_weekly_outlook_meeting_20260101.json` vs `20260104_ds_weekly_outlook.json`). The player generator finds transcripts by date prefix automatically.

---

## 4) Generate Player

```bash
python scripts/generate_player.py excerpts/YYYYMMDD_slug.json
```

**What it does:**
1. Loads player template
2. Extracts actual transcript text for each excerpt's time range
3. Formats speaker changes (`>>` → line breaks)
4. Outputs self-contained HTML with 2-column layout

**Player Features:**
- Left column: Video player, controls, excerpt list with insights
- Right column: PM Takeaway card, Transcript panel
- Mobile responsive (stacks vertically)
- Works from file:// (no server needed) via iframe embeds

---

## 5) Generate PDF

```bash
pandoc analyses/YYYYMMDD_slug.md -s --css=styles/report.css -o tmp/YYYYMMDD_slug.html && \
DYLD_LIBRARY_PATH=/opt/homebrew/lib weasyprint --base-url . tmp/YYYYMMDD_slug.html pdfs/YYYYMMDD_slug.pdf
```

---

## 6) Push to GitHub Pages

```bash
git add players/ pdfs/ analyses/ excerpts/
git commit -m "Add YYYYMMDD_slug"
git push
```

**URLs after push:**
- Player: `https://maelstroem0.github.io/podcast-players/players/YYYYMMDD_slug.html`
- PDF: `https://maelstroem0.github.io/podcast-players/pdfs/YYYYMMDD_slug.pdf`

---

## 7) Deliverables

| Artifact | Local Path | Hosted URL |
|----------|------------|------------|
| Transcript (JSON) | `transcripts/YYYYMMDD_slug.json` | — |
| Transcript (text) | `transcripts/YYYYMMDD_slug.txt` | — |
| Analysis | `analyses/YYYYMMDD_slug.md` | — |
| Excerpts | `excerpts/YYYYMMDD_slug.json` | — |
| Player | `players/YYYYMMDD_slug.html` | `maelstroem0.github.io/podcast-players/players/...` |
| PDF | `pdfs/YYYYMMDD_slug.pdf` | `maelstroem0.github.io/podcast-players/pdfs/...` |

---

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| No styling in PDF | Wrong working directory | Run from `/Users/adham/Claude-sandbox/Podcasts/` |
| PDF link broken in player | Wrong relative path | Use `../pdfs/SLUG.pdf` in excerpts JSON |
| Player link broken in PDF | Local path | Use full GitHub Pages URL in analysis.md |
| Video Error 150/153 | Opening from file:// with YT API | Use iframe embeds (current template does this) |
| Mobile no autoplay | Browser blocks autoplay | User must tap "Next Excerpt" manually |
| Transcript one block | Speaker changes not formatted | Generator now converts `>>` to line breaks |

---

## Executive Summary Writing Style

**Goal:** Extract alpha, not summarize. Crystallize 2-4 core concepts that change positioning.

**Structure (3 paragraphs):**
1. Para 1-2: Core concepts (bold the **concept**, not the quote)
2. Para 3: PM implications ("what does this mean for positioning?")

**Tone:** Authoritative, direct. Write like a senior analyst briefing a PM who has 2 minutes.
