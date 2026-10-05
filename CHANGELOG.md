# Changelog

## 0.4.0
Fixes two bugs from a side-by-side eval against plain Claude, makes runs leaner, and leans into what the plugin does that plain Claude cannot. Honesty, privacy and neutral-palette rules are unchanged.
- **Fix: section headings follow the CV's language.** All four templates use heading tokens. `LANG` (en, sv, da, nb, de, nl, fr) sets Profil/Erfarenhet/Utbildning/Kompetenser/Språk and so on, and any heading can be overridden. Cover-letter dates are written in the same language (5 oktober 2026, 5. Oktober 2026).
- **New: `SECTION_ORDER`** puts education and projects before experience for career switchers and recent graduates.
- **New: Word output.** `build_docx.py` makes a single-column .docx (standard headings, real bullets, no tables, text boxes, images or headers/footers) from the same JSON, for portals and recruitment systems. The skill delivers it when the ad points to a portal or ATS, or when asked. It installs python-docx once if missing and skips with a one-line note if it cannot.
- **New: `--fit`** in `build_cv.py` rebuilds an over-length CV with tighter spacing, margins and slightly smaller type (body text never below 9.5pt) and reports what it did, so the skill only cuts content when that is not enough.
- **Leaner skill.** SKILL.md is about half its previous size. Detail moved into `references/` (new `template_data.md`) and references load only when needed: the cover-letter guide only for a cover letter, the example only when unsure.
- **New: repeat-application fast path.** With a `master_cv.md` attached or already in the conversation, a new job ad goes straight to the tailored PDF with no questions (also in `/made-for-you-cv:cv`).
- Smoke test covers Swedish headings, `SECTION_ORDER`, the .docx, and `--fit`. New `tests/evals/` holds three fictional cases and their checks.

## 0.3.0
First-run activation. Honesty rules, templates and privacy behavior are unchanged.
- Skill description rewritten so it triggers on common phrasings (CV, resume, résumé, cover letter, job application, "apply for this job", "tailor my CV", "update my resume for this role", Swedish "personligt brev" and "anpassa mitt CV").
- New fast path: a first message with a CV and a job ad now produces the PDF in the same turn. The master CV is built silently, the template defaults to `minimal` (`designer-accent` for design-led roles) with no template question, and at most one short batch of blocking questions is asked. Gaps (`[TODO]` fields, missing numbers) are listed after the first PDF instead of before it.
- No dead ends: `build_cv.py --fallback` writes the finished HTML and a `.txt` (exit code 2) when no PDF engine is available, and SKILL.md tells the user to use Print, Save as PDF. Every script call in SKILL.md now uses an absolute `SKILL_DIR` path that works from any working directory.
- README starts with "Start in 10 seconds", example prompts (including Swedish) and a feedback link. `/made-for-you-cv:cv` handles the fast path and works with no arguments.
- `plugin.json`: description leads with the action; added a listing icon.
- Smoke test covers the no-PDF-engine fallback (simulated) and the frontmatter limits.

## 0.2.2
- `build_cv.py` no longer reads any environment variables. `CHROME_PATH`, `CHROME_NO_SANDBOX` and `PLAYWRIGHT_BROWSERS_PATH` are removed. Use the optional `--chrome <path>` argument to pick a browser binary; `--no-sandbox` is used only when running as root; Playwright's browser cache is searched in fixed folders only.
- Audited the repo for other environment, credential, token and network access: none in scripts, tests, commands or docs.

## 0.2.1
- Add `PRIVACY.md` and link it from the README.
- Add directory listing fields to `plugin.json`: `privacyPolicyUrl`, `documentationUrl`, `supportUrl`.
- Restore `displayName` ("Made For You CV") in `plugin.json`, which is a valid optional manifest field. (0.2.0 removed it by mistake.)

## 0.2.0
- Add `fill_template.py`: fill templates from JSON (escaping, URL normalization, optional contact items and sections removed cleanly, required-field and leftover-token checks).
- Add `cover-letter` template so the cover letter really matches the CV header.
- `build_cv.py`: find Chrome/Chromium in more places (Playwright cache, Windows, snap, `CHROME_PATH`), add `--no-sandbox` when running as root (cloud/Docker), use a throwaway Chrome profile, refuse to build with leftover placeholders, fix page-count regex.
- `preview_cv.py`: PyMuPDF / pypdfium2 fallbacks when poppler is missing.
- Templates: fix two-column sidebar and spacing on page 2, designer-accent skills layout, unstyled `tech` line in minimal, page-break handling, print colours; `lang` attribute is now settable.
- SKILL.md: resolve script paths relative to the skill folder, use the new scripts, document JSON keys and block HTML.
- Add `/made-for-you-cv:cv` command, smoke test, CI, and marketplace metadata.

## 0.1.0
- Initial release.
