#!/usr/bin/env python3
"""Generate a branded Word (.docx) version of the Commission Accrual business case.

Written without em/en dashes to read as human-authored. The prose here is kept in
sync with cases/case-commission-accrual-automation.html; edit both if you change wording.

Usage:
    pip install python-docx
    python scripts/build_docx.py
Output is written to cases/case-commission-accrual-automation.docx (relative to the
repo root, regardless of where you run it from).
"""
import os
from docx import Document
from docx.shared import Pt, RGBColor, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

# Hach / Veralto brand palette (approximate defaults)
BLUE   = RGBColor(0x00, 0x53, 0x9B)
NAVY   = RGBColor(0x00, 0x3C, 0x71)
TEAL   = RGBColor(0x00, 0xA9, 0xCE)
INK    = RGBColor(0x1F, 0x29, 0x33)
SLATE  = RGBColor(0x52, 0x60, 0x6D)
WHITE  = RGBColor(0xFF, 0xFF, 0xFF)
CAUT   = RGBColor(0xC7, 0x77, 0x00)
POS    = RGBColor(0x1F, 0x8A, 0x54)
RISK   = RGBColor(0xC0, 0x39, 0x2B)
NAVY_H = "003C71"; TINT_H = "F5F8FB"; GREEN_H = "E7F6EA"; WARN_H = "FDF6EC"

doc = Document()
st = doc.styles['Normal']
st.font.name = 'Calibri'; st.font.size = Pt(10.5); st.font.color.rgb = INK


def shade(cell, hexfill):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd'); shd.set(qn('w:val'), 'clear'); shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), hexfill); tcPr.append(shd)


def run(p, text, *, color=INK, bold=False, size=10.5, italic=False):
    r = p.add_run(text); r.bold = bold; r.italic = italic
    r.font.size = Pt(size); r.font.color.rgb = color
    return r


def spacer(pts=4):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(pts); p.paragraph_format.space_before = Pt(0)
    return p


def h2(num, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(14); p.paragraph_format.space_after = Pt(2)
    run(p, f"{num}  ", color=TEAL, bold=True, size=14)
    run(p, text, color=BLUE, bold=True, size=14)
    pPr = p._p.get_or_add_pPr(); pbdr = OxmlElement('w:pBdr'); bottom = OxmlElement('w:bottom')
    bottom.set(qn('w:val'), 'single'); bottom.set(qn('w:sz'), '6'); bottom.set(qn('w:space'), '2')
    bottom.set(qn('w:color'), '00A9CE'); pbdr.append(bottom); pPr.append(pbdr)
    return p


def h3(text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(8); p.paragraph_format.space_after = Pt(1)
    run(p, text, color=NAVY, bold=True, size=11)
    return p


def body(text, bullet=False):
    p = doc.add_paragraph(style='List Bullet' if bullet else None)
    p.paragraph_format.space_after = Pt(3)
    if text:
        run(p, text)
    return p


def make_table(headers, rows, numeric=(), rec_rows=(), widths=None):
    t = doc.add_table(rows=1, cols=len(headers)); t.alignment = WD_TABLE_ALIGNMENT.CENTER
    t.style = 'Table Grid'
    hdr = t.rows[0].cells
    for i, htext in enumerate(headers):
        shade(hdr[i], NAVY_H)
        p = hdr[i].paragraphs[0]
        p.paragraph_format.space_after = Pt(1); p.paragraph_format.space_before = Pt(1)
        if i in numeric:
            p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        run(p, htext, color=WHITE, bold=True, size=9.5)
    for ri, rowdata in enumerate(rows):
        cells = t.add_row().cells
        is_rec = ri in rec_rows
        for ci, val in enumerate(rowdata):
            if is_rec:
                shade(cells[ci], GREEN_H)
            elif ri % 2 == 1:
                shade(cells[ci], TINT_H)
            p = cells[ci].paragraphs[0]
            p.paragraph_format.space_after = Pt(1); p.paragraph_format.space_before = Pt(1)
            if ci in numeric:
                p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
            bold = (ci == 0 and is_rec)
            run(p, str(val), size=9.5, bold=bold)
    if widths:
        for row in t.rows:
            for ci, w in enumerate(widths):
                row.cells[ci].width = Inches(w)
    spacer(6)
    return t


def callout(title, text, warn=False):
    tbl = doc.add_table(rows=1, cols=1); tbl.style = None
    cell = tbl.rows[0].cells[0]; shade(cell, WARN_H if warn else TINT_H)
    tcPr = cell._tc.get_or_add_tcPr(); borders = OxmlElement('w:tcBorders')
    left = OxmlElement('w:left'); left.set(qn('w:val'), 'single'); left.set(qn('w:sz'), '24')
    left.set(qn('w:space'), '0'); left.set(qn('w:color'), 'C77700' if warn else '00A9CE')
    borders.append(left); tcPr.append(borders)
    p = cell.paragraphs[0]; p.paragraph_format.space_after = Pt(2)
    run(p, title, color=(CAUT if warn else NAVY), bold=True, size=10.5)
    p2 = cell.add_paragraph(); run(p2, text, size=10)
    spacer(6)


def kpi_strip(items):
    t = doc.add_table(rows=2, cols=len(items)); t.alignment = WD_TABLE_ALIGNMENT.CENTER
    for i, (num, lab) in enumerate(items):
        top = t.rows[0].cells[i]; bot = t.rows[1].cells[i]
        shade(top, TINT_H); shade(bot, TINT_H)
        pn = top.paragraphs[0]; pn.alignment = WD_ALIGN_PARAGRAPH.CENTER
        pn.paragraph_format.space_after = Pt(0)
        run(pn, num, color=BLUE, bold=True, size=16)
        pl = bot.paragraphs[0]; pl.alignment = WD_ALIGN_PARAGRAPH.CENTER
        pl.paragraph_format.space_before = Pt(0)
        run(pl, lab, color=SLATE, size=8.5)
    spacer(8)


# ===== COVER =====
cov = doc.add_table(rows=1, cols=1); cell = cov.rows[0].cells[0]; shade(cell, NAVY_H)
p = cell.paragraphs[0]; p.paragraph_format.space_after = Pt(2)
run(p, "BUSINESS CASE  ·  FINANCE AUTOMATION", color=RGBColor(0xBF, 0xE0, 0xF0), bold=True, size=9)
p2 = cell.add_paragraph(); p2.paragraph_format.space_after = Pt(3)
run(p2, "Commission Accrual Automation", color=WHITE, bold=True, size=22)
p3 = cell.add_paragraph()
run(p3, "Solution 1: replacing the manual monthly commission accrual with an automated "
        "process that hands Accounting a ready-to-book workbook, keeps the audit evidence "
        "attached, and gives leadership a clear view of the numbers.",
        color=RGBColor(0xDC, 0xEC, 0xF6), size=10.5)
pa = doc.add_paragraph(); pa.paragraph_format.space_after = Pt(6)
pPr = pa._p.get_or_add_pPr(); pbdr = OxmlElement('w:pBdr'); bottom = OxmlElement('w:bottom')
bottom.set(qn('w:val'), 'single'); bottom.set(qn('w:sz'), '18'); bottom.set(qn('w:space'), '1')
bottom.set(qn('w:color'), '00A9CE'); pbdr.append(bottom); pPr.append(pbdr)

meta = [("Sponsor", "[Finance / Commercial Analytics Leadership]"),
        ("Author", "Tanushree Arora"),
        ("Process Owner", "Stephen (Accounting)"),
        ("Date", "3 July 2026"), ("Version", "1.0"),
        ("Status", "Draft / For Review")]
mt = doc.add_table(rows=2, cols=3)
for i, (k, v) in enumerate(meta):
    r, c = divmod(i, 3)
    cellk = mt.rows[r].cells[c]
    pp = cellk.paragraphs[0]; pp.paragraph_format.space_after = Pt(0)
    run(pp, k.upper(), color=SLATE, size=7.5, bold=True)
    pv = cellk.add_paragraph(); pv.paragraph_format.space_before = Pt(0)
    run(pv, v, color=INK, bold=True, size=9.5)
spacer(8)

# ===== 1 EXEC SUMMARY =====
h2(1, "Executive Summary")
p = body(""); run(p, "Recommendation: ", bold=True, color=NAVY)
run(p, "Approve building an automated Commission Accrual solution (Solution 1) to "
       "replace today's manual, Excel-based routine. It takes out the fragile pivot "
       "tables and copy-paste steps and hands Accounting a workbook they can book "
       "straight away, with the audit evidence kept alongside it. Finance leadership "
       "gets a clear month-end picture without chasing it.")
p = body(""); run(p, "The ask: ", bold=True, color=NAVY)
run(p, "Fund a one-time build of about $45,000, plus roughly $4,000 a year to run it. "
       "The work should take three to four months. All dollar figures are estimates "
       "pending validated inputs.")
kpi_strip([("~$45K", "One-time investment"), ("~$26K", "Net benefit / yr"),
           ("~$54K", "5-yr NPV @10%"), ("~1.7 yr", "Payback"), ("~50%", "IRR")])
body("The dollars matter, but they are not the whole story. The bigger wins are harder "
     "to put a number on: the accrual becomes easier to audit, the risk of a "
     "misstatement drops, and leadership finally gets its reporting in a consistent "
     "format. Today the work eats several senior-analyst days a month and leans on "
     "spreadsheets that break whenever the row counts change. Automating it turns that "
     "monthly scramble into a repeatable output Accounting can book directly.")
callout("Note on financials",
        "Every dollar figure here is a placeholder estimate, put in so the case reads as "
        "a finished document. Before it goes forward for approval, swap them for real "
        "numbers: a build quote, the fully-loaded analyst rate, the hours the process "
        "actually takes today, and the discount rate Finance wants used. Section 14 lists "
        "what still needs confirming.", warn=True)

# ===== 2 PROBLEM =====
h2(2, "Problem and Opportunity")
body("Each month, Commercial Analytics publishes the commission reports and Stephen gets "
     "a note that they are ready. He downloads the files and builds the accrual by hand "
     "in Excel, working from two workbooks: Commissions Payment Made and Commissions "
     "Payment Remaining. Getting to a workbook Accounting can book takes a long list of "
     "manual steps:")
for x in ["Opening the prior month's workbook and copying detailed data and Oracle BI screenshot sheets",
          "Refreshing pivot tables and repairing formulas broken by changing row counts",
          "Calculating accruals, forecasting the final three business days, and preparing Cost Center and Account summaries",
          "Sending the completed workbook to Accounting for journal booking"]:
    body(x, bullet=True)
h3("Pain points")
for x in ["Manual copy/paste of detailed reports and screenshot sheets",
          "Heavy dependence on fragile Excel pivot tables that shift monthly as row counts vary",
          "Formula references break after each refresh",
          "Manual reconciliation, data validation, and three-day forecasting",
          "Large, slow Excel files and no executive-level reporting",
          "Time spent maintaining spreadsheets instead of analyzing financials, with elevated error risk on a booked accrual"]:
    body(x, bullet=True)
callout("Cost of inaction (do-nothing baseline)",
        "Leave it as is and the process keeps taking an estimated three to four "
        "senior-analyst days a month. The errors also land on a number that is "
        "financially material, there is no consistent audit trail, and leadership has no "
        "real reporting to look at. It gets more fragile as volumes grow, and almost all "
        "of the know-how sits with one person.")

# ===== 3 STRATEGIC =====
h2(3, "Strategic Alignment")
body("The initiative directly advances Veralto Enterprise System (VES) principles:")
for x in ["Continuous improvement and lean: eliminates repetitive, low-value manual work and standardizes a recurring close activity.",
          "Quality and problem-solving: removes fragile pivot/formula dependencies that are a root cause of month-end errors.",
          "Customer-centricity (internal): delivers accounting-ready output and clear executive visibility for Finance stakeholders."]:
    body(x, bullet=True)
body("It should also ladder up to [STRATEGIC PRIORITY], whichever priority your org is "
     "tracking this against, for example finance transformation, a faster close, or "
     "tighter controls. Drop in the right one.")

# ===== 4 SOLUTION =====
h2(4, "Proposed Solution and Scope")
body("Build a tool that takes in the two commission workbooks, checks and maps the data, "
     "applies the commission logic already in use, and writes out a single new workbook "
     "that is ready for Accounting. It never touches the source files.")
h3("Core capabilities")
for x in ["Guided workbook mapping: proposes which file is Payment Made vs Payment Remaining and requires user confirmation before processing. It never assumes the mapping.",
          "Automated validation: required columns, missing Cost Centers or Bill-To Account Numbers, blank/invalid/negative values, and duplicates; reports imported row counts and whether screenshots are included.",
          "Fiscal-aware three-day forecast: auto-derives the fiscal divisor from the Fiscal Period (four-week uses 17, five-week uses 22). The user is never asked which divisor to use, only for the Fiscal Period if it cannot be determined automatically.",
          "Aging analysis on Payment Remaining (Current, 31 to 60, 61 to 90, 91 to 180, 181 to 365, Over 365 days) for visibility into outstanding liabilities.",
          "Audit evidence preservation: Oracle BI screenshot sheets copied into the output with original formatting. No OCR, no interpretation, no row-count comparison.",
          "Executive dashboard and AI commentary: KPI cards, accrual by month, top cost centers/accounts, Payment Made vs Remaining split, aging distribution, and a data-supported narrative (no speculation). Charts use summarized data only."]:
    body(x, bullet=True)
h3("Output workbook (12 sheets)")
body("Executive Summary, Configuration, Month-Year Summary, Cost Center Summary, "
     "Cost Center plus Account Summary (primary booking view), Account Summary, Aging "
     "Summary, Payment Made Detail, Payment Remaining Detail, Validation Report, "
     "Audit Evidence, and Executive Dashboard.")
h3("Key business logic")
make_table(["Measure", "Definition"],
    [["Payment Made Total", "Sum of Commission Amount (payable now, customer payment received)"],
     ["Payment Remaining Total", "Sum of Commission Amount (future liability, payment not yet received)"],
     ["Estimated Commission", "(Payment Made Total / Fiscal Divisor) x 3 remaining business days"],
     ["Final Accrual", "Payment Made + Payment Remaining + Estimated Commission"]],
    widths=[2.0, 4.5])
h3("In scope (Solution 1)")
for x in ["Payment Made and Payment Remaining workbooks",
          "Validation, mapping confirmation, three-day forecasting",
          "All summaries, aging, dashboard, commentary",
          "Audit-evidence preservation and accounting-ready output workbook"]:
    body(x, bullet=True)
h3("Out of scope (goes to Solution 2)")
for x in ["GL Supplemental reporting",
          "Vendor payment analysis and views (by vendor, cost center, account)",
          "JE Source filtering (exclude manual journal entries)",
          "External commission-vendor payment visibility"]:
    body(x, bullet=True)

# ===== 5 OPTIONS =====
h2(5, "Options Considered")
make_table(["Option", "Pros", "Cons", "Rel. cost"],
    [["A. Do nothing (status quo)", "No investment", "Ongoing manual effort, error risk, no audit trail or executive reporting; worsens with volume", "None"],
     ["B. Improve Excel (templates/macros)", "Low cost; familiar", "Still pivot/formula-dependent and fragile; limited validation, dashboard, or audit control", "Low"],
     ["C. Purpose-built automation (Recommended)", "Removes manual work and pivots; built-in validation, forecasting, aging, dashboard, audit preservation; accounting-ready", "Requires development and UAT investment", "Medium"],
     ["D. Commercial commission software", "Vendor-supported, feature-rich", "High cost and licensing; heavy integration; likely over-scoped", "High"]],
    numeric={3}, rec_rows={2}, widths=[1.7, 2.2, 2.2, 0.7])
p = body(""); run(p, "Why C wins: ", bold=True, color=NAVY)
run(p, "it fixes the exact things that break today (copy/paste, pivot refreshes, "
       "hand-done forecasting) and still delivers the validation, audit trail, and "
       "executive views we need, without the cost and integration effort of a full "
       "commercial platform.")

# ===== 6 BENEFITS =====
h2(6, "Benefits")
h3("Quantified (estimate)")
make_table(["Benefit", "Basis", "Annual value"],
    [["Analyst time saved", "About 28 hrs/month at $65 fully-loaded rate (about 336 hrs/yr)", "$21,840"],
     ["Error / rework reduction", "Fewer accrual corrections and reconciliation cycles", "$8,160"],
     ["Total quantified annual benefit", "", "$30,000"]],
    numeric={2}, rec_rows={2}, widths=[2.0, 3.4, 1.1])
h3("Qualitative / strategic")
for x in ["Improved audit readiness and standardized evidence; reduced financial-misstatement risk",
          "Consistent, repeatable month-end output; executive-level visibility and trend analysis",
          "Reduced key-person dependency; analyst time redirected to analysis",
          "Scalable as transaction volume grows; faster, lower-stress close"]:
    body(x, bullet=True)

# ===== 7 FINANCIAL =====
h2(7, "Financial Analysis")
p = body(""); run(p, "Base case. Horizon: 5 years. Discount / hurdle rate: 10% ", color=SLATE, size=9.5)
run(p, "[confirm with Finance]. All figures are estimates.", color=CAUT, size=9.5, bold=True)
make_table(["Cash flow ($)", "Year 0", "Yr 1", "Yr 2", "Yr 3", "Yr 4", "Yr 5"],
    [["Implementation (one-time)", "(45,000)", "-", "-", "-", "-", "-"],
     ["Gross annual benefit", "-", "30,000", "30,000", "30,000", "30,000", "30,000"],
     ["Recurring cost", "-", "(4,000)", "(4,000)", "(4,000)", "(4,000)", "(4,000)"],
     ["Net cash flow", "(45,000)", "26,000", "26,000", "26,000", "26,000", "26,000"],
     ["Cumulative net", "(45,000)", "(19,000)", "7,000", "33,000", "59,000", "85,000"],
     ["Discount factor @10%", "1.000", "0.909", "0.826", "0.751", "0.683", "0.621"],
     ["Present value", "(45,000)", "23,636", "21,488", "19,535", "17,759", "16,144"],
     ["Cumulative PV (NPV build)", "(45,000)", "(21,364)", "124", "19,659", "37,418", "53,562"]],
    numeric={1, 2, 3, 4, 5, 6}, rec_rows={3, 7})
kpi_strip([("$53.6K", "NPV (5-yr,10%)"), ("~50%", "IRR"), ("1.7 yr", "Simple payback"),
           ("~2.0 yr", "Disc. payback"), ("189%", "5-yr ROI")])
body("ROI equals (5-yr net benefit of $130K less investment of $45K) divided by $45K, "
     "which is 189%. Investment is recovered partway through Year 2.")
h3("Sensitivity / scenario analysis")
make_table(["Scenario", "Investment", "Net benefit/yr", "NPV (10%,5yr)", "IRR", "Payback"],
    [["Conservative", "$60,000", "$13,400", "($9,200)", "~4%", "4.5 yr"],
     ["Base", "$45,000", "$26,000", "$53,600", "~50%", "1.7 yr"],
     ["Optimistic", "$35,000", "$50,600", "$156,800", "over 140%", "0.7 yr"]],
    numeric={1, 2, 3, 4, 5}, rec_rows={1})
p = body(""); run(p, "What moves the result most: ", bold=True, color=NAVY)
run(p, "the hours saved each month, the fully-loaded analyst rate, and the one-time "
       "build cost. The base and optimistic cases both stay comfortably positive. Only "
       "the conservative case gets tight, and that is a higher build cost meeting lower "
       "measured savings, so nail those two down first.")

# ===== 8 RISKS =====
h2(8, "Risks and Mitigations")
make_table(["Risk", "Likelihood", "Impact", "Mitigation"],
    [["Source workbook format changes (columns/layout)", "Medium", "High", "Robust column mapping plus validation that fails clearly when structure changes"],
     ["Incorrect Payment Made / Remaining mapping", "Low", "High", "Mandatory user confirmation before processing (never assumed)"],
     ["Fiscal Period mis-detected, wrong divisor", "Low", "Medium", "Auto-derive divisor; prompt only for Fiscal Period when undetermined"],
     ["User adoption / trust in automated accrual", "Medium", "Medium", "Parallel run vs manual for 1 to 2 months; transparent validation report"],
     ["Audit acceptance of preserved evidence", "Low", "Medium", "Preserve screenshots unaltered; align with audit early"],
     ["Estimated benefits not realized", "Medium", "Medium", "Baseline current effort before build; measure post-launch vs KPIs"]],
    numeric={}, widths=[2.4, 0.9, 0.8, 2.5])

# ===== 9 IMPLEMENTATION =====
h2(9, "Implementation Plan")
make_table(["Phase", "Key activities", "Duration (est.)"],
    [["1. Discovery and baseline", "Confirm logic, sample workbooks, baseline current effort, finalize requirements", "2 to 3 wks"],
     ["2. Build", "Ingestion, validation, mapping confirmation, calculations, forecasting, aging, summaries", "4 to 6 wks"],
     ["3. Dashboard and commentary", "Executive dashboard, KPI cards, data-supported narrative, audit-evidence handling", "2 wks"],
     ["4. UAT and parallel run", "Validate output vs manual for 1 to 2 close cycles; Accounting sign-off", "2 to 4 wks"],
     ["5. Go-live and handover", "Documentation, training, transition to standard monthly use", "1 wk"]],
    widths=[1.7, 3.7, 1.1])
body("Indicative total: about 3 to 4 months, dependent on sample-data and reviewer availability.")

# ===== 10 RESOURCE =====
h2(10, "Resource and Organizational Impact")
for x in ["People: process owner (Stephen) for requirements and UAT; a developer/automation resource for the build; Accounting for sign-off; light Finance-leadership input on the dashboard.",
          "Process change: monthly routine shifts from manual assembly to upload, confirm mapping, review validation, then book. Analyst time is redirected from spreadsheet maintenance to review and analysis.",
          "Skills: minimal new skills for end users; short training on the new workflow and validation report."]:
    body(x, bullet=True)

# ===== 11 DEPENDENCIES =====
h2(11, "Dependencies and Constraints")
for x in ["Timely monthly availability of the two commission workbooks from Commercial Analytics",
          "Consistent source column structure (or advance notice of changes)",
          "Reliable determination of Fiscal Period for divisor selection",
          "Reviewer/UAT availability across 1 to 2 close cycles",
          "Solution 1 is limited to the two workbooks; GL Supplemental and vendor analysis are Solution 2"]:
    body(x, bullet=True)

# ===== 12 SUCCESS METRICS =====
h2(12, "Success Metrics / KPIs")
make_table(["KPI", "Target", "Measurement"],
    [["Manual copy/paste and pivot steps eliminated", "100%", "Process walkthrough vs current steps"],
     ["Analyst time per close", "Down about 85% (3 to 4 days to under half a day)", "Timed baseline vs post-launch"],
     ["Accrual booking-ready output", "Used directly by Accounting", "Accounting sign-off; no rework"],
     ["Forecast correctness", "Divisor auto-applied correctly every close", "Config/validation report review"],
     ["Manual accrual errors / corrections", "Down toward zero", "Post-close correction count"],
     ["Audit evidence completeness", "Screenshots preserved every close", "Validation report screenshot flag is Yes"],
     ["Executive dashboard delivered", "Every close", "Dashboard produced and reviewed by leadership"]],
    widths=[2.4, 2.0, 2.1])

# ===== 13 RECOMMENDATION =====
h2(13, "Recommendation and Next Steps")
p = body(""); run(p, "Recommendation: ", bold=True, color=NAVY)
run(p, "Go with Option C and build the Commission Accrual Automation (Solution 1). It "
       "clears up the parts of the current process that break, gives Accounting output "
       "they can book and an audit trail they can stand behind, and puts a real month-end "
       "view in front of leadership. The estimated return is strong, and the risk and "
       "audit gains are worth as much as the dollars.")
for x in ["Confirm the financial inputs and replace the estimates (implementation quote, loaded analyst rate, measured effort, discount rate).",
          "Secure sponsor approval and funding for the estimated $45K one-time investment.",
          "Baseline current monthly effort before build begins (needed to prove savings).",
          "Kick off Phase 1 (Discovery) with sample workbooks and the process owner."]:
    p = doc.add_paragraph(style='List Number'); p.paragraph_format.space_after = Pt(2); run(p, x)

# ===== 14 ASSUMPTIONS =====
h2(14, "Assumptions and Open Questions")
h3("Assumptions made (to validate)")
for x in ["Current effort is about 3 to 4 senior-analyst days (about 28 hrs) per month, with about 85% reduction after automation.",
          "Fully-loaded analyst rate is about $65/hour.",
          "One-time implementation is about $45,000; recurring is about $4,000/year.",
          "Error/rework reduction is about $8,000/year.",
          "5-year horizon; 10% discount/hurdle rate; benefits begin in Year 1.",
          "Solution is internally built or AI-assisted rather than a licensed commercial platform."]:
    body(x, bullet=True)
h3("Open questions")
for x in ["Actual implementation cost, internal build vs vendor quote?",
          "Confirmed fully-loaded analyst rate and measured monthly hours?",
          "Finance-approved discount/hurdle rate?",
          "Who is the executive sponsor, and what strategic priority does this roll up to?",
          "Target go-live month relative to the close calendar?",
          "Any control/SOX requirements affecting the audit-evidence approach?"]:
    body(x, bullet=True)

pf = doc.add_paragraph(); pf.paragraph_format.space_before = Pt(12)
run(pf, "Confidential, internal use. Generated with the reusable Business Case Generator "
        "prompt. Financial figures are illustrative estimates pending validated inputs. "
        "Hach / Veralto brand palette applied (approximate; replace with official hex codes if available).",
    color=SLATE, size=8, italic=True)

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
out = os.path.join(repo_root, "cases", "case-commission-accrual-automation.docx")
os.makedirs(os.path.dirname(out), exist_ok=True)
doc.save(out)
print("saved", out)
