"""Build a client-facing .docx of the Digital Marketing Strategy (EN-primary + FR).

Produces: docs/digital-marketing-strategy-CLIENT.docx

Mirrors the structure of docs/digital-marketing-strategy.md. Layout choices:
- Bilingual headings: EN heading (dark) with FR subtitle (grey italic) below.
- Body prose: EN paragraph in regular 11pt, FR paragraph immediately below in
  italic 10pt slightly muted grey — so the EN reading flow stays primary and
  the FR works as a parallel translation, not a competing column.
- Tables: bilingual column headers (EN line 1, FR line 2 italic grey).
- Callout boxes for the strategic insight blocks.

Run:  python3 scripts/build-marketing-strategy-doc.py
"""
from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "docs" / "digital-marketing-strategy-CLIENT.docx"

# Colour palette — kept close to build-client-doc.py for consistency.
COLOR_INK = RGBColor(0x1A, 0x1A, 0x1A)
COLOR_BODY = RGBColor(0x22, 0x22, 0x22)
COLOR_FR = RGBColor(0x55, 0x55, 0x55)
COLOR_META = RGBColor(0x88, 0x88, 0x88)
COLOR_ACCENT = RGBColor(0xB8, 0x6B, 0x00)  # Baroque-ish ochre for callouts
COLOR_WHITE = RGBColor(0xFF, 0xFF, 0xFF)


# ---------- Low-level helpers ----------

def shade_cell(cell, hex_color):
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), hex_color)
    tc_pr.append(shd)


def add_heading(doc, text, level=1, fr=None):
    """Add an EN heading with an optional FR subtitle line below."""
    h = doc.add_heading(text, level=level)
    for run in h.runs:
        run.font.color.rgb = COLOR_INK
    if fr:
        sub = doc.add_paragraph()
        rs = sub.add_run(fr)
        rs.italic = True
        rs.font.size = Pt(11 if level <= 2 else 10)
        rs.font.color.rgb = COLOR_FR
    return h


def add_para(doc, text, *, bold=False, italic=False, size=11, color=None):
    p = doc.add_paragraph()
    r = p.add_run(text)
    r.font.size = Pt(size)
    r.bold = bold
    r.italic = italic
    if color:
        r.font.color.rgb = color
    else:
        r.font.color.rgb = COLOR_BODY
    return p


def add_bilingual(doc, en, fr):
    """EN paragraph in primary style + FR paragraph below in muted italic."""
    add_para(doc, en, size=11)
    add_para(doc, fr, italic=True, size=10, color=COLOR_FR)


def add_callout(doc, label, text):
    """Ochre-tinted strategic-insight line — used for 'Why this matters'."""
    p = doc.add_paragraph()
    r1 = p.add_run(f"▸ {label}  ")
    r1.bold = True
    r1.font.color.rgb = COLOR_ACCENT
    r2 = p.add_run(text)
    r2.font.size = Pt(10.5)
    r2.italic = True
    r2.font.color.rgb = COLOR_BODY
    return p


def add_bilingual_table(doc, headers, rows, col_widths=None):
    """Build a table where each header cell holds EN (top) + FR (bottom)
    and each row cell may be a single string or a tuple (EN, FR)."""
    n_cols = len(headers)
    table = doc.add_table(rows=len(rows) + 1, cols=n_cols)
    table.style = "Light Grid Accent 1"

    # Header row
    for ci, header in enumerate(headers):
        cell = table.rows[0].cells[ci]
        if col_widths:
            cell.width = col_widths[ci]
        cell.text = ""
        shade_cell(cell, "1A1A1A")

        if isinstance(header, tuple):
            en_text, fr_text = header
        else:
            en_text, fr_text = header, None

        p_en = cell.paragraphs[0]
        r_en = p_en.add_run(en_text)
        r_en.bold = True
        r_en.font.size = Pt(10)
        r_en.font.color.rgb = COLOR_WHITE

        if fr_text:
            p_fr = cell.add_paragraph()
            r_fr = p_fr.add_run(fr_text)
            r_fr.italic = True
            r_fr.font.size = Pt(8.5)
            r_fr.font.color.rgb = RGBColor(0xCC, 0xCC, 0xCC)

    # Data rows
    for ri, row in enumerate(rows, start=1):
        for ci, val in enumerate(row):
            cell = table.rows[ri].cells[ci]
            if col_widths:
                cell.width = col_widths[ci]
            cell.text = ""

            if isinstance(val, tuple):
                en_text, fr_text = val
            else:
                en_text, fr_text = val, None

            p_en = cell.paragraphs[0]
            r_en = p_en.add_run(en_text)
            r_en.font.size = Pt(9.5)
            r_en.font.color.rgb = COLOR_BODY

            if fr_text:
                p_fr = cell.add_paragraph()
                r_fr = p_fr.add_run(fr_text)
                r_fr.italic = True
                r_fr.font.size = Pt(8.5)
                r_fr.font.color.rgb = COLOR_FR
    return table


def add_spacer(doc, lines=1):
    for _ in range(lines):
        doc.add_paragraph()


# ---------- Document content ----------

def build():
    doc = Document()

    # Page margins — slightly tighter than default to accommodate dense tables.
    for section in doc.sections:
        section.left_margin = Cm(2.0)
        section.right_margin = Cm(2.0)
        section.top_margin = Cm(2.0)
        section.bottom_margin = Cm(2.0)

    # ---------- Title block ----------
    t = doc.add_paragraph()
    t.alignment = WD_ALIGN_PARAGRAPH.CENTER
    rt = t.add_run("Digital Marketing Strategy")
    rt.bold = True
    rt.font.size = Pt(24)

    t2 = doc.add_paragraph()
    t2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    rt2 = t2.add_run("Stratégie de Marketing Digital")
    rt2.italic = True
    rt2.font.size = Pt(14)
    rt2.font.color.rgb = COLOR_FR

    sub = doc.add_paragraph()
    sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    rs = sub.add_run("Lully 1661 · Lisbon")
    rs.font.size = Pt(13)
    rs.font.color.rgb = COLOR_INK

    meta = doc.add_paragraph()
    meta.alignment = WD_ALIGN_PARAGRAPH.CENTER
    rm = meta.add_run("Draft v0.1   ·   Prepared 2026-05-22   ·   EN primary · FR secondary")
    rm.font.size = Pt(10)
    rm.font.color.rgb = COLOR_META

    add_spacer(doc, 1)

    # ---------- Status / Statut ----------
    add_heading(doc, "Status & Scope", level=2, fr="Statut & Périmètre")
    add_bilingual(
        doc,
        "Draft for client review. Companion documents: competitor-scan, "
        "platform-recommendation-v2, architecture. Scope: integrated digital "
        "marketing across website, e-commerce, Instagram, Xiaohongshu, SEO, "
        "GEO, Google Business, reviews and CRM, for the three-store Lisbon "
        "footprint.",
        "Brouillon pour relecture client. Documents associés : competitor-scan, "
        "platform-recommendation-v2, architecture. Périmètre : marketing "
        "digital intégré sur site, e-commerce, Instagram, Xiaohongshu, SEO, "
        "GEO, Google Business, avis et CRM, pour l'empreinte de trois "
        "boutiques à Lisbonne.",
    )

    doc.add_page_break()

    # ---------- § 0 TL;DR ----------
    add_heading(doc, "0. TL;DR — Five Strategic Anchors", level=1,
                fr="0. Résumé — Cinq Ancres Stratégiques")

    add_bilingual(
        doc,
        "Lully 1661 has one real digital moat its four competitors do not: a "
        "Baroque-heritage narrative in a Lisbon market where every alternative "
        "is a flavour of \"modern minimalist.\" The job of the next 12 months "
        "is to convert that brand asymmetry into a measurable lead in (a) "
        "Google search for \"brunch / bakery / Sunday brunch Lisbon\", (b) "
        "Instagram and TikTok discovery, (c) traveler-facing review platforms "
        "(Google, TripAdvisor), and (d) generative engines (ChatGPT, "
        "Perplexity, Gemini) — while parallel-tracking a migration of Uber "
        "Eats and Glovo customers to direct ordering once Phase-2 commerce "
        "ships.",
        "Lully 1661 possède un fossé de marque que ses quatre concurrents "
        "directs n'ont pas : un récit baroque dans un marché lisboète où "
        "chaque alternative est une déclinaison du « minimalisme moderne ». "
        "La mission des 12 prochains mois est de transformer cette asymétrie "
        "de marque en avance mesurable sur (a) la recherche Google « brunch / "
        "boulangerie / brunch du dimanche Lisbonne », (b) la découverte sur "
        "Instagram et TikTok, (c) les plateformes d'avis des voyageurs "
        "(Google, TripAdvisor), et (d) les moteurs génératifs (ChatGPT, "
        "Perplexity, Gemini) — tout en orchestrant en parallèle la migration "
        "des clients Uber Eats et Glovo vers la commande directe dès le "
        "lancement de la Phase 2 e-commerce.",
    )

    add_spacer(doc)

    anchors = [
        ("1", "Own the Baroque story",
         "Posséder le récit baroque",
         "Convert visual heritage into a content engine — the only "
         "differentiator competitors cannot copy.",
         "Transformer l'héritage visuel en moteur de contenu — le seul "
         "différenciateur incopiable."),
        ("2", "Win Anjos Sunday brunch first",
         "Gagner d'abord le brunch dominical d'Anjos",
         "Wedge into a micro-segment competitors don't serve (Dear Breakfast "
         "off-zone, Padaria 110 closed Sunday).",
         "S'enraciner dans un micro-segment vacant (Dear Breakfast hors zone, "
         "Padaria 110 fermée le dimanche)."),
        ("3", "Treat Uber Eats / Glovo as paid acquisition",
         "Considérer Uber Eats / Glovo comme acquisition payante",
         "Design a packaging → newsletter → direct-order funnel from day one.",
         "Concevoir un entonnoir packaging → infolettre → commande directe "
         "dès le premier jour."),
        ("4", "Build GEO-ready content infrastructure",
         "Bâtir une infrastructure prête pour le GEO",
         "Schema.org + FAQ-shaped journal + Wikidata entry — 18-month "
         "compounding bet.",
         "Schema.org + journal en format FAQ + fiche Wikidata — pari à effet "
         "composé sur 18 mois."),
        ("5", "Reviews are SEO",
         "Les avis sont du SEO",
         "Google + TripAdvisor reviews matter as much as backlinks for the "
         "traveler audience.",
         "Les avis Google et TripAdvisor pèsent autant que les backlinks pour "
         "l'audience voyageurs."),
    ]

    anchor_rows = []
    for num, en_anchor, fr_anchor, en_one, fr_one in anchors:
        anchor_rows.append([
            num,
            (en_anchor, fr_anchor),
            (en_one, fr_one),
        ])
    add_bilingual_table(
        doc,
        headers=[
            ("#", None),
            ("Anchor", "Ancre"),
            ("One-liner", "En une ligne"),
        ],
        rows=anchor_rows,
        col_widths=[Cm(1.0), Cm(5.0), Cm(11.0)],
    )

    doc.add_page_break()

    # ---------- § 1 Where Lully 1661 Stands ----------
    add_heading(doc, "1. Where Lully 1661 Stands", level=1,
                fr="1. Positionnement Actuel")
    add_heading(doc, "1.1 Asset Inventory", level=2,
                fr="1.1 Inventaire des Actifs")

    asset_rows = [
        [
            ("Stores", "Boutiques"),
            "3 — Anjos (flagship + brunch + dine-in + only Sunday opening), "
            "Beato, Campo de Ourique",
        ],
        [
            ("Brand position", "Positionnement de marque"),
            "\"Boulangerie Renaissance\" — Baroque copperplate + 1661 namesake "
            "heritage + three sub-brands (Caffetier, Meunier, Patissière)",
        ],
        [
            ("Product range", "Gamme produit"),
            "48h-fermented sourdough breads (Paillard, Fâcheux) + French "
            "viennoiserie + cosmopolitan brunch (Benedict, Florentine, "
            "Cilbir, Pain Perdu, Avocado, Le Menuet, Le Monsieur, Sopa do Mês)",
        ],
        [
            ("Digital maturity", "Maturité digitale"),
            "Bottom of competitive set today — no live site, social-only. "
            "After v1 launch: parity with Dear Breakfast, ahead of doBeco "
            "and Padaria 110, still behind The Folks on commerce depth",
        ],
        [
            ("Delivery", "Livraison"),
            "Uber Eats + Glovo only (no direct online order in v1)",
        ],
        [
            ("Site languages", "Langues du site"),
            "PT + EN (per lib/i18n/routing.ts) — CN not in scope for v1",
        ],
        [
            ("CMS", "CMS"),
            "Keystatic, git-backed, owner-editable weekly menu",
        ],
    ]
    add_bilingual_table(
        doc,
        headers=[("Dimension", "Dimension"),
                 ("Current state", "État actuel")],
        rows=asset_rows,
        col_widths=[Cm(4.5), Cm(12.5)],
    )

    add_spacer(doc)
    add_heading(doc, "1.2 The Three Truths of the Lisbon Landscape", level=2,
                fr="1.2 Les Trois Vérités du Paysage Lisboète")

    add_para(doc, "Truth 1.", bold=True)
    add_bilingual(
        doc,
        "You are not competing for \"the nearest bakery.\" You are competing "
        "for algorithmic visibility — in Google Search, Instagram Explore, "
        "Google Maps, TripAdvisor, and increasingly in generative-AI answers. "
        "By the time a traveler types \"best brunch Lisbon\" on the plane, "
        "the fight is already underway. Dear Breakfast and The Folks have a "
        "multi-year head-start on this front; we close it with structure "
        "(schema markup, multilingual SEO, journal content) rather than "
        "spend.",
        "Vous ne vous battez pas pour « la boulangerie la plus proche ». Vous "
        "vous battez pour la visibilité algorithmique — Google Search, "
        "Instagram Explore, Google Maps, TripAdvisor, et de plus en plus les "
        "réponses des IA génératives. Au moment où un voyageur tape « best "
        "brunch Lisbon » dans l'avion, la bataille a déjà commencé. Dear "
        "Breakfast et The Folks ont plusieurs années d'avance ; nous "
        "rattrapons par la structure (balisage schema.org, SEO multilingue, "
        "journal éditorial) plutôt que par la dépense publicitaire.",
    )

    add_para(doc, "Truth 2.", bold=True)
    add_bilingual(
        doc,
        "The Folks proves that \"Lisbon bakery/café e-commerce works\" — they "
        "ship coffee worldwide via Shopify with full B2B wholesale. This is "
        "not aspiration; it's validation of Lully's Phase-2 commerce "
        "hypothesis. They are the benchmark we will eventually be compared "
        "against, not a model to copy wholesale (their category is "
        "coffee-first, ours is bakery-first).",
        "The Folks démontre qu'un e-commerce de boulangerie/café à Lisbonne "
        "fonctionne — ils expédient du café dans le monde entier via Shopify "
        "et gèrent un wholesale B2B complet. Ce n'est pas une aspiration, "
        "c'est la validation de l'hypothèse e-commerce Phase 2 de Lully. Ils "
        "sont le benchmark de référence, pas un modèle à copier intégralement "
        "(leur catégorie est avant tout café, la nôtre avant tout "
        "boulangerie).",
    )

    add_para(doc, "Truth 3.", bold=True)
    add_bilingual(
        doc,
        "doBeco is the most dangerous neighbour — same 3-store scale, same "
        "bakery + brunch positioning, same Lisbon geography, same premium "
        "pricing. Their advantage is a chef-driven origin story (António José "
        "de Mello, pandemic garage). Our advantage is a richer brand "
        "vocabulary (1661, Renaissance, three guild sub-brands). To convert "
        "that into a real lead, the heritage story has to leave the moodboard "
        "and live in journal articles, packaging plaques, and store fittings.",
        "doBeco est le voisin le plus dangereux — même échelle de 3 "
        "boutiques, même positionnement boulangerie + brunch, même géographie "
        "lisboète, même tarification premium. Leur avantage est un récit "
        "fondateur porté par un chef (António José de Mello, garage en "
        "confinement). Le nôtre est un vocabulaire de marque plus riche "
        "(1661, Renaissance, trois sous-marques de corporation). Pour "
        "transformer cet avantage en avance réelle, le récit patrimonial doit "
        "sortir du moodboard et s'incarner dans des articles éditoriaux, des "
        "cartouches sur les emballages, et le mobilier des boutiques.",
    )

    doc.add_page_break()

    # ---------- § 2 Audience Segmentation ----------
    add_heading(doc, "2. Audience Segmentation", level=1,
                fr="2. Segmentation des Audiences")
    add_bilingual(
        doc,
        "The client brief identifies two audiences (local + traveler). "
        "Operationally this is too coarse — different sub-segments make "
        "decisions through entirely different funnels. We refine into six "
        "segments below; the channel matrix in § 3 is built directly on this "
        "segmentation.",
        "Le brief client identifie deux audiences (locaux + voyageurs). "
        "Opérationnellement c'est trop large — les sous-segments décident à "
        "travers des entonnoirs entièrement différents. Nous affinons en six "
        "segments ci-dessous ; la matrice de canaux (§ 3) en découle "
        "directement.",
    )

    add_spacer(doc)

    segments = [
        ("A1", ("Neighbourhood regular", "Habitué·e du quartier"),
         ("Weekend ritual, commute pass-by", "Rituel week-end, trajet"),
         ("Instant / habit", "Instantané / habitude"),
         ("Google Maps + IG + word of mouth",
          "Google Maps + IG + bouche-à-oreille")),
        ("A2", ("Local delivery user", "Client livraison local"),
         ("Sunday morning, rainy day", "Dimanche matin, jour de pluie"),
         ("Short / impulse", "Court / impulsion"),
         ("Uber Eats + Glovo + IG Stories", "Uber Eats + Glovo + Stories IG")),
        ("A3", ("Cross-city Lisboner", "Lisboète d'un autre quartier"),
         ("Destination weekend brunch", "Brunch week-end de destination"),
         ("Mid / planned", "Moyen / planifié"),
         ("Google + IG saves + TripAdvisor",
          "Google + sauvegardes IG + TripAdvisor")),
        ("A4", ("International traveler — planner",
                "Voyageur international planificateur"),
         ("Pre-trip research, 1–4 weeks out",
          "Recherche pré-voyage, 1–4 semaines"),
         ("Long / high-research", "Long / forte recherche"),
         ("Google + TripAdvisor + Reddit + AI chatbots (GEO)",
          "Google + TripAdvisor + Reddit + IA génératives (GEO)")),
        ("A5", ("International traveler — walker",
                "Voyageur international en exploration"),
         ("On the street in Lisbon", "Dans la rue à Lisbonne"),
         ("Instant / impulse", "Instantané / impulsion"),
         ("Google Maps + IG geotag + walking guides",
          "Google Maps + géotags IG + guides à pied")),
        ("A6", ("Chinese traveler", "Voyageur chinois"),
         ("Pre-trip Xiaohongshu + on-trip search",
          "Inspiration Xiaohongshu + recherche sur place"),
         ("Long / visual-driven", "Long / piloté par le visuel"),
         ("Xiaohongshu + Dianping + Baidu", "Xiaohongshu + Dianping + Baidu")),
    ]
    seg_rows = [[s[0], s[1], s[2], s[3], s[4]] for s in segments]
    add_bilingual_table(
        doc,
        headers=[
            ("#", None),
            ("Segment", "Segment"),
            ("Trigger", "Déclencheur"),
            ("Decision", "Décision"),
            ("Primary channels", "Canaux principaux"),
        ],
        rows=seg_rows,
        col_widths=[Cm(1.0), Cm(4.0), Cm(4.0), Cm(3.5), Cm(4.5)],
    )

    add_spacer(doc)
    add_heading(doc, "2.1 What the Client Brief Missed", level=2,
                fr="2.1 Ce que le Brief Client a Manqué")

    add_para(doc, "Gap 1 — The Uber Eats / Glovo \"channel economics\" gap.",
             bold=True)
    add_bilingual(
        doc,
        "Each Uber/Glovo order pays ~30% to a third party AND donates the "
        "customer relationship to that platform. Without an explicit "
        "migration funnel (packaging insert → newsletter signup → direct "
        "order discount), the brand is paying to grow someone else's "
        "database. This needs to be designed before Phase-2 commerce "
        "launches, not after.",
        "Chaque commande Uber/Glovo verse ~30 % à un tiers ET cède la "
        "relation client à cette plateforme. Sans entonnoir de migration "
        "explicite (encart d'emballage → inscription infolettre → réduction "
        "sur commande directe), la marque paie pour faire grossir la base de "
        "données d'un autre. Cela doit se concevoir avant le lancement Phase "
        "2 e-commerce, pas après.",
    )

    add_para(doc, "Gap 2 — The A4 vs A5 gap.", bold=True)
    add_bilingual(
        doc,
        "The pre-trip planner and the on-street walker use entirely different "
        "surfaces — the first is reached by SEO, GEO, and TripAdvisor; the "
        "second by Google Business Profile and Instagram geotags. Many "
        "bakeries reach one and miss the other.",
        "Le planificateur pré-voyage et le marcheur sur place utilisent des "
        "surfaces entièrement différentes — le premier via SEO, GEO et "
        "TripAdvisor ; le second via Google Business Profile et géotags "
        "Instagram. Beaucoup de boulangeries en atteignent un et manquent "
        "l'autre.",
    )

    doc.add_page_break()

    # ---------- § 3 Channel Strategy ----------
    add_heading(doc, "3. Channel Strategy", level=1,
                fr="3. Stratégie de Canaux")
    add_bilingual(
        doc,
        "We organise channels in three tiers by time-to-launch and dependency "
        "on website v1.",
        "Nous organisons les canaux en trois tiers selon le temps de "
        "lancement et la dépendance au site v1.",
    )

    add_heading(doc, "3.1 Tier 0 — Launch immediately", level=2,
                fr="3.1 Tier 0 — Démarrage immédiat, sans dépendance au site")

    tier0_rows = [
        [("Google Business Profile (×3)", "Profil Google Business (×3)"),
         ("A1, A3, A5 first touch", "Premier point de contact A1, A3, A5"),
         ("Verify all 3 listings; photos; Sunday hours @ Anjos; menu link; "
          "reservation link; seed 5–10 Q&As per store (EN + PT)",
          "Vérifier les 3 fiches ; photos ; horaires dimanche @ Anjos ; lien "
          "menu ; lien réservation ; 5–10 Q&R amorcées par boutique")],
        [("Instagram (existing)", "Instagram (existant)"),
         ("Brand visual + A4/A5 discovery + A1/A2 retention",
          "Image de marque + découverte A4/A5 + fidélisation A1/A2"),
         ("Reels ≥ 50% weekly; geotag + EN hashtags; 5 Story Highlights with "
          "Baroque covers",
          "Reels ≥ 50 % hebdo ; géotag + hashtags EN ; 5 Stories à la Une "
          "avec couvertures baroques")],
        [("In-store review programme", "Programme d'avis en boutique"),
         ("Reviews = SEO + GEO fuel", "Les avis = carburant SEO + GEO"),
         ("Bilingual review cards with QR; baristas trained on 30s ask; "
          "target ≥ 200 reviews/store at ≥ 4.7 in 6 months",
          "Cartes d'avis bilingues avec QR ; baristas formés à la demande "
          "de 30s ; cible ≥ 200 avis/boutique à ≥ 4,7 en 6 mois")],
        [("Newsletter (footer already wired)",
          "Infolettre (déjà câblée en pied de page)"),
         ("Uber → Direct migration container; weekly menu",
          "Conteneur de migration Uber → Direct ; menu hebdomadaire"),
         ("Open signups via IG bio + in-store posters; cadence aligned with "
          "weeklyMenuItem releases",
          "Ouvrir les inscriptions via bio IG + affiches en boutique ; "
          "cadence alignée sur les sorties weeklyMenuItem")],
    ]
    add_bilingual_table(
        doc,
        headers=[("Channel", "Canal"), ("Role", "Rôle"),
                 ("Specific actions", "Actions concrètes")],
        rows=tier0_rows,
        col_widths=[Cm(3.8), Cm(4.5), Cm(8.7)],
    )

    add_spacer(doc)
    add_heading(doc, "3.2 Tier 1 — Activate at website v1 launch", level=2,
                fr="3.2 Tier 1 — Activation au lancement du site v1")

    tier1_rows = [
        [("Website (lully1661.*)", "Site (lully1661.*)"),
         ("SEO + GEO ground truth", "Vérité de référence SEO + GEO"),
         ("Sitemap to GSC + Bing; LocalBusiness/Restaurant JSON-LD per store; "
          "MenuItem schema per dish; canonical + hreflang",
          "Sitemap vers GSC + Bing ; JSON-LD LocalBusiness/Restaurant par "
          "boutique ; schema MenuItem par plat ; canonical + hreflang")],
        [("Brunch landing page", "Page d'atterrissage brunch"),
         ("Primary A3 + A4 target", "Cible principale A3 + A4"),
         ("Optimised for brunch lisbon / sunday brunch lisbon; FAQ block "
          "(LLM-friendly)",
          "Optimisée pour brunch lisbon / sunday brunch lisbon ; bloc FAQ "
          "(format adapté aux LLM)")],
        [("Per-store detail pages (×3)",
          "Fiches détaillées par boutique (×3)"),
         ("A1 + A5 geographic SEO", "SEO géographique A1 + A5"),
         ("Each targets {cuisine type} {neighbourhood} long-tails",
          "Chacune cible les longues traînes {type cuisine} {quartier}")],
        [("Per-menu-item pages (×9)",
          "Fiches par item du menu (×9)"),
         ("Long-tail SEO + journal seed", "SEO longue traîne + amorce "
                                          "journal"),
         ("One page per signature item with Recipe/MenuItem schema",
          "Une page par item signature avec schema Recipe/MenuItem")],
        [("Journal (blog)", "Journal (blog)"),
         ("SEO + GEO content engine", "Moteur de contenu SEO + GEO"),
         ("Two lines: (a) Lisbon-context, (b) Craft + heritage — operationalise "
          "the Baroque moat",
          "Deux fils : (a) contexte lisboète, (b) artisanat + héritage — "
          "opérationnaliser le fossé baroque")],
        [("TripAdvisor business listing", "Fiche TripAdvisor"),
         ("A4 traveler primary funnel", "Entonnoir principal A4"),
         ("Claim, complete, integrate review request into in-store programme",
          "Revendiquer, compléter, intégrer la demande d'avis au programme "
          "en boutique")],
    ]
    add_bilingual_table(
        doc,
        headers=[("Channel", "Canal"), ("Role", "Rôle"),
                 ("Specific actions", "Actions concrètes")],
        rows=tier1_rows,
        col_widths=[Cm(3.8), Cm(4.5), Cm(8.7)],
    )

    add_spacer(doc)
    add_heading(doc, "3.3 Tier 2 — Post-launch (Months 3–9)", level=2,
                fr="3.3 Tier 2 — Post-lancement (Mois 3–9)")

    tier2_rows = [
        [("TikTok", "TikTok"),
         ("A4 + A5 + A6 discovery, lower competition than Reels",
          "Découverte A4 + A5 + A6, moins concurrentiel que Reels"),
         ("Mirror IG Reels initially; add Lisbon city-context content; "
          "weekly cadence",
          "Refléter les Reels IG d'abord ; ajouter du contenu contexte "
          "lisboète ; cadence hebdomadaire")],
        [("Xiaohongshu (RED)", "Xiaohongshu (RED)"),
         ("A6 — Chinese traveler, currently 0% covered",
          "A6 — voyageur chinois, 0 % couvert actuellement"),
         ("Do NOT self-operate. Verified account + CN menu + 5 polished "
          "notes. Real lever: 5–10 Lisbon-based Chinese KOC partnerships "
          "at €100–€300/post",
          "NE PAS auto-gérer. Compte certifié + menu CN + 5 notes "
          "soignées. Vrai levier : 5–10 partenariats KOC chinois basés à "
          "Lisbonne à €100–€300/post")],
        [("GEO", "GEO"),
         ("A4 — increasingly discovers via ChatGPT/Perplexity/Gemini",
          "A4 — découverte croissante via ChatGPT/Perplexity/Gemini"),
         ("(1) FAQ-shaped journal answers; (2) Wikidata entry; (3) press "
          "pitches to Time Out / Eater / Condé Nast; (4) Reddit r/Lisbon "
          "organic seeding via review quality",
          "(1) Réponses éditoriales en format FAQ ; (2) fiche Wikidata ; "
          "(3) pitches presse Time Out / Eater / Condé Nast ; (4) ensemencement "
          "organique Reddit r/Lisbon via qualité des avis")],
        [("Direct online order (Phase 2)",
          "Commande directe en ligne (Phase 2)"),
         ("Migration target for A2", "Cible de migration pour A2"),
         ("Pickup-first launch; gift box second; designed against The Folks "
          "Shopify reference",
          "Lancement retrait d'abord ; coffret cadeau ensuite ; conçu contre "
          "la référence Shopify The Folks")],
        [("B2B wholesale (\"Lully Inside\")",
          "Wholesale B2B (« Lully Inside »)"),
         ("Margin-accretive; The Folks-validated pattern",
          "Accroît la marge ; pattern validé par The Folks"),
         ("Landing page + B2B sheet + enquiry form; activate Q4",
          "Page d'atterrissage + fiche B2B + formulaire de contact ; "
          "activer T4")],
    ]
    add_bilingual_table(
        doc,
        headers=[("Channel", "Canal"), ("Role", "Rôle"),
                 ("Specific actions", "Actions concrètes")],
        rows=tier2_rows,
        col_widths=[Cm(3.8), Cm(4.5), Cm(8.7)],
    )

    add_spacer(doc)
    add_heading(doc, "3.4 Channel × Audience Matrix", level=2,
                fr="3.4 Matrice Canaux × Audiences")
    add_para(
        doc,
        "★★★ = primary  ·  ★★ = secondary  ·  ★ = supporting  ·  – = not "
        "relevant",
        italic=True, size=10, color=COLOR_FR,
    )

    matrix_headers = [("Channel", "Canal"), "A1", "A2", "A3", "A4", "A5", "A6"]
    matrix_rows = [
        ["Google Business Profile", "★★★", "★", "★★", "★", "★★★", "★"],
        ["Website SEO", "★", "–", "★★★", "★★★", "★", "–"],
        ["Instagram", "★★", "★", "★★", "★★", "★★", "★"],
        ["TikTok", "–", "–", "★", "★★", "★★", "★"],
        ["Xiaohongshu", "–", "–", "–", "–", "★", "★★★"],
        ["Uber Eats / Glovo", "–", "★★★", "–", "–", "–", "–"],
        ["TripAdvisor", "–", "–", "–", "★★★", "★★", "–"],
        ["GEO (LLM)", "–", "–", "★", "★★", "–", "–"],
        ["Email / Newsletter", "★★", "★", "★", "–", "–", "–"],
        ["Reviews (Google)", "★", "–", "★★", "★★★", "★★★", "★"],
    ]
    add_bilingual_table(
        doc,
        headers=matrix_headers,
        rows=matrix_rows,
        col_widths=[Cm(5.2)] + [Cm(2.0)] * 6,
    )

    doc.add_page_break()

    # ---------- § 4 Three Asymmetric Opportunities ----------
    add_heading(doc, "4. Three Asymmetric Opportunities", level=1,
                fr="4. Trois Opportunités Asymétriques")
    add_bilingual(
        doc,
        "If only three bets matter in the next 12 months, these are them. "
        "Each shares a property: the lever is \"do what no competitor does\", "
        "not \"spend more on the same channel.\"",
        "S'il ne fallait retenir que trois paris pour les 12 prochains mois, "
        "ce sont ceux-ci. Chacun partage une propriété : le levier est "
        "« faire ce qu'aucun concurrent ne fait », non « dépenser plus sur "
        "le même canal ».",
    )

    add_heading(doc, "Opportunity 1 — Operationalise the Baroque story",
                level=2, fr="Opportunité 1 — Opérationnaliser le récit baroque")
    add_bilingual(
        doc,
        "All four Lisbon competitors sit inside a \"modern minimalist\" "
        "aesthetic. Lully's Baroque-contemporary positioning is the only real "
        "differentiator, but today it lives mainly in logo and moodboard. "
        "Concrete content programme: a \"1661 Series\" of long-form journal "
        "pieces; bilingual Baroque plaques next to in-store engravings with "
        "QR linking to articles; packaging and gift boxes designed as IG / "
        "Xiaohongshu props rather than mere wrapping.",
        "Les quatre concurrents lisboètes vivent tous dans une esthétique "
        "« minimalisme moderne ». Le positionnement baroque-contemporain de "
        "Lully est le seul différenciateur réel, mais il vit aujourd'hui "
        "surtout dans le logo et le moodboard. Programme concret : une série "
        "éditoriale « 1661 » d'articles longs ; cartouches baroques "
        "bilingues à côté des gravures en boutique avec QR vers les "
        "articles ; emballages et coffrets cadeaux conçus comme accessoires "
        "IG / Xiaohongshu, non comme simples emballages.",
    )
    add_callout(
        doc, "Why this matters",
        "This is the only lever Dear Breakfast cannot match by spending more — "
        "it requires owning a brand vocabulary they don't have.",
    )

    add_heading(doc, "Opportunity 2 — Win Anjos Sunday brunch first", level=2,
                fr="Opportunité 2 — Gagner d'abord le brunch dominical d'Anjos")
    add_bilingual(
        doc,
        "Dear Breakfast is not in Anjos. doBeco's flagship is in Estefânia. "
        "Padaria 110 closes Sunday. Anjos Sunday brunch is an under-defended "
        "micro-segment. Focus all early marketing pressure on owning it "
        "before fanning out to weekday brunch and other neighbourhoods. This "
        "is a wedge strategy: narrow first, defend, then expand.",
        "Dear Breakfast n'est pas à Anjos. La maison-mère de doBeco est à "
        "Estefânia. Padaria 110 ferme le dimanche. Le brunch dominical à "
        "Anjos est un micro-segment sous-défendu. Concentrer toute la "
        "pression marketing initiale pour le posséder avant de s'étendre au "
        "brunch en semaine et aux autres quartiers. C'est une stratégie de "
        "coin : étroit d'abord, défendre, puis élargir.",
    )

    add_heading(doc, "Opportunity 3 — GEO-ready content infrastructure",
                level=2,
                fr="Opportunité 3 — Infrastructure de contenu prête pour le GEO")
    add_bilingual(
        doc,
        "Generative engines (ChatGPT, Perplexity, Gemini, Claude) increasingly "
        "mediate the \"best of Lisbon\" query. None of the four direct "
        "competitors are visibly optimising for this. The lever is early "
        "infrastructure investment whose returns compound over 12–24 months: "
        "schema.org completeness, FAQ-shaped journal content, a Wikidata "
        "entry with P31/P159/P571/P1448, and editorial press as LLM training "
        "corpus.",
        "Les moteurs génératifs (ChatGPT, Perplexity, Gemini, Claude) "
        "médient de plus en plus la requête « best of Lisbon ». Aucun des "
        "quatre concurrents directs ne s'y prépare visiblement. Le levier "
        "est un investissement d'infrastructure précoce dont les retours se "
        "composent sur 12 à 24 mois : complétude schema.org, contenu "
        "éditorial en format FAQ, fiche Wikidata avec P31/P159/P571/P1448, "
        "et presse éditoriale comme corpus d'entraînement des LLM.",
    )
    add_callout(
        doc, "Honest caveat",
        "GEO ROI is hard to measure today. We invest because the cost is "
        "low and the asymmetric upside is real, not because we can show a "
        "clean attribution chain.",
    )

    doc.add_page_break()

    # ---------- § 5 Roadmap ----------
    add_heading(doc, "5. Roadmap", level=1, fr="5. Feuille de Route")
    add_bilingual(
        doc,
        "A 12-month plan organised in four phases, each with concrete "
        "deliverables and a single binary \"are we on track\" question. "
        "Dates assume kickoff in early June 2026; adjust if website v1 "
        "launch slips.",
        "Un plan sur 12 mois en quatre phases, chacune avec des livrables "
        "concrets et une seule question binaire « sommes-nous dans les temps ». "
        "Les dates supposent un démarrage début juin 2026 ; à ajuster si le "
        "lancement v1 du site glisse.",
    )

    # Phase 0
    add_heading(doc, "Phase 0 — Pre-launch foundation (Weeks 1–4)", level=2,
                fr="Phase 0 — Fondations pré-lancement (Semaines 1–4)")
    add_para(
        doc,
        "Goal: build everything that does not depend on the website. "
        "Companion sprint plan: docs/marketing-phase-0-sprint.md",
        italic=True, size=10, color=COLOR_FR,
    )
    phase0_rows = [
        ["3× GBP fully optimised", "All listings 100% complete + reservation-ready"],
        ["Bilingual in-store review cards", "Live at all 3 store counters"],
        ["IG cadence locked (Reels ≥ 50%)", "4 weeks of scheduled content"],
        ["5 Story Highlight covers (Baroque)", "Highlights live on IG profile"],
        ["Newsletter capture on IG + posters", "First 50 subscribers from non-site sources"],
        ["Baseline tracking doc", "docs/marketing-baseline.md committed"],
    ]
    add_bilingual_table(
        doc,
        headers=[("Deliverable", "Livrable"), ("Done when", "Terminé quand")],
        rows=phase0_rows,
        col_widths=[Cm(6.5), Cm(10.5)],
    )
    add_callout(
        doc, "Phase 0 question",
        "Is the foot-traffic acquisition engine running without the website?",
    )

    # Phase 1
    add_heading(doc, "Phase 1 — Website launch + organic foundation (Months 1–3)",
                level=2,
                fr="Phase 1 — Lancement du site + fondations organiques (Mois 1–3)")
    phase1_rows = [
        ["Sitemap submitted to GSC + Bing", "First impressions visible in GSC"],
        ["LocalBusiness/Restaurant JSON-LD live", "Rich Results test passes"],
        ["Brunch landing page SEO-live", "Indexed; ranking ≤ 50 for primary term"],
        ["9× menu-item pages live with schema", "All indexed"],
        ["3× store detail pages live", "Indexed in PT + EN"],
        ["Journal launched (4 inaugural articles)", "First articles live; first GSC impressions"],
        ["TripAdvisor business listings claimed", "All 3 show \"claimed\""],
        ["Influencer outreach round 1", "First sponsored post live"],
        ["Packaging insert programme live", "First newsletter signups attributed to insert QR"],
    ]
    add_bilingual_table(
        doc,
        headers=[("Deliverable", "Livrable"), ("Done when", "Terminé quand")],
        rows=phase1_rows,
        col_widths=[Cm(6.5), Cm(10.5)],
    )
    add_callout(
        doc, "Phase 1 question",
        "Are organic Google impressions trending upward and reviews accumulating?",
    )

    # Phase 2
    add_heading(doc, "Phase 2 — Commerce + brand depth (Months 4–6)", level=2,
                fr="Phase 2 — E-commerce + profondeur de marque (Mois 4–6)")
    phase2_rows = [
        ["Direct pickup ordering live", "First direct order placed without Uber/Glovo"],
        ["Festive Orders online", "First festive order placed online"],
        ["Uber → direct migration campaign active", "Migration rate ≥ 10% measurable"],
        ["Press round 1 (Time Out, Eater, Observador, Le Monde Voyage)",
         "At least one feature published"],
        ["\"The 1661 Series\" launched in Journal", "3 articles live; first external citation"],
        ["In-store Baroque plaque programme (Anjos pilot)", "Plaques installed at Anjos"],
        ["Influencer round 2 (2 micro + 1 travel blogger)", "3 sponsored posts live"],
    ]
    add_bilingual_table(
        doc,
        headers=[("Deliverable", "Livrable"), ("Done when", "Terminé quand")],
        rows=phase2_rows,
        col_widths=[Cm(6.5), Cm(10.5)],
    )
    add_callout(
        doc, "Phase 2 question",
        "Is the direct revenue path covering its own marketing cost?",
    )

    # Phase 3
    add_heading(doc, "Phase 3 — International + GEO + scale (Months 7–12)",
                level=2,
                fr="Phase 3 — International + GEO + échelle (Mois 7–12)")
    phase3_rows = [
        ["Xiaohongshu KOC programme (5 partnerships)", "5 posts live with attribution"],
        ["TikTok channel independent of IG", "12+ TikTok-native videos posted"],
        ["Wikidata entry created and verified", "Entity live with required properties"],
        ["GEO content audit + gap-closing articles",
         "Audit doc + 5 new FAQ-shaped articles"],
        ["B2B \"Lully Inside\" landing page + form", "First B2B enquiry received"],
        ["Press round 2 (Condé Nast Traveler, AFAR, The Infatuation)",
         "At least one international feature"],
        ["Gift box online + worldwide-ship feasibility", "Scoping doc + go/no-go"],
        ["Annual SEO + reviews + GEO state-of-play report",
         "Year-1 KPI tree filled in"],
    ]
    add_bilingual_table(
        doc,
        headers=[("Deliverable", "Livrable"), ("Done when", "Terminé quand")],
        rows=phase3_rows,
        col_widths=[Cm(6.5), Cm(10.5)],
    )
    add_callout(
        doc, "Phase 3 question",
        "Are international audiences (A4, A6) measurably part of the customer mix?",
    )

    doc.add_page_break()

    # ---------- § 6 KPI Framework ----------
    add_heading(doc, "6. KPI Framework", level=1, fr="6. Cadre de Mesure")
    add_bilingual(
        doc,
        "KPIs organised by funnel stage. Do not chase all metrics "
        "simultaneously — each phase has one primary metric the phase "
        "question is testing.",
        "KPI organisés par étape d'entonnoir. Ne poursuivez pas tous les "
        "indicateurs à la fois — chaque phase a un indicateur principal que "
        "la question de phase teste.",
    )

    kpi_rows = [
        [("Awareness", "Notoriété"),
         ("Google organic impressions (PT + EN)",
          "Impressions organiques Google"),
         "30k → 200k/month"],
        [("Awareness", "Notoriété"),
         ("GBP \"Discovery searches\" (3 stores combined)",
          "Recherches de découverte GBP (3 boutiques)"),
         "5× growth"],
        [("Awareness", "Notoriété"),
         ("IG reach + TikTok views", "Portée IG + vues TikTok"),
         "Baseline → +200%"],
        [("Consideration", "Considération"),
         ("Site sessions (organic)", "Sessions site (organique)"),
         "0 → 25k/month"],
        [("Consideration", "Considération"),
         ("Newsletter subscribers", "Abonnés infolettre"),
         "0 → 3,000"],
        [("Consideration", "Considération"),
         ("Google Reviews count + rating",
          "Nombre + note des avis Google"),
         "Total ≥ 600, avg ≥ 4.7"],
        [("Conversion", "Conversion"),
         ("Table reservations (Anjos)", "Réservations (Anjos)"),
         "Baseline → +60%"],
        [("Conversion", "Conversion"),
         ("Uber/Glovo orders", "Commandes Uber/Glovo"),
         "Baseline → +40%"],
        [("Conversion", "Conversion"),
         ("Direct online orders (Phase 2)",
          "Commandes directes en ligne (Phase 2)"),
         "0 → 20% of online volume"],
        [("Loyalty", "Fidélité"),
         ("Email open rate", "Taux d'ouverture infolettre"),
         "≥ 35%"],
        [("Loyalty", "Fidélité"),
         ("Repeat purchase rate (direct only)",
          "Taux de réachat (direct)"),
         "≥ 30% within 60 days"],
    ]
    add_bilingual_table(
        doc,
        headers=[("Funnel stage", "Étape"),
                 ("Metric", "Indicateur"),
                 ("12-month target", "Cible 12 mois")],
        rows=kpi_rows,
        col_widths=[Cm(3.0), Cm(8.0), Cm(6.0)],
    )

    add_spacer(doc)
    add_heading(doc, "6.1 North Star Metrics", level=2,
                fr="6.1 Étoiles Polaires")
    add_bilingual(
        doc,
        "Two metrics matter above all others: (1) Anjos Sunday brunch "
        "table-fill rate — validates the wedge strategy. (2) Direct revenue % "
        "of total online revenue (Phase 2 onwards) — validates that the "
        "marketing engine is building Lully's database, not Uber Eats'.",
        "Deux indicateurs comptent plus que tous les autres : (1) Taux de "
        "remplissage des tables du brunch dominical à Anjos — valide la "
        "stratégie de coin. (2) Part du chiffre d'affaires direct dans le "
        "total en ligne (à partir de la Phase 2) — valide que le moteur "
        "marketing alimente la base de données de Lully, non celle d'Uber "
        "Eats.",
    )

    doc.add_page_break()

    # ---------- § 7 Investment Shape ----------
    add_heading(doc, "7. Investment Shape", level=1,
                fr="7. Forme d'Investissement")
    add_bilingual(
        doc,
        "A directional budget split for year 1, not a fixed allocation. "
        "Adjust quarterly based on phase questions.",
        "Une répartition budgétaire directionnelle pour l'année 1, non une "
        "allocation figée. À ajuster trimestriellement selon les questions "
        "de phase.",
    )

    inv_rows = [
        [("Content production (photo, video, journal)",
          "Production de contenu (photo, vidéo, journal)"),
         "~40%",
         ("Highest-ROI investment; everything else fails without good content.",
          "Investissement à plus fort ROI ; tout le reste échoue sans bon "
          "contenu.")],
        [("Influencer / KOC partnerships",
          "Partenariats influenceurs / KOC"),
         "~25%",
         ("Lisbon food + travel + Xiaohongshu KOC mix; €100–€500/post.",
          "Mix food + voyage Lisbonne + KOC Xiaohongshu ; €100–€500/post.")],
        [("Tools + paid-media testing",
          "Outils + tests média payants"),
         "~20%",
         ("Ahrefs/Semrush; Buffer/Later; Meta + Google Ads for retargeting "
          "only in months 1–6.",
          "Ahrefs/Semrush ; Buffer/Later ; Meta + Google Ads en retargeting "
          "uniquement, mois 1–6.")],
        [("PR + media outreach", "Relations presse"),
         "~15%",
         ("Critical for GEO via training-corpus inclusion.",
          "Crucial pour le GEO via inclusion dans les corpus d'entraînement.")],
    ]
    add_bilingual_table(
        doc,
        headers=[("Category", "Catégorie"),
                 ("Year-1 share", "Part année 1"),
                 ("Notes", "Notes")],
        rows=inv_rows,
        col_widths=[Cm(5.0), Cm(3.0), Cm(9.0)],
    )

    add_spacer(doc)
    add_callout(
        doc, "What we deliberately do not invest in (year 1)",
        "Large-scale paid social ads (build organic moat first); SEO "
        "link-building agencies (a Time Out feature beats a link farm); a "
        "self-operated Xiaohongshu account (KOC partnerships dominate this "
        "channel).",
    )

    doc.add_page_break()

    # ---------- § 8 Decisions Needed ----------
    add_heading(doc, "8. Decisions Needed from Client", level=1,
                fr="8. Décisions Attendues du Client")
    add_bilingual(
        doc,
        "Five decisions unblock the Phase 0 sprint. Each one is binary or "
        "short-list.",
        "Cinq décisions débloquent le sprint de Phase 0. Chacune est binaire "
        "ou à choix court.",
    )

    dec_rows = [
        ["1", ("Domain locked?", "Domaine arrêté ?"),
         ("lully1661.pt / lully1661.com / other — needed for GBP linking and "
          "email setup",
          "lully1661.pt / lully1661.com / autre — requis pour le lien GBP "
          "et la configuration email")],
        ["2", ("Social ownership", "Propriété des comptes sociaux"),
         ("In-house manager / agency / hybrid — affects content cadence "
          "feasibility",
          "Manager interne / agence / hybride — affecte la faisabilité de la "
          "cadence")],
        ["3", ("Review programme go/no-go", "Programme d'avis : feu vert ?"),
         ("Print cards + train staff (low cost, high ROI) — needs operational "
          "sign-off",
          "Imprimer les cartes + former le personnel (faible coût, fort "
          "ROI) — validation opérationnelle nécessaire")],
        ["4", ("Phase-2 commerce timeline",
               "Calendrier Phase 2 e-commerce"),
         ("Confirm month for direct pickup launch — drives migration funnel "
          "design",
          "Confirmer le mois du lancement retrait direct — pilote la "
          "conception de l'entonnoir de migration")],
        ["5", ("PR budget commitment", "Engagement budget RP"),
         ("Year-1 envelope for press outreach (€3k / €8k / €15k tiers) — "
          "drives GEO realism",
          "Enveloppe année 1 pour les relations presse (tranches €3k / €8k "
          "/ €15k) — pilote le réalisme GEO")],
    ]
    add_bilingual_table(
        doc,
        headers=[("#", None), ("Decision", "Décision"),
                 ("Options", "Options")],
        rows=dec_rows,
        col_widths=[Cm(1.0), Cm(5.0), Cm(11.0)],
    )

    doc.add_page_break()

    # ---------- § 9 Out of scope ----------
    add_heading(doc, "9. What This Strategy Does Not Cover", level=1,
                fr="9. Ce Que Cette Stratégie ne Couvre Pas")
    add_bilingual(
        doc,
        "Honest scope boundaries — items we acknowledge but defer.",
        "Limites de périmètre honnêtes — éléments reconnus mais reportés.",
    )
    add_para(doc, "·  Paid media playbooks (deferred until Tier 1 organic "
                  "baseline exists)")
    add_para(doc, "·  Loyalty programme mechanics (year 2 once direct CRM "
                  "has scale)")
    add_para(doc, "·  Catering & events marketing (Phase 3+)")
    add_para(doc, "·  Internal team org / hiring (separate doc)")
    add_para(doc, "·  Crisis communications playbook (out of scope here)")

    add_spacer(doc)

    # ---------- § 10 Glossary ----------
    add_heading(doc, "10. Glossary", level=1, fr="10. Glossaire")
    glossary_rows = [
        [("GBP (Google Business Profile)", "Profil Google Business"),
         ("Free Google listing for physical businesses; controls Maps + "
          "Knowledge Panel presence.",
          "Fiche Google gratuite pour entreprises physiques ; contrôle la "
          "présence sur Maps + Knowledge Panel.")],
        [("GEO (Generative Engine Optimization)",
          "Optimisation pour Moteurs Génératifs"),
         ("The discipline of making a brand likely to be recommended by AI "
          "chatbots (ChatGPT, Perplexity, Gemini, Claude).",
          "Discipline visant à faire recommander une marque par les IA "
          "génératives (ChatGPT, Perplexity, Gemini, Claude).")],
        [("JSON-LD / schema.org", "JSON-LD / schema.org"),
         ("Structured-data format embedded in pages so engines + LLMs "
          "understand entities (business, menu items, hours).",
          "Format de données structurées intégré aux pages pour que moteurs "
          "et LLM comprennent les entités (entreprise, plats, horaires).")],
        [("hreflang", "hreflang"),
         ("HTML attribute signalling to search engines that two pages are "
          "the same content in different languages.",
          "Attribut HTML signalant aux moteurs que deux pages sont un même "
          "contenu en différentes langues.")],
        [("KOC (Key Opinion Consumer)", "KOC (Key Opinion Consumer)"),
         ("Small/medium influencer treated as a peer recommender rather "
          "than celebrity endorser; dominant on Xiaohongshu.",
          "Influenceur de petite/moyenne taille perçu comme un pair, non "
          "comme une célébrité ; dominant sur Xiaohongshu.")],
        [("Wedge strategy", "Stratégie de coin"),
         ("Win a narrow micro-segment first (here: Anjos Sunday brunch), "
          "then expand outward.",
          "Gagner d'abord un micro-segment étroit (ici : brunch dominical à "
          "Anjos), puis s'étendre.")],
        [("Xiaohongshu (RED / 小红书)", "Xiaohongshu (RED / 小红书)"),
         ("Chinese visual social platform dominant for travel + lifestyle "
          "discovery.",
          "Plateforme sociale visuelle chinoise dominante pour la "
          "découverte voyage + lifestyle.")],
    ]
    add_bilingual_table(
        doc,
        headers=[("Term", "Terme"), ("Definition", "Définition")],
        rows=glossary_rows,
        col_widths=[Cm(5.5), Cm(11.5)],
    )

    add_spacer(doc, 2)
    closing = doc.add_paragraph()
    closing.alignment = WD_ALIGN_PARAGRAPH.CENTER
    rc = closing.add_run("End of document — Fin du document   ·   v0.1 · 2026-05-22")
    rc.italic = True
    rc.font.size = Pt(9)
    rc.font.color.rgb = COLOR_META

    OUT.parent.mkdir(parents=True, exist_ok=True)
    doc.save(OUT)
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    build()
