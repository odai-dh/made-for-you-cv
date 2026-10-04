# Made For You CV

## Start in 10 seconds

**Attach your CV, paste a job ad, and say: _Tailor my CV for this job._**

You get a tailored, ATS-aware PDF CV (plus a plain-text copy for web forms) in one go. No setup, no questions first.

Three prompts to try:

- "Tailor my CV for this job and write a cover letter too: [paste job ad]" (with your CV attached)
- "Anpassa mitt CV efter den här annonsen och skriv ett personligt brev: [klistra in annonsen]" (Swedish job ad, Swedish output)
- "This is a design role at a small studio, use the two-column template: [paste job ad]"

Prefer a command? Run `/made-for-you-cv:cv` and attach your CV and the ad.

Found a bug or have an idea? [Open an issue on GitHub](https://github.com/odai-dh/made-for-you-cv/issues).

---

A Claude plugin that turns **your own CV** and **a job posting** into a tailored, designed PDF CV, plus an optional cover letter.

- **Honest tailoring**: reorders, reframes and selects from your real experience. It never invents skills, numbers or titles, and it flags gaps instead.
- **ATS-aware**: steers you to single-column layouts when the employer probably uses an applicant tracking system, checks keyword coverage against the posting's must-haves, and gives you a plain-text copy for web forms.
- **Three neutral A4 CV templates** (`minimal`, `two-column`, `designer-accent`) plus a matching cover-letter template.
- **Regional conventions**: Sweden/Nordics, UK, Netherlands, Germany and the rest of Europe (photos, birthdates, ID numbers, length, tone).
- **Cover letters on request**, in the posting's language.

## How to use

1. Install the plugin and start a chat.
2. Attach your current CV (PDF, Word, text or a LinkedIn PDF export) and paste the job ad.
3. Claude builds a reusable `master_cv.md` behind the scenes, tailors it, and hands you the PDF and a plain-text version. It uses the `minimal` template by default (`designer-accent` for clearly design-led roles) and tells you about the other two afterwards.
4. After the first PDF it lists a few things you could tell it to make the CV stronger. Keep `master_cv.md` and attach it next time to skip the CV upload.

If your environment can't make PDFs (for example code execution is off), you still get the finished HTML and a text version: open the HTML and use Print, Save as PDF.

Example prompts:

- "Update my resume for this Frontend Engineer role at [company]: [paste JD]"
- "Make a CV and a cover letter for this posting, two-column template."
- "Set up my master CV" (attach your current CV)

## Requirements

- Code execution must be enabled (Claude builds the PDF with small Python scripts). Python 3.8+, standard library only.
- One PDF renderer: Google Chrome / Chromium / Edge (found automatically, including Playwright's browser cache and root/Docker setups), or `pip install weasyprint`, or Playwright. Pass `--chrome <path>` to `build_cv.py` to use a specific binary.
- Optional, for the visual check: `pdftoppm` (poppler) or `pip install pymupdf`.

## Development

```
python3 tests/smoke_test.py          # fills and builds every template, checks page count, edge cases and the no-PDF-engine fallback
claude plugin validate .             # manifest check
```

`scripts/fill_template.py` fills a template from JSON, `build_cv.py` renders the PDF, `html_to_text.py` makes the ATS plain-text copy, `preview_cv.py` renders PNGs for the visual check.

## Privacy

Your CV is only used within your own Claude conversation to produce your documents. The plugin has no server and sends nothing anywhere. National ID numbers and full street addresses are never put on a CV. See the full [privacy policy](PRIVACY.md).

## Install (Claude Code)

```
/plugin marketplace add odai-dh/made-for-you-cv
/plugin install made-for-you-cv@odai-plugins
```

## Structure

```
.claude-plugin/
  plugin.json
  marketplace.json
commands/cv.md
skills/made-for-you-cv/
  SKILL.md
  assets/master_cv_template.md
  assets/templates/{minimal,two-column,designer-accent,cover-letter}.html
  references/  (tailoring, JD parsing, cover letter, worked example)
  scripts/     (fill_template.py, build_cv.py, preview_cv.py, html_to_text.py)
tests/         (smoke test + fictional sample data)
```

## License

MIT
