# SEO audit — aigenetic.in

Date: 23 November 2026. Live site measured before the change: `https://aigenetic.in`. The branch was measured afterwards from a local static server (`python3 -m http.server`), with Lighthouse’s own throttling. GitHub Pages still builds `main` with Jekyll. This pass does not switch the site to a GitHub Actions deploy.

`logo/logoMedium.png` is unchanged (md5 `ba7b3a6ca887a3034a04e1a00f6fa188`). The mp3 files were not edited. The hero copy and the Google Calendar iframe URL are unchanged. The visible call to action on the page is **Book a demo**. The brief also named “Try the autopilot”; that sentence is not in the repo, and the smoke tests require “Book a demo”, so it was left as published.

## Lighthouse

### Before (live GitHub Pages)

| Page | Form | Performance | Accessibility | Best Practices | SEO | LCP | FCP | CLS | TBT |
|---|---|---:|---:|---:|---:|---|---|---|---|
| Home | Mobile | 99 | 100 | 79 | 100 | 1.3 s | 1.0 s | 0 | 100 ms |
| Home | Desktop | 100 | 100 | 78 | 100 | 0.3 s | 0.3 s | 0 | 0 ms |
| Privacy | Mobile | 100 | 100 | 100 | 100 | 1.2 s | 1.0 s | 0 | 10 ms |
| Privacy | Desktop | 100 | 100 | 100 | 100 | 0.3 s | 0.2 s | 0 | 0 ms |
| Terms | Mobile | 100 | 100 | 100 | 100 | 1.1 s | 0.9 s | 0 | 10 ms |

Home Best Practices failed on third-party cookies (`NID`, `_GRECAPTCHA`) from the Google Calendar iframe, which loaded on every view.

### After (this branch, local server)

| Page | Form | Performance | Accessibility | Best Practices | SEO | LCP | FCP | CLS | TBT |
|---|---|---:|---:|---:|---:|---|---|---|---|
| Home | Mobile | 98 | 100 | 100 | 100 | 2.0 s | 1.6 s | 0 | 120 ms |
| Home | Desktop | 100 | 100 | 100 | 100 | 0.5 s | 0.4 s | 0 | 0 ms |
| Privacy | Mobile | 99 | 100 | 100 | 100 | 1.9 s | 1.2 s | 0 | 0 ms |
| Privacy | Desktop | 100 | 100 | 100 | 100 | 0.5 s | 0.3 s | 0 | 0 ms |
| Terms | Mobile | 99 | 100 | 100 | 100 | 1.8 s | 1.2 s | 0 | 0 ms |
| Clinics use case | Mobile | 99 | 100 | 100 | 100 | 1.9 s | 1.5 s | 0 | 30 ms |

Best Practices is 100 because the same iframe now has `loading="lazy"` while the dialog is `display: none`. A headless check saw 0 requests to `calendar.google.com` before “Book a demo”, and 1 request after the dialog opened. The `src` is still the live appointment URL. LCP is higher than production because this run was not on the GitHub CDN. It is still under 2.5 s. CLS is 0.

## Keyword check against published copy

| Candidate | On the site today |
|---|---|
| AI receptionist India | Yes. “An AI receptionist for appointment-led businesses.” and “An AI receptionist for clinics in India”. |
| AI front desk | Yes. “Front Desk as a Service”, the WhatsApp prefill “AI front desk”, and the footer line. |
| AI phone assistant | Partly. The terms page says “AI front-desk and phone assistant services”. The homepage price card says “Configured AI voice assistant”. |
| WhatsApp appointment booking bot | Yes. The salons card uses that phrase. |
| AI voice agent for clinics | Not verbatim. The supported line is “AI receptionist for clinics in India”, plus the healthcare demo “AI agent handling patient inquiries and support”. |
| Appointment booking automation | Not verbatim. The site says “Appointments on autopilot”, “Booking & rescheduling”, and “appointment/calendar booking”. |
| AI call answering service | Partly. Real estate card: “AI call answering in Hindi and English”. |

Titles and headings use the lines that are actually published. “AI voice agent for clinics” and “appointment booking automation” were not forced into new copy.

## Findings

### Critical

**C1. Two public price lists disagree.** Status: open, TODO(owner). The homepage (and the new pricing page, which repeats it) says Flex ₹2,999 / month with 500 minutes and Pro ₹7,999 / month with 1,500 minutes, then ₹6 per minute, and Enterprise “Let’s talk”. The Terms of Service and Refund Policy say a ₹10,000 setup fee and monthly plans of ₹4,999–₹9,999. Offer rich results were not added, so Google is not handed one of those prices as the official offer. The legal pages were not rewritten.

**C2. The terms promise “31+ Indian languages”.** Status: open, TODO(owner). The homepage, and every new page, says Hindi, English and Hinglish only. The terms service description was not rewritten.

### High

**H1. No IPv6 at the apex.** Status: open, TODO(owner). `aigenetic.in` has the four GitHub Pages A records (`185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`) and no AAAA records. `www` is a CNAME to `shubhangna.github.io` and 301s to `https://aigenetic.in/`. `http://aigenetic.in/` 301s to HTTPS. DNS host is DomainControl (GoDaddy/Namecheap-style nameservers `ns45.domaincontrol.com`).

**H2. Titles, descriptions, Open Graph and Twitter cards were thin.** Status: done. Unique titles and descriptions, self-canonicals, `hreflang="en-in"` and `x-default`, `og:image` 1200×630 (`/assets/og-image.png`) with width, height and alt, and Twitter `summary_large_image`. The homepage H1 is still “Appointments on autopilot.”

**H3. No use-case or supporting URLs.** Status: done, with gaps. New indexable pages, all from published sentences: how it works, features, pricing, FAQ, about, contact, a use-case index, and nine use cases (clinics/healthcare, salons, real estate, coaching, hospitality, lead qualification, e-commerce, payment reminders, recruitment). Sample-call pages that only had a one-line blurb stay that short. Full transcripts are TODO(owner).

**H4. Crawl files and icons were missing.** Status: done. `robots.txt` points at the sitemap and disallows internal paths. `sitemap.xml` lists the indexable URLs with `lastmod` 2026-11-23. Added `llms.txt`, `/.well-known/security.txt` (Jekyll `include: .well-known`, because Jekyll otherwise skips dot paths), `site.webmanifest`, `favicon.ico`, and 180/192/512 icons. `security.txt` expires 2027-11-23 and contacts `connect@aigenetic.in`.

**H5. Structured data was only Organization plus FAQ.** Status: done, with a deliberate omission. Home now has Organization (`@id`), WebSite, Service and the existing FAQPage. Inner pages have BreadcrumbList and WebPage (AboutPage or ContactPage where that is the type). Demo pages add AudioObject with the published description and the mp3 URL. Organization `sameAs` lists the official Facebook page, Instagram, and YouTube channel. No personal profile was added. No `Offer` (see C1). No `LocalBusiness` (the published address is “Rajiv Gandhi Infotech Park, Pune, India”, with no street, PIN or opening hours). No `SearchAction` (there is no site search).

**H6. Calendar iframe loaded Google on every page view.** Status: done for the cookie hit, booking URL unchanged. `loading="lazy"` plus the hidden dialog. Opening the dialog still requests the same schedule. Focus moves to Close, Escape and the backdrop still close it, and Tab cycles inside the dialog.

### Medium

**M1. `/index.html` is a second URL for the homepage.** Status: open, TODO(owner). It returns 200. The canonical is `https://aigenetic.in/`. A 301 needs Cloudflare or another host in front of Pages. GitHub Pages branch deploys cannot redirect that path without replacing the homepage.

**M2. `/CNAME` is publicly readable.** Status: accepted. The body is `aigenetic.in`. Removing it would risk the custom domain. It stays.

**M3. Dev files.** Status: already hidden in production, kept that way. On the live site, `/CODED-Thers/`, `/newSite/`, `/tests/`, `/___Archive/`, `/.git/`, `/.env`, `/README.md` and `/package.json` return 404 via Jekyll’s dot rules and `_config.yml` `exclude`. This branch also excludes `scripts/`, `seo-audit.md` and `seo-tracker.html`. A local Python server still serves repo files; that is not production. A GitHub Actions allow-list was not added. Switching Pages from “Deploy from a branch” to “GitHub Actions” is a cutover: until the owner flips the setting the workflow does nothing, and a bad first Actions deploy can drop the custom domain. The current Jekyll exclude already returns 404 for the internal paths, so the cutover is not worth that risk.

**M4. Privacy policy mentions analytics cookies. The site has no analytics tag.** Status: open, TODO(owner). No GA4 or Plausible tag was added.

**M5. Internal links were only the three policies.** Status: done. Footer explore links, homepage cards and sample titles, and “Related pages” on the new URLs. Anchor text is the existing heading or sentence, not “click here”.

**M6. Audio demos have no transcript.** Status: open, TODO(owner). Pages label the clips “Demo audio” and repeat the one-line homepage description. They do not invent a script.

### Low

**L1. `robots.txt` was a comment template.** Status: done. Replaced with a short allow list, internal `Disallow`, and the sitemap line. Crawl-delay was not set (Google ignores it).

**L2. `logo.png` is a 133×123 PNG shown at about 44 px.** Status: left as-is. Lighthouse estimated about 11 KiB from a modern format. Re-encoding the mark on the page was skipped so the header logo stays the file the site already ships. Performance was already 99.

**L3. `home.js` is unminified (about 3 KiB).** Status: left as-is. The aurora and waveform animations were not rewritten.

**L4. Security headers.** Status: open, TODO(owner). GitHub Pages does not set HSTS, CSP or `X-Frame-Options`. The playbook’s optional Cloudflare step is the practical place to add them.

**L5. Social profiles, Google Business Profile, CIN, GSTIN.** Social profiles are done. Organization `sameAs`, the footer, about, contact, and `llms.txt` list the official Facebook page (`https://www.facebook.com/profile.php?id=61593292055918`), Instagram (`https://www.instagram.com/aigenetic.in/`), and YouTube (`https://www.youtube.com/@aigenetic4Clinics`). No personal Facebook profile was added. Google Business Profile, CIN, and GSTIN stay open, TODO(owner). They are not on the site. An internal note already says not to publish GST or CIN until the real numbers are confirmed. They were not invented.

## What is indexable after this pass

Home, how it works, features, use cases index, nine use-case pages, pricing, FAQ, about, contact, privacy, terms, refund. `404.html` and `seo-tracker.html` are `noindex`. The tracker and this file are in the Jekyll exclude list.

Retired URLs stay retired and were not redirected back into the site: `/healthcare.html`, `/realestate.html`, `/education.html`, `/summary.html` (the smoke tests expect 404). No existing public URL was renamed, so no new redirects were required.

## Checks that still need a live URL

Google’s Rich Results Test and validator.schema.org were not run against production, because this branch is not deployed. JSON-LD on the branch parses. After merge, test the homepage and `/use-cases/healthcare-support.html`.

Confirm `https://aigenetic.in/.well-known/security.txt` and `https://aigenetic.in/llms.txt` return 200. If `security.txt` is 404, Jekyll ignored `include: .well-known` and the file needs another route.

## Manual steps for the owner

### GitHub

1. Merge this PR. Leave Pages on **Deploy from a branch** (`main`, `/`). Do not switch the source to GitHub Actions for this change.
2. Settings → Pages: custom domain `aigenetic.in`, DNS check green, **Enforce HTTPS** on.
3. Code → About: website `https://aigenetic.in`. Description along the lines of “AI front desk for Indian businesses. Answers calls, replies on WhatsApp, books appointments and follows up, 24×7.” Topics, lowercase: `ai-front-desk`, `ai-receptionist`, `voice-ai`, `whatsapp`, `appointment-booking`, `india`.
4. Settings → Social preview: upload `assets/og-image.png` (1200×630).

### DNS

At the DNS host for `aigenetic.in`, add AAAA records on `@` if they are still missing:

- `2606:50c0:8000::153`
- `2606:50c0:8001::153`
- `2606:50c0:8002::153`
- `2606:50c0:8003::153`

Keep the four A records that are already correct. Keep the `www` CNAME to `shubhangna.github.io`. Check `https://dns.google/resolve?name=aigenetic.in&type=AAAA`.

### Search Console

1. https://search.google.com/search-console → Add property → Domain → `aigenetic.in`.
2. Add the TXT record on `@`. Confirm with `https://dns.google/resolve?name=aigenetic.in&type=TXT`, then Verify.
3. Sitemaps: submit `https://aigenetic.in/sitemap.xml` (full URL).
4. URL Inspection → Request indexing for `/`, `/pricing.html`, `/faq.html`, `/use-cases.html`, and the clinic, salon and real-estate use cases.

### Bing

1. https://www.bing.com/webmasters → Import from Google Search Console, or add the site and verify.
2. Submit `https://aigenetic.in/sitemap.xml`.
3. URL Submission: the same key URLs.
4. IndexNow is optional.

### Profiles

Organization `sameAs`, the footer, about, contact, and `llms.txt` use the official profiles:

- Facebook page: `https://www.facebook.com/profile.php?id=61593292055918`
- Instagram: `https://www.instagram.com/aigenetic.in/`
- YouTube: `https://www.youtube.com/@aigenetic4Clinics`

Set each profile’s website to `https://aigenetic.in`. Also set the GitHub profile website field and the repo About website. LinkedIn, X, Product Hunt, Crunchbase, G2, and Capterra were not supplied, so they are not linked. Google Business Profile waits on a precise public address. Do not buy links.

### Content the owner still has to supply

- Which price list is current (homepage ₹2,999 / ₹7,999 versus terms ₹10,000 setup and ₹4,999–₹9,999), then align the terms, the refund policy and the homepage.
- Whether “31+ Indian languages” in the terms is still true. The marketing pages only say Hindi, English and Hinglish.
- Transcripts of the six mp3 demos, if those pages should rank for more than the one-line blurb.
- A full street address and PIN, opening hours, CIN, GSTIN.
- Whether to add analytics (the privacy policy already mentions analytics cookies) or to edit that section so it matches the site.
- Confirmed calendar, telephony and WhatsApp products. The FAQ says no calendar is assumed until setup, so no integration logos were added.

### Optional

Put Cloudflare in front for caching, HSTS, security headers, and a 301 from `/index.html` to `/`. Point any old domains at `https://aigenetic.in` with a 301.
