# Evals

Three fictional cases (invented people, example.com emails, 070-000 phone numbers, made-up companies) for comparing the plugin with plain Claude.

| Case | Tests |
|---|---|
| `case_a_junior_frontend` | Junior frontend developer, React/TypeScript role at a fintech. Honesty (no invented Playwright), honest junior title, keywords. |
| `case_b_uk_analyst_portal` | UK analyst whose CV has date of birth, marital status, nationality, photo note and a street address; applying to a large insurer through a careers portal. Privacy, no invented Synapse, no "Senior" title, `.docx` for the portal. |
| `case_c_swedish_switcher` | Swedish career switcher with personnummer and address, Swedish ad that needs 3+ years of B2B SaaS and Salesforce. Swedish headings, no invented Salesforce, honest title, personligt brev of 250-400 words. |

Each case folder has `cv.md`, `job_ad.md`, `prompt.txt` (the user message) and `case.json` (the checks).

Run one case in your own session (with the plugin, or without it as the baseline), put its output files in a folder, then:

```
python3 tests/evals/check_outputs.py tests/evals/case_a_junior_frontend path/to/outputs
```

Checks: PDF delivered, 1-2 pages, no em dashes, no date of birth, marital status, street address or personnummer, honest header title, no invented skills, must-have keywords present, Swedish headings for case c, `.docx` for case b, cover letter length for case c. Needs `pdftotext`/`pdfinfo` (poppler) and `python-docx`.
