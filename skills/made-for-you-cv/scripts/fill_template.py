#!/usr/bin/env python3
"""
fill_template.py — Populate a CV / cover-letter template from a JSON file.

Usage:
    fill_template.py <template.html|template-name> <data.json> <output.html>

<template> is a path or a bare template name (minimal, two-column,
designer-accent, cover-letter) resolved against ../assets/templates.

The JSON file maps token names (without braces) to values. Example:

    {
      "NAME": "Jane Doe",
      "TITLE": "Frontend Developer",
      "EMAIL": "jane@example.com",
      "PORTFOLIO": "janedoe.dev",
      "SUMMARY": "Frontend developer with ...",
      "EXPERIENCE_BLOCK": "<div class=\\"entry\\">...</div>"
    }

What it does for you:
  - Plain-text fields (NAME, TITLE, LOCATION, EMAIL, PHONE, *_DISPLAY, URLs,
    DATE, SALUTATION, CLOSING) are HTML-escaped. Block fields (*_BLOCK, BODY)
    are inserted as raw HTML. SUMMARY is raw HTML if it contains a tag,
    otherwise it is escaped and wrapped in <p>.
  - URL fields get https:// added if missing; *_DISPLAY is derived from the URL
    when you don't supply it (janedoe.dev, linkedin.com/in/jane-doe).
  - Optional items (<!--IF:TOKEN-->...<!--/IF:TOKEN-->) are removed when that
    token is empty or missing, including their separators, so there are no
    empty headings or stray "·" characters.
  - Fails (exit 1) if a required field is missing or any {{TOKEN}} is left over.

Standard library only.
"""

import html
import json
import re
import sys
from pathlib import Path

TEMPLATE_DIR = Path(__file__).resolve().parent.parent / "assets" / "templates"

REQUIRED = {
    "cv": ["NAME", "TITLE", "EMAIL", "SUMMARY", "EXPERIENCE_BLOCK"],
    "cover-letter": ["NAME", "EMAIL", "DATE", "SALUTATION", "BODY", "CLOSING"],
}

URL_FIELDS = ["PORTFOLIO", "GITHUB", "LINKEDIN"]
RAW_HTML_FIELDS_SUFFIX = ("_BLOCK",)
RAW_HTML_FIELDS = {"BODY"}
DEFAULTS = {"LANG": "en"}

SEP_RE = r'(?:<span class="sep">[^<]*</span>\s*)'


def display_url(url):
    """janedoe.dev for https://www.janedoe.dev/ ; keeps path (linkedin.com/in/x)."""
    d = re.sub(r"^[a-z]+://", "", url.strip(), flags=re.I)
    d = re.sub(r"^www\.", "", d, flags=re.I)
    return d.rstrip("/")


def normalize(data):
    out = {}
    for k, v in data.items():
        if v is None:
            v = ""
        if not isinstance(v, str):
            v = str(v)
        out[k] = v.strip()
    for k, v in DEFAULTS.items():
        out.setdefault(k, v)
    for f in URL_FIELDS:
        url = out.get(f, "")
        if url and not re.match(r"^[a-z]+://", url, re.I):
            url = "https://" + url
        out[f] = url
        if url and not out.get(f + "_DISPLAY"):
            out[f + "_DISPLAY"] = display_url(url)
    return out


def render_value(key, value):
    if key == "RECIPIENT_BLOCK":
        if "<" in value:
            return value
        return "<br>".join(html.escape(l.strip(), quote=False) for l in value.splitlines())
    if key in RAW_HTML_FIELDS or key.endswith(RAW_HTML_FIELDS_SUFFIX):
        return value
    if key == "SUMMARY":
        if "<" in value:
            return value
        return f"<p>{html.escape(value, quote=False)}</p>"
    return html.escape(value, quote=True)


def strip_empty_ifs(text, data):
    """Remove <!--IF:X-->...<!--/IF:X--> blocks whose token is empty; unwrap the rest."""
    def repl(m):
        tok, body = m.group(1), m.group(2)
        return body if data.get(tok, "").strip() else ""

    # Non-greedy, same-token pairing; run to a fixpoint for any nesting.
    pat = re.compile(r"<!--IF:([A-Z_]+)-->(.*?)<!--/IF:\1-->", re.S)
    prev = None
    while prev != text:
        prev = text
        text = pat.sub(repl, text)
    return text


def tidy_contact(text):
    """Drop the trailing separator left at the end of the contact line."""
    def fix(m):
        inner = m.group(1)
        inner = re.sub(SEP_RE + r"\s*$", "", inner.rstrip())
        return inner.strip()

    return re.sub(r"<!--CONTACT-->(.*?)<!--/CONTACT-->", fix, text, flags=re.S)


def fill(template_path, data):
    text = Path(template_path).read_text(encoding="utf-8")
    kind = "cover-letter" if "{{BODY}}" in text else "cv"
    data = normalize(data)

    missing = [k for k in REQUIRED[kind] if not data.get(k)]
    if missing:
        raise ValueError("Missing required field(s): " + ", ".join(missing))

    # Two-column CVs keep skills/languages in the sidebar. Accept the common names too.
    if "SIDEBAR_SKILLS_BLOCK" in text:
        data.setdefault("SIDEBAR_SKILLS_BLOCK", data.get("SKILLS_BLOCK", ""))
        data.setdefault("SIDEBAR_LANGUAGES_BLOCK", data.get("LANGUAGES_BLOCK", ""))

    text = strip_empty_ifs(text, data)
    text = tidy_contact(text)

    def sub(m):
        key = m.group(1)
        return render_value(key, data.get(key, ""))

    text = re.sub(r"\{\{([A-Z_]+)\}\}", sub, text)
    text = re.sub(r"<!--/?(?:IF:[A-Z_]+|CONTACT)-->", "", text)
    return text, kind


def main():
    if len(sys.argv) != 4:
        print("Usage: fill_template.py <template.html|name> <data.json> <output.html>", file=sys.stderr)
        sys.exit(1)

    template = Path(sys.argv[1])
    if not template.exists():
        candidate = TEMPLATE_DIR / (sys.argv[1] if sys.argv[1].endswith(".html") else sys.argv[1] + ".html")
        if candidate.exists():
            template = candidate
        else:
            avail = ", ".join(sorted(p.stem for p in TEMPLATE_DIR.glob("*.html")))
            print(f"❌ Template not found: {sys.argv[1]} (available: {avail})", file=sys.stderr)
            sys.exit(1)

    try:
        data = json.loads(Path(sys.argv[2]).read_text(encoding="utf-8"))
    except Exception as e:
        print(f"❌ Could not read JSON {sys.argv[2]}: {e}", file=sys.stderr)
        sys.exit(1)

    try:
        text, kind = fill(template, data)
    except ValueError as e:
        print(f"❌ {e}", file=sys.stderr)
        sys.exit(1)

    leftover = sorted(set(re.findall(r"\{\{[A-Z_]+\}\}", text)))
    if leftover:
        print(f"❌ Unfilled tokens remain: {', '.join(leftover)}", file=sys.stderr)
        sys.exit(1)

    out = Path(sys.argv[3])
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(text, encoding="utf-8")
    print(f"✅ Filled {template.name} ({kind}) → {out}")


if __name__ == "__main__":
    main()
