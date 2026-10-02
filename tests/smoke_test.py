#!/usr/bin/env python3
"""
Smoke test: fill every template with fictional sample data, build PDFs, and
check the output. Run from the repo root:  python3 tests/smoke_test.py
Exits non-zero on failure. Needs one PDF renderer (Chrome/Chromium, WeasyPrint
or Playwright).
"""
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "skills" / "made-for-you-cv" / "scripts"
TESTS = Path(__file__).resolve().parent
failures = []


def run(*args):
    return subprocess.run([sys.executable, *map(str, args)], capture_output=True, text=True)


def check(cond, msg):
    print(("  ok   " if cond else "  FAIL ") + msg)
    if not cond:
        failures.append(msg)


with tempfile.TemporaryDirectory() as tmp:
    tmp = Path(tmp)
    cv = json.loads((TESTS / "sample_cv.json").read_text())

    jobs = [(t, TESTS / "sample_cv.json", 2) for t in ("minimal", "two-column", "designer-accent")]
    jobs.append(("cover-letter", TESTS / "sample_cover_letter.json", 1))

    for tpl, data, max_pages in jobs:
        print(f"\n[{tpl}]")
        html_out, pdf_out, txt_out = tmp / f"{tpl}.html", tmp / f"{tpl}.pdf", tmp / f"{tpl}.txt"
        r = run(SCRIPTS / "fill_template.py", tpl, data, html_out)
        check(r.returncode == 0, "fill_template succeeds " + r.stderr.strip())
        if r.returncode:
            continue
        html = html_out.read_text()
        check("{{" not in html and "<!--IF" not in html, "no leftover tokens or markers")
        r = run(SCRIPTS / "build_cv.py", html_out, pdf_out)
        check(r.returncode == 0, "build_cv produces a PDF " + r.stderr.strip()[-200:])
        if r.returncode == 0:
            m = re.search(r"Page count: (\d+)", r.stdout)
            check(bool(m) and int(m.group(1)) <= max_pages, f"page count {m.group(1) if m else '?'} <= {max_pages}")
        r = run(SCRIPTS / "html_to_text.py", html_out, txt_out)
        txt = txt_out.read_text() if txt_out.exists() else ""
        check("Jane Doe" in txt, "plain-text export contains the name")

    print("\n[optional fields]")
    slim = {k: v for k, v in cv.items() if k not in ("PHONE", "PORTFOLIO", "GITHUB", "PROJECTS_BLOCK", "LANGUAGES_BLOCK")}
    (tmp / "slim.json").write_text(json.dumps(slim))
    r = run(SCRIPTS / "fill_template.py", "minimal", tmp / "slim.json", tmp / "slim.html")
    html = (tmp / "slim.html").read_text()
    check(r.returncode == 0, "fill with optional fields missing")
    check("Selected Projects" not in html and "Languages" not in html, "empty sections removed")
    check("+46" not in html and "janedoe.dev" not in html, "empty contact items removed")
    check(not re.search(r'class="sep">·</span>\s*</div>', html), "no trailing separator")

    print("\n[guards]")
    (tmp / "bad.json").write_text(json.dumps({"NAME": "X"}))
    r = run(SCRIPTS / "fill_template.py", "minimal", tmp / "bad.json", tmp / "bad.html")
    check(r.returncode != 0, "missing required fields rejected")
    (tmp / "raw.html").write_text("<html>{{NAME}}</html>")
    r = run(SCRIPTS / "build_cv.py", tmp / "raw.html", tmp / "raw.pdf")
    check(r.returncode != 0, "build refuses unfilled placeholders")

print()
if failures:
    print(f"{len(failures)} check(s) failed")
    sys.exit(1)
print("All checks passed")
