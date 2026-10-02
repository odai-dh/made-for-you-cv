#!/usr/bin/env python3
"""
build_cv.py — Convert a populated CV HTML file to a print-ready PDF.

Usage:
    build_cv.py <input.html> <output.pdf>

Renderer order:
    1. Headless Chrome / Chromium / Edge / Brave. Found via $CHROME_PATH, common
       install locations (macOS, Linux, Windows), PATH, and Playwright's browser
       cache ($PLAYWRIGHT_BROWSERS_PATH, ~/.cache/ms-playwright, /opt/pw-browsers).
    2. WeasyPrint (pip install weasyprint)
    3. Playwright (pip install playwright && playwright install chromium)

Chrome is launched with --no-sandbox automatically when running as root (cloud
containers, Docker), where it otherwise refuses to start.

Refuses to build if the HTML still contains {{TOKEN}} placeholders.
Exits non-zero on any failure with a clear message.
"""

import glob
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


CHROME_PATHS = [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser",
    "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
    "/usr/bin/google-chrome",
    "/usr/bin/google-chrome-stable",
    "/usr/bin/chromium",
    "/usr/bin/chromium-browser",
    "/snap/bin/chromium",
    "/usr/bin/microsoft-edge",
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
]

CHROME_COMMANDS = (
    "google-chrome", "google-chrome-stable", "chromium", "chromium-browser",
    "chrome", "microsoft-edge", "msedge",
)

PLAYWRIGHT_CACHE_DIRS = [
    os.environ.get("PLAYWRIGHT_BROWSERS_PATH", ""),
    "/opt/pw-browsers",
    str(Path.home() / ".cache" / "ms-playwright"),
    str(Path.home() / "Library" / "Caches" / "ms-playwright"),
    str(Path.home() / "AppData" / "Local" / "ms-playwright"),
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
            browser = p.chromium.launch(args=["--no-sandbox"] if _is_root() else [])
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
    """Locate a Chrome/Chromium binary, or None."""
    env = os.environ.get("CHROME_PATH")
    if env and Path(env).exists():
        return env
    for path in CHROME_PATHS:
        if Path(path).exists():
            return path
    for cmd in CHROME_COMMANDS:
        found = shutil.which(cmd)
        if found:
            return found
    # Playwright's browser cache (full chromium first, then the headless shell).
    for base in PLAYWRIGHT_CACHE_DIRS:
        if not base:
            continue
        patterns = [
            "chromium-*/chrome-linux*/chrome",
            "chromium-*/chrome-mac*/Chromium.app/Contents/MacOS/Chromium",
            "chromium-*/chrome-win*/chrome.exe",
            "chromium_headless_shell-*/chrome-linux*/headless_shell",
            "chromium_headless_shell-*/chrome-linux*/chrome",
        ]
        for pat in patterns:
            hits = sorted(glob.glob(os.path.join(base, pat)), reverse=True)
            for hit in hits:
                if os.access(hit, os.X_OK):
                    return hit
    return None


def _is_root():
    return hasattr(os, "geteuid") and os.geteuid() == 0


def try_chrome(input_html, output_pdf):
    """Try rendering with headless Chrome. Returns True on success."""
    chrome = find_chrome()
    if not chrome:
        return False
    input_url = Path(input_html).resolve().as_uri()
    output_abs = str(Path(output_pdf).resolve())

    base = [chrome, "--disable-gpu", "--hide-scrollbars", "--no-first-run"]
    if _is_root() or os.environ.get("CHROME_NO_SANDBOX"):
        base += ["--no-sandbox", "--disable-dev-shm-usage"]

    # Newer Chrome uses --no-pdf-header-footer; older used --print-to-pdf-no-header.
    attempts = [
        ["--headless=new", "--no-pdf-header-footer"],
        ["--headless", "--no-pdf-header-footer"],
        ["--headless", "--print-to-pdf-no-header"],
    ]
    with tempfile.TemporaryDirectory(prefix="cv-chrome-") as profile:
        for flags in attempts:
            cmd = base + flags + [
                f"--user-data-dir={profile}",
                f"--print-to-pdf={output_abs}",
                input_url,
            ]
            try:
                result = subprocess.run(cmd, capture_output=True, timeout=90)
            except Exception as e:
                print(f"  Chrome failed: {e}", file=sys.stderr)
                continue
            if result.returncode == 0 and Path(output_pdf).exists() and Path(output_pdf).stat().st_size > 0:
                return True
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

        count = len(re.findall(rb"/Type\s*/Page(?![a-zA-Z])", data))
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

    leftover = sorted(set(re.findall(r"\{\{[A-Z_]+\}\}", input_html.read_text(encoding="utf-8"))))
    if leftover:
        print(
            f"❌ Unfilled placeholders in {input_html.name}: {', '.join(leftover)}\n"
            "   Fill them (see scripts/fill_template.py) before building.",
            file=sys.stderr,
        )
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
        "    or install Google Chrome / Chromium (or set CHROME_PATH to its binary)\n",
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
