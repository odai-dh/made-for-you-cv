# Made For You CV

A Claude plugin that turns **your own CV** and **a job posting** into a tailored, designed PDF CV, plus an optional cover letter.

- **Honest tailoring**: reorders, reframes and selects from your real experience. It never invents skills, numbers or titles, and it flags gaps instead.
- **ATS-aware**: steers you to single-column layouts when the employer probably uses an applicant tracking system, checks keyword coverage against the posting's must-haves, and gives you a plain-text copy for web forms.
- **Three neutral A4 CV templates** (`minimal`, `two-column`, `designer-accent`) plus a matching cover-letter template.
- **Regional conventions**: Sweden/Nordics, UK, Netherlands, Germany and the rest of Europe (photos, birthdates, ID numbers, length, tone).
- **Cover letters on request**, in the posting's language.

## How to use

1. Install the plugin and start a chat.
2. Say "I'm applying for this job" and paste the job description.
3. The first time, Claude asks for your current CV (PDF, Word, text or a LinkedIn PDF export) and turns it into a reusable `master_cv.md`. Keep that file and attach it next time to skip this step.
4. Pick a template (or let Claude pick), and you get a PDF + a plain-text version.

You can also run the slash command `/made-for-you-cv:cv` and paste the posting after it.

Example prompts:

- "Tailor my CV for this Frontend Engineer role at [company]: [paste JD]"
- "Make a CV and a cover letter for this posting, two-column template."
- "Set up my master CV" (attach your current CV)

## Requirements

- Code execution must be enabled (Claude builds the PDF with small Python scripts). Python 3.8+, standard library only.
- One PDF renderer: Google Chrome / Chromium / Edge (found automatically, including Playwright's browser cache and root/Docker setups), or `pip install weasyprint`, or Playwright. Set `CHROME_PATH` to use a specific binary.
- Optional, for the visual check: `pdftoppm` (poppler) or `pip install pymupdf`.

## Development

```
python3 tests/smoke_test.py          # fills and builds every template, checks page count and edge cases
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
