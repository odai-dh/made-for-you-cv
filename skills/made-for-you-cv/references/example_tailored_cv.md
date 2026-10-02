# Worked Example: One Full Tailoring Pass

A reference-quality example of the whole flow: a sample JD, the parse, the
pre-generation summary, and the finished tailored CV content. Use it as the
quality bar for tone, bullet style, length, and honesty. Do not copy its
wording into real CVs; match its *level*, not its text.

The candidate, companies, and contact details below are **fictional**.

This example uses the `minimal` template (the JD is long and from a mid-size
company, so ATS is likely; see the ATS caveat in `SKILL.md` step 1).

---

## Input: the pasted JD (excerpt)

> **Frontend Engineer, Nordvik Mobility (Stockholm, hybrid)**
> We're looking for a Frontend Engineer to help build the rider and operations
> web apps that keep our fleet moving. You'll work in a small, product-focused
> team shipping features end-to-end.
>
> **You have:** Strong React and TypeScript. Experience building responsive,
> accessible UIs. Comfort working with REST APIs and turning designs into
> polished interfaces. You care about user experience and ship fast.
> **Nice to have:** Next.js, data-visualization experience, an eye for design,
> exposure to Node.js.

---

## Internal parse (not shown to the user)

```
Company: Nordvik Mobility
Role title: Frontend Engineer
Location: Stockholm (hybrid)
Region: Sweden
Seniority: mid (no years stated, "small product-focused team")
Archetype: Product-focused frontend dev

MUST-HAVE:
- React
- TypeScript
- Responsive, accessible UIs
- REST API integration
- Design-to-UI / polish
NICE-TO-HAVE:
- Next.js
- Data visualization
- Design sense
- Node.js
Domain signals: micromobility, rider + ops web apps, ship-fast small team
Tone signals: direct, product-focused, "ship fast" → ownership/breadth framing
Hidden requirements: end-to-end ownership in a small team
```

## Pre-generation summary (shown to the user)

> This is a product-focused frontend role at Nordvik Mobility, based in
> Stockholm (hybrid, Swedish conventions). Must-haves: React, TypeScript,
> responsive + accessible UIs, REST API work, design-to-UI polish. Strongest
> matches from your background: the Brightlane refactor and component work, the
> company website you built end-to-end, and your dashboard data-viz (which also
> covers the Next.js and data-viz nice-to-haves). Gap to flag: accessibility
> isn't called out in your master CV, so I'll only claim it where your work
> supports it. Going with the minimal template (long JD, mid-size company, ATS
> likely), generating now.

---

## Finished tailored CV content

**Alex Lindgren**
Frontend Developer
Stockholm, Sweden · alex@example.com · +46 70 000 00 00 · alexlindgren.dev · github.com/alex-example · linkedin.com/in/alex-example

### Summary
Frontend developer with production experience across two Stockholm
internships, shipping React and TypeScript interfaces end-to-end in small,
product-focused teams. Comfortable turning designs into polished, responsive UIs
and integrating REST APIs, with a track record of refactoring large codebases
and building products from scratch.

### Experience

**Frontend Developer Intern, Brightlane AB**
Stockholm · Sep 2025 – Mar 2026
- Refactored a 4,000-line Shopify app into smaller, reusable React components
  with error handling and clear documentation.
- Built the company website end-to-end (19,000+ lines across 131 files) in
  Next.js and TypeScript, integrating REST APIs and third-party tools.
- Shipped investor-facing dashboards with KPI cards, data tables, and Chart.js
  visualizations used in board meetings.
- Iterated on responsive UI through multiple design rounds based on team feedback.

React · TypeScript · Next.js · Tailwind · Chart.js · REST APIs

**Frontend Developer Intern, Matchpoint Sports**
Stockholm · May 2025 – Sep 2025
- Built and improved responsive React + TypeScript UI components for a
  sports-tech platform.
- Worked in an agile team alongside developers and designers, shipping features
  while keeping the design consistent.

React · TypeScript · Tailwind · Git

### Education
**Nordic Code Academy, Frontend Developer Program (YH)**, 2024 – 2026
Component-based UIs in React, e-commerce builds in Next.js/TypeScript, agile
team projects. Currently extending into Node.js, Express, and MongoDB.

### Skills
- **Frontend**: React, Next.js, TypeScript, JavaScript (ES6+), HTML, CSS
- **Styling / UI**: Tailwind CSS, Framer Motion, shadcn/ui
- **Data / integration**: Chart.js, Recharts, REST APIs, Shopify API
- **Tooling**: Git, GitHub, Figma, Vercel, Netlify

### Languages
Swedish: fluent · English: fluent · Arabic: native

---

## Why this passes the quality bar

- **One page.** An older restaurant-management job and an IT-support role were
  cut because they don't reinforce a product-frontend application (cut, don't
  compress).
- **Mirrors JD language**: "React", "TypeScript", "responsive", "REST APIs",
  "end-to-end", "product-focused" all appear, in the candidate's own true wording.
- **Keyword coverage**: covers React, TypeScript, responsive UIs, REST APIs, and
  design-to-UI. Accessibility was *not* claimed because the master CV doesn't
  support it; it was flagged in the summary instead of fabricated.
- **Title stays honest**: "Frontend Developer", not "Senior" or a bare
  "Full-stack" (this is a frontend JD; backend isn't the story here).
- **Nice-to-haves landed for free**: Next.js and data-viz came straight from
  real internship work, no stretching.
- **Numbers are real** (taken from the master CV): 4,000-line refactor,
  19,000+ lines / 131 files.
- **No em dashes in CV text, no emojis, neutral palette.**
