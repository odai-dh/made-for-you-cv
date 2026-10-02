---
name: made-for-you-cv
description: Turn your own CV and a pasted job description into a tailored, designed, ATS-aware PDF CV (and an optional cover letter). Use when the user is applying for a job and wants a CV adapted to a specific posting, asks to "tailor my CV", "make a CV for this job", or wants a cover letter for a role. Three neutral templates, honest tailoring (never invents experience), and regional conventions for Sweden, the Nordics, the UK and the rest of Europe.
---

# Made For You CV

## Purpose

Produce a tailored, professional, designed PDF CV from the user's own master CV and a job description they provide. Each application gets a CV that mirrors the role's language, surfaces the most relevant experience first, respects the regional conventions of the target market, and never claims anything the user's real background doesn't support.

## When to Use

Trigger this skill when the user:
- Says they're applying for a job and pastes or links a job description
- Asks for a "CV", "resume", or "tailored CV" for a specific role
- Asks for a cover letter for a specific role (CV + cover letter together)
- Says something like "make me a CV for this", "tailor my CV for X", "I'm applying to Y"
- Wants to set up their master CV for future applications

Do not trigger this skill for:
- General career advice or job-hunt strategy
- LinkedIn profile rewrites

## Workflow

Follow these steps in order. Do not skip steps.

### Step 0: Find or create the user's master CV

The master CV is the single source of truth for everything that goes on a tailored CV. This skill never ships with one; it always comes from the user.

1. **Look for an existing master CV first**, in this order:
   - A file named `master_cv.md` attached to the conversation, in the current project, or in the working/connected folder
   - A master CV produced earlier in this conversation
   - Any CV the user attached (PDF, DOCX, TXT, MD) or pasted
2. **If none exists, onboard the user:**
   - Ask them to upload or paste their current CV (a LinkedIn "Save to PDF" export also works). One message, no long questionnaire.
   - Convert it into the structure in `assets/master_cv_template.md`. Keep every fact; do not polish, invent, or drop anything at this stage. The master should hold *more* than any single CV will show.
   - Ask, in one short batch, only for things that are missing and matter: target job title, location and willingness to relocate, work authorization (only if they're likely to apply across borders), and any real numbers behind their achievements (team size, users, revenue, lines of code, time saved). Mark anything still unknown with `[TODO]`.
   - Save the result as `master_cv.md` and deliver it to the user. Tell them in one sentence to keep it (in a Claude Project, their folder, or just re-upload it) so future applications skip this step.
3. If the master CV contains `[TODO]` markers in fields needed for the current application, surface them before generating. Either ask for the values or say clearly that those fields will be left out.

### Step 1: Confirm inputs

Before generating anything, confirm the user has provided:
1. A job description (pasted text is the default; if they give a URL, try to read it, and ask them to paste it if that fails)
2. Optional: which template they want (minimal / two-column / designer-accent). If unspecified, ask once briefly. Default to `minimal` if they say "you pick".
   - **ATS caveat**: `two-column` places skills/contact in a sidebar, which many applicant tracking systems parse out of order or drop entirely. When the JD signals an ATS-likely pipeline (long, multi-section JD; large/enterprise company; explicit "apply through our portal"), steer toward a single-column template (`minimal` or `designer-accent`) and say why. Reserve `two-column` for clearly design-led or human-reviewed applications (small studios, design roles, direct-to-hiring-manager). If the user explicitly asks for two-column anyway, honor it but note the ATS risk once.
3. Optional: whether they want a cover letter alongside. Do not generate one unless asked.

### Step 2: Read the references

Read `references/job_parsing_guide.md` for the JD parsing approach.
Read `references/cv_writing_guide.md` for tailoring principles and regional conventions.
Read `references/example_tailored_cv.md` for a worked end-to-end example. Use it as the quality bar for tone, bullet style, length, and honesty (match its level, not its wording or its candidate).
If a cover letter was requested, also read `references/cover_letter_guide.md`.

Also read the "Notes for tailoring" section of the user's master CV if it has one: it holds their personal preferences (title rules, things to always or never include, style dislikes) and those override the defaults in this skill.

### Step 3: Parse the JD

Following `references/job_parsing_guide.md`, produce an internal structured breakdown of the job. Do not output this raw to the user; synthesize it into the brief summary in step 4.

### Step 4: Pre-generation summary

Output a brief summary to the user before any tailoring:

> "This is a [archetype] role at [company], based in [location/region]. Must-haves: [3-4 key items]. Strongest matches from your background: [2-3 items]. Gaps to flag: [1-2 items, if any]. Going with the [chosen template], generating now."

This gives the user a chance to redirect. Do not wait for explicit confirmation unless gaps are significant; proceed to step 5 in the same turn.

### Step 5: Tailor the content

Following `references/cv_writing_guide.md`:
- Rewrite the summary to mirror the role.
- Reorder experience and projects so the most relevant comes first.
- Rewrite bullets to mirror JD language, lead with strong action verbs, and quantify using the real numbers from the master CV. Never invent numbers.
- Trim the skills list to JD-relevant + adjacent. Do not include every tool in the master CV.
- Apply the regional conventions in `references/cv_writing_guide.md` (photo, birthdate, national ID numbers, etc.).
- Page length: prefer 1 page, allow 2 if the content genuinely needs it. Cut, don't compress.

### Step 6: Populate the chosen template

The three templates live in `assets/templates/`:
- `minimal.html`: single column, lots of whitespace, conservative
- `two-column.html`: sidebar with skills/contact + main column for experience
- `designer-accent.html`: bold name treatment, mono-font skill tags, more personality (still neutral palette)

Each template uses `{{TOKEN}}` placeholders. To populate:
1. Copy the chosen template HTML to a working file (e.g. `/tmp/cv_working.html`).
2. Replace each token with the tailored content. Tokens vary slightly by template, so open the template file and check.

Common tokens across templates:
- `{{NAME}}`, `{{TITLE}}`, `{{LOCATION}}`, `{{EMAIL}}`, `{{PHONE}}`
- `{{PORTFOLIO}}`, `{{PORTFOLIO_DISPLAY}}` (URL vs human-readable form, e.g. `janedoe.dev`)
- `{{LINKEDIN}}`, `{{LINKEDIN_DISPLAY}}` (e.g. `linkedin.com/in/jane-doe`)
- `{{GITHUB}}`, `{{GITHUB_DISPLAY}}`
- `{{SUMMARY}}`: the tailored 2-3 line profile paragraph
- `{{EXPERIENCE_BLOCK}}`: full HTML for all experience entries
- `{{PROJECTS_BLOCK}}`: full HTML for selected projects (drop the section if not used)
- `{{EDUCATION_BLOCK}}`: full HTML for education entries
- `{{SKILLS_BLOCK}}` (or `{{SIDEBAR_SKILLS_BLOCK}}` in two-column): grouped skills HTML
- `{{LANGUAGES_BLOCK}}` (or `{{SIDEBAR_LANGUAGES_BLOCK}}` in two-column): languages HTML

**Optional contact fields**: if the user has no portfolio, LinkedIn, GitHub, or phone, leave both tokens empty AND remove the surrounding markup so the line doesn't render with empty content or stray separators.

For each entry block, generate clean HTML matching the template's existing class structure. Example entry HTML:

```html
<div class="entry">
  <div class="entry-header">
    <span class="entry-title">Frontend Developer</span>
    <span class="entry-meta">Sep 2024 – Present</span>
  </div>
  <div class="entry-sub">Example Company AB · Stockholm</div>
  <ul>
    <li>Refactored a 4,000-line legacy app into reusable React components with error handling and documentation.</li>
    <li>Built the company website end-to-end in Next.js, TypeScript, and Tailwind CSS.</li>
  </ul>
  <div class="tech">React · TypeScript · Next.js · Tailwind</div>
</div>
```

The `tech` line is optional; for non-technical roles use it for tools or methods, or drop it.

If a section is empty (e.g. no projects on this version of the CV), remove its entire `<section>` rather than leaving an empty heading.

### Step 7: Build the PDF

Run the build script to convert the populated HTML to PDF:

```bash
python3 scripts/build_cv.py /tmp/cv_working.html /tmp/cv_output.pdf
```

The script tries headless Chrome/Chromium first, then WeasyPrint, then Playwright, and prints install instructions if none is available. It also reports the page count and warns at 3+ pages; if so, return to step 5 and trim.

Filename convention for the final PDF:
`[FirstnameLastname]_CV_[Company]_[Role].pdf`, e.g. `JaneDoe_CV_Spotify_Frontend.pdf`. Underscores, no spaces.

Also generate a plain-text version for ATS web forms, LinkedIn Easy Apply, and email bodies that don't accept a PDF:

```bash
python3 scripts/html_to_text.py /tmp/cv_working.html /tmp/[FirstnameLastname]_CV_[Company]_[Role].txt
```

Present the `.txt` alongside the PDF. (For a cover letter, do the same.)

### Step 8: Verify and present

Before presenting the PDF, check:
- **Page count**: 1 preferred, 2 acceptable. If 3+, return to step 5 and trim harder.
- **Visual check**: render the PDF to PNG and look at it. This catches overflow, broken layout, and awkward page breaks that an HTML-only check misses:
  ```bash
  python3 scripts/preview_cv.py /tmp/cv_output.pdf /tmp/cv_preview
  ```
  Then view `/tmp/cv_preview-1.png` (and `-2.png` if 2 pages). Fix the HTML and rebuild if anything is off.
- **No leftover placeholders**: no `{{TOKEN}}` remaining in the final HTML.
- **No empty sections** with headings, no stray separators from removed contact fields.
- **Keyword coverage**: confirm each must-have from step 3 appears, in the JD's own wording, somewhere in the CV. If a must-have is supported by the master CV but missing, add it. If it's missing because the user's background doesn't support it, leave it out and flag it. Report coverage briefly, e.g. "Covered 6/7 must-haves; 'GraphQL' left out since it's not in your background."

Present the files to the user. Briefly note, in plain prose:
- Which template was used
- What was emphasized vs trimmed for this role
- Any gaps or honest concerns

Offer to iterate. If the user shares new facts while iterating (a new job, a number, a skill), offer to add them to their master CV and deliver the updated `master_cv.md`.

## Cover Letters

When (and only when) explicitly requested, follow `references/cover_letter_guide.md` to write a tailored cover letter as a separate PDF using the same template family for visual consistency. Filename: `[FirstnameLastname]_CoverLetter_[Company]_[Role].pdf`.

## Style Constraints

- **Tone**: direct, plain. No overly literary or AI-flavored prose. Avoid em dashes in CV and cover-letter text (use commas, colons, or parentheses); they are a common "written by AI" tell.
- **Honesty**: tailoring means reframing, reordering, selecting. It never means inventing experience, inflating titles, or claiming skills not held. Flag mismatches instead of fabricating.
- **Numbers**: use the real numbers from the master CV over generic claims.
- **Palette**: neutral black/white/grey across all templates. No brand colors or accents.
- **No emojis** anywhere in CV output.
- **Privacy**: never put national ID numbers (personnummer, etc.), full street addresses, or other sensitive identifiers on a CV, even if they appear in the source CV.

## Resources

### `assets/master_cv_template.md`
The structure for a user's master CV. Used in step 0 to convert whatever CV the user provides into a reusable source of truth.

### `assets/templates/`
Three HTML/CSS templates: `minimal.html`, `two-column.html`, `designer-accent.html`. All A4, print-ready, neutral palette, with `{{TOKEN}}` placeholders.

### `references/cv_writing_guide.md`
Tailoring principles, regional conventions (Sweden/Nordics vs UK/NL/DE), section ordering, anti-patterns, and example reframings.

### `references/job_parsing_guide.md`
How to extract must-haves, nice-to-haves, archetype, and tone signals from a pasted JD.

### `references/cover_letter_guide.md`
Loaded only when a cover letter is requested. Structure, tone matching, and anti-patterns.

### `references/example_tailored_cv.md`
A worked end-to-end example with a fictional candidate (sample JD, parse, summary, finished CV), used as the quality bar.

### `scripts/build_cv.py`
Converts a populated template HTML to PDF. Tries Chrome → WeasyPrint → Playwright and reports the page count. Run as `python3 scripts/build_cv.py <input.html> <output.pdf>`.

### `scripts/preview_cv.py`
Renders a built PDF's pages to PNG for the visual check. Tries pdftoppm (all pages) then sips on macOS (first page). Run as `python3 scripts/preview_cv.py <input.pdf> [output_prefix]`.

### `scripts/html_to_text.py`
Converts a populated CV/cover-letter HTML to clean plain text for ATS forms. Standard library only. Run as `python3 scripts/html_to_text.py <input.html> [output.txt]`.
