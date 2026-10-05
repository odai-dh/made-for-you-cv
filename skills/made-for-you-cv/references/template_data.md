# Template data (JSON for fill_template.py and build_docx.py)

One JSON file drives the HTML templates and the Word file. All values are strings (`SECTION_ORDER` may be a list). Leave an optional key out or empty and its item or section disappears cleanly (no stray separators, no empty headings).

## CV keys

| Key | Required | Notes |
|---|---|---|
| `NAME`, `TITLE`, `EMAIL`, `SUMMARY`, `EXPERIENCE_BLOCK` | yes | `SUMMARY` is plain text (2-3 lines) or HTML |
| `LANG` | no | `en` (default), `sv`, `da`, `nb`, `de`, `nl`, `fr`. Sets section headings and document language. Override any heading with `H_EXPERIENCE`, `H_EDUCATION`, `H_PROJECTS`, `H_SKILLS`, `H_LANGUAGES`, `H_PROFILE`, `H_CONTACT`. Swedish: Profil, Erfarenhet, Projekt, Utbildning, Kompetenser, Språk |
| `SECTION_ORDER` | no | e.g. `"education,projects,experience"`. Named sections go first, the rest keep their default order. Use for career switchers and recent graduates |
| `LOCATION`, `PHONE` | no | city and country only, never a street address |
| `PORTFOLIO`, `LINKEDIN`, `GITHUB` | no | URL or bare domain; `*_DISPLAY` is derived, override if needed |
| `PROJECTS_BLOCK`, `EDUCATION_BLOCK`, `SKILLS_BLOCK`, `LANGUAGES_BLOCK` | no | raw HTML as below. In `two-column`, skills and languages sit in the sidebar |

## Block HTML

Entries (experience, projects, education):

```html
<div class="entry">
  <div class="entry-header">
    <span class="entry-title">Frontend Developer</span>
    <span class="entry-meta">Sep 2024 – Present</span>
  </div>
  <div class="entry-sub">Example Company AB · Stockholm</div>
  <ul>
    <li>Refactored a 4,000-line legacy app into reusable React components.</li>
  </ul>
  <div class="tech">React · TypeScript · Next.js</div>
</div>
```

`<ul>`, `entry-sub` and `tech` are optional (education usually has no bullets). For non-technical roles use `tech` for tools or methods, or drop it.

Skills, one group per line: `<div class="skills-group"><strong>Frontend</strong> <span class="items">React, TypeScript</span></div>`

Languages: `<span class="lang">Swedish (fluent)</span> <span class="lang">English (fluent)</span>`

## Cover letter keys (`cover-letter` template, or `build_docx.py` with `BODY`)

Required: `NAME`, `EMAIL`, `SALUTATION`, `BODY` (HTML `<p>` paragraphs), `CLOSING`. Optional: `TITLE`, `LOCATION`, `PHONE`, `PORTFOLIO`, `LINKEDIN`, `GITHUB`, `RECIPIENT_BLOCK` (plain text, one line per line), `LANG`, `DATE`. `DATE` empty means today; `2026-10-05` is written out in the `LANG` format (5 oktober 2026, 5. Oktober 2026, 5 October 2026).

## Never put in the JSON
National ID numbers, street addresses, date of birth, marital status, anything the CV should not show.
