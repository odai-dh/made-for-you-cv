# Job Description Parsing Guide

This reference covers how to extract the right information from a pasted job description. Load this when starting a new tailoring session.

## What to Extract

Parse every JD into a structured breakdown before writing CV content. Use this internal scratchpad:

```
Company: [name]
Role title: [exact title from JD]
Location: [city / remote / hybrid]
Region: [Sweden / UK / NL / DE / other]
Seniority: [intern / junior / mid / senior / lead]

MUST-HAVE skills (explicit requirements, "required", "must have"):
- ...

NICE-TO-HAVE skills ("plus", "bonus", "preferred"):
- ...

Domain / industry signals:
- ...

Tone signals:
- ...

Hidden requirements (read between lines):
- ...
```

## How to Distinguish Must-Have from Nice-to-Have

Language patterns to watch for:

**Must-haves** typically use:
- "Required", "must have", "essential"
- "You have…", "You bring…"
- Items in a "Requirements" or "What we're looking for" section
- Hard skills mentioned multiple times across the JD

**Nice-to-haves** typically use:
- "Plus", "bonus", "ideally", "preferred"
- "Familiar with", "exposure to", "interest in"
- Items in a "Nice to have" or "Bonus points" section
- Skills mentioned once in passing

When unclear, treat as must-have. Better to address it than skip.

## Reading Between the Lines

JDs contain signals beyond their explicit requirement lists.

### Stack signals
If the JD mentions a specific framework (e.g. Remix, Astro, SvelteKit) but it's not in the candidate's master CV, note it. The candidate may have transferable React/Next.js experience worth framing toward it.

### Team-size signals
- "Small team", "startup", "fast-paced" → emphasize ownership, breadth, shipping speed in CV bullets
- "Established product", "enterprise", "scale" → emphasize reliability, testing, working with existing codebases

### Culture signals
- "Design-led", "design-driven" → surface design collaboration, Figma fluency, attention to UI detail
- "Data-driven" → surface analytics integration, A/B test work, dashboard work
- "Open source", "community" → surface any contributions, public projects, community or volunteer work
- "Customer-obsessed", "user-focused" → surface user-facing work, internship client projects

### Tone signals
- Casual, emoji-laden JD → CV summary can be slightly more personal
- Formal, corporate JD → keep CV summary tight and professional
- Long detailed JD with many sections → company likely has structured hiring process, ATS likely; prioritize keyword matching
- Short punchy JD → likely small team; CV summary matters more than skills checklist

### Location/region signals
The country listed determines CV conventions (see `cv_writing_guide.md` regional section). A Stockholm-based job from a German company may still follow Swedish norms; a Berlin-based job from a US company may follow more international norms. Default to the country where the role is physically based.

## Role Archetypes

Most JDs fall into a few patterns per field. Identifying the archetype helps prioritize what to surface. Below are worked archetypes for frontend/web roles; for other fields, name the archetype the same way (what the team mostly needs: shipping, craft, scale, breadth, leadership) and pick what to surface accordingly.

### Frontend / web examples

### "Product-focused frontend dev"
Emphasis on shipping features, user-facing work, collaboration with designers and PMs.
→ Surface: shipped projects, user-facing impact, design collaboration, cross-functional work.

### "UI engineer / design engineer"
Emphasis on craft, animations, design systems, design tool fluency.
→ Surface: Framer Motion, Tailwind, component libraries, Figma-to-code work, attention to detail.

### "Full-stack-leaning frontend"
Emphasis on APIs, integrations, some backend.
→ Surface: third-party integrations, API work, full-stack project ownership.

### "Frontend platform / infra"
Emphasis on tooling, build systems, performance, DX.
→ Surface: any build tooling, performance optimization, internal tooling work. (Often a weak match for entry-level applicants; flag this honestly.)

### "Generalist / startup engineer"
Emphasis on breadth, ownership, learning fast.
→ Surface: variety of stack, side projects, self-directed learning, internship breadth.

## Red Flags Worth Flagging to the User

If the JD asks for things clearly mismatched with the candidate's level, mention it before tailoring rather than producing a CV that misrepresents:

- Many more years required than the candidate has
- A specific niche stack (Elixir, Rust, Solid.js, etc.) the candidate has zero exposure to
- Senior leadership experience
- Specific certifications or degrees the candidate doesn't hold

Flag once, briefly, then let the user decide whether to proceed.

## Output of This Step

After parsing, produce a brief summary back to the user before tailoring:

> "This is a [archetype] role at [company], based in [location]. Must-haves: [3-4 key items]. Strongest matches from your background: [2-3 items]. Gaps to be aware of: [1-2 items, if any]. Going with the [chosen template], generating now."

This gives the user a chance to redirect before any writing happens.
