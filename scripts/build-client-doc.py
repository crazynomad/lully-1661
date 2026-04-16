"""Build a client-facing .docx from the requirements-understanding markdown.

Produces: docs/requirements-understanding-CLIENT-REVIEW.docx

The client version reorganizes the content so confirmation items come first
(as a fillable table) and context follows. Designed to convert cleanly when
uploaded to Google Drive and opened with Google Docs.
"""
from pathlib import Path
from docx import Document
from docx.shared import Pt, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "docs" / "requirements-understanding-CLIENT-REVIEW.docx"


def shade_cell(cell, hex_color):
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), hex_color)
    tc_pr.append(shd)


def add_heading(doc, text, level=1):
    h = doc.add_heading(text, level=level)
    for run in h.runs:
        run.font.color.rgb = RGBColor(0x1A, 0x1A, 0x1A)
    return h


def add_para(doc, text, bold=False, italic=False, size=11, color=None):
    p = doc.add_paragraph()
    r = p.add_run(text)
    r.font.size = Pt(size)
    r.bold = bold
    r.italic = italic
    if color:
        r.font.color.rgb = color
    return p


def add_callout(doc, label, text):
    """Yellow-highlighted 'action required' line."""
    p = doc.add_paragraph()
    r1 = p.add_run(f"⚠ {label}: ")
    r1.bold = True
    r1.font.color.rgb = RGBColor(0xB8, 0x6B, 0x00)
    r2 = p.add_run(text)
    r2.font.size = Pt(11)
    return p


def build():
    doc = Document()

    # --- Title ---
    title = doc.add_paragraph()
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = title.add_run("lully 1661 — Website Requirements")
    r.bold = True
    r.font.size = Pt(22)

    sub = doc.add_paragraph()
    sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    rs = sub.add_run("Our understanding of the brief — for your review and confirmation")
    rs.italic = True
    rs.font.size = Pt(12)
    rs.font.color.rgb = RGBColor(0x55, 0x55, 0x55)

    meta = doc.add_paragraph()
    meta.alignment = WD_ALIGN_PARAGRAPH.CENTER
    rm = meta.add_run("Draft v0.1   ·   Prepared 2026-04-16")
    rm.font.size = Pt(10)
    rm.font.color.rgb = RGBColor(0x88, 0x88, 0x88)

    doc.add_paragraph()

    # --- How to use this doc ---
    add_heading(doc, "How to read this document", level=1)
    add_para(
        doc,
        "We have read through the materials you shared (website brief, brand "
        "introduction, motto deck, weekly menu, logos, and moodboard) and "
        "written below how we understand the project today. Before we begin "
        "scoping and design, we need you to confirm or correct the items in "
        "the table on the next page.",
    )
    add_para(
        doc,
        "Two of the original fifteen questions have already been answered by "
        "you (marked ✅ below). Thirteen remain. Each has a short explanation "
        "in Section 3 — feel free to leave comments there, or simply fill in "
        "the answer column in the table.",
    )

    doc.add_page_break()

    # --- ACTION REQUIRED — the main value of this doc for the client ---
    add_heading(doc, "1. Action required — please confirm", level=1)
    add_para(
        doc,
        "These are the decisions we need from you before we can start. "
        "Anything left blank will block scoping or design.",
        italic=True,
    )
    doc.add_paragraph()

    rows = [
        ("#", "Question", "Your answer / decision"),
        (
            "Q1",
            "Brand spelling is “lully” (double L), with domain www.Lully1661.com. "
            "Please confirm so we can rename the GitHub repository accordingly.",
            "",
        ),
        (
            "Q2 ✅",
            "Languages: PT + EN (no FR), PT default at /, URL structure /pt/… and /en/…. "
            "— Confirmed 2026-04-16.",
            "Confirmed",
        ),
        (
            "Q3",
            "Platform: the brief mentions Shopify as “fully functional in Portugal”. "
            "Is Shopify the chosen platform, or open to alternatives (e.g. headless Next.js "
            "with a PT-friendly checkout)? This is the single biggest decision for cost and timeline.",
            "",
        ),
        (
            "Q4",
            "Payment providers on launch: Multibanco is mandatory in Portugal. "
            "Any preference for gateway (Stripe, SumUp, Mollie, others)?",
            "",
        ),
        (
            "Q5",
            "Click & collect — ordering cutoffs (same day? 24h? per-category?) and "
            "inventory: live stock per SKU, or order-taking form that staff reconcile daily?",
            "",
        ),
        (
            "Q6",
            "Restaurant reservations — The Fork, another partner (SevenRooms, OpenTable, Resy), "
            "or a “coming soon” placeholder at launch with phone/email contact?",
            "",
        ),
        (
            "Q7",
            "B2B “Lully Inside” page — showcase & lead-gen only at launch, or a wholesale "
            "ordering portal for existing partners too?",
            "",
        ),
        (
            "Q8",
            "Recruitment — integrate with an ATS (Workable, Teamtailor, etc.) or simple "
            "email-based applications?",
            "",
        ),
        (
            "Q9",
            "Is there a formal brand guidelines document (colors, typography, logo usage rules) "
            "we have not yet received?",
            "",
        ),
        (
            "Q10",
            "Is a vector version of the logo available (SVG / AI / EPS)? We currently only have a raster PNG.",
            "",
        ),
        (
            "Q11",
            "Current status of the first Lisbon outlet (open / soft-launched / pre-launch) and "
            "target website go-live date. Any marketing event the site must be live for?",
            "",
        ),
        (
            "Q12",
            "Who produces product photography, interior photography, and final copy (PT + EN)? "
            "Is copywriting part of this engagement, or supplied by you?",
            "",
        ),
        (
            "Q13",
            "Meunier / Pâtissière / Caffetier — are these archival illustrations only, or also "
            "used as section labels / counter signage? Affects site navigation.",
            "",
        ),
        (
            "Q14",
            "Ambient Baroque audio on the website? (If yes, it must be user-triggered — browsers "
            "block autoplay — and should be off during checkout.)",
            "",
        ),
        (
            "Q15",
            "Dedicated Events section (e.g. guest-chef luncheons like “Gareth × Sezin”), "
            "or keep events under News / Journal?",
            "",
        ),
    ]

    table = doc.add_table(rows=len(rows), cols=3)
    table.style = "Light Grid Accent 1"
    # column widths
    widths = [Cm(1.6), Cm(10.5), Cm(5.5)]
    for row_idx, row_data in enumerate(rows):
        for col_idx, value in enumerate(row_data):
            cell = table.rows[row_idx].cells[col_idx]
            cell.width = widths[col_idx]
            cell.text = ""
            p = cell.paragraphs[0]
            run = p.add_run(value)
            run.font.size = Pt(10)
            if row_idx == 0:
                run.bold = True
                shade_cell(cell, "1A1A1A")
                run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
            elif "✅" in row_data[0]:
                shade_cell(cell, "E6F4EA")
            else:
                shade_cell(cell, "FFF8E1")

    doc.add_paragraph()
    add_para(
        doc,
        "When you are done, please share this doc back with comments resolved, "
        "or simply reply with the answers in an email.",
        italic=True,
    )

    doc.add_page_break()

    # --- Section 2: What we have understood ---
    add_heading(doc, "2. What we have understood so far", level=1)

    add_heading(doc, "2.1 Brand at a glance", level=2)
    add_para(
        doc,
        "lully 1661 is an artisanal French bakery and all-day brunch concept, opening first "
        "in Lisbon with ambition to grow into a pan-European brand over five years. The name "
        "honours Jean-Baptiste Lully, the Baroque composer granted French citizenship in 1661. "
        "The brand positions itself as a “Renaissance of bakery” — tradition as starting "
        "point, continuous reinvention as daily practice. The tone of voice is operatic, "
        "sensory, intimate, authentic, and accessibly priced.",
    )

    add_heading(doc, "2.2 Three product pillars", level=2)
    add_para(
        doc,
        "Three Baroque sub-marks — Meunier (miller / bread), Pâtissière (pastry), and "
        "Caffetier (coffee and brunch) — represent the three product pillars. We interpret "
        "these as potential site-navigation cues (see Q13).",
    )

    add_heading(doc, "2.3 Proposed sitemap", level=2)
    add_para(doc, "Based on the information tree in your website brief:")
    sitemap = [
        "Home",
        "  History — who we are, commitment to tradition",
        "  Shop (click & collect first; full delivery later)",
        "    Breads · Pastries · Desserts · Snacks · Brunch · Drinks",
        "  Special Orders",
        "  Restaurant Reservations",
        "  Lully Inside (B2B partnerships)",
        "  Recruitment",
        "  Legal / Contact",
    ]
    for line in sitemap:
        p = doc.add_paragraph()
        r = p.add_run(line)
        r.font.name = "Courier New"
        r.font.size = Pt(10)

    add_heading(doc, "2.4 eCommerce scope", level=2)
    add_para(
        doc,
        "Phase 1 at launch: online menu browsing and click & collect. "
        "Phase 2 later: integrated payments and third-party delivery (Uber Eats, Glovo). "
        "Multibanco support is mandatory for Portugal.",
    )

    add_heading(doc, "2.5 Design direction", level=2)
    add_para(
        doc,
        "Baroque decorative motifs (engravings of millers, coffee vendors, pastry-makers, "
        "and instruments) set against a contemporary white / marble / tile backdrop — "
        "as shown in your 3D shop render. Reference sites you shared (do-beco, liberte-paris, "
        "loulou-paris, thefrenchbastards) all lean on strong typography, editorial product "
        "photography, and a clean menu/shop UX. We would aim for a similar feel with the "
        "Baroque illustrations as the distinctive layer.",
    )

    doc.add_page_break()

    # --- Section 3: detailed context for each question ---
    add_heading(doc, "3. Context behind each confirmation item", level=1)
    add_para(
        doc,
        "Short explanation for each question in Section 1. You can comment inline here or "
        "simply answer in the table above.",
        italic=True,
    )

    blocks = [
        (
            "Q1 — Brand spelling",
            "All of your materials (logo, brief, domain www.Lully1661.com) use "
            "“lully” with double L — consistent with Jean-Baptiste Lully. The GitHub "
            "repository was initially created as lullly-1661 (triple L) following a verbal "
            "spelling. Confirming the double-L spelling lets us rename the repo before any "
            "public link is shared.",
        ),
        (
            "Q3 — Platform",
            "Your brief says Shopify “seems to be fully functional in Portugal”. That sounds "
            "exploratory rather than decided. Shopify would be fastest and cheapest to launch, "
            "but limits flexibility for bespoke visuals and later self-hosted payments. A "
            "headless stack (Next.js + Shopify or a custom commerce backend) gives full design "
            "freedom but costs more upfront. We would like a direction before scoping.",
        ),
        (
            "Q4 — Payment providers",
            "Multibanco is the Portuguese reference/voucher payment system and is non-negotiable "
            "for local customers. Stripe, SumUp, and Mollie all offer Multibanco; each differs on "
            "fees and Shopify integration maturity.",
        ),
        (
            "Q5 — Click & collect",
            "Two very different implementations: (a) live inventory per SKU, customer sees real "
            "availability, or (b) order-form where customer books tomorrow’s items and staff "
            "reconcile each morning. Option (b) is dramatically simpler for a bakery; option (a) "
            "is what Shopify defaults to.",
        ),
        (
            "Q6 — Reservations",
            "Deciding the booking partner (if any) at launch lets us build the integration once. "
            "If not critical for launch, a simple “Reservations coming soon + phone/email” page is "
            "fastest.",
        ),
        (
            "Q7 — B2B",
            "We read “Lully Inside” as a public showcase page with a partnership enquiry form. "
            "A full wholesale ordering portal would be a separate, larger piece of work.",
        ),
        (
            "Q8 — Recruitment",
            "If your team already uses an ATS, we can link to it. Otherwise a lightweight careers "
            "page with an email or form-based application is enough for launch.",
        ),
        (
            "Q9 — Brand guidelines",
            "We have the wordmark (PNG) and three Baroque sub-marks. We have not seen a formal "
            "color palette, typography system, or logo-usage rules. If these exist, they save us "
            "guesswork; if not, we will propose them during design.",
        ),
        (
            "Q10 — Vector logo",
            "SVG / AI / EPS versions of the logo are needed for print, favicons, retina displays, "
            "and social-media adaptations. A raster PNG only works at a limited size.",
        ),
        (
            "Q11 — Launch status & timeline",
            "Your 2022 brief mentioned a September 2023 opening, but the January 2026 motto deck "
            "and your 2026 weekly menu (EUR-priced, PT + EN) strongly suggest the Lisbon outlet "
            "is opening imminently or already soft-launched. The website timeline must line up "
            "with the outlet launch or any press moment.",
        ),
        (
            "Q12 — Content",
            "At present we have only vintage engravings, one 3D render, and the wordmark. Real "
            "interior, product, and team photography — plus final PT + EN copy — are needed "
            "before the site can go live. Knowing now whether you supply them or whether we "
            "commission them determines the cost and timeline.",
        ),
        (
            "Q13 — Pillar labels",
            "Using Meunier / Pâtissière / Caffetier as primary navigation would be distinctive "
            "but demands that customers learn the vocabulary. Using conventional labels "
            "(Bread / Pastry / Drinks) and keeping the Baroque sub-marks as decorative is safer. "
            "Your preference shapes the information architecture.",
        ),
        (
            "Q14 — Ambient audio",
            "Browsers block autoplayed audio. A user-triggered Baroque-music toggle on "
            "the home / history pages is feasible, but should be off on shop and checkout pages "
            "to avoid disrupting purchase flows.",
        ),
        (
            "Q15 — Events",
            "The Gareth × Sezin guest-chef poster suggests recurring special events. These can "
            "either live as their own section (good if frequent) or under a News / Journal "
            "section (good if occasional).",
        ),
    ]
    for title, body in blocks:
        add_heading(doc, title, level=3)
        add_para(doc, body)

    doc.add_page_break()

    # --- Section 4: next steps ---
    add_heading(doc, "4. What happens after you confirm", level=1)
    steps = [
        "We rename the repository to reflect the confirmed brand spelling.",
        "We produce a scope & sitemap v1 — a clear split of what is in phase 1 versus phase 2.",
        "We recommend a platform (Shopify or headless) with cost and timeline impact.",
        "We wireframe Home and the Shop flow to validate the information architecture before any visual design.",
        "We share these back with you for a second round of review before design begins.",
    ]
    for i, s in enumerate(steps, 1):
        p = doc.add_paragraph()
        r = p.add_run(f"{i}. ")
        r.bold = True
        p.add_run(s)

    doc.add_paragraph()
    add_para(
        doc,
        "Thank you — we are looking forward to your feedback.",
        italic=True,
    )

    OUT.parent.mkdir(parents=True, exist_ok=True)
    doc.save(OUT)
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    build()
