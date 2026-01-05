# Podcast Analysis Framework v5.0
Senior investment analyst playbook for podcast transcripts. Goal: extract alpha, not summarize. Core question: **Does this change what we hold, size, hedge, or monitor?**

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
