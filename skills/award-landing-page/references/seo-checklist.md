# SEO & Performance Checklist

Run this mechanically in Phase 5. Every unchecked item is a real ranking or conversion leak.

## Document head

- [ ] `<title>` — ≤ 60 chars, primary query/promise first, brand last ("Tax Advisory for Berlin Freelancers | Northwind")
- [ ] `<meta name="description">` — 50–160 chars, written as ad copy with the value prop and an implicit CTA; this is your SERP conversion copy
- [ ] `<meta name="viewport" content="width=device-width, initial-scale=1">`
- [ ] `<link rel="canonical">` pointing at the final URL
- [ ] Open Graph: `og:title`, `og:description`, `og:image` (1200×630), `og:url`, `og:type`
- [ ] Twitter: `twitter:card` (`summary_large_image`), `twitter:title`, `twitter:description`, `twitter:image`
- [ ] Favicon + `theme-color`
- [ ] Fonts: `<link rel="preconnect">` to font host; `font-display: swap`; preload only the hero display face — but if the deliverable is self-contained, use system stacks or embedded fonts instead of any external font host
- [ ] `og:image:alt` alongside `og:image`

## Local & international pages (when the market or language is split)

- [ ] `hreflang` alternates for each language version plus `x-default`
- [ ] On-page NAP (name, address, phone, hours) in the footer, matching the JSON-LD business entity **exactly** — consistency is the local ranking signal
- [ ] Geo meta (`geo.region`, `geo.position`) and `areaServed` in the JSON-LD
- [ ] `sameAs` links to real profiles (Google Business, LinkedIn) — omit rather than invent
- [ ] The target query's language appears in title, h1, and first paragraph naturally
- [ ] Legal pages the market expects (e.g. Impressum/Datenschutz in Germany) linked for real or explicitly flagged as pre-launch placeholders; a GDPR consent line near any email form

## Semantic structure

- [ ] Exactly one `<h1>` — the hero headline, containing the primary query language naturally
- [ ] Heading levels strictly descend (no h2 → h4 jumps); headings describe content, not decoration
- [ ] Landmarks: `<header>`, `<main>`, `<section>`/`<article>`, `<footer>`; `<nav>` for any nav
- [ ] Buttons are `<button>`/`<a href>` (real links for navigation — crawlable and middle-clickable)
- [ ] Forms: `<label>` for every input, `type`/`autocomplete` attributes, real `action`/endpoint

## Structured data (JSON-LD)

Include the types that genuinely match the page; validate the JSON parses. Common picks:

- SaaS: `SoftwareApplication` (name, description, offers) + `Organization`
- Physical product: `Product` (name, image, offers with price/priceCurrency/availability)
- Service business: `LocalBusiness`/`ProfessionalService` (name, address, geo, areaServed) — critical for local queries
- Any page with FAQ section: `FAQPage` (mirror the on-page Q&A exactly)

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "SoftwareApplication",
  "name": "Refold",
  "applicationCategory": "BusinessApplication",
  "description": "Turns customer feedback into a prioritized product roadmap.",
  "offers": { "@type": "Offer", "price": "0", "priceCurrency": "USD", "description": "14-day free trial" }
}
</script>
```

## Media

- [ ] Every `<img>`: descriptive `alt` (empty `alt=""` only for pure decoration), explicit `width` + `height` (prevents CLS)
- [ ] `loading="lazy"` on below-fold images; **never** on the LCP/hero image (use `fetchpriority="high"` there)
- [ ] Modern formats (WebP/AVIF) with sensible dimensions; `srcset` where layout width varies meaningfully
- [ ] Video: `preload="metadata"`, `poster`, muted+`playsinline` for autoplay heroes

## Performance budgets

- [ ] LCP < 2.5s: hero image/type renders without waiting on JS
- [ ] CLS < 0.1: dimensions on all media, no layout-shifting font swaps on display text, reserve space for late content
- [ ] No render-blocking scripts: `defer`/`type="module"`; inline critical CSS if the page is a single file
- [ ] Animation only via `transform`/`opacity`; scroll handlers passive or IntersectionObserver-based

## Accessibility spot-checks (rankings and conversions both)

- [ ] Text contrast ≥ 4.5:1 (3:1 for large display text)
- [ ] Visible `:focus-visible` styles on all interactive elements
- [ ] `prefers-reduced-motion: reduce` disables non-essential animation and leaves all content visible (nothing stranded at `opacity: 0`)
- [ ] Interactive widgets keyboard-operable
