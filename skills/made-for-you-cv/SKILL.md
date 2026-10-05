---
name: made-for-you-cv
description: "Tailor your CV or resume to a specific job and get a designed, ATS-aware PDF, plus a cover letter on request. Use whenever someone wants a CV, resume or résumé made, updated or adapted for a job: 'tailor my CV', 'update my resume for this role', 'apply for this job', 'job application', 'cover letter', 'personligt brev', 'anpassa mitt CV', 'skriv ett CV till den här tjänsten'. Works from an attached or pasted CV and a pasted job ad, and builds a reusable master CV on first use. Honest tailoring (never invents experience), a plain-text copy for web forms, and Swedish, Nordic and European conventions."
---

# Made For You CV

Turn the user's own CV and a job ad into a tailored, designed, ATS-aware PDF CV (and a cover letter on request). Tailoring means reframing, reordering and selecting real experience. It never means inventing any.

## When to use
The user wants a CV, resume or cover letter made, updated or adapted for a job, or attaches or pastes a CV and a job ad (even with no instruction). Do not use it for general career advice or LinkedIn rewrites.

## Fast paths (check first)
**First run**: the first message has a CV (attached or pasted) and a job ad. Build the master CV silently (step 0), tailor it and deliver the PDF in the same turn. No template question, no interview.
**Repeat application**: a `master_cv.md` is attached or already in the conversation and the user brings a new job ad. Go straight to the tailored PDF with no questions at all (skip step 0, reuse the master CV's "Notes for tailoring").

**Missing input** (ask once, in one short message, only for what blocks the PDF): only a CV, then build the master CV and ask "Paste the job ad (or a link) and I'll tailor it."; only an ad, then ask "Send your CV in any format: PDF, Word, a LinkedIn PDF export or pasted text."; neither, then ask for both. Everything else (`[TODO]` fields, missing numbers, target title) never blocks the first PDF: leave unknown fields out, never invent them, and ask afterwards.

## Paths
`scripts/`, `assets/` and `references/` are relative to this skill's folder, so use absolute paths. Start each command with:
```bash
SKILL_DIR=$(dirname "$(dirname "$(find / -name fill_template.py -path '*made-for-you-cv*' -not -path '/proc/*' 2>/dev/null | head -1)")")
```
Work in a scratch directory (temp or `/tmp`), never inside the skill folder.

## Workflow

**0. Master CV.** Look for `master_cv.md` (attached, in the project or folder, or earlier in the chat); otherwise use the CV the user gave. Convert it to markdown with these sections (no need to open the template file): header and contact; summary; experience (title, company, place, dates, every bullet, tools); projects; education; skills (grouped); languages; certifications; and a "Notes for tailoring (never shown on the CV)" section. Keep every fact, do not polish or drop anything, mark unknowns `[TODO]`. Deliver `master_cv.md` with the PDF and say in one sentence to keep it so next time skips this step.

**1. Inputs.** Job ad: pasted text, or read the URL (ask for a paste if that fails). Template: do not ask. Use the one the user named; else `minimal`, or `designer-accent` for a clearly design-led role. `two-column` only if asked or the application is clearly design-led or human-reviewed (small studio, direct to a hiring manager): its sidebar is parsed badly by many applicant tracking systems, so note that once if the user asks for it on an ATS-likely ad. **Language**: set `LANG` (en, sv, da, nb, de, nl, fr) from the language of the job ad; the CV and any cover letter are written in that language and the section headings follow `LANG`.

**2. Read the ad** (internally). Role, company, region, seniority; must-haves (required, "you have") vs nice-to-haves; stack and tone signals. When unclear, treat as a must-have. Read `references/job_parsing_guide.md` only for a long, vague or non-tech ad.

**3. Say what you are doing, then continue in the same turn:** "This is a [archetype] role at [company] in [region]. Must-haves: [3-4]. Strongest matches: [2-3]. Gaps: [1-2]. Generating now." Pause only if the gaps are so large that a tailored CV would mislead.

**4. Tailor.**
- Summary (2-3 lines) mirrors the role. Reorder experience and projects, most relevant first. Trim skills to the ad plus adjacent; group them.
- Bullets: past-tense action verb, then outcome, using the master CV's real numbers. Mirror the ad's own wording ("TypeScript", not "TS"). Never invent numbers, skills, tools, employers or titles.
- Header title matches the ad's wording but stays within what the experience supports: no added seniority, no widened scope (a qualified title such as "Full-stack Developer (Frontend Focus)" is fine). Keep the user's own title rules.
- Gaps: a must-have the background does not support stays out and is flagged to the user, never faked.
- Order: experience first. For career switchers and recent graduates put education and projects first with `SECTION_ORDER`. Education is short for experienced people, fuller for graduates and vocational programs.
- Length: 1 page preferred, 2 at most. Cut low-relevance items rather than shrink (`--fit` handles small overflows).
- Region defaults (Sweden/Nordics, UK, NL, DE, other EU): omit photo, date of birth, marital status and nationality unless the user explicitly asks; location is city and country only; Nordic CVs may list languages with levels. Never put national ID numbers (personnummer, CPR) or street addresses on a CV, even if the source has them. Details: `references/cv_writing_guide.md` (read only when unsure about a market, a framing or an anti-pattern).
- Quality bar: `references/example_tailored_cv.md` (read only when unsure).

**5. Write the data file.** One JSON file drives everything (strings; `SECTION_ORDER` may be a list). Required: `NAME`, `TITLE`, `EMAIL`, `SUMMARY` (plain text), `EXPERIENCE_BLOCK`. Optional: `LANG`, `SECTION_ORDER` (e.g. `"education,projects,experience"`), `LOCATION` (city, country), `PHONE`, `PORTFOLIO`, `LINKEDIN`, `GITHUB`, and the blocks `PROJECTS_BLOCK`, `EDUCATION_BLOCK`, `SKILLS_BLOCK`, `LANGUAGES_BLOCK`; empty or missing items disappear cleanly. Blocks are small HTML:
- entry: `<div class="entry"><div class="entry-header"><span class="entry-title">Title</span><span class="entry-meta">Sep 2024 – Present</span></div><div class="entry-sub">Company · City</div><ul><li>Bullet</li></ul><div class="tech">React · TypeScript</div></div>` (`ul`, `entry-sub` and `tech` optional)
- skills group: `<div class="skills-group"><strong>Frontend</strong> <span class="items">React, TypeScript</span></div>`
- language: `<span class="lang">Swedish (fluent)</span>`
Cover letter keys (`BODY` as `<p>` paragraphs, `SALUTATION`, `CLOSING`, optional `RECIPIENT_BLOCK`, `DATE`) and every detail are in `references/template_data.md`; open it only if a call fails or you need something unusual.

**6. Build everything in one call.**
`python3 "$SKILL_DIR/scripts/make_cv.py" /tmp/cv_data.json --out [outputs folder] --name [FirstnameLastname]_CV_[Company]_[Role] [--template designer-accent] [--docx]`
It fills the template, builds the PDF, writes the `.txt` for web forms, and with `--docx` a single-column Word copy (standard headings, no tables or images). Add `--docx` when the ad signals a portal or ATS ("apply through our careers portal", large company, long structured ad) or the user asks for Word; otherwise just mention that it is available.
- It tightens spacing and type slightly (body text never below 9.5pt) if the CV runs over one page and reports it. Only if it still does not fit, cut the least relevant content and run again. `--pages 2` allows two pages for a long career.
- Exit code 2 means no PDF engine here: the finished `.html` and `.txt` were written instead. Deliver them and say in one sentence to open the HTML and use Print, Save as PDF (A4, margins None), and that turning on code execution lets me make the PDF directly. If you cannot run scripts at all, write the filled HTML yourself and paste the plain text in the chat.
- If `--docx` prints "Skipped", say so in one line and carry on.
- Cover letter: a second data file with the letter keys, same command with `--name [FirstnameLastname]_CoverLetter_[Company]_[Role]` (the `cover-letter` template is picked automatically).

**7. Verify.** Read the build output: 1-2 pages, no warnings. Look at a PNG (`python3 "$SKILL_DIR/scripts/preview_cv.py" file.pdf /tmp/prev`) only if `--fit` could not reach the target or the output looks wrong; images are costly. Every must-have the background supports appears in the ad's wording; report coverage briefly ("Covered 6/7; GraphQL left out, not in your background").

**8. Deliver** into the user's folder or outputs location if there is one (else attach): PDF, `.txt`, `.docx` when made, `master_cv.md` on a first run. Keep intermediates (JSON, HTML, PNG) in scratch. Filenames use underscores, no spaces. Then, briefly: template used, what was emphasized or trimmed, honest gaps.

**After the first PDF** add, short: one line that two other templates exist (name them); a list "To make it stronger, tell me:" with at most 3-5 concrete items ([TODO] fields, achievements without numbers); a one-line offer of a cover letter; and on a first run a reminder to keep `master_cv.md`. If the user shares new facts later, offer to update `master_cv.md`.

## Cover letters
Only when asked (in the first message too, then deliver both in one turn). Read `references/cover_letter_guide.md` first. Build it in step 6 as described there (`DATE` is localized from `LANG`). 250-400 words, in the ad's language.

## Rules that never change
- **Honesty**: reframe, reorder, select. Never invent experience, numbers, titles, skills or tools; flag mismatches instead.
- **Privacy**: no national ID numbers, no street addresses, no date of birth or marital status by default. The skill sends nothing anywhere.
- **Style**: direct, plain prose. No em dashes in CV or letter text (use commas, colons, parentheses). No emojis. Neutral black, white and grey only.
- **Efficiency**: do not reread references you do not need, and do not narrate steps. One status line, then the files.

## Resources
`assets/master_cv_template.md`; `assets/templates/` (minimal, two-column, designer-accent, cover-letter); `references/` (`template_data.md`, `job_parsing_guide.md`, `cv_writing_guide.md`, `cover_letter_guide.md`, `example_tailored_cv.md`); `scripts/` (`make_cv.py` runs the rest; `fill_template.py`, `build_cv.py`, `build_docx.py`, `html_to_text.py`, `preview_cv.py`, shared `cv_common.py`).
