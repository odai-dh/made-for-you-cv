#!/usr/bin/env python3
"""
html_to_text.py — Convert a populated CV/cover-letter HTML file to clean plain text.

Usage:
    html_to_text.py <input.html> [output.txt]

Produces a pasteable plain-text version for ATS web forms, LinkedIn Easy Apply,
and email bodies that don't accept a PDF. If no output path is given, writes
alongside the input with a .txt extension.

Uses only the Python standard library (html.parser) — no dependencies.
"""

import sys
import re
from pathlib import Path
from html.parser import HTMLParser

# Tags whose content should be skipped entirely.
SKIP_CONTENT = {"style", "script", "head", "title"}

# Block-level tags that force a line break after their content.
BLOCK_TAGS = {
    "p", "div", "section", "header", "footer", "article",
    "h1", "h2", "h3", "h4", "h5", "h6",
    "ul", "ol", "tr", "table",
}


class TextExtractor(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts = []
        self._skip_depth = 0

    def handle_starttag(self, tag, attrs):
        if tag in SKIP_CONTENT:
            self._skip_depth += 1
        elif tag == "li":
            self.parts.append("\n- ")
        elif tag == "br":
            self.parts.append("\n")
        elif tag in BLOCK_TAGS:
            self.parts.append("\n")

    def handle_endtag(self, tag):
        if tag in SKIP_CONTENT and self._skip_depth > 0:
            self._skip_depth -= 1
        elif tag in BLOCK_TAGS:
            self.parts.append("\n")

    def handle_data(self, data):
        if self._skip_depth:
            return
        text = re.sub(r"\s+", " ", data)
        if text.strip():
            self.parts.append(text)
        elif self.parts and not self.parts[-1].endswith((" ", "\n", "- ")):
            self.parts.append(" ")

    def get_text(self):
        raw = "".join(self.parts)
        # Tidy " - " bullets that picked up a leading space.
        raw = raw.replace(" \n- ", "\n- ").replace("\n - ", "\n- ")
        # Collapse 3+ blank lines into a single blank line.
        raw = re.sub(r"\n[ \t]*\n[ \t]*\n+", "\n\n", raw)
        # Strip trailing spaces on each line.
        raw = "\n".join(line.rstrip() for line in raw.splitlines())
        return raw.strip() + "\n"


def convert(input_html, output_txt):
    input_html = Path(input_html)
    if not input_html.exists():
        print(f"❌ Input file not found: {input_html}", file=sys.stderr)
        return False

    parser = TextExtractor()
    parser.feed(input_html.read_text(encoding="utf-8"))
    text = parser.get_text()

    output_txt = Path(output_txt)
    output_txt.parent.mkdir(parents=True, exist_ok=True)
    output_txt.write_text(text, encoding="utf-8")
    print(f"✅ Plain text written: {output_txt} ({len(text.splitlines())} lines)")
    return True


def main():
    if len(sys.argv) not in (2, 3):
        print("Usage: html_to_text.py <input.html> [output.txt]", file=sys.stderr)
        sys.exit(1)

    input_html = Path(sys.argv[1])
    output_txt = sys.argv[2] if len(sys.argv) == 3 else str(input_html.with_suffix(".txt"))
    sys.exit(0 if convert(input_html, output_txt) else 1)


if __name__ == "__main__":
    main()
