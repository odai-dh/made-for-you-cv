# Cover Letter Guide

Load this only when the user explicitly asks for a cover letter alongside the CV. Default behavior is CV-only.

## When to Write One

Generate a cover letter when:
- The user asks ("also write a cover letter", "include a CL", etc.)
- The JD explicitly requires one (some Swedish and UK applications still do)

Do not generate one proactively. The CV is the default deliverable.

## Length and Format

- **Length**: 250-350 words. One page max, usually half a page.
- **Format**: Plain prose, 3-4 short paragraphs. No bullet points, no headers within the body.
- **Style**: Avoid em dashes. Use commas, colons, or parentheses instead.
- **File**: Same template family as the CV (matching header) so they look like a set. Output as PDF.

## Structure

### Date and salutation (above the body)
- **Date**: include the date the letter is generated, formatted for the region (Sweden / EU: `6 June 2026`; avoid the US `June 6, 2026` form). Place it above the greeting.
- **Addressee**: if the JD or company page names a hiring manager or team lead, address them by name (`Dear Anna Lindqvist,`). If no name is available, use `Dear Hiring Team,` — never `To Whom It May Concern` (dated) or `Dear Sir/Madam` (assumes gender). Do not invent a name; when unsure, ask the user or default to the team greeting.
- Keep the header (name + contact) visually consistent with the CV template so the pair reads as a set.

### Opening (2-3 sentences)
State the role, where it was found, and a one-line hook on why this specific company. Avoid "I am writing to apply for…" — start with something specific.

Good opening:
> "I've been following [Company]'s work on [specific product/feature/value] since [moment], and the [Role Title] posting feels like a natural next step from my recent work at [Previous Company]."

Bad opening:
> "I am writing to apply for the position of Frontend Developer at your esteemed company."

### Middle 1 — Why this candidate (5-7 sentences)
Pick **one** thread from the CV that maps cleanly to the role's must-haves. Tell that thread as a short story rather than re-listing CV bullets. Concrete project + what was learned + how it applies.

Don't recap the whole CV. The reader has it. The cover letter's job is to add narrative the CV can't.

If the master CV includes a reference quote that maps directly to a JD must-have, weave it in naturally (e.g. "My manager described me as 'super reliable and keen to learn'"). Don't force it if it doesn't fit, and only use quotes the user has supplied.

### Middle 2 — Why this company (3-5 sentences)
Interest in the role's specific stack or responsibilities is a perfectly valid reason. Not every company deserves performative enthusiasm.

When possible, demonstrate having actually looked at the company. Reference a product, a recent post, a value, a public talk by an engineer there, anything specific. Generic praise ("I love your mission") reads as filler.

If genuinely nothing specific can be said, ask the user for one detail rather than making something up.

### Closing (1-2 sentences)
Forward-looking, no apology, no "thank you for your time" filler. Mention availability for next steps.

## Tone Matching

Match the JD's tone. A casual JD with emojis allows a slightly warmer cover letter. A corporate JD wants a tighter, more formal one. Never go more casual than the JD signals.

## Honesty Boundaries

The cover letter doesn't permit invention. If the user has no specific reason for wanting this company beyond "I need a job," ask them for one — even one sentence of genuine interest beats fabricated enthusiasm.

If nothing genuine surfaces, default to truthful framing: interest in the role's specific responsibilities or stack, rather than performative passion for the company.

## Anti-Patterns

- "I am a hardworking, passionate, motivated…" — adjective stacking, no information.
- Restating CV bullets verbatim.
- "I would be a great fit because…" followed by generic claims.
- Over-explaining gaps or weaknesses unprompted.
- Closing with "I look forward to hearing from you" — fine, but not as the only closing line.
- Em dashes. Use commas, colons, or parentheses.
- "I'm passionate about..." — vague, overused.
- "I would love the opportunity to..." — begging energy.
- "Thank you for considering my application" — filler closing.
- "I'm a fast learner" — show it with examples instead.
- "Despite my lack of experience..." — never apologize for gaps.
- Any buzzwords: "leverage," "synergy," "passionate about."

## Language

Match the language of the JD. Swedish companies with Swedish-language postings get a Swedish cover letter. English for international or English-language postings. Same warm, direct tone in both.

## Pre-send Checklist

Before finalizing, verify:
1. Did I name their product or company specifically?
2. Did I mirror at least one phrase from their posting?
3. Did I include at least one concrete number?

## Output

Generate the cover letter as a separate file using the same template's header style. Filename pattern: `[FirstnameLastname]_CoverLetter_[Company]_[Role].pdf`, matching the CV's filename pattern.
