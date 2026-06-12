# Podcast Analysis Framework v6.0
Senior investment analyst playbook for podcast transcripts. Goal: extract alpha, not summarize. Core question: **Does this change what we hold, size, hedge, or monitor?**

## v6.0 — Apex Quantix Dashboard Format (2026-06-12)

Supersedes the Maelstroem prose-first layout. Reference implementation: `analyses/20260611_bg2_spacex_ipo_fable5_ai_capex.md`. Old analyses stay in v5.0 format; build them with the legacy pandoc command if regeneration is ever needed.

### Build pipeline (replaces pandoc+report.css)
```bash
SLUG="YYYYMMDD_slug"
python scripts/generate_player.py excerpts/${SLUG}.json          # unchanged
conda run -n ai python scripts/build_pdf.py ${SLUG}              # md -> branded PDF (pdfs/<slug>.pdf)
```
`scripts/build_pdf.py`: pandoc md→HTML, injects Apex Quantix header (embedded `styles/assets/logo_black.png`), applies `styles/apex_quantix_report.css`, renders via WeasyPrint (sets `DYLD_LIBRARY_PATH=/opt/homebrew/lib` internally). Brand tokens shared with Apexium daily brief: navy `#0f172a`, blue `#3b82f6`, Playfair Display + IBM Plex Sans/Mono.

### v6.0 document order (dashboard-first)
1. `# Title` (Playfair, becomes cover headline)
2. **Cover dashboard** (raw HTML, see snippets): `title-block` → `verdict-grid` (verdict-box + conflict-box) → `top-ideas`
3. `## 0) Who Is On It` — `speaker-cards` HTML (name/firm/role + skin-in-the-game chips) THEN the detailed researched table
4. Executive Summary (3-4 paras, alpha-first)
5. Episode map (chapters table)
6. Core theses, attributed per speaker (claim/mechanism/falsifier/confidence)
7. Verification layer — "they said vs our data" table with ✅/⚠️ verdicts (local bars + RS overlay + external research)
8. Key quotes (numbered blockquotes w/ timestamps)
9. Where they're most likely wrong (anti-theses)
10. BS & Bias filter — ranked per person, sourced (selling-into-event facts, fund stakes, track record)
11. **Companies & sectors map** — sector-grouped tables w/ our-data overlay + stance per name (the closing spread)
12. Companion-files pointer + PM bottom line + dated key watches

### Raw-HTML component snippets (pandoc passes divs through)
Cover dashboard:
```html
<div class="title-block">
<p class="show-line">SHOW — HOST w/ GUESTS</p>
<p class="meta-line">Published YYYY-MM-DD · 1h20m · <a href="URL">YouTube source</a> · <a href="players/SLUG.html">⏱ excerpt player</a></p>
</div>
<div class="verdict-grid">
<div class="verdict-box">
<p class="verdict-label">Verdict</p>
<p class="verdict-value">Must-Listen | Worth It | Skip</p>
<div class="ratings"><span class="stars">★★★★★</span> signal density<br>
<span class="stars">★★★★☆</span> actionability<br>
<span class="stars">★★★★☆</span> novel insights<br>
<span class="stars">★★☆☆☆</span> independence</div>
</div>
<div class="conflict-box [low|medium]">   <!-- no extra class = HIGH/red -->
<p class="conflict-label">Conflict Meter — HIGH|MEDIUM|LOW</p>
<div class="meter"><div class="fill" style="width:NN%"></div></div>
<p class="conflict-note">One-paragraph why.</p>
</div>
</div>
<div class="top-ideas">
<p class="ideas-label">Top 3 Takeaways for the Book</p>
<ol><li><strong>TICKER</strong> — stance + one-line rationale</li>...</ol>
</div>
```
Speaker card (repeat per person inside `<div class="speaker-cards">`):
```html
<div class="speaker-card">
<p class="sp-name">Name</p>
<p class="sp-firm">FIRM — ROLE</p>
<p class="sp-role">Role in this episode, one line.</p>
<span class="chip chip-red">HARD CONFLICT</span><span class="chip chip-amber">SOFT CONFLICT</span><span class="chip chip-blue">ACCESS/EDGE</span><span class="chip chip-green">CREDIT</span><span class="chip chip-gray">NEUTRAL FACT</span>
</div>
```
Chip semantics: red = direct financial conflict w/ the content; amber = same-book/correlated interest; blue = privileged access or channel checks; green = epistemic credit (disclosure, dissent); gray = neutral context.

Optional thesis card (alternative to `### T1` prose):
```html
<div class="thesis-card">
<p class="th-title"><span class="th-num">T1</span>Title (Speaker)</p>
<p class="th-row"><span class="th-key">Claim</span>...</p>
<p class="th-row"><span class="th-key">Mechanism</span>...</p>
<p class="th-row"><span class="th-key">Falsifier</span>...</p>
<p class="th-row"><span class="th-key">Confidence</span><span class="chip chip-green">HIGH</span></p>
</div>
```

### v6.0 rules (additive to v5.0 operating rules)
- **Conflict meter is mandatory** — every episode gets a scored HIGH/MEDIUM/LOW with the why; "talking his book" analysis ranks participants by conflict intensity with sourced facts (research the guests: funds, 13Fs, disclosed privates, selling-into-event statements).
- **Verification layer is mandatory** — cross-check market claims against Apexium local bars/RS snapshots and key factual claims against web research; tag ✅/⚠️ and mark UNVERIFIED honestly.
- **Companies & sectors map is the closing deliverable** — every name/sector mentioned, grouped, with our-data overlay and an explicit stance (Rotate-watch / Hold / Avoid / Trail-stop / Monitor).
- **Keep all work**: transcript json+txt+description in `transcripts/`, claims inventory + participants brief as `_claims.md` / `_participants.md` companions.
- Key watches must be **dated catalysts**, not vague bullets.

---

## v5.0 reference (legacy structure — superseded by v6.0 above)

## Operating Rules
- No fluff: synthesize; ignore non-actionable chatter.
- Hard filter: only actionable/testable insights survive.
- Cross-asset: map rates → FX → equities/credit/commodities/crypto.
- Verification: label Data vs Narrative; favor sourced numbers.
- Precision: use trade expressions (e.g., `Pay 2y1y`, `Sell ES 1m 5% OTM puts`).

## Output Template

### Header Format
```markdown
# [Speaker Name]: [Key Phrase from Title]
## Extracted from: [Podcast/Show Name]

*Source: [Channel Name (YouTube)](URL)*

*Published: DD-MM-YYYY*

**⏱️ 5-Minute Version:** [Watch Key Excerpts](players/YYYYMMDD_slug.html)

---
```
**Note:** Blank line between Source and Published required or pandoc merges them.

### Executive Summary
**Goal:** Extract alpha, not summarize. Crystallize 2-4 core concepts that change positioning.

**Depth Assessment (do first):** Count markers in transcript:
- Hard data anchors (numbers, levels, dates)
- Multi-layer mechanism (A → B → C)
- Regime contrast (before/after)
- Behavioral/positioning insight
- Contrarian thesis with falsifiable trigger
- Cross-asset transmission chain

**5+ markers = Rich (300-400 words, 3-4 paragraphs):**
- Para 1-2: Core concepts with data woven in
- Para 3: Mechanism/regime layer—how it works, what changed
- Para 4: PM implications

**2-4 markers = Adequate (200-300 words, 2-3 paragraphs):**
- Para 1-2: Core concepts
- Para 3: PM implications

**Rules:**
- Bold **concepts**, not quotes (quotes support, concepts lead)
- 3-6 green highlights max
- No summary language ("discusses", "talks about", "shares thoughts")
- Every sentence: "Does this change what I hold, size, hedge, or monitor?"
- Don't pad thin content—tier down and keep tight

### Listen or Skip?
**Verdict:** Must-listen / Worth it / Skip

| Aspect | Rating |
| :--- | :--- |
| Signal density | ★☆☆☆☆ to ★★★★★ |
| Actionability | ★☆☆☆☆ to ★★★★★ |
| Novel insights | ★☆☆☆☆ to ★★★★★ |
| Production quality | ★☆☆☆☆ to ★★★★★ |

**Best for:** [target audience]
**Skip if:** [who should pass]

### Key Quotes
5-8 memorable quotes as **numbered blockquotes**. Blank line between each quote.
```markdown
1. > "Quote one here."

2. > "Quote two here."
```
Choose lines that capture core thesis, contrarian takes, or memorable formulations.

### Key Excerpts (for 5-Minute Player)

**Output:** `excerpts/YYYYMMDD_slug.json`

Select 5-8 video segments (30-60 seconds each) totaling ~5 minutes. These power the auto-play excerpt player.

**Selection criteria:**
- Map directly to Key Investable Insights and Key Quotes
- Must be complete thoughts (no mid-sentence cuts)
- Prefer high-clarity audio moments (speaker emphasis, not mumbling)
- Each excerpt needs: start timestamp, end timestamp, label, insight summary

**Format:**
```json
{
  "video_id": "ABC123xyz",
  "url": "https://www.youtube.com/watch?v=ABC123xyz",
  "title": "Speaker Name: Key Phrase",
  "channel": "Channel Name",
  "total_duration": 7200,
  "pdf_link": "pdfs/YYYYMMDD_slug.pdf",
  "excerpts": [
    {
      "id": 1,
      "start": 342,
      "end": 398,
      "duration": 56,
      "label": "The negative art of investing",
      "insight": "Core thesis: avoiding losers beats picking winners"
    }
  ]
}
```

**How to identify timestamps:**
1. From transcript JSON: find the segment containing the quote
2. Use segment `start` time, extend `end` to capture full thought
3. Round to nearest second
4. Verify chunk is 30-60 seconds

### 1) Executive Dashboard (PM Read)
| Metric | Assessment |
| :--- | :--- |
| Net Signal | `Risk-On` / `Risk-Off` / `Neutral` / `Idiosyncratic` |
| Conviction | `High` / `Medium` / `Low` |
| Time Horizon | `Tactical (0-1m)` / `Cyclical (1-6m)` / `Structural (1y+)` |
| Primary Domain(s) | Multi-select: `Macro` `Rates` `FX` `Equities` `Credit` `Commodities` `Crypto` |
| Why Now? | One-line catalyst/timing driver |

**Top 3 Investable Ideas (if fewer, leave blanks):**

1) **[Long/Short Asset]** — expression + brief rationale

2) **[Long/Short Asset]** — expression + brief rationale

3) **[Long/Short Asset]** — expression + brief rationale

### 2) Key Investable Insights (cap at 3)
For each insight:
- **Claim:** one-sentence clear thesis.
- **Asset Class:** e.g., US Rates, EM FX.
- **Mechanism:** why price moves.
- **Expression:** concrete trade/hedge (e.g., `Receive 3m SOFR`, `Long XLE vs SPY`).
- **Trigger to Exit/Flip:** level/event invalidating the view.
- **Confidence:** `High` / `Medium` / `Low`.

### 3) Transmission & Cross-Asset Map
| Primary Driver | Direct Impact (1st Order) | Spillover (2nd Order) | Correlation Risk | Funding/Carry Impact | Positioning/Flows |
| :--- | :--- | :--- | :--- | :--- | :--- |

### 4) Regime & Scenario Analysis
- **Current Regime Fit:** confirm/challenge (e.g., Goldilocks, Reflation, Stagflation).
- **Base vs Alt Cases:** assign probabilities with timing check-in (e.g., "Revisit post-NFP, 0.6 base / 0.4 alt").
- **Anti-Thesis Trigger:** specific data/event that proves the speaker wrong.
- **Tail Risks:** low-probability but material events noted.

### 5) Hard Data & Verifiable Claims
List items as `Data:` (sourced numbers/levels) or `Claim:` (unsourced narrative). Include numeric precision, levels, dates, and source if given.

### 6) BS & Bias Filter
- **Incentives:** what are they selling/promoting?
- **Blind Spots:** coverage gaps (e.g., ignores earnings/flows).
- **Track Record / Hit-Rate:** if forecasts cited.
- **Consensus Check:** contrarian or herd echo?
- **Sample Bias:** geography/sector bias (e.g., only US data).

### 7) PM Bottom Line
Format:
```markdown
**Action → [Trade/Hedge/Monitor/Ignore]**

2-3 sentences with key reasoning. End with **Key watches:** specific data/events to monitor.
```
