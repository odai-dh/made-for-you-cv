# Made For You CV

A Claude plugin that turns **your own CV** and **a job posting** into a tailored, designed PDF CV, plus an optional cover letter.

- **Honest tailoring**: reorders, reframes and selects from your real experience. It never invents skills, numbers or titles, and it flags gaps instead.
- **ATS-aware**: steers you to single-column layouts when the employer probably uses an applicant tracking system, checks keyword coverage against the posting's must-haves, and gives you a plain-text copy for web forms.
- **Three neutral A4 templates**: `minimal`, `two-column`, `designer-accent`.
- **Regional conventions**: Sweden/Nordics, UK, Netherlands, Germany and the rest of Europe (photos, birthdates, ID numbers, length, tone).
- **Cover letters on request**, in the posting's language.

## How to use

1. Install the plugin and start a chat.
2. Say "I'm applying for this job" and paste the job description.
3. The first time, Claude asks for your current CV (PDF, Word, text or a LinkedIn PDF export) and turns it into a reusable `master_cv.md`. Keep that file and attach it next time to skip this step.
4. Pick a template (or let Claude pick), and you get a PDF + a plain-text version.

Example prompts:

- "Tailor my CV for this Frontend Engineer role at [company]: [paste JD]"
- "Make a CV and a cover letter for this posting, two-column template."
- "Set up my master CV" (attach your current CV)

## Requirements

Code execution must be enabled (Claude builds the PDF with a small Python script). The script uses headless Chrome/Chromium, WeasyPrint or Playwright, whichever is available.

## Privacy

Your CV is only used within your own Claude conversation to produce your documents. The plugin has no server and sends nothing anywhere. National ID numbers and full street addresses are never put on a CV.

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
skills/made-for-you-cv/
  SKILL.md
  assets/master_cv_template.md
  assets/templates/{minimal,two-column,designer-accent}.html
  references/  (tailoring, JD parsing, cover letter, worked example)
  scripts/     (build_cv.py, preview_cv.py, html_to_text.py)
```

## License

MIT
