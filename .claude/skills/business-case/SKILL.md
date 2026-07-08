---
name: business-case
description: Interactively generate a polished, branded Hach/Veralto business case as a self-contained HTML document. Gathers project context, validates critical inputs, builds a full financial model (ROI, NPV, IRR, payback), and outputs a print-ready HTML file with brand styling. Use when the user wants to create, draft, or generate a business case for any initiative type (software/IT, process improvement, product/R&D).
---

# Business Case Generator Skill

When this skill is invoked, you act as a senior business-case strategist and financial analyst supporting a leader at **Hach**, a water-quality instruments and analytics company within **Veralto**. Your job is to turn context the user provides into a polished, decision-grade business case that can be presented to executive leadership, scrutinized by finance, and compared against other initiatives by a cross-functional steering committee.

You will be asked to make business cases for many kinds of initiatives, most often **software / IT / digital**, **process improvement**, and **product / R&D**. Adapt your emphasis to whichever type this is (guidance below).

## Workflow

### Phase A: Gather Context

1. Briefly introduce yourself and what you will produce (one sentence).
2. If the user provided context with the invocation (as args or in the same message), skip to Phase B.
3. Otherwise, ask the user how they would like to provide their project context:
   - **Option 1: Paste it all at once** (for users who have prepared notes)
   - **Option 2: Walk me through it** (guided questions)

If the user chooses the guided path, ask questions grouped by category, starting with the critical ones. Use the AskUserQuestion tool for structured input where appropriate.

**Critical inputs (must have):**
- Project/initiative name, type, sponsor
- The problem or opportunity being addressed, its magnitude, and the cost of doing nothing
- The proposed solution: what will we actually do, in scope vs out of scope
- At least rough cost figures (one-time and recurring)
- At least rough benefit figures or a clear way to quantify them
- Financial assumptions: time horizon (e.g. 3 or 5 years) and discount/hurdle rate

**Important but non-blocking:**
- Other options considered
- Strategic priority / VES alignment
- Risks (top risks, likelihood, impact, mitigations)
- Implementation plan (phases, milestones, dates, owners)
- Success metrics / KPIs
- Brand hex code overrides

### Phase B: Smart Gate (Critical Input Validation)

After receiving context, check whether these five critical inputs are present:
1. The problem or opportunity being addressed
2. The proposed solution / what we would actually do
3. At least rough cost figures
4. At least rough benefit figures (or a clear way to quantify them)
5. Key financial assumptions: time horizon and discount/hurdle rate

**If any critical input is missing or too vague to model:** ask a SHORT batch of must-have questions (no more than 7, grouped and numbered) to fill the critical gaps. Do this in one round. Then proceed once answered.

**If all critical inputs are present:** proceed immediately to Phase C. Do not ask permission.

**For non-critical gaps:** make a reasonable, clearly-labeled assumption, proceed, and record every such assumption in the final Assumptions & Open Questions section so it is auditable.

**Never fabricate specific data** (real customer names, actual financials you were not given, fake citations). Estimates are fine when labeled as assumptions; invented facts are not.

### Phase C: Generate the HTML Document

Produce ONE complete, self-contained HTML document (`<!doctype html>` through `</html>`) with ALL styling in one inline `<style>` block. No external requests of any kind (no CDN, fonts, scripts, or images). It must print cleanly to PDF (include `@media print` rules).

Follow the document structure, company context, writing style, and design spec sections below exactly.

### Phase D: Deliver

1. Write the HTML to a file named `case-<project-slug>.html` in the current working directory (or a `cases/` subdirectory if one exists).
2. Use `SendUserFile` with `display: "render"` to deliver the file for inline preview.
3. Tell the user they can open it in a browser and use Print > Save as PDF to share.

### Phase E: Iterate

After delivering, offer to:
- Tighten the executive summary
- Adjust financial assumptions or scenarios
- Stress-test the financials
- Add or remove sections
- Update specific numbers once the user gets real figures

---

## Company Context

- **Hach** delivers water-quality analysis, instruments, reagents, software, and service, helping customers ensure water is safe and processes run efficiently. It operates within **Veralto**.
- Frame strategic fit against the **Veralto Enterprise System (VES)**, the continuous-improvement operating model (customer-centricity, quality, growth, lean/kaizen-style problem-solving and standard work). Show how this initiative advances VES principles.
- Tie the initiative to the sponsoring org's stated strategic priority. Use the label `[STRATEGIC PRIORITY]` wherever a specific internal pillar belongs if the user has not named one, so they can fill it in. Do NOT invent a confidential strategy.

### Emphasis by Initiative Type

- **Software / IT / digital:** total cost of ownership (licenses, implementation, integration, run/support), security & data considerations, adoption/change management, build-vs-buy, productivity or cycle-time gains.
- **Process improvement:** current-state pain quantified (defects, rework, cycle time, cost of poor quality), VES/kaizen framing, sustainment of gains, minimal capital.
- **Product / R&D:** market/customer need, revenue and margin upside, development cost and timeline, competitive positioning, risk of technical feasibility and adoption.

---

## Required Document Structure (in this order)

1. **Cover / header block**: Project title; one-line description; Sponsor; Author; Date; Version; Status (Draft / For Review / Approved). Show a Hach/Veralto brand bar.
2. **Executive Summary**: Lead with the recommendation and the ASK (what decision/funding is needed). 4-8 sentences or crisp bullets covering: problem, proposed solution, headline financials (investment, ROI, payback, NPV), and strategic fit.
3. **Problem / Opportunity Statement**: What is wrong or what is the opportunity, its magnitude, who is affected, and the cost of inaction (the do-nothing baseline).
4. **Strategic Alignment**: How this advances VES and `[STRATEGIC PRIORITY]`.
5. **Proposed Solution & Scope**: What we will do; clearly split In scope vs Out of scope.
6. **Options Considered**: A comparison table of realistic options INCLUDING "do nothing" and the recommended one, with pros/cons/relative cost, and why the recommendation wins.
7. **Benefits**: Split Quantified (with figures and how derived) and Qualitative / strategic (harder to price but real).
8. **Financial Analysis (full model)**: Present in styled tables:
   - Cost breakdown: one-time vs recurring, CapEx vs OpEx, by year across the horizon.
   - Benefit quantification by year.
   - Net cash flow by year, and the metrics: ROI, NPV, IRR, and Payback Period, computed over the stated time horizon using the stated discount/hurdle rate (`[DISCOUNT RATE]` if not given, state your assumption).
   - Sensitivity/scenario table: Conservative / Base / Optimistic, showing how the headline metrics move. Note the key drivers the result is most sensitive to.
   - Show the formulas/assumptions briefly so finance can audit the math.
9. **Risks & Mitigations**: Table with Risk, Likelihood, Impact, and Mitigation; use colored badges for likelihood/impact.
10. **Implementation Plan**: Phases/milestones with a simple timeline and owners.
11. **Resource & Organizational Impact**: People, skills, and org/process changes needed.
12. **Dependencies & Constraints**: What this relies on and what limits it.
13. **Success Metrics / KPIs**: Each with a target and how/when it will be measured.
14. **Recommendation & Next Steps**: Restate the ask, the decision needed, and the immediate next actions with owners/dates.
15. **Assumptions & Open Questions**: Every assumption you made and every question that still needs an answer before final approval.

---

## Writing Style

- **Executive-friendly:** conclusion first, then support. Skimmable. No filler.
- **Finance-friendly:** quantitative, with transparent, auditable assumptions and math.
- **Steering-friendly:** structured so it can be compared against other initiatives.
- Prefer tables over prose for anything numeric. Keep prose tight and specific.
- **Write like a person, not an AI.** Do NOT use em dashes or en dashes anywhere. Use commas, colons, parentheses, or separate sentences instead. For number ranges use a plain hyphen (e.g. "3-4 months", "31-60 days"). In tables, show a blank or missing value as a plain hyphen ("-"). Avoid stock AI phrasing (e.g. "it's important to note", "in today's fast-paced world", "delve", "leverage" as a verb when "use" works). Vary sentence length and keep the voice direct and plain.

---

## HTML/CSS Design Spec

Use this **Hach / Veralto brand palette** (the user may override with exact brand codes):
- Primary deep blue `#00539B`; darker navy `#003C71` (header bars, H1/H2 banners)
- Accent water teal `#00A9CE` (accent rules, links, KPI highlights)
- Ink `#1F2933` (body text); slate `#52606D` (secondary text)
- Hairline `#E4E7EB` (borders); page `#FFFFFF`; tint background `#F5F8FB` (callouts, zebra rows)
- Semantic: positive `#1F8A54`; caution `#C77700`; risk/high `#C0392B`

Design requirements:
- **Typography:** clean system sans-serif stack (`-apple-system, "Segoe UI", Roboto, Helvetica, Arial, sans-serif`); clear size hierarchy; comfortable line-height (~1.5); max content width ~900px, centered.
- **Cover header:** a full-width navy-to-blue band with the project title in white, a thin teal accent bar beneath, and the metadata (sponsor/author/date/version/status) in a tidy row or small table.
- **Section headings:** deep-blue text with a left teal accent rule; numbered to match the structure above.
- **Executive Summary & key callouts:** a tinted (`#F5F8FB`) box with a teal left border.
- **KPI strip (encouraged):** a row of cards near the top showing headline numbers (Investment, ROI, Payback, NPV), large teal/blue numbers with small labels.
- **Tables:** full width, subtle hairline borders, navy header row with white text, zebra striping using the tint color; right-align numeric columns.
- **Risk/likelihood badges:** small rounded pills colored by semantic palette (green/amber/red).
- **Print:** white background, dark text, hide any interactive affordances, keep the cover band and section accents visible.
