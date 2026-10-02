# Changelog

## 0.2.0
- Add `fill_template.py`: fill templates from JSON (escaping, URL normalization, optional contact items and sections removed cleanly, required-field and leftover-token checks).
- Add `cover-letter` template so the cover letter really matches the CV header.
- `build_cv.py`: find Chrome/Chromium in more places (Playwright cache, Windows, snap, `CHROME_PATH`), add `--no-sandbox` when running as root (cloud/Docker), use a throwaway Chrome profile, refuse to build with leftover placeholders, fix page-count regex.
- `preview_cv.py`: PyMuPDF / pypdfium2 fallbacks when poppler is missing.
- Templates: fix two-column sidebar and spacing on page 2, designer-accent skills layout, unstyled `tech` line in minimal, page-break handling, print colours; `lang` attribute is now settable.
- SKILL.md: resolve script paths relative to the skill folder, use the new scripts, document JSON keys and block HTML.
- Add `/made-for-you-cv:cv` command, smoke test, CI, and marketplace metadata. Remove non-standard `displayName` from `plugin.json`.

## 0.1.0
- Initial release.
