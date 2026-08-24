# CLAUDE.md — newSite/ template system

This folder is the **content + asset template** for the Aigenetic site, extracted
from the live `index.html` / `healthcare.html` / `config.js` on 2026-08-24 with
zero content loss. It is a design-time source of truth, not a deployed part of
the site — GitHub Pages serves the repo root, nothing under `newSite/`.

Read this file before making any change that originates from, or should feed
back into, this template system. It supplements — never replaces — the root
`/CLAUDE.md`, whose rules (site name casing, logo consistency, main/child
look-and-feel sync) apply here too, generalized from "index.html ↔
healthcare.html" to "any main page ↔ any page built from this template".

## What's in here

- **`template.json`** — all copy (headings, subheadings, pricing, testimonials,
  nav labels, footer text, everything) plus a `theme` block (two named design
  token sets: `default` for the main React page, `clinicalTeal` for vanilla
  child pages) and an `assets` manifest mapping usage → file path.
- **`assets/common/`** — logos, favicon, and the full shared audio-demo set:
  identical across every page, used as-is, never edited per-page.
- **`assets/pages/<pageKey>/`** — files unique to, or deliberately duplicated
  for, one page (e.g. `assets/pages/healthcare/audio/onboarding-sample.mp3`,
  a copy of the common healthcare clip that only `healthcare.html`'s own voice
  player uses).
- **`assets/pages/_template/`** — an empty pattern stub; duplicate it to start
  a new vertical's asset folder.
- **`templates/vertical-page.template.html`** — an annotated HTML skeleton with
  `{{token}}` placeholders matching `pages.healthcare`'s schema in
  `template.json`. It is a manual copy/replace skeleton, not a build-time
  templating engine (the project has no build step — see root CLAUDE.md).

## Asset rules

- `assets/common/<type>/<usage-name>.<ext>` — anything reused identically on
  every page (logos, favicon, the 6-clip shared audio showcase set).
- `assets/pages/<pageKey>/<type>/<usage-name>.<ext>` — anything unique to one
  page, or a deliberate local duplicate of a common asset for that page's own
  use (e.g. the one demo clip a vertical page plays in its own player).
- Never edit a file in `assets/common/` for the sake of one page — if a page
  needs a different version of a shared asset, that's a `assets/pages/<key>/`
  duplicate, not an edit to the common file.
- Original repo assets (`logo/`, `mp3/`, `favicon.svg`) are untouched by this
  folder's existence — `newSite/assets/` holds **copies**, reorganized by
  usage. When you actually deploy a new page, its assets get copied again from
  `newSite/assets/` to root-relative paths (`logo/...`, `mp3/...`) the same way
  `index.html`/`healthcare.html` reference them today.

## How to build a new vertical page (e.g. `realestate.html`)

1. **Content**: In `template.json`, add a new `pages.realestate` object with
   the *exact same keys* as `pages.healthcare` (nav, hero, signatureCallSheet,
   voiceSample, callTypesGrid, limits, setup, pricingSection, demoCta,
   calendarModal, footer). Write real estate-specific copy into every field —
   don't leave healthcare copy in a renamed key. The signature "call sheet"
   section especially should become whatever artifact best proves this
   vertical works (e.g. a site-visit-booking transcript instead of a clinic
   appointment transcript).
2. **Assets**: duplicate `assets/pages/_template/` → `assets/pages/realestate/`
   for anything unique to this page; otherwise reference `assets/common/`.
   Register new files under `assets.audio.pages.realestate` (or
   `assets.images.pages.realestate`) in `template.json`.
3. **Skeleton**: copy `templates/vertical-page.template.html` to the repo root
   as `realestate.html`, then replace every `{{token}}` with the matching
   `brand.*` / `theme.clinicalTeal.*` / `pages.realestate.*` value. Copy the
   full `<style>` block and the two trailing `<script>` blocks byte-for-byte
   from `healthcare.html` — they're theme/behavior, not copy, so
   `template.json` doesn't parameterize them.
4. **Wire it up**: if this vertical should be linked from the main page's Use
   Cases grid, set `link` on the matching card in `config.js`'s
   `CONFIG.useCases` (mirrored in `brand.useCasesSection.cards` here) to
   `/realestate.html`, and add the page to `sitemap.xml`.
5. **Test**: run `python -m pytest tests/` (see root CLAUDE.md) against the
   new page before shipping. Add it to `tests/test_website_e2e.py` if the
   existing suite doesn't already parametrize across pages.

## Keeping pages in sync — do this automatically, without being asked each time

The user drives all future changes to this site through Claude, using this
template as the shared source of truth. That means:

- **Any copy change** (a heading, a price, a testimonial, a footer line) that
  applies to more than one page must be made in `template.json` first, then
  propagated to every HTML page that uses it — not hand-edited independently
  in each HTML file.
- **Any UI/look-and-feel change** (color, spacing, a new section pattern, a
  button style) made on one page must be evaluated for whether it should apply
  to the shared `theme` block and therefore every page using that theme —
  update `theme.default` or `theme.clinicalTeal` in `template.json`, then
  reapply the change to every page sharing that theme's CSS block, exactly
  like the root CLAUDE.md's index.html ↔ healthcare.html rule, generalized to
  all current and future pages.
- **Site name casing** is always `Aigenetic` (capital A only) — check
  `meta.siteNameCasingRule` in `template.json`.
- **Logos** must always come from `assets/common/logos/` (or the equivalent
  root-relative `logo/` files once deployed) — never a re-exported or
  re-colored one-off copy for a single page, unless `assets/pages/<key>/` is
  used deliberately and documented as such.
- When you finish a change, update this template.json (and this file, if the
  *pattern* itself changed) so the next page-generation stays accurate — the
  template must never drift out of sync with what's actually live.

## Known gaps carried over from the source pages (fix opportunistically)

- `realestate.html` has no voice-sample audio player — there's no
  real-estate-specific demo clip in `mp3/` yet (only Healthcare/Ecommerce/
  BFSI/EdTech/HRTech/Hospitality exist), and playing a mismatched clip under
  a "Hear the assistant" banner would misrepresent what a caller would
  actually hear. See `assets.audio.pages.realestate.note` in `template.json`
  and the matching `CODED-Thers/TODO.md` entry. Once a real clip is recorded,
  add it under `assets/common/audio/` + `assets/pages/realestate/audio/` and
  restore the two-column `.callsheet-grid` + sticky voice-sample layout
  (currently a single centered `.sheet-solo` column instead).
- `realestate.html`'s CRM/portal chips (Zoho, Sell.Do, LeadSquared, 99acres,
  MagicBricks, Housing.com) are deliberately **not** marked `.chip.on` —
  they aren't verified live integrations, only illustrative examples of
  "attach whatever you use." Don't mark one active without confirming it's
  genuinely built first (see `pages.realestate.setup.integrationsHonestyNote`).
- `theme.default` and `theme.clinicalTeal` use the same ink/teal/mint hues
  under different variable names and slightly different implementations
  (Tailwind CDN vs. hand-rolled CSS). They aren't formally unified into one
  stylesheet — if you ever do that consolidation, update both theme blocks
  here to point at the same source. Both now carry the same *derived*
  surface/motion tokens (`--card`/`--r-*`/`--sh-*`/`--ease` and equivalents)
  too, added in the 2026-08-23/24 redesign pass — keep those in sync as well.

## Resolved (kept for history)

- ~~`healthcare.html` had no meta description / Open Graph tags~~ — fixed
  2026-08-23; see `pages.healthcare.seo.note`.
- ~~`index.html` and `healthcare.html` had drifted apart visually~~ — both
  pages carry the same design language again as of 2026-08-24 (derived
  tokens, sticky nav with scroll state, a working mobile menu on both pages,
  card-style stat rail, reveal/stagger entrances, dark closing CTA panel).
  See `theme.default.$designNote` and `pages.healthcare.$designNote` in
  `template.json` for exactly what changed on each page. index.html's mobile
  menu is a **new fix**, not a resync — it previously had no mobile nav at
  all (links just vanished under `hidden md:flex`).
- ~~The "Real Estate" Use Cases card had no `link`~~ — fixed 2026-08-24:
  `realestate.html` built (the second `pages.*` instance, proving the
  template pattern out beyond healthcare), `config.js`'s Real Estate card now
  links to it with its own `linkCtaLabel`, and a real bug was fixed alongside
  it — `index.html` had hardcoded the literal text "Explore for clinics →"
  for *any* linked Use Cases card, which would have wrongly shown clinic
  copy on the Real Estate card too. See `pages.realestate.$builtNote`.
