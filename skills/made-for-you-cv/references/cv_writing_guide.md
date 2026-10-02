# CV Writing Guide

This reference covers the principles for tailoring a CV to a specific job. Load this when actively writing or editing CV content.

## Core Tailoring Principles

### 1. Mirror the job description's language
ATS and human reviewers both pattern-match on keywords. If the JD says "TypeScript" use TypeScript, not "TS". If it says "component-driven development", use that exact phrase somewhere in the CV. Mirror without copy-pasting full sentences — extract terms.

### 2. Lead each bullet with an action verb in past tense
For completed work: built, shipped, designed, implemented, migrated, optimized, reduced, integrated, refactored, scaled, automated, owned, led.
For ongoing/current role: build, ship, design, lead, maintain.

Avoid weak openers: "Worked on", "Helped with", "Was responsible for", "Assisted in", "Participated in".

### 3. Quantify wherever possible
Numbers create concreteness. Even rough numbers beat none.
- Bad: "Improved page load times"
- OK: "Reduced page load times significantly"
- Good: "Reduced page load times by ~40% by lazy-loading routes"

If exact numbers are unknown, use scale indicators: "~", "over", "~10k+ users", "across 3 product lines".

### 4. Show outcome, not just activity
Each bullet should ideally answer "and what changed?". Activity → outcome:
- Activity-only: "Built investor dashboard in React"
- With outcome: "Built investor dashboard in React used in monthly board meetings to surface KPIs across 3 product lines"

### 5. Cut, don't compress
When fitting on one page, prefer dropping low-relevance items entirely over shrinking everything to fit. A tight, focused CV beats a dense one.

Drop candidates first:
- Unrelated old jobs (retail, hospitality) unless used as a deliberate angle (e.g. restaurant management experience for leadership-oriented roles)
- Hobby projects that don't reinforce the role
- Generic "soft skills" sections
- Long lists of every tool ever touched — keep only what's relevant to the JD

## Tailoring Workflow

For each new application:

1. **Parse the JD first** (see `job_parsing_guide.md`). Extract must-have skills, nice-to-haves, and tone signals.
2. **Reorder the master CV's content** to surface most-relevant projects/experience first within each section.
3. **Rewrite bullets** to match JD language. Same project can be described 3 different ways depending on the role.
4. **Trim the skills list** to what's in the JD + adjacent things that strengthen the story. Don't list everything.
5. **Update the summary/headline** (top of CV) to mirror the role being applied for.
6. **Re-check page length** at the end. Cut, don't compress.

## Same Project, Different Framings (Example)

The same piece of work (an internship building dashboards and a website for a startup) can be framed differently:

For a **React/TypeScript role**:
> "Built production investor dashboards in React + TypeScript using Recharts and shadcn/ui, integrating real-time data from internal APIs."

For an **e-commerce role**:
> "Shipped production Shopify tools used by the merchant operations team, including custom storefront integrations and admin tooling."

For a **full-stack role**:
> "Owned end-to-end delivery of the company website (Next.js/TypeScript) and investor dashboards, working across third-party API integrations and frontend architecture."

The underlying experience is identical; the framing changes. The same applies outside tech: a sales role can be framed around revenue, relationships, or process depending on the JD.

## Regional CV Conventions

The skill's defaults cover Sweden/the Nordics and English-language European markets. Conventions differ, so adjust per JD location. For other countries, apply the closest set and follow local norms you're confident about (e.g. US résumés: no photo, no birthdate, 1 page strongly preferred).

### Sweden and the Nordics
- Photo: optional, common but not required. Keep professional if included.
- Birthdate: traditionally included but increasingly optional, especially in tech. **Default to omitting unless the master CV has it and the user specifies inclusion.**
- Personal pronouns ("han"/"hon"): not required.
- Length: 1-2 pages standard.
- Tone: relatively direct, less self-promotional than US style.
- National ID numbers (personnummer, CPR, fødselsnummer, etc.): **never include on a CV.** This is sensitive ID data.
- Languages section: include with proficiency levels (e.g. "Swedish: fluent, English: fluent, Arabic: native"). Useful in Stockholm market.

### UK / Netherlands / Germany / general EU English-speaking
- Photo: **omit by default**, especially for UK and Netherlands. Germany historically used photos but now mixed; default omit unless JD or company suggests otherwise.
- Birthdate: omit. Anti-discrimination norms.
- Marital status / nationality: omit.
- Length: 1-2 pages, 1 strongly preferred for entry/mid level.
- Tone: outcome-focused, slightly more confident than Swedish norm.
- Address: city + country is enough (e.g. "Stockholm, Sweden"). Don't include a full street address.
- Visa/work authorization: if relevant (non-EU citizen applying within EU), a single line near contact info clarifying status helps. If EU citizen with full work rights, mention it briefly when applying outside Sweden.

## Sections — Standard Order

Adjust order based on what's strongest for the target role:

1. **Header**: name, title (matched to JD), location, email, phone, portfolio, GitHub, LinkedIn
2. **Summary** (2-3 lines): tailored to the role. This is the highest-impact rewrite per application.
3. **Experience**: reverse chronological. Most recent first.
4. **Projects**: only if they strengthen the application beyond what experience already shows. For entry-level roles, projects often carry significant weight.
5. **Education**: brief for experienced candidates; fuller (program, key projects, credits) for recent graduates and bootcamp/vocational (e.g. Swedish YH) programs.
6. **Skills**: grouped (e.g. "Frontend", "Tools", "Languages") — not a flat blob.
7. **Languages**: spoken languages + proficiency (especially relevant in Sweden/EU).

For very experienced candidates education moves to bottom. For entry-level and career-switching candidates, education + projects sit above older unrelated experience.

## Anti-Patterns to Avoid

- Generic objectives ("Seeking a challenging role where I can grow…") — replace with a specific summary.
- Skill rating bars (★★★☆☆) — meaningless, looks dated, ATS-hostile.
- Listing every tool: "HTML, CSS, JS, React, Vue, Angular, Svelte, Next.js, Nuxt, Remix, Astro…" — signals breadth without depth.
- "References available upon request" — assumed, wastes space.
- Mixing past and present tense within the same role's bullets.
- Em dashes. Never use them. Use commas, colons, or parentheses instead.
- Overly literary or "AI-flavored" prose. Keep direct.

## Honesty Boundary

Tailoring means reframing, reordering, and selecting. It does not mean inventing experience, inflating job titles, or claiming skills not actually held. If the master CV doesn't support a claim the JD requires, flag it to the user rather than fabricating — they can decide whether to apply or upskill first.

### Header title matching
The header title is matched to the JD (e.g. "Frontend Developer" → "Frontend Engineer" is fine; they're equivalent). But the title must stay within what the experience genuinely supports:
- **Don't add seniority** the candidate hasn't reached. A JD for "Senior Frontend Developer" does not make the header "Senior Frontend Developer" — keep it at the honest level and let the experience speak.
- **Don't widen scope** beyond the real background. If the candidate's honest identity is, say, frontend-focused with some backend, a qualified header like "Full-stack Developer (Frontend Focus)" is fine for full-stack-leaning JDs; a plain "Full-stack Developer" that hides the weighting is not. Respect any title rules the user put in their master CV.
- Adjusting wording/framing of an equivalent-level title is fine; jumping levels or disciplines is not. When the JD's title overshoots the candidate's level, keep the honest title and flag the level gap to the user (see `job_parsing_guide.md` red flags).
