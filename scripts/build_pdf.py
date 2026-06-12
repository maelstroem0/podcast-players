#!/usr/bin/env python3
"""
Build Apex Quantix-branded PDF from a podcast analysis markdown file.

Pipeline: markdown -> pandoc (HTML fragment, raw HTML blocks pass through)
          -> wrap with brand header (embedded logo) -> WeasyPrint -> pdfs/<slug>.pdf

Usage:
    python scripts/build_pdf.py analyses/YYYYMMDD_slug.md
    python scripts/build_pdf.py YYYYMMDD_slug            # slug shorthand

Requires: pandoc on PATH, weasyprint in env, pango via
    DYLD_LIBRARY_PATH=/opt/homebrew/lib (handled internally on macOS).
"""

import base64
import os
import subprocess
import sys
from datetime import date
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
ROOT_DIR = SCRIPT_DIR.parent
STYLES = ROOT_DIR / "styles"
CSS_PATH = STYLES / "apex_quantix_report.css"
LOGO_PATH = STYLES / "assets" / "logo_black.png"
PDFS_DIR = ROOT_DIR / "pdfs"
TMP_DIR = ROOT_DIR / "tmp"

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<style>{css}</style>
</head>
<body>
<div class="aq-header">
  {logo_img}
  <div class="kicker">Podcast Intelligence<span class="date">{build_date}</span></div>
</div>
{body}
<div class="doc-footer">Apex Quantix &middot; Internal research &middot; Not investment advice &middot; Generated {build_date}</div>
</body>
</html>
"""


def resolve_md(arg: str) -> Path:
    p = Path(arg)
    if p.exists():
        return p
    candidate = ROOT_DIR / "analyses" / f"{arg}.md"
    if candidate.exists():
        return candidate
    raise FileNotFoundError(f"Cannot resolve markdown source: {arg}")


def build(md_arg: str) -> Path:
    md_path = resolve_md(md_arg)
    slug = md_path.stem
    TMP_DIR.mkdir(exist_ok=True)
    PDFS_DIR.mkdir(exist_ok=True)

    # 1) pandoc: markdown -> HTML fragment (raw HTML divs pass through)
    body = subprocess.run(
        ["pandoc", str(md_path), "-f", "markdown", "-t", "html"],
        capture_output=True, text=True, check=True,
    ).stdout

    # 2) wrap with brand header + embedded logo
    logo_img = ""
    if LOGO_PATH.exists():
        b64 = base64.b64encode(LOGO_PATH.read_bytes()).decode()
        logo_img = f'<img class="logo" src="data:image/png;base64,{b64}">'
    html = HTML_TEMPLATE.format(
        css=CSS_PATH.read_text(),
        logo_img=logo_img,
        body=body,
        build_date=date.today().isoformat(),
    )
    tmp_html = TMP_DIR / f"{slug}_aq.html"
    tmp_html.write_text(html, encoding="utf-8")

    # 3) WeasyPrint -> PDF (pango lib path for macOS/homebrew)
    env = dict(os.environ, DYLD_LIBRARY_PATH="/opt/homebrew/lib")
    out_pdf = PDFS_DIR / f"{slug}.pdf"
    subprocess.run(
        ["weasyprint", "--base-url", str(ROOT_DIR), str(tmp_html), str(out_pdf)],
        check=True, env=env,
    )
    print(f"✓ PDF built: {out_pdf}")
    return out_pdf


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    build(sys.argv[1])
