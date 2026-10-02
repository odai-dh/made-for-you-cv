#!/usr/bin/env python3
"""
preview_cv.py — Render a PDF's pages to PNG images for visual verification.

Usage:
    preview_cv.py <input.pdf> [output_prefix]

Produces one PNG per page (e.g. <prefix>-1.png, <prefix>-2.png). If no prefix
is given, images are written next to the PDF using its stem.

The skill uses this in step 8: render the built CV to PNG, then actually look
at the image to catch overflow, broken layout, and awkward page breaks that an
HTML-only check cannot see.

Renderer order:
    pdftoppm (poppler) — all pages, high fidelity. Preferred.
    PyMuPDF (pip install pymupdf) or pypdfium2 — all pages, pure pip.
    sips (macOS builtin) — first page only. Last resort.

Exits non-zero with a clear message if neither is available.
"""

import sys
import shutil
import subprocess
from pathlib import Path


def render_with_pdftoppm(input_pdf, prefix, dpi=150):
    """Render all pages with pdftoppm. Returns list of PNG paths or None."""
    pdftoppm = shutil.which("pdftoppm")
    if not pdftoppm:
        return None
    try:
        # pdftoppm appends -<page>.png to the prefix automatically.
        subprocess.run(
            [pdftoppm, "-png", "-r", str(dpi), str(input_pdf), str(prefix)],
            capture_output=True,
            check=True,
            timeout=120,
        )
    except Exception as e:
        print(f"  pdftoppm failed: {e}", file=sys.stderr)
        return None
    pngs = sorted(prefix.parent.glob(f"{prefix.name}-*.png"))
    return pngs or None


def render_with_python(input_pdf, prefix, dpi=150):
    """Render all pages with PyMuPDF or pypdfium2 if installed."""
    try:
        import fitz  # PyMuPDF

        doc = fitz.open(str(input_pdf))
        out = []
        for i, page in enumerate(doc, start=1):
            path = prefix.parent / f"{prefix.name}-{i}.png"
            page.get_pixmap(dpi=dpi).save(str(path))
            out.append(path)
        return out or None
    except ImportError:
        pass
    except Exception as e:
        print(f"  PyMuPDF failed: {e}", file=sys.stderr)
    try:
        import pypdfium2 as pdfium

        pdf = pdfium.PdfDocument(str(input_pdf))
        out = []
        for i in range(len(pdf)):
            path = prefix.parent / f"{prefix.name}-{i + 1}.png"
            pdf[i].render(scale=dpi / 72).to_pil().save(str(path))
            out.append(path)
        return out or None
    except ImportError:
        return None
    except Exception as e:
        print(f"  pypdfium2 failed: {e}", file=sys.stderr)
        return None


def render_with_sips(input_pdf, prefix):
    """Render the first page with sips (macOS). Returns list with one PNG or None."""
    sips = shutil.which("sips")
    if not sips:
        return None
    out = prefix.parent / f"{prefix.name}-1.png"
    try:
        subprocess.run(
            [sips, "-s", "format", "png", str(input_pdf), "--out", str(out)],
            capture_output=True,
            check=True,
            timeout=60,
        )
    except Exception as e:
        print(f"  sips failed: {e}", file=sys.stderr)
        return None
    if out.exists():
        print(
            "  Note: sips renders only the first page. Install poppler "
            "(brew install poppler) for full multi-page previews.",
            file=sys.stderr,
        )
        return [out]
    return None


def preview(input_pdf, prefix):
    input_pdf = Path(input_pdf)
    if not input_pdf.exists():
        print(f"❌ Input PDF not found: {input_pdf}", file=sys.stderr)
        return None

    prefix = Path(prefix)
    prefix.parent.mkdir(parents=True, exist_ok=True)

    print(f"Rendering preview: {input_pdf.name}")
    pngs = render_with_pdftoppm(input_pdf, prefix)
    if not pngs:
        pngs = render_with_python(input_pdf, prefix)
    if not pngs:
        pngs = render_with_sips(input_pdf, prefix)

    if not pngs:
        print(
            "\n❌ No PDF-to-image renderer available. Install one of:\n"
            "    brew install poppler / apt install poppler-utils   (pdftoppm)\n"
            "    pip install pymupdf\n"
            "    (macOS sips is builtin but renders only page 1)\n",
            file=sys.stderr,
        )
        return None

    for p in pngs:
        print(f"✅ {p}")
    return pngs


def main():
    if len(sys.argv) not in (2, 3):
        print("Usage: preview_cv.py <input.pdf> [output_prefix]", file=sys.stderr)
        sys.exit(1)

    input_pdf = Path(sys.argv[1])
    if len(sys.argv) == 3:
        prefix = sys.argv[2]
    else:
        prefix = str(input_pdf.with_suffix(""))

    pngs = preview(input_pdf, prefix)
    sys.exit(0 if pngs else 1)


if __name__ == "__main__":
    main()
