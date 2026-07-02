# Phase 1 — Research: URL in, brand + products + market intel out

Read this when starting a new campaign (or re-running research on an existing one). Phase 1
turns a single website URL into the campaign's foundation files: `brand.json`, `products.json`
(working set, max 50), `research.md` (market research), and `brief.md` (the synthesized
campaign brief). Everything downstream — audiences, personas, ad concepts, media prompts —
reads these files, so errors here compound. POPJAM's research quality comes from four
separated concerns, and this phase mirrors all of them: (1) deterministic CSS branding beats
LLM guessing for colors/logo/typography; (2) exclusion-list-heavy extraction keeps junk images
out; (3) asset URLs are validated by actually fetching them before storage; (4) research is
scoped BEFORE it runs and consumed AFTER — never generated blind. File shapes: see
[data-models.md](data-models.md).

## 1. Elicit, then infer

Ask the user up front — one message, all questions together:

- **Website URL** (required; the only truly mandatory input).
- **Campaign goal** — awareness, conversions, launch, seasonal push, lead gen.
- **Market & language** — where do the ads run, in what language? Note it as an IETF BCP 47
  code (e.g. `en`, `tr`, `de`). If pinned by the user, keep it pinned for the whole campaign.
- **Platforms** — which of TIKTOK / INSTAGRAM / FACEBOOK / LINKEDIN / TWITTER / YOUTUBE / GOOGLE / REDDIT matter (exact `Platform` enum values — the scorer's weight tables key on them).
- **Budget sensitivity** — cost-conscious (images only, fewer concepts) vs go-big (video,
  wider fan-out). This gates the media phase, so ask now.

Infer silently, never ask: brand name, tone, typography, colors, product set, competitor
landscape, and — when the user leaves language blank — the best-fit language for the brand's
market (a `.com.tr` site with Turkish copy targets `tr`; don't make the user say so). An empty
brief is fine: infer sensible direction from the brand and website, as POPJAM's scout does.

Then create the campaign directory (default `growth/<brand-slug>/` under the CWD, or wherever
the user asks) and open `log.md` with the elicited answers and inferred defaults — the first
entry of the append-only decision journal.

## 2. Extract the brand → brand.json

Fetch the URL with WebFetch. You want two distinct things from the page and you should treat
them differently:

- **Content facts** (name, tone, language, products) — LLM extraction over the page text.
- **Visual identity** (logo, colors, typography) — read from the page's *actual styling*,
  because CSS is ground truth and LLM guesses drift toward generic palettes.

### CSS branding beats LLM guessing

Fetch the raw HTML too (`curl -sL <url>` into the scratchpad works) and look at what the page
really uses: `<link rel="icon">`/header `<img>` logos, CSS custom properties and inline
styles for brand colors, `font-family` declarations, `color-scheme`/dark-mode hints. Apply
POPJAM's merge rules — observed styling wins over anything you inferred from reading copy:

- **Logos**: prefer an explicit header/nav logo image; record each as `{url, theme}` where
  theme is `"light"`, `"dark"`, or `"any"` (from the page's color scheme). Favicon only as a
  last-resort fallback. The OG/social-preview image is **never** a logo — it's a preview card.
- **Colors**: keep the hex values that carry brand identity — primary, secondary, accent.
  Drop semantic/UI colors (background, text-primary, text-secondary, link, success, warning,
  error); those describe the page, not the brand.
- **Typography**: prefer the heading font family, then the primary/body font, then the first
  font you can find. One concise descriptor string, usable directly in HTML.

If the Higgsfield MCP is connected, its `show_marketing_studio` tool can fetch a **brand kit**
from a URL server-side (logo, colors, fonts, tone) — use it as an accelerator, then
cross-check the result against the CSS you observed; it is a convenience, not the authority.

### Content extraction

Adapted from POPJAM's website-extraction agent — apply this to the fetched page:

```
Extract the brand name, messaging tone, and target language/locale, plus ALL distinct
products/services featured on this page (each with name, description, specs, and image
URLs). If the page features only one product, return a single-item list. For product image
URLs, include only images that show the actual product/service offering. Exclude brand
logos, favicons, app icons, Open Graph/social preview images, hero banners, partner/customer
logos, payment badges, trust badges, decorative icons, and tracking pixels. Use full
absolute URLs for all images — never relative paths. You do NOT need to extract colors,
fonts, or logo — those are handled separately.
```

Two rules from POPJAM's extract agent still apply: make sure the brand is of the
product/service being sold, not the ecommerce platform or the website merely hosting it; and
fill the brand URL with the brand's main landing page, the product URL with the specific
product's sales page.

The image exclusion list above is what keeps junk out of media generation later — a hero
banner stored as a "product image" becomes a reference image that poisons every creative.
Absolute URLs are non-negotiable: every stored image/logo URL must resolve on its own.
Validate by fetching each candidate (a HEAD request or small GET); drop URLs that don't load.
For logos specifically, look at the image before keeping it (adapted from POPJAM's logo_check
agent): keep it only if it is a clear brand logo, wordmark, lettermark, or brand icon — on any
background. Reject placeholders, generic stock or product photos, lifestyle/hero images,
OG/social previews, screenshots, advertisements, and payment/trust badges. When genuinely
uncertain, prefer keeping it — the image already loads, so a borderline-but-plausible logo is
worth more than none.

### Sparse-page fallbacks — research never dead-ends

Some pages give you almost nothing (JS-only shells, link-in-bio pages, holding pages). Never
stall or ask the user to fix their website; fall back exactly as POPJAM does and note the
fallback in `log.md`:

- **name** ← hostname: strip `www.`, take the first label, capitalize (`shop.acme-tools.io`
  → "Acme-tools").
- **language** ← the user's pinned language, else `en`.
- **tone** ← `professional`.  **typography** ← `sans-serif`.
- **products** ← if none extracted, one stub product named after the brand, with the site URL
  and an honest one-line description. The pipeline can run on a stub; it cannot run on nothing.

Write `brand.json` (shape in [data-models.md](data-models.md)) and show the user a compact
summary — name, logo(s), palette swatches, tone, language — before moving on. This is the
cheapest moment to correct a wrong brand read.

## 3. Product discovery → products.json

If the URL is a single product/service page, the extraction above already produced the
product list — write `products.json` and skip to §4. If it's a **catalog/listing site**
(category pages, an e-commerce grid, "shop all"), walk the catalog:

1. **Collect links, not prose.** Fetch the listing page and pull out its link list (all
   `[text](url)` hrefs and raw URLs). You select product pages from links the page actually
   contains — never from imagination.
2. **Select product-detail links.** Adapted from POPJAM's catalog-listing agent:

   ```
   You are given the URL of an e-commerce category/listing page and the list of links found
   on that page. Return ONLY the links that are individual product detail pages belonging to
   THIS listing's category. Choose only from the links provided — never invent, complete,
   guess, or modify a URL. Exclude navigation, header/footer, search, cart, account,
   blog/article, category/collection landing pages, pagination, filters/sorts, and links to
   OTHER categories or 'recommended' / 'related' / 'you may also like' / 'sponsored' /
   cross-sell / recently-viewed / wishlist products. If none of the links are product detail
   pages, return an empty list.
   ```

3. **Ground every selection deterministically.** POPJAM hard-fails ungrounded URLs and so
   must you: keep a URL only if it (a) appears among the page's actual links, OR (b) matches
   a high-confidence product-URL pattern — a path segment in
   `{product, products, item, items, p, pd, dp}` followed by a slug (regex
   `/(?:products?|items?|pd|dp)/[^/]{2,}$`), or an "identity query" detail page whose query
   keys include one of `{catid, code, descr, handle, id, item, item_id, pid, product,
   product_id, productid, sku, slug}` AND whose path matches
   `(?:product|item|urun|ürün|detail|details)`. Reject off-site links, the listing itself,
   media-file extensions, and nav segments (`account(s)`, `about`, `article(s)`, `blog(s)`,
   `cart`, `catalog`, `categories`, `category`, `checkout`, `collections`, `collection`,
   `contact`, `faq`, `help`, `login`, `lookbook`, `news`, `page(s)`, `policies`, `privacy`,
   `register`, `search`, `support`, `terms`, `wishlist`). Strip tracking params
   (`utm_*`, `fbclid`, `gclid`, `mc_cid`, `mc_eid`, `ref`, `spm`, `variant`). This is what
   prevents hallucinated products from entering the campaign.
4. **Paginate** by walking `?page=N` (then rendered `/page/N`-style links) until the first
   empty page, capped at 30 pages. If every fetch is blocked (bot walls, 403s), tell the user
   loudly — a silent zero-product catalog is worse than a failure.
5. **Extract each product page.** Adapted from POPJAM's catalog-product agent, run over each
   product page's markdown (cap ~100k chars):

   ```
   You extract a single product (or service) from a product detail page that has been
   rendered to markdown. Extract the product name, a concise description, its key
   specs/features, and its image URLs. For images, include only images of the actual
   product/service offering. Exclude logos, favicons, social/Open Graph preview images, hero
   banners, partner/customer logos, payment/trust badges, and decorative icons. Use full
   absolute image URLs (never relative paths). If the page is not a product detail page,
   return an empty name.
   ```

   Skip results with an empty name. Dedup by URL, then by near-identical name+description.

For catalogs beyond ~20 product pages, orchestrate the fetch+extract fan-out with the
Workflow tool (script templates in the skill's `workflows/` dir); for small runs, plain
sequential fetches are simpler and fine.

### The working set: max 50, pinned first

`products.json` is a **working set**, not a full catalog dump — downstream prompts degrade
when flooded, so cap it at 50 products. If the user named specific products ("pin"), those go
first, always kept; fill remaining slots with the most representative items (bestsellers,
category coverage, items with good images). Record how many products you discovered vs kept
in `log.md` so the user can re-scope later.

## 4. Market research → research.md

Research runs on **brand + catalog positioning only, never the full product list** — a
5,000-SKU dump adds nothing to market research that the brand and catalog description don't.

**Scope before you search.** Play POPJAM's campaign scout: from the brand, products, website
content, and the user's brief, write a `## Research focus` section at the top of
`research.md` BEFORE running any query — the single, sharp instruction the research should
answer, tailored to the goal: the market, the most promising audiences, the competitive
landscape (favour local competitors; ask for a comparison table of at least 10), and the ad
angles/hooks that convert for THIS goal. Turn a vague brief into a focused research agenda;
if the brief is empty, infer sensible direction from the brand and website.

**Then run it.** Prefer the perplexity MCP tools when connected — `perplexity_search` for the
default pass, `perplexity_research` when the user wants depth (mirrors POPJAM's
sonar-pro/sonar-deep-research split) — or the deep-research skill for a full fan-out report.
Otherwise WebSearch + WebFetch across several targeted queries works. Whichever engine, hold
the research to POPJAM's rules — adapted from its research agent:

```
- Only return the search results, no chatting.
- Return everything in markdown format, ready to be displayed beautifully.
- If inputs are provided, use it as context to do the research for.
- Aim for 100% accuracy without any hallucinations, only include trustworthy sources.
- Spend as much time as needed to gather all the information to be comprehensive.
```

Default research instruction (adapted from POPJAM's campaign flow): *research the brand, its
products, the market, the most promising target audiences, and the competitive landscape.
Include a competitor comparison table (at least 10 competitors, favouring local ones) and the
ad angles and hooks that convert in this industry.* Base all research on the given website
URL for the given brand name — and if the same brand/product name is in use for a different
kind of product elsewhere, disregard that other entity entirely (name collisions are the top
research-contamination failure).

`research.md` must end up containing, at minimum: the research focus, a market overview, a
**competitor table with ≥10 rows favouring local competitors** (name, positioning, price
tier, primary channels, standout creative angle), and a **converting ad angles & hooks**
section — concrete hook patterns observed in the industry, because the strategy phase mines
this section directly. Cite sources inline; unverifiable claims get dropped, not hedged.

## 5. Synthesize the brief → brief.md

Now play POPJAM's campaign brain: read `brand.json`, `products.json`, the website content,
and `research.md`, and write `brief.md` grounded in those findings — direction only, no
counts, budgets, metrics, timelines, or media-buying plans. Four sections, whose intent is
verbatim from POPJAM's CampaignPlan:

- **Campaign brief** — "A concise, creative-focused campaign brief (angles, hooks,
  positioning) for this brand and its audiences, grounded in the research findings. Strictly
  about ad creatives and target segments — NO budgets, metrics, timelines, or media-buying
  plans."
- **Audience guidance** — "How to choose/skew the audience segments, given the research."
- **Persona guidance** — "What the buyer personas should emphasise, given the brief and
  audiences."
- **Ad direction** — "The creative direction every ad should follow — tone, angle, hooks
  (favour those the research shows convert), do/don'ts."

Also record the campaign's pinned language in `brief.md` (all generated ad copy uses it
exclusively; `media_description` stays English regardless — see
[data-models.md](data-models.md)) and a short campaign title, POPJAM-style: `"Brand - X"`
where X is the single most salient dimension of this run (product, audience, goal, occasion,
market, or season), under ~40 characters.

## Exit checklist

Before moving to audience synthesis, confirm: `brand.json` has a validated logo, observed (not
guessed) colors and typography, tone, and language; `products.json` has ≤50 grounded products
with absolute, fetchable image URLs, pinned items first; `research.md` has the focus, a ≥10
competitor table, and an angles/hooks section; `brief.md` has all four sections; `log.md`
records every fallback and scoping decision. Show the user the brief and pause for a quick
confirm — it's the last cheap correction point before generation spends real effort.
