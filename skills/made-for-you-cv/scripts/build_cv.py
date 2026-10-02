#!/usr/bin/env python3
"""
build_cv.py — Convert a populated CV HTML file to a print-ready PDF.

Usage:
    build_cv.py <input.html> <output.pdf>

Prerequisites:
    Tries WeasyPrint first (pip install weasyprint).
    Falls back to headless Chrome / Chromium if WeasyPrint is unavailable.
    Falls back to Playwright if installed.

Designed to run on macOS where Google Chrome is typically pre-installed at:
    /Applications/Google Chrome.app/Contents/MacOS/Google Chrome

Exits non-zero on any failure with a clear message.
"""

import sys
import os
import shutil
import subprocess
from pathlib import Path


CHROME_PATHS = [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser",
    "/usr/bin/google-chrome",
    "/usr/bin/chromium",
    "/usr/bin/chromium-browser",
]


def try_weasyprint(input_html, output_pdf):
    """Try rendering with WeasyPrint. Returns True on success."""
    try:
        from weasyprint import HTML
    except ImportError:
        return False
    try:
        HTML(filename=str(input_html)).write_pdf(str(output_pdf))
        return True
    except Exception as e:
        print(f"  WeasyPrint failed: {e}", file=sys.stderr)
        return False


def try_playwright(input_html, output_pdf):
    """Try rendering with Playwright (Chromium). Returns True on success."""
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        return False
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.goto(f"file://{Path(input_html).resolve()}")
            page.pdf(
                path=str(output_pdf),
                format="A4",
                print_background=True,
                margin={"top": "0", "bottom": "0", "left": "0", "right": "0"},
            )
            browser.close()
        return True
    except Exception as e:
        print(f"  Playwright failed: {e}", file=sys.stderr)
        return False


def find_chrome():
    """Locate a Chrome/Chromium binary."""
    for path in CHROME_PATHS:
        if Path(path).exists():
            return path
    for cmd in ("google-chrome", "chromium", "chromium-browser"):
        found = shutil.which(cmd)
        if found:
            return found
    return None


def try_chrome(input_html, output_pdf):
    """Try rendering with headless Chrome. Returns True on success."""
    chrome = find_chrome()
    if not chrome:
        return False
    input_url = f"file://{Path(input_html).resolve()}"
    output_abs = str(Path(output_pdf).resolve())
    cmd = [
        chrome,
        "--headless=new",
        "--disable-gpu",
        "--no-pdf-header-footer",
        f"--print-to-pdf={output_abs}",
        "--no-margins",
        input_url,
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, timeout=60)
        if result.returncode == 0 and Path(output_pdf).exists():
            return True
        # Some Chrome versions don't support --no-pdf-header-footer; retry without it
        cmd_fallback = [c for c in cmd if c not in ("--no-pdf-header-footer", "--no-margins")]
        result = subprocess.run(cmd_fallback, capture_output=True, timeout=60)
        return result.returncode == 0 and Path(output_pdf).exists()
    except Exception as e:
        print(f"  Chrome failed: {e}", file=sys.stderr)
        return False


def count_pages(output_pdf):
    """Return the PDF page count, or None if it can't be determined.

    Tries pdfinfo (poppler) first, then a dependency-free byte scan.
    """
    output_pdf = Path(output_pdf)
    pdfinfo = shutil.which("pdfinfo")
    if pdfinfo:
        try:
            result = subprocess.run(
                [pdfinfo, str(output_pdf)], capture_output=True, text=True, timeout=30
            )
            for line in result.stdout.splitlines():
                if line.startswith("Pages:"):
                    return int(line.split(":", 1)[1].strip())
        except Exception:
            pass
    # Fallback: count page objects in the raw PDF bytes.
    try:
        data = output_pdf.read_bytes()
        import re

        count = len(re.findall(rb"/Type\s*/Page[^s]", data))
        return count or None
    except Exception:
        return None


def report_page_count(output_pdf):
    """Print the page count and warn if the CV runs long."""
    n = count_pages(output_pdf)
    if n is None:
        print("  Page count: could not determine")
        return
    print(f"  Page count: {n}")
    if n >= 3:
        print(
            f"⚠️  {n} pages — a CV should be 1 (preferred) or 2 at most. "
            "Trim content (cut, don't compress) and rebuild.",
            file=sys.stderr,
        )
    elif n == 2:
        print("  (2 pages — acceptable, but 1 is preferred for entry/mid level.)")


def build_cv(input_html, output_pdf):
    input_html = Path(input_html)
    output_pdf = Path(output_pdf)

    if not input_html.exists():
        print(f"❌ Input file not found: {input_html}", file=sys.stderr)
        return False

    output_pdf.parent.mkdir(parents=True, exist_ok=True)

    print(f"Building PDF: {input_html.name} → {output_pdf.name}")

    # Chrome first: reliably present on macOS and avoids WeasyPrint's noisy
    # native-lib import warnings when its system deps aren't installed.
    print("  Trying headless Chrome...")
    if try_chrome(input_html, output_pdf):
        print(f"✅ Rendered with Chrome: {output_pdf}")
        report_page_count(output_pdf)
        return True

    print("  Trying WeasyPrint...")
    if try_weasyprint(input_html, output_pdf):
        print(f"✅ Rendered with WeasyPrint: {output_pdf}")
        report_page_count(output_pdf)
        return True

    print("  Trying Playwright...")
    if try_playwright(input_html, output_pdf):
        print(f"✅ Rendered with Playwright: {output_pdf}")
        report_page_count(output_pdf)
        return True

    print(
        "\n❌ No PDF renderer available. Install one of:\n"
        "    pip install weasyprint\n"
        "    pip install playwright && playwright install chromium\n"
        "    or install Google Chrome\n",
        file=sys.stderr,
    )
    return False


def main():
    if len(sys.argv) != 3:
        print("Usage: build_cv.py <input.html> <output.pdf>", file=sys.stderr)
        sys.exit(1)

    success = build_cv(sys.argv[1], sys.argv[2])
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
