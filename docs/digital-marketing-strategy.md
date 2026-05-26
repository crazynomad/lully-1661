# Digital Marketing Strategy — Lully 1661
# Stratégie de Marketing Digital — Lully 1661

**Status / Statut :** v0.1 — Draft for client review / Brouillon pour relecture client
**Prepared / Préparé le :** 2026-05-22
**Languages / Langues :** English (primary working language) + French (client-facing)
**Scope / Périmètre :** Integrated digital marketing across website, e-commerce, Instagram, Xiaohongshu, SEO, GEO, Google Business, reviews & CRM — for the 3-store Lisbon footprint
**Companion docs / Documents liés :** [`competitor-scan.md`](./competitor-scan.md) · [`platform-recommendation-v2.md`](./platform-recommendation-v2.md) · [`architecture.md`](./architecture.md)

---

## 0. TL;DR — Five Strategic Anchors / Cinq Ancres Stratégiques

**EN.** Lully 1661 has one real digital moat its four competitors do not: a Baroque-heritage narrative in a Lisbon market where every alternative is a flavour of "modern minimalist." The job of the next 12 months is to convert that brand asymmetry into a measurable lead in (a) Google search for "brunch / bakery / Sunday brunch Lisbon", (b) Instagram and TikTok discovery, (c) traveler-facing review platforms (Google, TripAdvisor), and (d) generative engines (ChatGPT, Perplexity, Gemini) — while parallel-tracking a migration of Uber Eats / Glovo customers to direct ordering once Phase-2 commerce ships.

**FR.** Lully 1661 possède un fossé de marque que ses quatre concurrents directs n'ont pas : un récit baroque dans un marché lisboète où chaque alternative est une déclinaison du « minimalisme moderne ». La mission des 12 prochains mois est de transformer cette asymétrie de marque en avance mesurable sur (a) la recherche Google « brunch / boulangerie / brunch du dimanche Lisbonne », (b) la découverte sur Instagram et TikTok, (c) les plateformes d'avis des voyageurs (Google, TripAdvisor), et (d) les moteurs génératifs (ChatGPT, Perplexity, Gemini) — tout en orchestrant en parallèle la migration des clients Uber Eats / Glovo vers la commande directe dès que la Phase 2 e-commerce sera livrée.

| # | Anchor / Ancre | One-liner / En une ligne |
|---|----------------|--------------------------|
| 1 | **Own the Baroque story** / **Posséder le récit baroque** | Convert visual heritage into a content engine — the only differentiator competitors cannot copy. / Transformer l'héritage visuel en moteur de contenu — le seul différenciateur incopiable. |
| 2 | **Win Anjos Sunday brunch first** / **Gagner d'abord le brunch dominical d'Anjos** | Wedge into a micro-segment competitors don't serve (Dear Breakfast off-zone, Padaria 110 closed Sunday). / S'enraciner dans un micro-segment vacant (Dear Breakfast hors zone, Padaria 110 fermée le dimanche). |
| 3 | **Treat Uber Eats / Glovo as paid acquisition, not sales** / **Considérer Uber Eats / Glovo comme acquisition payante, non comme un canal de vente** | Design a packaging → newsletter → direct-order funnel from day one. / Concevoir un entonnoir packaging → infolettre → commande directe dès le premier jour. |
| 4 | **Build GEO-ready content infrastructure before competitors notice** / **Construire une infrastructure de contenu prête pour le GEO avant les concurrents** | Schema.org + FAQ-shaped journal + Wikidata entry — 18-month compounding bet. / Schema.org + journal en format FAQ + fiche Wikidata — pari à effet composé sur 18 mois. |
| 5 | **Reviews are SEO** / **Les avis sont du SEO** | Google + TripAdvisor reviews matter as much as backlinks for the traveler audience. / Les avis Google et TripAdvisor pèsent autant que les backlinks pour l'audience voyageurs. |

---

## 1. Where Lully 1661 Stands / Positionnement Actuel

### 1.1 Asset Inventory / Inventaire des Actifs

| Dimension | Current state / État actuel |
|---|---|
| **Stores / Boutiques** | 3 — Anjos (flagship + brunch + dine-in + only Sunday opening), Beato, Campo de Ourique |
| **Brand position / Positionnement de marque** | "Boulangerie Renaissance" — Baroque copperplate + 1661 namesake heritage + three sub-brands (Caffetier, Meunier, Patissière) |
| **Product range / Gamme produit** | 48h-fermented sourdough breads (Paillard, Fâcheux) + French viennoiserie + cosmopolitan brunch (Benedict, Florentine, Cilbir, Pain Perdu, Avocado, Le Menuet, Le Monsieur, Sopa do Mês) |
| **Digital maturity / Maturité digitale** | **Bottom of competitive set today** — no live site, social-only. After v1 launch: parity with Dear Breakfast, ahead of doBeco & Padaria 110, still behind The Folks on commerce depth |
| **Delivery / Livraison** | Uber Eats + Glovo only (no direct online order in v1) |
| **Site languages / Langues du site** | PT + EN (per `lib/i18n/routing.ts`) — CN not in scope for v1 |
| **CMS** | Keystatic, git-backed, owner-editable weekly menu |

### 1.2 The Three Truths of the Lisbon Landscape / Les Trois Vérités du Paysage Lisboète

**EN — Truth 1.** You are not competing for "the nearest bakery." You are competing for algorithmic visibility — in Google Search, Instagram Explore, Google Maps, TripAdvisor, and increasingly in generative-AI answers. By the time a traveler types "best brunch Lisbon" on the plane, the fight is already underway. Dear Breakfast and The Folks have a multi-year head-start on this front; we close it with structure (schema markup, multilingual SEO, journal content) rather than spend.

**FR — Vérité 1.** Vous ne vous battez pas pour « la boulangerie la plus proche ». Vous vous battez pour la visibilité algorithmique — Google Search, Instagram Explore, Google Maps, TripAdvisor, et de plus en plus les réponses des IA génératives. Au moment où un voyageur tape « best brunch Lisbon » dans l'avion, la bataille a déjà commencé. Dear Breakfast et The Folks ont plusieurs années d'avance ; nous rattrapons par la structure (balisage schema.org, SEO multilingue, journal éditorial) plutôt que par la dépense publicitaire.

**EN — Truth 2.** The Folks proves that "Lisbon bakery/café e-commerce works" — they ship coffee worldwide via Shopify with full B2B wholesale. This is not aspiration; it's validation of Lully's Phase-2 commerce hypothesis. They are the benchmark we will eventually be compared against, not a model to copy wholesale (their category is coffee-first, ours is bakery-first).

**FR — Vérité 2.** The Folks démontre qu'un e-commerce de boulangerie/café à Lisbonne fonctionne — ils expédient du café dans le monde entier via Shopify et gèrent un wholesale B2B complet. Ce n'est pas une aspiration, c'est la validation de l'hypothèse e-commerce Phase 2 de Lully. Ils sont le benchmark de référence, pas un modèle à copier intégralement (leur catégorie est avant tout café, la nôtre avant tout boulangerie).

**EN — Truth 3.** doBeco is the most dangerous neighbour — same 3-store scale, same bakery + brunch positioning, same Lisbon geography, same premium pricing. Their advantage is a chef-driven origin story (António José de Mello, pandemic garage). Our advantage is a richer brand vocabulary (1661, Renaissance, three guild sub-brands). To convert that into a real lead, the heritage story has to leave the moodboard and live in journal articles, packaging plaques, and store fittings.

**FR — Vérité 3.** doBeco est le voisin le plus dangereux — même échelle de 3 boutiques, même positionnement boulangerie + brunch, même géographie lisboète, même tarification premium. Leur avantage est un récit fondateur porté par un chef (António José de Mello, garage en confinement). Le nôtre est un vocabulaire de marque plus riche (1661, Renaissance, trois sous-marques de corporation). Pour transformer cet avantage en avance réelle, le récit patrimonial doit sortir du moodboard et s'incarner dans des articles éditoriaux, des cartouches sur les emballages, et le mobilier des boutiques.

---

## 2. Audience Segmentation / Segmentation des Audiences

**EN.** The client brief identifies two audiences (local + traveler). Operationally this is too coarse — different sub-segments make decisions through entirely different funnels. We refine into six segments below; the channel matrix in § 4 is built directly on this segmentation.

**FR.** Le brief client identifie deux audiences (locaux + voyageurs). Opérationnellement c'est trop large — les sous-segments décident à travers des entonnoirs entièrement différents. Nous affinons en six segments ci-dessous ; la matrice de canaux (§ 4) en découle directement.

| # | Segment | Trigger / Déclencheur | Decision window / Fenêtre de décision | Primary channels / Canaux principaux | Search/mental cue / Indice de recherche |
|---|---------|-----------------------|---------------------------------------|--------------------------------------|-----------------------------------------|
| **A1** | **Neighbourhood regular** / Habitué·e du quartier (PT residents + long-term expats) | Weekend ritual, commute pass-by / Rituel week-end, trajet quotidien | Instant / habit — Instantané / habitude | Google Maps + IG + word of mouth | "ma boulangerie du coin" / "the one near me" |
| **A2** | **Local delivery user** / Client livraison local (lives near, prefers not to leave home) | Sunday morning, rainy day / Dimanche matin, jour de pluie | Short / impulse — Court / impulsion | Uber Eats + Glovo + IG Stories | "Lully delivers pain perdu" / "Lully livre le pain perdu" |
| **A3** | **Cross-city Lisboner** / Lisboète d'un autre quartier | Destination weekend brunch / Brunch week-end de destination | Mid / planned — Moyen / planifié | Google "best brunch lisbon" + IG saves + TripAdvisor | "best brunch in Lisbon" / "meilleur brunch Lisbonne" |
| **A4** | **International traveler — planner** / Voyageur international planificateur | Pre-trip research, 1–4 weeks out / Recherche pré-voyage, 1–4 semaines avant | Long / high-research — Long / forte recherche | Google + TripAdvisor + Reddit + **AI chatbots (GEO)** | "best bakery lisbon" / "croissant lisbon" / "boulangerie Lisbonne" |
| **A5** | **International traveler — walker** / Voyageur international en exploration | On the street in Lisbon / Dans la rue à Lisbonne | Instant / impulse — Instantané / impulsion | Google Maps + IG geotag + walking guides | "bakery near me" / "boulangerie à proximité" |
| **A6** | **Chinese traveler** / Voyageur chinois | Pre-trip Xiaohongshu inspiration + on-trip search / Inspiration pré-voyage sur Xiaohongshu + recherche sur place | Long / visual-driven — Long / piloté par le visuel | **Xiaohongshu (RED) + Dianping (international) + Baidu** | "里斯本 brunch" / "里斯本面包店" |

### 2.1 What the Client Brief Missed / Ce que le Brief Client a Manqué

**EN.** Two strategic gaps in the client's own framing:

1. **The Uber Eats / Glovo "channel economics" gap.** Each Uber/Glovo order pays ~30% to a third party AND donates the customer relationship to that platform. Without an explicit migration funnel (packaging insert → newsletter signup → direct order discount), the brand is paying to grow someone else's database. This needs to be designed *before* Phase-2 commerce launches, not after.
2. **The A4 vs A5 gap.** The pre-trip planner and the on-street walker use entirely different surfaces — the first is reached by SEO, GEO, and TripAdvisor; the second by Google Business Profile and Instagram geotags. Many bakeries reach one and miss the other.

**FR.** Deux lacunes stratégiques dans la formulation du client :

1. **L'économie de canal Uber Eats / Glovo.** Chaque commande Uber/Glovo verse ~30 % à un tiers ET cède la relation client à cette plateforme. Sans entonnoir de migration explicite (encart d'emballage → inscription infolettre → réduction sur commande directe), la marque paie pour faire grossir la base de données d'un autre. Cela doit se concevoir *avant* le lancement Phase 2 e-commerce, pas après.
2. **L'écart A4 vs A5.** Le planificateur pré-voyage et le marcheur sur place utilisent des surfaces entièrement différentes — le premier via SEO, GEO et TripAdvisor ; le second via Google Business Profile et géotags Instagram. Beaucoup de boulangeries en atteignent un et manquent l'autre.

---

## 3. Channel Strategy / Stratégie de Canaux

We organise channels in three tiers by **time-to-launch** and **dependency on website v1**.

Nous organisons les canaux en trois tiers selon le **temps de lancement** et la **dépendance au site v1**.

### 3.1 Tier 0 — Launch immediately, no website dependency / Démarrage immédiat, sans dépendance au site

| Channel / Canal | Role / Rôle | Specific actions / Actions concrètes |
|---|---|---|
| **Google Business Profile (×3)** | A1, A3, A5 first touch — first point of contact for foot-traffic audiences | Verify all 3 listings; upload interior + product photos; mark Anjos Sunday hours; add menu link; add reservation link; seed 5–10 Q&As per store (EN + PT) |
| **Instagram (existing)** | Brand visual + A4/A5 discovery via geotag + A1/A2 retention | Reels ≥ 50% of weekly output; every post geotagged + 4–6 EN hashtags (#lisbonbakery #brunchlisbon #lisboneats); 5 Story Highlights with Baroque cover design (Brunch / Stores / Behind the bake / Press / Festive) |
| **In-store review programme** / Programme d'avis en boutique | Reviews are SEO (Truth above) — feeds Google, TripAdvisor, GEO | Print bilingual review cards with QR; train baristas on the 30-second ask; target 200+ reviews per store within 6 months at ≥ 4.7 average |
| **Newsletter (footer prompt already wired)** | Container for Uber→Direct migration; weekly menu container | Open signups now via IG bio + in-store posters; weekly cadence locked to `weeklyMenuItem` content model |

### 3.2 Tier 1 — Activate at website v1 launch / Activation au lancement du site v1

| Channel / Canal | Role / Rôle | Specific actions / Actions concrètes |
|---|---|---|
| **Website (lully1661.\*)** | Ground truth for SEO + GEO + hreflang + structured data | Submit sitemap to Google Search Console + Bing Webmaster Tools; complete LocalBusiness/Restaurant JSON-LD per store; MenuItem JSON-LD per dish; canonical + hreflang per page (already scaffolded in `lib/seo.ts`) |
| **Brunch landing page** | Primary A3 + A4 landing — "best brunch Lisbon" target | Single page optimised for `brunch lisbon`, `best brunch lisbon`, `sunday brunch lisbon`; Hero + signature dishes + Anjos location + reservation CTA; FAQ block (LLM-friendly format) |
| **Per-store detail pages (×3)** | A1 + A5 geographic SEO | Each page targets `{cuisine type} {neighbourhood}` long-tails: Anjos = brunch + bakery; Beato = bakery + viennoiserie; Campo de Ourique = bakery + pastry |
| **Per-menu-item pages (×9)** | Long-tail SEO + journal seed | One page per signature item with Recipe/MenuItem schema; targets `eggs benedict lisbon`, `pain perdu lisbon`, `cilbir lisbon` etc. |
| **Journal (blog)** | SEO + GEO content engine | Two content lines: (a) **Lisbon-context** — "Where to brunch in Anjos", walking guides; (b) **Craft + heritage** — "Why we ferment sourdough 48h", "The 1661 in Lully 1661" (this is the Baroque moat operationalised) |
| **TripAdvisor business listing** | A4 traveler primary funnel | Claim listing; complete profile; review request integrated into in-store programme |

### 3.3 Tier 2 — Activate post-launch (Months 3–9) / Activation post-lancement (Mois 3–9)

| Channel / Canal | Role / Rôle | Specific actions / Actions concrètes |
|---|---|---|
| **TikTok** | A4 + A5 + A6 discovery, lower competition than IG Reels | Mirror IG Reels initially; add Lisbon city-context content; weekly cadence |
| **Xiaohongshu (RED)** | A6 — Chinese traveler segment, currently 0% covered | **Do not run a self-operated account.** Minimum viable: claim verified account, 5 polished CN notes, CN menu. Real lever: 5–10 Lisbon-based Chinese KOC partnerships at €100–€300/post |
| **GEO (Generative Engine Optimization / Optimisation pour Moteurs Génératifs)** | A4 — increasingly discovers via ChatGPT/Perplexity/Gemini | (1) FAQ-shaped journal answers ("Where is the best Sunday brunch in Lisbon?"); (2) Wikidata entry with P31/P159/P571/P1448; (3) press pitches to Time Out Lisbon, Eater, Condé Nast Traveler (these are LLM training sources); (4) Reddit r/Lisbon organic seeding via review quality |
| **Direct online order (Phase 2)** | Migration target for A2 | Pickup-first launch; gift box second; designed against The Folks Shopify reference |
| **B2B wholesale ("Lully Inside")** | Margin-accretive channel; The Folks-validated pattern | Landing page + downloadable B2B sheet + enquiry form; activate Q4 |

### 3.4 Channel × Audience Matrix / Matrice Canaux × Audiences

★★★ = primary channel / canal principal · ★★ = secondary / secondaire · ★ = supporting / soutien · – = not relevant / non pertinent

|  | A1 | A2 | A3 | A4 | A5 | A6 |
|---|---|---|---|---|---|---|
| Google Business Profile | ★★★ | ★ | ★★ | ★ | ★★★ | ★ |
| Website SEO | ★ | – | ★★★ | ★★★ | ★ | – |
| Instagram | ★★ | ★ | ★★ | ★★ | ★★ | ★ |
| TikTok | – | – | ★ | ★★ | ★★ | ★ |
| Xiaohongshu | – | – | – | – | ★ | ★★★ |
| Uber Eats / Glovo | – | ★★★ | – | – | – | – |
| TripAdvisor | – | – | – | ★★★ | ★★ | – |
| GEO (LLM) | – | – | ★ | ★★ | – | – |
| Email / Newsletter | ★★ | ★ | ★ | – | – | – |
| Reviews (Google) | ★ | – | ★★ | ★★★ | ★★★ | ★ |

---

## 4. Three Asymmetric Opportunities / Trois Opportunités Asymétriques

**EN.** If only three bets matter in the next 12 months, these are the three. Each shares a property: the lever is "do what no competitor does", not "spend more on the same channel."

**FR.** S'il ne fallait retenir que trois paris pour les 12 prochains mois, ce sont ceux-ci. Chacun partage une propriété : le levier est « faire ce qu'aucun concurrent ne fait », non « dépenser plus sur le même canal ».

### Opportunity 1 — Operationalise the Baroque story / Opportunité 1 — Opérationnaliser le récit baroque

**EN.** Per the competitor scan, all four Lisbon competitors sit inside a "modern minimalist" aesthetic. Lully's Baroque-contemporary positioning is the only real differentiator, but today it lives mainly in logo and moodboard. Concrete content programme:

- **Journal series "The 1661 Series"** — long-form pieces on 17th-century French baking history, the Lully namesake, copperplate engraving craft, the multiple meanings of "Renaissance"
- **In-store Baroque plaques** — each engraving in the store gets a small bilingual plaque + QR linking to the related journal article
- **Packaging and gift boxes as IG/Xiaohongshu props** — the Baroque pattern is a visual hook, not decoration

**FR.** D'après l'analyse concurrentielle, les quatre concurrents lisboètes vivent tous dans une esthétique « minimalisme moderne ». Le positionnement baroque-contemporain de Lully est le seul différenciateur réel, mais il vit aujourd'hui surtout dans le logo et le moodboard. Programme de contenu concret :

- **Série éditoriale « The 1661 Series »** — articles longs sur l'histoire de la boulangerie française du XVIIᵉ siècle, le nom Lully, l'art de la gravure sur cuivre, les multiples sens de « Renaissance »
- **Cartouches baroques en boutique** — chaque gravure reçoit un petit cartouche bilingue + QR vers l'article correspondant
- **Emballages et coffrets cadeaux comme accessoires IG/Xiaohongshu** — le motif baroque est un crochet visuel, pas une décoration

> **Why this matters / Pourquoi c'est important.** This is the only lever Dear Breakfast cannot match by spending more — it requires owning a brand vocabulary they don't have. / C'est le seul levier que Dear Breakfast ne peut pas égaler en dépensant plus — il exige de posséder un vocabulaire de marque qu'ils n'ont pas.

### Opportunity 2 — Win Anjos Sunday brunch first / Opportunité 2 — Gagner d'abord le brunch dominical d'Anjos

**EN.** Dear Breakfast is not in Anjos. doBeco's flagship is in Estefânia. Padaria 110 closes Sunday. Anjos Sunday brunch is an under-defended micro-segment. Focus all early marketing pressure on owning it before fanning out to weekday brunch and other neighbourhoods. This is a "wedge strategy": narrow first, defend, then expand.

- Own the `sunday brunch lisbon` keyword
- Saturday-evening + Sunday-morning IG Stories ("we open tomorrow at 8:30" / "we're open now")
- Monthly "Sunday at Anjos" cinematic Reel

**FR.** Dear Breakfast n'est pas à Anjos. La maison-mère de doBeco est à Estefânia. Padaria 110 ferme le dimanche. Le brunch dominical à Anjos est un micro-segment sous-défendu. Concentrer toute la pression marketing initiale pour le posséder avant de s'étendre au brunch en semaine et aux autres quartiers. C'est une « stratégie de coin » : étroit d'abord, défendre, puis élargir.

- Posséder le mot-clé `brunch dimanche Lisbonne` / `sunday brunch lisbon`
- Stories Instagram du samedi soir et du dimanche matin (« on ouvre demain à 8h30 » / « ouvert maintenant »)
- Un Reel cinématique mensuel « Dimanche à Anjos »

### Opportunity 3 — GEO-ready content infrastructure / Opportunité 3 — Infrastructure de contenu prête pour le GEO

**EN.** Generative engines (ChatGPT, Perplexity, Gemini, Claude) increasingly mediate the "best of Lisbon" query. None of the four direct competitors are visibly optimising for this. The lever is early infrastructure investment whose returns compound over 12–24 months.

- **schema.org completeness** — already scoped in `lib/jsonld/`
- **FAQ-shaped journal content** — directly answer "Where is the best Sunday brunch in Lisbon?" as a declarative paragraph; LLMs preferentially retrieve these
- **Wikidata entry** — fill P31 (instance of: bakery), P159 (HQ location: Lisbon), P571 (founded: 2022), P1448 (official name: Lully 1661)
- **Press as training corpus** — one feature in Time Out Lisbon, Eater, Condé Nast Traveler is worth more for GEO than 100 backlinks of the same DA, because LLMs train on editorial corpora

**FR.** Les moteurs génératifs (ChatGPT, Perplexity, Gemini, Claude) médient de plus en plus la requête « best of Lisbon ». Aucun des quatre concurrents directs ne s'y prépare visiblement. Le levier est un investissement d'infrastructure précoce dont les retours se composent sur 12–24 mois.

- **Complétude schema.org** — déjà prévue dans `lib/jsonld/`
- **Contenu éditorial en format FAQ** — répondre directement « Where is the best Sunday brunch in Lisbon ? » par un paragraphe déclaratif ; les LLM les récupèrent en priorité
- **Fiche Wikidata** — renseigner P31 (nature de l'élément : boulangerie), P159 (siège : Lisbonne), P571 (fondation : 2022), P1448 (nom officiel : Lully 1661)
- **La presse comme corpus d'entraînement** — un papier dans Time Out Lisbon, Eater ou Condé Nast Traveler vaut plus pour le GEO que 100 backlinks de même autorité de domaine, parce que les LLM s'entraînent sur des corpus éditoriaux

> **Honest caveat / Mise en garde honnête.** GEO ROI is hard to measure today. We invest because the cost is low and the asymmetric upside is real, not because we can show a clean attribution chain. / Le ROI du GEO est difficile à mesurer aujourd'hui. Nous investissons parce que le coût est faible et le potentiel asymétrique réel, non parce qu'on peut produire une chaîne d'attribution propre.

---

## 5. Roadmap / Feuille de Route

**EN.** A 12-month plan organised in four phases, each with concrete deliverables and a single binary "are we on track" question. Dates assume kickoff in early June 2026; adjust if the website v1 launch slips.

**FR.** Un plan sur 12 mois en quatre phases, chacune avec des livrables concrets et une seule question binaire « sommes-nous dans les temps ». Les dates supposent un démarrage début juin 2026 ; à ajuster si le lancement v1 du site glisse.

### Phase 0 — Pre-launch foundation / Fondations pré-lancement (Weeks 1–4 / Semaines 1–4)

**Goal / Objectif :** Build everything that does not depend on the website. / Bâtir tout ce qui ne dépend pas du site.

| Deliverable / Livrable | Owner / Responsable | Done when / Terminé quand |
|---|---|---|
| 3× Google Business Profile fully optimised (photos, hours, menu, reservations link, Q&A seeds) | Marketing | All three listings show "100% complete" and accept reservations |
| Bilingual (PT/EN) in-store review cards designed + printed | Marketing + Design | Cards live at all 3 store counters |
| IG content cadence locked: Reels ≥ 50%, geotag + hashtag protocol | Social manager | 4 weeks of scheduled content in Buffer/Later |
| 5 Story Highlight covers designed in Baroque language | Design | Highlights live on IG profile |
| Newsletter capture live on IG bio + in-store posters | Marketing | First 50 subscribers from non-website sources |
| Baseline tracking: GBP insights baseline, IG insights export, current Google review count per store | Analytics | One-page baseline doc saved in `docs/marketing-baseline.md` |

**Phase 0 question / Question Phase 0 :** Is the foot-traffic acquisition engine running without the website? / Le moteur d'acquisition de trafic en boutique tourne-t-il sans le site ?

### Phase 1 — Website launch + organic foundation / Lancement du site + fondations organiques (Months 1–3 / Mois 1–3)

**Goal / Objectif :** Convert site launch into a measurable SEO + reviews flywheel. / Transformer le lancement du site en volant d'inertie SEO + avis.

| Deliverable / Livrable | Owner / Responsable | Done when / Terminé quand |
|---|---|---|
| Sitemap submitted to Google Search Console + Bing Webmaster | Dev + Marketing | First impressions visible in GSC |
| LocalBusiness/Restaurant + MenuItem JSON-LD live on all relevant pages | Dev | Rich Results test passes for at least Anjos store page + brunch page |
| Brunch landing page SEO-optimised for `brunch lisbon` / `sunday brunch lisbon` | Content + Dev | Page indexed; ranking ≤ 50 for primary term |
| 9× menu-item detail pages live with schema | Content + Dev | All pages indexed |
| 3× store detail pages live with schema + hreflang | Content + Dev | All 3 indexed in both PT and EN |
| Journal launched, 4 inaugural articles (2× craft, 2× Lisbon context) | Editorial | First articles live; first GSC impressions |
| TripAdvisor business listings claimed for all 3 stores | Marketing | Listings show "claimed" status |
| Influencer outreach round 1 — 3 Lisbon food KOCs invited | Marketing | First sponsored post live with proper FTC/PT disclosure |
| Packaging insert programme live on Uber Eats / Glovo orders | Operations + Marketing | First newsletter signups attributed to packaging QR |

**Phase 1 question / Question Phase 1 :** Are organic Google impressions trending upward and reviews accumulating? / Les impressions Google organiques croissent-elles et les avis s'accumulent-ils ?

### Phase 2 — Commerce + brand depth / E-commerce + profondeur de marque (Months 4–6 / Mois 4–6)

**Goal / Objectif :** Open the direct revenue path; deepen the brand story. / Ouvrir le canal de revenus direct ; approfondir le récit de marque.

| Deliverable / Livrable | Owner / Responsable | Done when / Terminé quand |
|---|---|---|
| Direct pickup ordering live (Phase 2 v1.1 cutover per `architecture.md` § 17) | Dev | First direct order placed without Uber/Glovo |
| Festive Orders online (Christmas + Easter + Santo António scoped) | Dev + Editorial | First festive order placed online |
| Uber Eats → direct migration campaign active (insert + discount code) | Marketing | Migration rate ≥ 10% measurable |
| Press round 1: pitches to Time Out Lisbon, Eater Lisbon, Observador, Le Monde Voyage | PR | At least one feature published |
| "The 1661 Series" launched in Journal (3 inaugural pieces) | Editorial | All 3 articles live; first Reddit / external citation appears |
| In-store Baroque plaque programme (Anjos pilot) | Operations + Design | Plaques installed at Anjos |
| Influencer round 2 — 2 micro-influencers + 1 Lisbon travel blogger | Marketing | 3 sponsored posts live |

**Phase 2 question / Question Phase 2 :** Is the direct revenue path covering its own marketing cost? / Le canal de revenus direct couvre-t-il son propre coût marketing ?

### Phase 3 — International + GEO + scale / International + GEO + échelle (Months 7–12 / Mois 7–12)

**Goal / Objectif :** Unlock the international segments; cement long-term GEO assets. / Débloquer les segments internationaux ; consolider les actifs GEO de long terme.

| Deliverable / Livrable | Owner / Responsable | Done when / Terminé quand |
|---|---|---|
| Xiaohongshu KOC programme (5 partnerships) | Marketing | 5 posts live with attribution tracking |
| TikTok channel independent of IG (Lisbon-context content layer) | Social | 12+ TikTok-native videos posted |
| Wikidata entry created and verified | Marketing | Lully 1661 entity live with required properties |
| GEO content audit — top 20 LLM queries tested + content gaps closed | Marketing + Content | Audit doc + 5 new FAQ-shaped articles published |
| B2B wholesale ("Lully Inside") landing page + enquiry form | Dev + Sales | First B2B enquiry received |
| Press round 2: Condé Nast Traveler, AFAR, The Infatuation pitches | PR | At least one international feature |
| Gift box online + worldwide-ship feasibility scoped (per The Folks benchmark) | Sales + Ops | Scoping doc + go/no-go decision |
| Annual SEO + reviews + GEO state-of-play report | Marketing | Year-1 review doc with KPI tree filled |

**Phase 3 question / Question Phase 3 :** Are international audiences (A4, A6) measurably part of the customer mix? / Les audiences internationales (A4, A6) font-elles mesurablement partie du mix client ?

---

## 6. KPI Framework / Cadre de Mesure

**EN.** KPIs organised by funnel stage. Do not chase all metrics simultaneously — each phase has one primary metric the phase question is testing.

**FR.** KPI organisés par étape d'entonnoir. Ne poursuivez pas tous les indicateurs à la fois — chaque phase a un indicateur principal que la question de phase teste.

| Funnel stage / Étape | Metric / Indicateur | 12-month target / Cible à 12 mois |
|---|---|---|
| **Awareness / Notoriété** | Google organic impressions (PT + EN) / Impressions organiques Google | 30k → 200k/month |
| **Awareness / Notoriété** | GBP "Discovery searches" (3 stores combined) | 5× growth / croissance ×5 |
| **Awareness / Notoriété** | IG reach + TikTok views | Baseline → +200% |
| **Consideration / Considération** | Site sessions (organic) | 0 → 25k/month |
| **Consideration / Considération** | Newsletter subscribers / Abonnés infolettre | 0 → 3,000 |
| **Consideration / Considération** | Google Reviews count + rating (3 stores combined) | Total ≥ 600, avg ≥ 4.7 |
| **Conversion** | Table reservations (Anjos) / Réservations (Anjos) | Baseline → +60% |
| **Conversion** | Uber/Glovo orders / Commandes Uber·Glovo | Baseline → +40% (acquisition mode) |
| **Conversion** | Direct online orders (Phase 2) / Commandes directes en ligne | 0 → 20% of total online order volume / 20 % du volume total en ligne |
| **Loyalty / Fidélité** | Email open rate / Taux d'ouverture infolettre | ≥ 35% (industry benchmark 25%) |
| **Loyalty / Fidélité** | Repeat purchase rate (direct only) / Taux de réachat (direct uniquement) | ≥ 30% within 60 days |

### 6.1 North Star Metrics / Étoiles Polaires

**EN.** Two metrics matter above all others:

1. **Anjos Sunday brunch table-fill rate** — validates the wedge strategy and the brand pull on the destination segment.
2. **Direct revenue % of total online revenue** (Phase 2 onwards) — validates that the marketing engine is building Lully's database, not Uber Eats'.

**FR.** Deux indicateurs comptent plus que tous les autres :

1. **Taux de remplissage des tables du brunch dominical à Anjos** — valide la stratégie de coin et l'attractivité de marque sur le segment destination.
2. **Part du chiffre d'affaires direct dans le total en ligne** (à partir de la Phase 2) — valide que le moteur marketing alimente la base de données de Lully, non celle d'Uber Eats.

---

## 7. Investment Shape / Forme d'Investissement

**EN.** A directional budget split for year 1, not a fixed allocation. Adjust quarterly based on phase questions.

**FR.** Une répartition budgétaire directionnelle pour l'année 1, non une allocation figée. À ajuster trimestriellement selon les questions de phase.

| Category / Catégorie | Year-1 share / Part année 1 | Notes |
|---|---|---|
| **Content production** (photo, video, Reels, journal writing) / **Production de contenu** | ~40% | Highest-ROI investment; everything else fails without good content. / Investissement à plus fort ROI ; tout le reste échoue sans bon contenu. |
| **Influencer / KOC partnerships** / **Partenariats influenceurs / KOC** | ~25% | Lisbon food + travel + Xiaohongshu KOC mix; €100–€500 per post bands. / Mix food + voyage Lisbonne + KOC Xiaohongshu ; tranches de €100–€500 par post. |
| **Tools + paid media testing** / **Outils + tests média payants** | ~20% | Ahrefs/Semrush (or one); Buffer/Later; Meta Ads + Google Ads for retargeting only in months 1–6. / Ahrefs/Semrush (l'un des deux) ; Buffer/Later ; Meta Ads + Google Ads en retargeting uniquement, mois 1–6. |
| **PR + media outreach** / **Relations presse** | ~15% | Critical for GEO via training-corpus inclusion. / Crucial pour le GEO via inclusion dans les corpus d'entraînement. |

> **What we deliberately do not invest in (year 1) / Ce dans quoi nous n'investissons délibérément pas (année 1) :**
> - Large-scale paid social ads — organic moat first / Publicités sociales à grande échelle — d'abord bâtir le fossé organique
> - SEO link-building agencies — quality editorial features > link farms / Agences de netlinking — préférer un papier éditorial de qualité à une ferme de liens
> - Self-operated Xiaohongshu account — KOC partnerships dominate this channel / Compte Xiaohongshu auto-géré — les partenariats KOC dominent ce canal

---

## 8. Decisions Needed from Client / Décisions Attendues du Client

**EN.** Five decisions unblock the Phase 0 sprint. Each one is binary or short-list.

**FR.** Cinq décisions débloquent le sprint de Phase 0. Chacune est binaire ou à choix court.

| # | Decision / Décision | Options |
|---|---------------------|---------|
| 1 | **Domain locked?** / **Domaine arrêté ?** | `lully1661.pt` / `lully1661.com` / other — needed for GBP linking and email setup |
| 2 | **Social ownership** / **Propriété des comptes sociaux** | In-house manager / agency / hybrid — affects content cadence feasibility |
| 3 | **Review programme go/no-go** / **Programme d'avis : feu vert ?** | Print cards + train staff (low cost, high ROI) — needs operational sign-off |
| 4 | **Phase-2 commerce timeline** / **Calendrier Phase 2 e-commerce** | Confirm month for direct pickup launch — drives migration funnel design |
| 5 | **PR budget commitment** / **Engagement budget RP** | Year-1 budget envelope for press outreach (€3k / €8k / €15k tiers) — drives GEO realism |

---

## 9. What This Strategy Does Not Cover / Ce Que Cette Stratégie ne Couvre Pas

**EN.** Honest scope boundaries:

- **Paid media playbooks** (Meta Ads, Google Ads creative + audience structures) — deferred until Tier 1 organic baseline exists
- **Loyalty programme mechanics** — relevant in year 2 once direct CRM has scale
- **Catering & events marketing** — adjacent but separate funnel; treat as Phase 3+
- **Internal team org / hiring** — strategy assumes 1 in-house marketer + agency or freelance support; org design is a separate doc
- **Crisis communications playbook** — needed but out of scope for this document

**FR.** Limites de périmètre honnêtes :

- **Playbooks de média payant** (Meta Ads, Google Ads — créatif + structures d'audience) — reportés tant que la base organique Tier 1 n'existe pas
- **Mécanique d'un programme de fidélité** — pertinent en année 2 quand le CRM direct aura de l'échelle
- **Marketing traiteur & événements** — entonnoir adjacent mais distinct ; à traiter en Phase 3+
- **Organisation interne / recrutement** — la stratégie suppose un·e responsable marketing interne + soutien agence ou freelance ; le design d'équipe est un document séparé
- **Plan de communication de crise** — nécessaire mais hors périmètre de ce document

---

## 10. Appendix — Glossary / Annexe — Glossaire

| Term / Terme | Definition / Définition |
|---|---|
| **GBP (Google Business Profile)** | Free Google listing for physical businesses; controls Maps + Knowledge Panel presence. / Fiche Google gratuite pour entreprises physiques ; contrôle la présence sur Maps + Knowledge Panel. |
| **GEO (Generative Engine Optimization)** | The discipline of making a brand likely to be recommended by AI chatbots (ChatGPT, Perplexity, Gemini, Claude). FR variants: optimisation pour moteurs génératifs / référencement génératif. |
| **JSON-LD / schema.org** | Structured-data format embedded in web pages so search engines + LLMs understand entities (business, menu items, opening hours). / Format de données structurées intégré aux pages web pour que moteurs et LLM comprennent les entités (entreprise, plats, horaires). |
| **hreflang** | HTML attribute signalling to search engines that two pages are the same content in different languages. / Attribut HTML signalant aux moteurs que deux pages sont un même contenu en différentes langues. |
| **KOC (Key Opinion Consumer)** | Small/medium influencer treated as a peer recommender rather than celebrity endorser; the dominant unit on Xiaohongshu. / Influenceur de petite/moyenne taille perçu comme un pair, non comme une célébrité ; unité dominante sur Xiaohongshu. |
| **Wedge strategy** / **Stratégie de coin** | Win a narrow micro-segment first (here: Anjos Sunday brunch), then expand outward from that defended position. / Gagner d'abord un micro-segment étroit (ici : brunch dominical à Anjos), puis s'étendre depuis cette position défendue. |
| **Xiaohongshu (RED / 小红书)** | Chinese visual social platform dominant for travel + lifestyle discovery; sometimes branded "RED" internationally. / Plateforme sociale visuelle chinoise dominante pour la découverte voyage + lifestyle ; parfois nommée « RED » à l'international. |

---

*End of document / Fin du document — v0.1 · 2026-05-22*
