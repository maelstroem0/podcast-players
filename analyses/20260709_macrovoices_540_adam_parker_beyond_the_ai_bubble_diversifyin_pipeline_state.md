# MV540 pipeline state — PAUSED 2026-07-12 (resume here)

Episode: MacroVoices #540, Adam Parker (Trivariate), 2026-07-09, 41:57.
Source: Apple link resolved → YouTube exact-duration match `-wKLuErezzQ` (2517s == Apple trackTimeMillis). Extended cut `nIFH7B6OQzs` (3498s) NOT used.

## Done (steps 1-3 of podcast-deep-analysis skill)
- Transcript: `transcripts/20260709_..._diversifyin.{json,txt}` (1181 segments) + `_description.txt`
- Agent A claims/quotes: `analyses/..._claims.md` — 18 quotes, ~96-row claims table, ticker/stance map. **Caveat: agent used the .txt (no timecodes) — its timestamps are proportional ESTIMATES (±30-60s). Re-anchor excerpt timestamps against the .json segments (grep quote text) before building excerpts.**
- Agent B participants/verification: `analyses/..._participants.md` — Parker LOW book-talk risk (research subs, no AUM/13F; Trivector plug confirmed $110/mo), Townsend MEDIUM (self-funded via own Fourth Turning entity, pro-nuclear/uranium tilt steers energy framing), Ceresna HIGH (Big Picture Trading funnel, XLE-collar trade-of-week ties directly to his paid service). 10-row claim verification table w/ sources.
- Step 3 local-data verification: `analyses/..._market_verification.md` (Apexium bars + RS + XLE-SMH corr -0.27 6M — Parker's core diversification claim confirmed emphatically).

## Remaining (steps 4-6)
4. **Write v6.0 report** (main session, NOT delegated) — read `podcast_analysis_framework.md` v6.0 section first (lines 1-88). Structure: cover dashboard (verdict box, conflict meter, top-3 takeaways) → speaker cards w/ conflict chips → exec summary → episode map → attributed theses w/ falsifiers → verification table (merge Agent B table + market_verification.md) → key quotes → anti-theses → ranked talking-their-book audit (Ceresna HIGH / Townsend MED / Parker LOW) → companies & sectors map w/ stance (from claims.md section C; flag CEG ⚠️ and Eaton/CAT false-diversifier warning) → dated key watches.
5. Excerpts (6-8 × 45-90s, timestamps from .json) → `conda run -n ai python scripts/generate_player.py excerpts/<slug>.json` → `conda run -n ai python scripts/build_pdf.py <slug>` → sanity-check cover page 1 via pdf2image.
6. Telegram (send-telegram skill) + commit slug files + push.

## Notes
- Short-slug files (`20260709_macrovoices_540_adam_parker_participants*.md`, `_description.txt`) = prior aborted attempt, superseded by long-slug set; left uncommitted.
- Agent B died at session-limit AFTER writing its deliverable (verified on disk, complete incl. sources).
- Related: Iris feature design (Apple-link ingest automation) lives in iris repo `docs/superpowers/specs/2026-07-12-apple-podcast-ingest-design.md`.
