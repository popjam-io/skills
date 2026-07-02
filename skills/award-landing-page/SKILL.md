---
name: award-landing-page
description: Design and build pages that sell — landing pages, homepages, pricing pages, waitlist and pre-launch pages, signup/registration pages, webinar/event pages, product-launch pages, and marketing-site heroes or sections. Use this whenever the user wants to create, redesign, or rework any page whose job is to persuade visitors to act, and equally when the ask is outcome-framed with no page type named ("get more signups", "our page doesn't convert", "make it feel premium", "we're launching Thursday"). It owns the full deliverable — business and funnel research, award-level art direction, conversion copywriting, distinctive design and motion, technical SEO, and CTA/funnel wiring — so prefer it over frontend-design or any generic UI skill when the page's purpose is to market, sell, or convert. Skip for internal tools and dashboards, docs sites, blog/SEO articles, standalone audits, analytics or A/B-test instrumentation, and consent banners on an otherwise untouched site.
---

# Award-Winning Landing Pages

A landing page has exactly one job: move a specific visitor toward a specific action. "Award-winning" is not decoration on top of that job — the pages that win Awwwards/FWA and the pages that convert best share the same properties: a distinctive point of view, a narrative that unfolds as you scroll, motion that explains rather than decorates, copy that sounds like a person who knows the customer, and flawless execution (fast, accessible, semantic).

Work through the phases below **in order**. The most common failure mode is jumping straight to code: you get a generic template with placeholder energy, because design and copy decisions were made implicitly instead of deliberately. Each phase produces a short written artifact that constrains the next one — that's what keeps the result intentional.

The second most common failure mode is the **generic AI aesthetic**: dark background, purple-to-blue gradient, glassmorphism cards in a 3-column grid, emoji section icons, "Supercharge your workflow" headlines. If you notice the page drifting there, stop and return to your research memo.

## Phase 0 — Understand the business and its funnels (never skip)

You cannot write a persuasive page for a product you haven't understood, and a beautiful page that dead-ends is worthless. Before anything visual:

1. **Inventory the business.** What is sold, to whom, at what price, against which alternatives? If you're inside a codebase or the user gave a URL, read it: existing pages, pricing config, docs, README. If information is missing, ask the user or research the market — do not invent facts, testimonials, or metrics.
2. **Map the real funnels.** Find every conversion path that actually exists: signup/trial route, checkout/preorder, demo booking, newsletter/lead capture, contact. In a codebase, find the real routes/endpoints; the page must link to them exactly. A CTA pointing at a made-up URL is a broken funnel.
3. **Choose ONE primary conversion action** and write it down (e.g. "start free trial at /signup"). Everything on the page argues for this action. Pick one **secondary action** for visitors who aren't ready (newsletter, docs, lead magnet) — this catches the 95% who won't convert today. Match CTA to visitor temperature: cold traffic gets low-commitment asks, hot traffic gets the direct ask.
4. **Collect real assets.** Logos, product screenshots, real data, real customer quotes. A real screenshot in a tasteful device frame beats a fabricated mockup every time — visitors can smell fake. If no assets exist, build honest abstract/illustrative visuals rather than faking product UI.

Write a 5–10 line brief: audience, promise, primary/secondary action with exact URLs, available assets, tone. This brief is the contract for every later phase.

## Phase 1 — Research award-winning work (the prep step)

Never design from memory. Spend real effort here — 15–30 minutes of research repays itself in every section of the page.

1. Search for recent award-winning and best-in-class sites in the same industry and adjacent ones: Awwwards (Site of the Day), FWA, CSS Design Awards, Godly, Land-book, Lapa Ninja, siteinspire, plus "best <industry> landing pages <current year>" teardowns. Fetch and actually study 3–5.
2. For each, extract **concrete, reusable moves** — not vibes: hero structure (headline/visual relationship), type system (faces, scale, weight contrast), color strategy, scroll narrative (what each viewport-chapter does), signature motion (the one animation you remember), how they present the product, how they handle social proof.
3. Write a **design-direction memo**: 2–3 candidate directions, each named, with the reference sites and the specific moves you'd borrow. Then commit to one and note why it fits this brand and audience.

Synthesize, don't copy: borrow structural ideas and motion grammar, never verbatim visuals or copy. The goal is a page with an *ownable* point of view — something a reader could describe in one sentence ("the one with the giant serif numerals and the ink-bleed transitions").

See [references/research.md](references/research.md) for the source list, extraction checklist, and memo template.

## Phase 2 — Copy before pixels

Write the entire copy document before any HTML. Copy is the argument; design is its typography. When copy is written to fill boxes in an existing layout, it reads like filler.

Structure the page as answers to the visitor's questions, in the order they ask them:

1. **What is this and is it for me?** (hero: one-line value prop + qualifier)
2. **What would my life look like with it?** (outcome, shown not told)
3. **How does it actually work?** (product proof: 3–4 concrete capabilities)
4. **Can I trust it works?** (social proof: specific, attributed, quantified)
5. **What's the catch?** (objections: price, effort, switching, risk — answer them right where they arise, and again near the final CTA)
6. **What do I do now?** (final CTA with risk reversal)

Rules that matter (each exists because its violation is the #1 amateur tell):

- **Specificity beats adjectives.** "Turns 400 support tickets into a ranked roadmap in 4 minutes" outsells "Powerful AI-driven insights". Numbers, timeframes, and named outcomes only.
- **CTA copy states value, not effort.** "Start free — no card required", not "Submit" or "Sign up".
- **One idea per section.** If a section argues two things, split or cut it.
- **Write skimmable.** Most visitors read only headlines and bolds; the page must persuade on headlines alone. Read just your headlines top to bottom — do they form a complete argument?
- **Sound like a person.** Read the copy aloud; delete anything you'd never say to a customer's face ("leverage", "seamless", "revolutionize").
- **Trust must survive zero customers.** Never fabricate logos, named testimonials, or precision stats — it's a legal and credibility blocker the moment a real visitor checks. But don't leave a trust vacuum either (a page with *no* proof loses to a page with fake proof): build honest substitutes — founder/team credibility, methodology transparency ("here's the exact formula"), verifiable domain facts, security posture, guarantees and risk reversal, an honest "built for / not for (yet)" panel — and label demo content "sample data".
- **Close with a segmented funnel, not repeated buttons.** End with side-by-side primary/secondary path cards, each answering its own audience's objections (self-serve: no card, cancel by doing nothing; enterprise: SSO, DPA, data residency, migration path). Where cost is the audience's main anxiety, anchor the price — from-prices, payback math, or a statutory fee basis. Price silence suppresses conversion; an unjustified price is a statement, not an argument.

See [references/copywriting.md](references/copywriting.md) for headline formulas, section patterns, and worked good/bad examples.

## Phase 3 — Design and build

Now, and only now, build. Start from a mini design system, not from the hero:

- **Type first.** Landing page quality is 70% typography. Pick a distinctive display face plus a workhorse body face (variable fonts preferred), define a scale with real contrast (hero display should be 3–5× body size), and set tight leading on display sizes. System-font-plus-one-weight is how templates look.
- **An ownable palette.** One dominant color with conviction beats five timid ones. Check the direction memo — the palette should be recognizably *this brand's*.
- **Spacing rhythm.** Consistent spacing scale; generous whitespace around the moments that matter. Award sites are confident enough to let one element own a viewport.

**Build the page as a narrative journey.** Each scroll "chapter" advances the argument from Phase 2. The visitor should *experience* the product, not read about it — this is what "interactive user journey" means in practice:

- Put the product's core verb **in the hero as a self-running demonstration** — value visible within ~3 seconds, no click required. Most visitors never click; a demo gated behind a button below the fold gets missed by the majority.
- Build one **signature interaction** that enacts the brand's central metaphor (the fold, the pull, the translation) instead of spreading effort across generic feature grids — then bridge it straight to conversion ("In the product, this runs on your data → Start free").
- Sticky/scroll-driven sequences work when explaining a process: pin the visual, swap the steps.
- Every interactive element degrades gracefully: keyboard accessible, `aria-live` narration for state changes, hit targets on the real control (not invisible overlays), and a sensible no-JS state.

**Animation has a job or it goes.** The three legitimate jobs: guide attention (draw the eye to the CTA, not away), explain (show the transformation the product performs), reward (micro-interactions that make the page feel alive). And the demo must do what the adjacent copy says: if the headline says "it fills as your shot pulls", the visual fills in sync — a decorative loop sitting next to a claim reads as fake proof and actively erodes trust. Implementation rules:

- Hero gets the motion budget; below the fold, restrained scroll-triggered reveals (staggered, 300–600ms, ease-out, translate ≤ 24px). If everything animates, nothing does.
- Animate only `transform` and `opacity` (compositor-friendly); never `top/left/width`.
- Honor `prefers-reduced-motion` — wrap animation activation in the media query, with the no-motion experience fully legible (content must not be stuck at opacity 0).
- Micro-interactions on every interactive element: hover/focus states on CTAs, subtle magnetic or scale effects — 100–200ms, felt not seen.
- Vanilla IntersectionObserver + CSS covers 90% of needs on a static page; reach for GSAP/Lenis only for scroll-scrubbed narratives.

**Creative assets:** produce real ones — edited screenshots with consistent framing, SVG illustrations in the page's visual language, or generated imagery that matches the direction memo. Never ship stock-photo-smiling-team, watermarked placeholders, or gray boxes. Budget hero art to the audience's taste bar: if the pitch is "a beautiful object", the hero render *is* the page's centerpiece and a crude illustration undersells the product more than plain text would — invest there first, or choose a type-led direction instead.

**Page chrome and rhythm:**

- **Navigation parity on mobile.** If desktop nav exposes section links, small screens get a hamburger/disclosure — never silently drop them, leaving only a logo and CTA. Include a skip link.
- **Vary the canvas.** Alternate section backgrounds or plan deliberate palette breaks to pace the scroll; one unbroken background until the finale reads as monotony. Hunt for near-empty viewport-height bands — whitespace should feel composed, not like drift.
- **Respect the delivery constraint.** If the deliverable is "self-contained", use system font stacks or embedded fonts — a Google Fonts `<link>` is an external, render-blocking dependency that breaks the contract.

## Phase 4 — SEO and performance (built in, not bolted on)

Do this as part of the build, because retrofitting semantics is harder than writing them:

- Semantic structure: exactly one `<h1>` (the hero headline), heading levels in order, landmarks (`<header> <main> <section> <footer>`), `<nav>` where present.
- `<title>` (≤ 60 chars, keyword + promise), meta description (50–160 chars, written as ad copy — it's your SERP CTA), canonical URL, Open Graph + Twitter Card tags (og:title, og:description, og:image), viewport meta.
- JSON-LD structured data matched to the page (`Organization`/`Product`/`SoftwareApplication`/`LocalBusiness` + `FAQPage` if there's a FAQ). Validate that it parses.
- Every `<img>` has descriptive `alt`, explicit `width`/`height` (prevents CLS), `loading="lazy"` below the fold — never on the LCP image.
- Fonts: `preconnect` + `font-display: swap`; preload only the display face used in the hero.
- Budgets: LCP < 2.5s, CLS < 0.1, no blocking scripts in `<head>` (defer/module), hero image optimized.
- If targeting a search query (e.g. local service), the query's language must appear naturally in title, h1, and early body copy — write for the reader first, but don't make Google guess.

Full checklist with JSON-LD examples: [references/seo-checklist.md](references/seo-checklist.md).

## Phase 5 — Verify like a critic

Claiming done without looking at the page is how broken heroes ship.

1. **Open it.** Use the preview/browser tooling available; otherwise at minimum validate the HTML parses and scripts have no syntax errors. Screenshot at mobile (375px) and desktop (1280px+).
2. **Walk every link, not just the CTAs.** Each CTA must resolve to the exact URLs from the Phase 0 brief; forms must point at the real endpoint with the right method. Footer and nav links resolve to real anchors/pages or are explicitly flagged as pre-launch placeholders — a plausible-looking sitemap of dead `#` links reads as fake the moment anyone clicks one.
3. **Test the states:** reduced motion (content visible?), keyboard navigation (focus visible, interactive elements reachable), dark mode if the site supports it, and the no-JS/print/bot view — scroll-reveal styling must never leave the page a blank field of `opacity: 0` content for crawlers, readers, or printing.
4. **Check the choreography at several scroll offsets and viewport heights**, not one smooth pass: hunt for dead viewport-height whitespace bands, half-revealed dimmed sections, and sticky-header overlap or backdrop artifacts.
5. **Run the Phase 4 checklist** mechanically — headings, meta lengths, JSON-LD validity, alts, one h1.
6. **The adversarial pass.** Look at the page cold and ask: *would a design-literate stranger screenshot this, or does it look like a template?* Find the weakest section and rebuild it. There is always one. Then read the sections in order — each must add a **new** argument (problem → mechanism → proof → objections → close); cut any section that restates the tagline in fresh typography. Finally, read only the headlines top-to-bottom — is the argument complete?

## Definition of done

- [ ] Phase 0 brief exists; every CTA matches its URLs exactly; every other link resolves or is flagged as a placeholder
- [ ] Direction memo exists; the page has a describable, ownable point of view with deliberate visual rhythm (no unbroken monotone canvas, no dead whitespace bands)
- [ ] Headlines alone form a complete persuasive argument; each section adds a new argument; zero filler phrases, zero fabricated proof — and an honest trust section that works at zero customers
- [ ] The hero demonstrates the product without a click; one signature interaction enacts the brand metaphor and bridges to a CTA; animation passes the "does what the copy says" test; `prefers-reduced-motion` honored
- [ ] One h1, ordered headings, title/description/OG/JSON-LD present and valid, all images have alt + dimensions
- [ ] Page verified in a browser at mobile and desktop widths with nav parity on small screens; every funnel walked
