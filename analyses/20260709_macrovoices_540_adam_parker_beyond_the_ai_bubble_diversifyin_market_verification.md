# MV540 — Market-Claim Verification vs Apexium Local Bars (step 3 output)

Computed 2026-07-12 from `~/AI/Apexium/data/bars/<SYM>/daily.parquet` (last bar 2026-07-10) + `rs_dashboard_stocks/2026-07-10/rows_27d.parquet`.

## Returns / levels

| Sym | Close (07-10) | YTD% | 1M% | 3M% | off 52wH% | off MayHi% |
|---|---|---|---|---|---|---|
| NVDA | 210.96 | 13.1 | 5.3 | 11.8 | -10.8 | -10.8 |
| MU | 979.30 | 243.1 | 9.8 | 132.8 | -22.0 | -0.2 |
| GEV | 1091.57 | 67.2 | 25.9 | 10.1 | -8.7 | -3.0 |
| VST | 158.86 | -1.5 | 14.7 | 2.7 | -27.6 | -5.7 |
| CEG | 251.38 | -28.7 | 3.7 | -12.3 | -38.9 | -23.5 |
| GLW | 190.89 | 118.4 | 13.5 | 11.5 | -29.8 | -9.9 |
| CIEN | 460.72 | 97.0 | 6.0 | -7.1 | -27.7 | -23.9 |
| AAPL | 315.32 | 16.1 | 8.1 | 21.1 | -0.7 | 0.1 |
| ETN | 407.28 | 28.3 | 8.5 | 1.1 | -6.7 | -6.5 |
| CAT | 952.41 | 66.6 | 11.2 | 20.5 | -11.3 | 2.3 |
| XLE | 55.08 | 23.2 | -5.4 | -3.3 | -13.2 | -10.7 |
| SPY | 754.95 | 11.0 | 4.1 | 11.1 | -0.7 | -0.4 |
| GLD | 377.01 | -4.9 | 0.6 | -13.8 | -26.0 | -13.8 |
| GC_CONT | 4140.80 | -5.1 | -3.4 | -14.1 | -25.8 | -13.3 |
| CL_CONT | 72.08 | 27.2 | -18.3 | -26.4 | -38.7 | -32.5 |
| USO | 108.70 | 57.2 | -19.1 | -12.9 | -29.5 | -29.5 |

## RS 27d overlay (2026-07-10, r1k universe)

| Ticker | rs_pct | rs_pct_63d | rs_pct_weighted |
|---|---|---|---|
| GEV | 0.914 | 0.696 | 0.878 |
| CAT | 0.787 | 0.824 | 0.935 |
| GLW | 0.714 | 0.688 | 0.977 |
| AAPL | 0.521 | 0.827 | 0.779 |
| VST | 0.511 | 0.513 | 0.158 |
| ETN | 0.482 | 0.455 | 0.528 |
| CEG | 0.278 | 0.190 | 0.208 |
| MU | 0.275 | 0.995 | 0.997 |
| NVDA | 0.261 | 0.737 | 0.741 |
| CIEN | 0.062 | 0.282 | 0.995 |

## They-said vs our-data verdicts

- **S&P systematic sell-trigger 7,300–7,350** (trading desk): SPY 754.95 → SPX ≈ 7,550. Level is ~3% below spot. ✅ plausible.
- **Gold $4,000 psychological support**: GC 4,140.8, -25.8% off 52w high (~5,580), -13.3% off May high. ✅ level is live and close.
- **Oil ~$90 = 50% retracement / rebound ~$9 / pre-war <$70**: CL 72.08, May high ≈ 107. Retracement midpoint of the 107→~68 decline ≈ 88-90. ✅ geometry consistent; note Agent B found the "850bps weekly" surge overstated (~4% actual).
- **XLE collar $50P/$65C**: XLE 55.08 — strikes bracket spot sensibly. ✅
- **"Energy 50% correction from May highs"** (co-host): XLE only -10.7% off May high. ⚠️ retracement-speak, not a 50% decline — flag in report.
- **CEG named bullish in AI-power chain**: CEG -28.7% YTD, -38.9% off highs, rs_pct 0.28. ⚠️ contrarian or stale — highlight in company map.
- **Parker: energy at generational correlation low vs tech**: XLE–SMH daily-return corr **-0.273 (6M)**, **-0.143 (12M)** vs **+0.101 (2024)**. ✅ emphatic — currently *negatively* correlated. Core diversification thesis checks out.
- **MU "4-5x peak / 10x normalized earnings"**: earnings-multiple claim, not checkable from bars. Agent B: partially confirmed (single-digit fwd P/E per some vintages). MU +243% YTD, rs_pct_63d 0.995 but 27d 0.275 → huge run, cooling momentum — context for the report.
