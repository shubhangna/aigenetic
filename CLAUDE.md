# CLAUDE.md
Always ensure the site name is consistent with caps sensitivity Aigenetic
Verify logos are consistent as per logo folder
Always ensure if any change is made on UI or look and feel on main site the same should be implimented on /healthcare.html and viseversa to maintain consistency

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project purpose

Static marketing site for Aigenetic, an AI voice-assistant product for Indian SMEs. Served as a GitHub Pages
site on the custom domain `aigenetic.in` (see `CNAME`). No backend, no build pipeline — plain HTML/CSS/JS
files deployed as-is.
Intent is to keep all child pages like healthcare.html and the main page index.html always in sync in terms of look and feel and theme, as much as possible header and footer

Always keep looking for issues while implimenting and accessing the site either local or live and add any issues found in the CODED-Thers/TODO.md 

Always use CLAUDE_Result.html with minimal coding only clean minimal
Over write this report or update as needed, keep a log of all done things on what has already been done [4 words per activity ]

If any todo item is done move it to Done section at the bottom with Comment - claude moved at the end
## Codebase shape

- `index.html` — the main landing page. A single-page React 18 app loaded via UMD `<script>` tags and
  written as JSX compiled in-browser by Babel Standalone (`<script type="text/babel">`, ~line 182 onward).
  There is no `npm`/webpack/vite pipeline; React, ReactDOM, Babel, and Tailwind are all pulled from CDNs.
  Component tree is one big `App()` function rendering sections (`header`, hero, how-it-works, use cases,
  audio showcase, USPs, testimonials, pricing, footer) that read their copy from `window.CONFIG`.
- `healthcare.html` — a clinic-focused landing page variant. Plain HTML + vanilla JS (no React/Babel), but
  still loads `config.js` and applies shared contact data (`data-phone-link`, `data-whatsapp-link`,
  `data-email-link`, etc. attributes) via a small IIFE. Has its own copy of the calendar-modal and
  waveform/audio-player logic — these are duplicated between `index.html` and `healthcare.html`, not shared.
- `config.js` — sets `window.CONFIG`, the single source of truth for all business copy: company info,
  hero content, pricing plans, use cases, testimonials, audio demo metadata, etc. Keep this file **data
  only** — no DOM logic or JSX here. Both `index.html` and `healthcare.html` load it before their own
  scripts run.
- `styles.css` — shared custom CSS (beyond Tailwind utility classes) used by `index.html`.
- `mp3/` — audio demo files referenced by `CONFIG.audioDemos[].file`.
- `logo/`, `favicon.svg` — brand assets referenced by both HTML pages.
- `privacy-policy.html`, `refund-policy.html`, `terms-of-service.html` — standalone static legal pages.
- `openapi.json` — reference OpenAPI spec for an unrelated third-party telephony API (FreJun Teler); not
  loaded or consumed by any page in this repo, kept for reference only.
- `robots.txt`, `sitemap.xml`, `CNAME` — GitHub Pages / SEO plumbing for the `aigenetic.in` custom domain.
- `tests/` — Python test suite (see below).

## Development guidelines

- Maintain the zero-build approach: rely on CDN React/Tailwind/Babel; do not introduce npm/build tooling
  unless explicitly requested.
- Write new UI as JSX inside `index.html`'s `<script type="text/babel">` block, compatible with Babel
  standalone — no ES module `import`/`export` syntax.
- `healthcare.html` is vanilla JS/HTML, not JSX — match that style there instead.
- Put new copy or business details (pricing, taglines, feature lists, etc.) in `config.js`'s `CONFIG`
  object, not hardcoded in markup. Keep new keys consistent with the existing structure so both pages can
  read them.
- **Pricing/policy changes**: any change should be checked for whether it also requires updating the
  pricing plan (`CONFIG.pricing`, `CONFIG.pricingMeta`) and the policy pages
  (`terms-of-service.html`, `refund-policy.html`, `privacy-policy.html`) — update them if so.
- Favor semantic HTML and Tailwind utility classes; keep gradients/animations lightweight to preserve page
  load performance. Avoid adding large external assets.
- Preserve accessibility: meaningful `alt` text, ARIA labels where needed, keyboard-friendly controls.
- Keep canonical/SEO meta tags intact when editing `<head>` content; don't break GitHub Pages custom-domain
  assumptions (the `CNAME` file, absolute `/`-rooted asset paths like `/favicon.svg`, `/logo/...`).
- If touching the calendar-modal or audio-player logic, remember it's duplicated in both `index.html` and
  `healthcare.html` — update both if the fix/feature applies to both pages.

## Testing

Tests live in `tests/` and use `unittest` (not pytest's own test collection, though pytest is the runner —
see `.vscode/settings.json` which configures VS Code's test explorer for `unittest`).

- `tests/test_website_e2e.py` — Playwright-based E2E tests against a running instance of the site (checks
  hero content, sections, CTA links, pricing cards, console errors, etc.). Reads target from `BASE_URL`
  env var, defaulting to `http://localhost:8989`.
- `tests/test_github_ips.py` — verifies DNS for `aigenetic.in` resolves to the expected GitHub Pages IPs.
- `tests/conftest.py` — pytest plugin adding `--site {local,remote}` (maps to `localhost:8989` or
  `https://aigenetic.in`) and `--html-report` options, and auto-generates/opens an HTML test report after
  each run.

Run the full suite with pytest (serve the static site locally first for the E2E tests):

```
python -m http.server 8989          # in one terminal, from repo root
python -m pytest tests/             # in another terminal — defaults to --site local
```

Run against the live production site instead of localhost:

```
python -m pytest tests/ --site remote
```

Run a single test:

```
python -m pytest tests/test_website_e2e.py::TestWebsiteE2E::test_06_pricing_section_with_cards
```

Install test dependencies (Playwright browser binaries required once):

```
pip install -r tests/requirements-test.txt
python -m playwright install chromium
```

If changing DNS/IP expectations, update `tests/test_github_ips.py` accordingly.

## Git commit message structure

- Format: `<type>: <short summary>` where type is one of `feat|fix|chore|docs|test|refactor|style`.
- Keep summary <= 72 chars, imperative mood (e.g., "fix header CTA links").
- Body (optional): bullet list of key changes; wrap at ~100 chars; no trailing punctuation.
- Tests (optional): add a final `Tests:` line describing what was run (e.g., `Tests: manual smoke`,
  `Tests: n/a`).
