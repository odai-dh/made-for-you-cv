# Eval results: plugin (0.4.0) vs plain Claude

Three fictional cases (see README.md), one run each, same model, same prompts. "Plain Claude" had no skill and no plugin files. Tokens and time are the totals reported for each run (subagent usage), so treat them as indicative, not exact: n=1 per cell.

| | Plain Claude | Plugin, first 0.4.0 draft | Plugin, final 0.4.0 |
|---|---|---|---|
| Objective checks passed | 25 / 26 (96%) | 26 / 26 (100%) | 26 / 26 (100%) |
| Tokens, mean per run | 59,325 | 73,022 (+23%) | 66,085 (+11%) |
| Time, mean per run | 33.0 s | 50.7 s (+53%) | 35.9 s (+9%) |

Per case (tokens / seconds), plain Claude, first draft, final:

| Case | Plain Claude | First draft | Final |
|---|---|---|---|
| a, junior frontend | 58,130 / 25.9 | 70,576 / 42.5 | 64,617 / 30.5 |
| b, UK analyst, portal | 59,580 / 32.3 | 69,883 / 41.4 | 64,670 / 32.7 |
| c, Swedish switcher | 60,265 / 40.9 | 78,606 / 68.1 | 68,967 / 44.4 |

What the checks found: both arms passed every honesty and privacy check (no invented Playwright/Synapse/Salesforce, no date of birth, marital status, address or personnummer, honest header titles, no em dashes, 1 page). The only difference was the portal case: the plugin delivered the Word copy for the careers-portal application, plain Claude delivered only a PDF. The plugin also delivered a plain-text copy and the reusable `master_cv.md` in every run; plain Claude did not, so the plugin's runs do more work for roughly the same cost.

How the draft became the final version: the first draft cost 23% more tokens and 53% more time, mostly from separate script calls, three reference reads and PNG previews. `make_cv.py` (one call for PDF, text and Word), inline data keys and conditional previews brought it to +11% and +9%.

Checker corrections made after looking at the first results, all false positives rather than behavior changes: letter-spaced PDF headings ("E R FA R E N H E T") are rejoined before matching Swedish headings; "ansökan till Customer Success Manager" in a header names the target role and does not claim the title; "Jag har inte arbetat med Salesforce" is an honest gap statement, not a claim. A real claim is still flagged. Before these corrections plain Claude scored 23 / 26 and the final plugin run 25 / 26.

Not measured: first-run quality as judged by a human reader, repeat applications with a master CV, and other languages or templates.

## 0.4.1: repeat use (case d) and closing lines

Case d: the master CV already exists in the conversation, the user pastes a second ad. Same single-run caveat as above. "Plain Claude" saw the same conversation, including the earlier keep-it and several-ads tips.

| Case d, 15 checks | Checks passed | Tokens | Time |
|---|---|---|---|
| Plain Claude | 12 / 15 | 72,211 | 36.6 s |
| Plugin, first wording of 0.4.1 | 14 / 15 | 76,786 | 69.3 s |
| Plugin, final 0.4.1 | 15 / 15 | 76,115 | 26.4 s |

Both arms asked no questions, delivered a one-page PDF, kept honest titles and invented nothing, and neither repeated the Project or several-ads tip. Plain Claude failed on the message: a 197-word summary (limit 120), no next-application line, and a closing that was not the next-application line. The first wording of the plugin still carried the first-run "This is a ... role, generating now" recap (156 words); the fix made the repeat run skip that recap and end with the file list, a 2-3 line summary and the next-application line. Time differences between runs of the same version are large (69 s vs 26 s at about the same tokens), so read the time column loosely.

First run (case a, 13 checks, plugin only): 13 / 13 after the fix, at 78,026 tokens and 37.4 s. The next-application line is last and the Project tip and the several-ads tip each appear once. The first wording put the next-application line before the template and "to make it stronger" lists, which a "last line" check caught; the wording now puts the closing lines last.

Checker notes: the message checks (no questions, summary length, next-application line, tips) were written before the runs; the "last line" check was added after the first runs showed the ordering problem, and the several-ads pattern was widened after "several job ads" was missed. Controls in the smoke test confirm each message check catches a bad message.
