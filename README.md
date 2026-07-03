# Business Case Documentation

A reusable AI prompt for producing strong, on-brand **business cases** for any project or
initiative — software/IT, process improvement, product/R&D, and beyond. Paste the prompt
into your AI assistant along with your project context, and it generates a complete,
decision-grade business case as a **single self-contained HTML file**, styled in the
Hach / Veralto brand palette and ready to present or print to PDF.

## What's in here

| File | Purpose |
|------|---------|
| [`business-case-prompt.md`](business-case-prompt.md) | **The reusable prompt.** Copy the fenced block and paste it into your AI. |
| [`input-checklist.md`](input-checklist.md) | What to gather *before* you run the prompt, so the draft comes out strong. |
| `README.md` | This guide. |

## How to use it

1. **Gather your inputs.** Skim [`input-checklist.md`](input-checklist.md) and jot down
   what you know: the problem, the proposed solution, rough costs and benefits, and your
   financial assumptions (time horizon, discount/hurdle rate).
2. **Copy the prompt.** Open [`business-case-prompt.md`](business-case-prompt.md) and copy
   everything inside the ```` ```text ```` code fence.
3. **Paste it into your AI assistant**, then paste your project context underneath it.
4. **Run it.**
   - If you provided the critical inputs, the AI drafts the full business case in one pass.
   - If something critical is missing, it first asks a **short batch of must-have
     questions**. Answer them, and it produces the document.
5. **Save & share.** The output is a complete HTML document. Save it as
   `case-<project>.html`, open it in any browser, then **Print → Save as PDF** to
   distribute.

## What the business case contains

A full, decision-grade document: executive summary and the ask up front, problem/
opportunity (with cost of inaction), strategic alignment to the **Veralto Enterprise
System (VES)**, proposed solution and scope, options considered, quantified and
qualitative benefits, a **full financial model** (cost breakdown, ROI, NPV, IRR, payback,
and a conservative/base/optimistic sensitivity analysis), risks and mitigations,
implementation plan, resource/org impact, dependencies, success metrics/KPIs, the
recommendation, and an audit trail of assumptions.

## Branding

The prompt bakes in a Hach / Veralto-inspired palette (deep blues and water-tone teal)
with brand banners, styled financial tables, KPI cards, and print-friendly layout.

The hex values in the prompt are **sensible approximations**. If you have your official
Hach/Veralto brand guidelines, paste the exact hex codes into your context and tell the
AI to use them instead of the defaults — everything else stays the same.

## Tips

- **More input = better output.** Filling in more of the checklist means fewer clarifying
  questions and a sharper first draft.
- **Iterate.** After the first draft, ask the AI to tighten the executive summary, stress-
  test the financials, or adjust the scenario assumptions.
- **Keep your finished cases.** Consider saving generated documents under a `cases/`
  folder in this repo so you build a searchable library over time.
