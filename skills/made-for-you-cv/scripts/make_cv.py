#!/usr/bin/env python3
"""
make_cv.py: one call from tailored JSON to deliverables.

Usage:
    make_cv.py <data.json> --out <dir> --name <Basename> [--template minimal]
               [--docx] [--pages N] [--chrome <path>]

Does, in order: fill the template (fill_template.py), build the PDF with
--fit --fallback (build_cv.py), write the plain-text copy (html_to_text.py) and,
with --docx, the Word copy (build_docx.py). Files land in <dir> as
<Basename>.pdf / .txt / .docx. Use --template cover-letter (or a data file with
BODY) for a cover letter.

If no PDF engine is available the finished <Basename>.html and .txt are written
instead and the exit code is 2 (tell the user to open the HTML and use Print,
Save as PDF). Exit codes: 0 PDF built, 2 HTML + text fallback, 1 error.
"""

import json
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_cv
import build_docx
import fill_template
import html_to_text

TEMPLATE_DIR = fill_template.TEMPLATE_DIR


def parse_args(argv):
    opts = {"template": None, "out": None, "name": None, "docx": False, "pages": 1, "chrome": None}
    data = None
    i = 0
    while i < len(argv):
        a = argv[i]
        if a == "--docx":
            opts["docx"] = True
        elif a in ("--template", "--out", "--name", "--chrome", "--pages"):
            i += 1
            if i >= len(argv):
                raise SystemExit(f"{a} needs a value")
            opts[a[2:]] = int(argv[i]) if a == "--pages" else argv[i]
        elif a.startswith("--"):
            raise SystemExit(f"Unknown option {a}")
        elif data is None:
            data = a
        else:
            raise SystemExit("Only one data file is expected")
        i += 1
    if not data or not opts["out"] or not opts["name"]:
        raise SystemExit(__doc__)
    return data, opts


def main():
    data_path, o = parse_args(sys.argv[1:])
    try:
        data = json.loads(Path(data_path).read_text(encoding="utf-8"))
    except Exception as e:
        print(f"❌ Could not read JSON {data_path}: {e}", file=sys.stderr)
        sys.exit(1)

    template = o["template"] or ("cover-letter" if "BODY" in data else "minimal")
    tpl = TEMPLATE_DIR / f"{template}.html"
    if not tpl.exists():
        avail = ", ".join(sorted(p.stem for p in TEMPLATE_DIR.glob("*.html")))
        print(f"❌ Template not found: {template} (available: {avail})", file=sys.stderr)
        sys.exit(1)

    out = Path(o["out"])
    out.mkdir(parents=True, exist_ok=True)
    pdf = out / f"{o['name']}.pdf"

    try:
        html, kind = fill_template.fill(tpl, data)
    except ValueError as e:
        print(f"❌ {e}", file=sys.stderr)
        sys.exit(1)

    with tempfile.TemporaryDirectory(prefix="cv-make-") as tmp:
        work = Path(tmp) / f"{o['name']}.html"
        work.write_text(html, encoding="utf-8")
        code = build_cv.build_or_fallback(work, pdf, o["chrome"], o["pages"])
        if code == 1:
            sys.exit(1)
        if code == 0:
            html_to_text.convert(work, out / f"{o['name']}.txt")
        # code == 2: write_fallback already left .html and .txt next to the PDF path.

    if o["docx"]:
        build_docx.build(data, out / f"{o['name']}.docx")

    produced = sorted(p.name for p in out.glob(f"{o['name']}.*"))
    print(f"\nDelivered in {out}: {', '.join(produced)}")
    sys.exit(code)


if __name__ == "__main__":
    main()
