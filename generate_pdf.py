"""
Convert PROJECT_REPORT_AR.md to a print-ready PDF with proper Arabic RTL rendering.
Uses markdown -> HTML -> Playwright (Chromium) -> PDF.
"""
import markdown
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).parent
MD_FILE  = ROOT / "PROJECT_REPORT_AR.md"
HTML_FILE = ROOT / "PROJECT_REPORT_AR.html"
PDF_FILE  = ROOT / "PROJECT_REPORT_AR.pdf"

# ── Convert Markdown → HTML body ─────────────────────────────────
md_text = MD_FILE.read_text(encoding="utf-8")
html_body = markdown.markdown(
    md_text,
    extensions=["tables", "fenced_code", "toc", "sane_lists", "attr_list"],
)

# ── Wrap in a print-ready HTML template ──────────────────────────
HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="UTF-8">
<title>تقرير المشروع الشامل - AI Labor Market Simulation</title>
<link href="https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;600;700;900&family=Amiri:wght@400;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
  /* ─── Reset & Base ─── */
  * { box-sizing: border-box; }
  html, body {
    margin: 0; padding: 0;
    font-family: 'Cairo', 'Segoe UI', Tahoma, sans-serif;
    font-size: 11pt;
    line-height: 1.75;
    color: #1a202c;
    background: #fff;
    direction: rtl;
    text-align: right;
  }
  body {
    padding: 0 32px;
    max-width: 100%;
  }

  /* ─── Cover Page Feel ─── */
  h1:first-of-type {
    margin-top: 24px;
    padding-bottom: 18px;
    font-size: 28pt;
    text-align: center;
    border-bottom: 4px double #1a365d;
    color: #1a365d;
    page-break-after: avoid;
  }
  h1:first-of-type + h1 {
    margin-top: 4px;
    padding-bottom: 24px;
    font-size: 18pt;
    text-align: center;
    color: #2c5282;
    border: none;
    font-weight: 600;
  }

  /* ─── Headings ─── */
  h1, h2, h3, h4 {
    font-family: 'Cairo', sans-serif;
    font-weight: 700;
    color: #1a365d;
    page-break-after: avoid;
  }
  h1 {
    font-size: 22pt;
    margin: 38px 0 18px;
    padding-bottom: 10px;
    border-bottom: 3px solid #2c5282;
  }
  h2 {
    font-size: 17pt;
    margin: 32px 0 14px;
    padding: 10px 16px;
    background: linear-gradient(90deg, #ebf4ff 0%, transparent 100%);
    border-right: 5px solid #2c5282;
    color: #2a4365;
  }
  h3 {
    font-size: 14pt;
    margin: 24px 0 10px;
    color: #2b6cb0;
  }
  h4 {
    font-size: 12pt;
    margin: 18px 0 8px;
    color: #2c5282;
  }

  /* ─── Paragraphs ─── */
  p {
    margin: 10px 0;
    text-align: justify;
    text-justify: inter-word;
  }

  /* ─── Strong & Emphasis ─── */
  strong { color: #1a365d; font-weight: 700; }
  em { color: #2b6cb0; }

  /* ─── Lists ─── */
  ul, ol {
    margin: 10px 0;
    padding-right: 28px;
  }
  li {
    margin: 6px 0;
    line-height: 1.7;
  }

  /* ─── Tables ─── */
  table {
    width: 100%;
    border-collapse: collapse;
    margin: 18px 0;
    font-size: 10.5pt;
    page-break-inside: avoid;
    box-shadow: 0 2px 4px rgba(0,0,0,0.04);
  }
  thead {
    background: linear-gradient(135deg, #2c5282 0%, #2a4365 100%);
    color: #fff;
  }
  th {
    padding: 11px 12px;
    text-align: right;
    font-weight: 700;
    font-size: 10.5pt;
    border: 1px solid #1a365d;
  }
  td {
    padding: 10px 12px;
    border: 1px solid #cbd5e0;
    background: #fff;
    vertical-align: top;
  }
  tbody tr:nth-child(even) td {
    background: #f7fafc;
  }
  tbody tr:hover td {
    background: #ebf4ff;
  }

  /* ─── Code Blocks ─── */
  pre {
    font-family: 'JetBrains Mono', 'Consolas', monospace;
    background: #1a202c;
    color: #e2e8f0;
    padding: 14px 18px;
    border-radius: 6px;
    overflow-x: auto;
    font-size: 9.5pt;
    line-height: 1.55;
    direction: ltr;
    text-align: left;
    page-break-inside: avoid;
    margin: 12px 0;
    border-right: 4px solid #4299e1;
  }
  pre code {
    background: transparent;
    color: inherit;
    padding: 0;
    border: none;
  }
  code {
    font-family: 'JetBrains Mono', 'Consolas', monospace;
    background: #edf2f7;
    color: #c53030;
    padding: 2px 7px;
    border-radius: 4px;
    font-size: 0.92em;
    direction: ltr;
    display: inline-block;
  }

  /* ─── Horizontal Rules ─── */
  hr {
    border: none;
    border-top: 2px solid #cbd5e0;
    margin: 28px 0;
  }

  /* ─── Blockquotes ─── */
  blockquote {
    margin: 16px 0;
    padding: 12px 20px;
    background: #fffaf0;
    border-right: 4px solid #d69e2e;
    color: #744210;
    font-style: italic;
    border-radius: 4px;
  }
  blockquote p { margin: 4px 0; }

  /* ─── Links ─── */
  a {
    color: #2b6cb0;
    text-decoration: none;
  }
  a:hover { text-decoration: underline; }

  /* ─── Special Icons in Lists (✓ ⚠ 🎯) ─── */
  /* Already handled by font emoji rendering */

  /* ─── Page Breaks for Print ─── */
  @media print {
    body { padding: 0 18px; }
    h1 { page-break-before: auto; }
    h1:first-of-type { page-break-before: avoid; }
    table, pre, blockquote { page-break-inside: avoid; }
    h2, h3, h4 { page-break-after: avoid; }
  }

  /* ─── Page Numbering Footer (handled by playwright) ─── */
</style>
</head>
<body>
{BODY}
</body>
</html>
"""

html_full = HTML_TEMPLATE.replace("{BODY}", html_body)
HTML_FILE.write_text(html_full, encoding="utf-8")
print(f"[1/2] HTML written: {HTML_FILE}")

# ── Convert HTML → PDF via Playwright ────────────────────────────
with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto(HTML_FILE.as_uri(), wait_until="networkidle")

    # A4, professional margins, with page numbers in footer
    page.pdf(
        path=str(PDF_FILE),
        format="A4",
        print_background=True,
        margin={
            "top":    "20mm",
            "bottom": "22mm",
            "left":   "15mm",
            "right":  "15mm",
        },
        display_header_footer=True,
        header_template="""
          <div style="font-size:9px; width:100%; padding:0 15mm; color:#4a5568;
                      direction:rtl; text-align:left; font-family:sans-serif;">
            <span>AI Labor Market Simulation — Project Report</span>
          </div>
        """,
        footer_template="""
          <div style="font-size:9px; width:100%; padding:0 15mm; color:#4a5568;
                      display:flex; justify-content:space-between; font-family:sans-serif;">
            <span>تقرير المشروع الشامل</span>
            <span>صفحة <span class="pageNumber"></span> من <span class="totalPages"></span></span>
          </div>
        """,
    )
    browser.close()

size_kb = PDF_FILE.stat().st_size / 1024
print(f"[2/2] PDF written: {PDF_FILE}  ({size_kb:.1f} KB)")
