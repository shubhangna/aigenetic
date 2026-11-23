#!/usr/bin/env python3
"""Generate inner SEO pages, icons, crawl files, and legal-page head tags.

Copy is taken from index.html and assets/js/home.js. The script does not
invent testimonials, client names, stats, or prices. Re-run from the repo
root after editing the homepage copy those pages should repeat:

    python3 scripts/render-seo-pages.py
"""

from __future__ import annotations

import html
import json
import re
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
ORIGIN = "https://aigenetic.in"
TODAY = "2026-11-23"
CALENDAR = (
    "https://calendar.google.com/calendar/appointments/schedules/"
    "AcZssZ2-oLNDtD7wJRTQhnQ4WwsQE_f0x_wePzs82A2ihrxI7WZJb-XRed0ak2ltUfH1zohb-16awYx4?gv=true"
)

EXPLORE = [
    ("/how-it-works.html", "How it works"),
    ("/features.html", "Features"),
    ("/use-cases.html", "Use cases"),
    ("/pricing.html", "Pricing"),
    ("/faq.html", "FAQ"),
    ("/about.html", "About"),
    ("/contact.html", "Contact"),
]
POLICIES = [
    ("/privacy-policy.html", "Privacy Policy"),
    ("/terms-of-service.html", "Terms of Service"),
    ("/refund-policy.html", "Refund Policy"),
]


def esc(value: str) -> str:
    return html.escape(value, quote=True)


def load_sources() -> tuple[str, str]:
    page = (ROOT / "index.html").read_text(encoding="utf-8")
    script = (ROOT / "assets/js/home.js").read_text(encoding="utf-8")
    return page, script


def slice_between(text: str, start: str, end: str) -> str:
    i = text.index(start)
    j = text.index(end, i)
    return text[i:j]


def require(text: str, needle: str) -> None:
    if needle not in text:
        raise SystemExit(f"Expected copy missing: {needle}")


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    names = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    ]
    for name in names:
        if Path(name).exists():
            return ImageFont.truetype(name, size)
    return ImageFont.load_default()


def write_icons() -> None:
    icons = ROOT / "assets" / "icons"
    icons.mkdir(parents=True, exist_ok=True)
    logo = Image.open(ROOT / "logo" / "logoMedium.png").convert("RGBA")

    def square(size: int) -> Image.Image:
        canvas = Image.new("RGBA", (size, size), (5, 7, 15, 255))
        pad = int(size * 0.18)
        fitted = logo.copy()
        fitted.thumbnail((size - pad * 2, size - pad * 2), Image.Resampling.LANCZOS)
        canvas.alpha_composite(fitted, ((size - fitted.width) // 2, (size - fitted.height) // 2))
        return canvas

    square(180).save(icons / "apple-touch-icon.png", "PNG")
    square(192).save(icons / "icon-192.png", "PNG")
    square(512).save(icons / "icon-512.png", "PNG")
    icon32 = square(32)
    icon32.save(ROOT / "favicon.ico", format="ICO", sizes=[(16, 16), (32, 32)])

    og = Image.new("RGB", (1200, 630), (5, 7, 15))
    draw = ImageDraw.Draw(og, "RGBA")
    draw.ellipse((40, -160, 760, 560), fill=(88, 48, 180, 90))
    draw.ellipse((620, -80, 1280, 420), fill=(16, 110, 170, 80))
    draw.ellipse((180, 280, 980, 860), fill=(160, 40, 130, 50))
    mark = logo.copy()
    mark.thumbnail((340, 340), Image.Resampling.LANCZOS)
    plate = Image.new("RGBA", og.size, (0, 0, 0, 0))
    plate.alpha_composite(mark, (78, (630 - mark.height) // 2))
    og = Image.alpha_composite(og.convert("RGBA"), plate).convert("RGB")
    draw = ImageDraw.Draw(og)
    draw.text((470, 150), "AIGENETIC", font=font(22, True), fill=(154, 215, 255))
    draw.text((470, 200), "Appointments", font=font(68, True), fill=(238, 243, 255))
    draw.text((470, 278), "on autopilot.", font=font(68, True), fill=(238, 243, 255))
    draw.text((470, 390), "Talk. Text. Follow up. Slot booking.", font=font(28, True), fill=(213, 222, 242))
    draw.text((470, 450), "AI front desk for Indian businesses", font=font(24), fill=(183, 195, 220))
    og_path = ROOT / "assets" / "og-image.png"
    og.save(og_path, "PNG", optimize=True)
    if og.size != (1200, 630):
        raise SystemExit(f"OG image is {og.size}, expected 1200x630")


def write_manifest() -> None:
    manifest = {
        "name": "Aigenetic",
        "short_name": "Aigenetic",
        "description": "AI front desk for Indian businesses. Calls, WhatsApp, appointments and follow-ups, 24×7.",
        "start_url": "/",
        "scope": "/",
        "display": "browser",
        "background_color": "#05070f",
        "theme_color": "#05070f",
        "lang": "en-IN",
        "icons": [
            {"src": "/assets/icons/icon-192.png", "sizes": "192x192", "type": "image/png", "purpose": "any"},
            {"src": "/assets/icons/icon-512.png", "sizes": "512x512", "type": "image/png", "purpose": "any"},
        ],
    }
    (ROOT / "site.webmanifest").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")


def write_robots() -> None:
    (ROOT / "robots.txt").write_text(
        """# https://aigenetic.in/
User-agent: *
Allow: /
Disallow: /seo-tracker.html
Disallow: /seo-audit.md
Disallow: /CODED-Thers/
Disallow: /newSite/
Disallow: /tests/
Disallow: /scripts/
Disallow: /___Archive/

Sitemap: https://aigenetic.in/sitemap.xml
""",
        encoding="utf-8",
    )


def write_security() -> None:
    well = ROOT / ".well-known"
    well.mkdir(exist_ok=True)
    (well / "security.txt").write_text(
        """Contact: mailto:connect@aigenetic.in
Expires: 2027-11-23T00:00:00.000Z
Preferred-Languages: en
Canonical: https://aigenetic.in/.well-known/security.txt
""",
        encoding="utf-8",
    )


def head(title: str, description: str, url: str) -> str:
    return f"""  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="color-scheme" content="dark">
  <meta name="theme-color" content="#05070f">
  <title>{esc(title)}</title>
  <meta name="description" content="{esc(description)}">
  <link rel="canonical" href="{esc(url)}">
  <link rel="alternate" hreflang="en-in" href="{esc(url)}">
  <link rel="alternate" hreflang="x-default" href="{esc(url)}">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="Aigenetic">
  <meta property="og:title" content="{esc(title)}">
  <meta property="og:description" content="{esc(description)}">
  <meta property="og:url" content="{esc(url)}">
  <meta property="og:image" content="{ORIGIN}/assets/og-image.png">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:image:alt" content="Aigenetic. Appointments on autopilot. Talk. Text. Follow up. Slot booking.">
  <meta property="og:locale" content="en_IN">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{esc(title)}">
  <meta name="twitter:description" content="{esc(description)}">
  <meta name="twitter:image" content="{ORIGIN}/assets/og-image.png">
  <meta name="twitter:image:alt" content="Aigenetic. Appointments on autopilot. Talk. Text. Follow up. Slot booking.">
  <link rel="icon" href="/favicon.ico" sizes="32x32">
  <link rel="icon" href="/favicon.svg" type="image/svg+xml">
  <link rel="apple-touch-icon" href="/assets/icons/apple-touch-icon.png">
  <link rel="manifest" href="/site.webmanifest">
  <link rel="stylesheet" href="/assets/css/home.css">"""


def crumbs(items: list[tuple[str, str]]) -> str:
    parts = ['<nav class="crumbs" aria-label="Breadcrumb"><ol>']
    for name, href in items[:-1]:
        parts.append(f'<li><a href="{esc(href)}">{esc(name)}</a></li>')
    parts.append(f'<li><a href="{esc(items[-1][1])}" aria-current="page">{esc(items[-1][0])}</a></li>')
    parts.append("</ol></nav>")
    return "".join(parts)


def breadcrumb_ld(items: list[tuple[str, str]]) -> dict:
    return {
        "@type": "BreadcrumbList",
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": i + 1,
                "name": name,
                "item": ORIGIN + href if href.startswith("/") else href,
            }
            for i, (name, href) in enumerate(items)
        ],
    }


def header() -> str:
    return """    <div class="top" id="top">
      <header class="wrap has-contact">
        <a class="brand" href="/" aria-label="Aigenetic home">
          <img src="/logo/logo.png" alt="Aigenetic logo" class="original-logo" width="133" height="123" decoding="async">
          Aigenetic
        </a>
        <nav class="primary" aria-label="Main">
          <a href="/#system">The system</a>
          <a href="/#samples">Samples</a>
          <a href="/#conversation">Journey</a>
          <a href="/pricing.html">Pricing</a>
          <a class="btn" href="#calendar-booking" data-open-calendar>Book a demo <span class="arrow" aria-hidden="true">↗</span></a>
        </nav>
        <div class="header-contact" role="group" aria-label="Contact Aigenetic">
          <a class="btn icon-btn" data-phone-link href="tel:+917428497033" aria-label="Call Aigenetic" title="Call">
            <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 3h4l2 5-3 2c1 3 3 5 6 6l2-3 5 2v4c0 1-1 2-2 2C10 21 3 14 3 5c0-1 1-2 2-2Z"/></svg>
          </a>
          <a class="btn icon-btn whatsapp" data-whatsapp-link href="https://wa.me/917428497033" target="_blank" rel="noopener noreferrer" aria-label="Chat with Aigenetic on WhatsApp" title="WhatsApp">
            <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M20.5 12a8.5 8.5 0 0 1-12.4 7.5l-4.6 1 1.1-4.4A8.5 8.5 0 1 1 20.5 12Z"/><path d="M9 8c0 3.5 3.5 7 7 7l1-1.6-2.2-1-1 1c-1.2-.6-2.2-1.6-2.8-2.8l1-1-1-2.2Z"/></svg>
          </a>
          <a class="btn icon-btn" data-email-link href="mailto:connect@aigenetic.in" aria-label="Email Aigenetic" title="Email">
            <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M3 5h18v14H3zM3 6l9 7 9-7"/></svg>
          </a>
        </div>
        <div class="mobile-nav">
          <button type="button" class="nav-toggle" aria-expanded="false" aria-controls="mobile-nav-panel" aria-label="Open menu">Menu</button>
          <div id="mobile-nav-panel" class="links glass" hidden>
            <a href="/#system">The system</a>
            <a href="/#samples">Samples</a>
            <a href="/#conversation">Journey</a>
            <a href="/pricing.html">Pricing</a>
            <a href="#calendar-booking" data-open-calendar>Book a demo ↗</a>
          </div>
        </div>
      </header>
    </div>"""


def footer(current: str | None = None) -> str:
    explore = []
    for href, name in EXPLORE:
        current_attr = ' aria-current="page"' if href == current else ""
        explore.append(f'<a href="{href}"{current_attr}>{esc(name)}</a>')
    policies = []
    for href, name in POLICIES:
        current_attr = ' aria-current="page"' if href == current else ""
        policies.append(f'<a href="{href}"{current_attr}>{esc(name)}</a>')
    return f"""    <footer>
      <div class="wrap">
        <div class="footer-row">
          <a href="/" class="brand" aria-label="Aigenetic home">
            <img src="/logo/logo.png" alt="Aigenetic logo" class="original-logo" width="133" height="123" decoding="async" loading="lazy">
            Aigenetic
          </a>
          <span>Front Desk as a Service for Indian businesses.</span>
          <span>Aigenetic (OPC) Pvt Ltd · Rajiv Gandhi Infotech Park, Pune, India</span>
        </div>
        <nav class="footer-nav footer-links" aria-label="Explore">
          {''.join(explore)}
        </nav>
        <nav class="footer-nav footer-links" aria-label="Policies">
          {''.join(policies)}
        </nav>
      </div>
    </footer>
    <nav class="sticky-cta" aria-label="Quick contact">
      <a class="btn secondary" data-phone-link href="tel:+917428497033">Call</a>
      <a class="btn secondary" data-whatsapp-link href="https://wa.me/917428497033?text=Hi%20Aigenetic%2C%20I%20would%20like%20a%20demo%20of%20the%20AI%20front%20desk." target="_blank" rel="noopener noreferrer">WhatsApp</a>
      <a class="btn" href="#calendar-booking" data-open-calendar>Book a demo</a>
    </nav>"""


def modal() -> str:
    return f"""    <div id="calendar-modal-main" role="dialog" aria-modal="true" aria-labelledby="calendar-modal-main-title" style="display:none">
      <div class="calendar-modal-main-content glass">
        <button type="button" class="calendar-close" onclick="closeCalendarModalMain()" aria-label="Close booking dialog">Close</button>
        <h2 id="calendar-modal-main-title">Schedule Your Demo</h2>
        <p>Pick a time that works for you — Google Calendar takes care of the invite and the Meet link.</p>
        <iframe class="calendar-modal-main-iframe" src="{CALENDAR}" style="border: 0" width="100%" height="600" frameborder="0" loading="lazy" title="Book a demo with Aigenetic"></iframe>
      </div>
    </div>"""


def closing() -> str:
    return """      <section id="preview" class="closing">
        <span id="calendar-booking" class="alias"></span>
        <div class="wrap">
          <div>
            <p class="eyebrow">Your front desk. As a service.</p>
            <h2>Put your front desk <br>on autopilot.</h2>
            <p>Talk. Text. Follow up. Slot booking. One managed service.</p>
            <p class="contact-line">
              <a data-phone-link href="tel:+917428497033">Call us</a>
              <a data-whatsapp-link href="https://wa.me/917428497033?text=Hi%20Aigenetic%2C%20I%20would%20like%20a%20demo%20of%20the%20AI%20front%20desk." target="_blank" rel="noopener noreferrer">WhatsApp</a>
              <a data-email-link href="mailto:connect@aigenetic.in">connect@aigenetic.in</a>
            </p>
          </div>
          <a class="btn" href="#calendar-booking" data-open-calendar>Book a demo <span aria-hidden="true">↗</span></a>
        </div>
      </section>"""


def related(links: list[tuple[str, str]]) -> str:
    items = "".join(f'<li><a href="{esc(href)}">{esc(name)}</a></li>' for href, name in links)
    return f"""      <section class="section page-section">
        <div class="wrap">
          <div class="section-head">
            <div>
              <p class="eyebrow">Keep going</p>
              <h2>Related pages</h2>
            </div>
          </div>
          <ul class="related-links">{items}</ul>
        </div>
      </section>"""


def coverage() -> str:
    return """        <div class="coverage">
          <div><strong>AI calls</strong><p>Answer &amp; understand</p></div>
          <div><strong>WhatsApp</strong><p>Chat &amp; keep customers updated</p></div>
          <div><strong>Calendar booking</strong><p>Turn intent into appointments</p></div>
          <div><strong>Follow-ups</strong><p>Keep the next step moving</p></div>
        </div>"""


def player(tag: str, title: str, blurb: str, src: str) -> str:
    return f"""        <article class="player glass" data-player id="sample">
          <audio preload="none" src="{esc(src)}"></audio>
          <button type="button" class="play-btn" data-play data-label="{esc(title)}" aria-pressed="false" aria-label="Play {esc(title)}">
            <svg class="icon-play" viewBox="0 0 24 24" aria-hidden="true"><path d="M8 5v14l11-7z"/></svg>
            <svg class="icon-pause" viewBox="0 0 24 24" aria-hidden="true"><path d="M6 5h4v14H6zM14 5h4v14h-4z"/></svg>
          </button>
          <div class="player-copy">
            <p class="tag">{esc(tag)}</p>
            <h3>{esc(title)}</h3>
            <p>{esc(blurb)}</p>
          </div>
          <p class="demo-pill">Demo audio</p>
          <div class="wave-wrap">
            <canvas class="wave-canvas" width="640" height="84" aria-hidden="true"></canvas>
          </div>
          <div class="player-times">
            <span data-current>00:00</span>
            <label class="scrub">
              <span class="visually-hidden">Seek {esc(title)}</span>
              <input type="range" min="0" max="1000" value="0" step="1" data-scrub disabled>
            </label>
            <span data-duration>00:00</span>
          </div>
          <p class="player-error" data-error hidden>This demo file could not be played.</p>
        </article>"""


def journey(steps: list[tuple[str, str, str]]) -> str:
    items = []
    for label, heading, body in steps:
        items.append(
            f'<li class="glass"><span class="journey-label">{esc(label)}</span>'
            f"<h3>{esc(heading)}</h3><p>{esc(body)}</p></li>"
        )
    return '<ol class="journey">' + "".join(items) + "</ol>"


def render(path: str, title: str, description: str, crumb: list[tuple[str, str]], body: str, graph: list[dict]) -> None:
    url = ORIGIN + path
    if not path.startswith("/"):
        raise SystemExit(path)
    visible = len(title)
    dlen = len(description)
    flag = ""
    if not 50 <= visible <= 60:
        flag += f" TITLE {visible}"
    if not 140 <= dlen <= 160:
        flag += f" DESC {dlen}"
    print(f"{path} title={visible} desc={dlen}{flag}")
    graph = [breadcrumb_ld(crumb), *graph]
    payload = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, indent=2)
    doc = f"""<!DOCTYPE html>
<html lang="en">
<head>
{head(title, description, url)}
  <script type="application/ld+json">
  {payload}
  </script>
</head>
<body>
  <canvas id="aurora" aria-hidden="true"></canvas>
  <div id="root">
    <a class="skip" href="#main">Skip to content</a>
{header()}
    <main id="main">
{body}
{closing()}
    </main>
{footer(path)}
  </div>
{modal()}
  <script>document.documentElement.classList.add("motion");</script>
  <script src="/assets/js/home.js" defer></script>
  <script src="/assets/js/calendar-modal.js" defer></script>
  <noscript><style>[data-reveal]{{opacity:1!important;transform:none!important}}</style></noscript>
</body>
</html>
"""
    dest = ROOT / path.lstrip("/")
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(doc, encoding="utf-8")


def hero(crumb: list[tuple[str, str]], eyebrow: str, h1: str, lede: str) -> str:
    return f"""      <section class="page-hero wrap">
        {crumbs(crumb)}
        <p class="eyebrow">{esc(eyebrow)}</p>
        <h1>{h1}</h1>
        <p class="subhead">{lede}</p>
        <div class="actions">
          <a class="btn" href="#calendar-booking" data-open-calendar>Book a demo <span aria-hidden="true">↗</span></a>
          <a class="btn secondary" href="/#samples">Hear a sample call <span aria-hidden="true">↓</span></a>
        </div>
        <p class="small hero-note">Hindi · English · Hinglish &nbsp; / &nbsp; Fully managed</p>
      </section>"""


def webpage(path: str, title: str, description: str, kind: str = "WebPage") -> dict:
    return {
        "@type": kind,
        "name": title,
        "description": description,
        "url": ORIGIN + path,
        "isPartOf": {"@id": ORIGIN + "/#website"},
        "about": {"@id": ORIGIN + "/#service"},
        "inLanguage": "en-IN",
        "publisher": {"@id": ORIGIN + "/#organization"},
    }


def main() -> None:
    page, script = load_sources()
    for needle in (
        "Appointments",
        "₹2,999",
        "₹7,999",
        "What does Front Desk as a Service include?",
        "Caller asks for a haircut and colour this Saturday.",
        "Buyer enquires about a 2 BHK and asks to see it.",
        "Parent asks about Class 10 maths batches.",
        "AI agent handling patient inquiries and support",
        "Edtech lead qualification",
        "AI-powered customer service for online stores",
        "Automated payment reminder calls",
        "AI-powered candidate screening and recruitment",
        "AI agent handling front desk inquiries and support",
    ):
        blob = page + script
        require(blob, needle)

    functions = slice_between(page, '<div class="four">', '<div class="four who">').rsplit("</div>", 1)[0] + "</div>"
    require(functions, "Start with a conversation.")
    setup = slice_between(page, '<ol class="steps">', "</ol>") + "</ol>"
    require(setup, "Map the customer journey")
    faq = slice_between(page, '<div class="glass faq-list"', "</div>") + "</div>"
    require(faq, "What does 24×7 cover?")
    prices = slice_between(page, '<div class="three">', '<p class="small pricing-note">').rstrip()
    require(prices, "₹2,999")
    require(prices, "₹7,999")
    require(prices, "Let’s talk")

    write_icons()
    write_manifest()
    write_robots()
    write_security()

    home_ref = [
        ("/", "Home"),
    ]

    def with_home(name: str, href: str) -> list[tuple[str, str]]:
        return [("Home", "/"), (name, href)]

    # --- info pages ---
    pages_meta: list[tuple[str, str, str]] = []

    path = "/how-it-works.html"
    title = "See How the AI Front Desk Works in India | Aigenetic"
    desc = "A call becomes a WhatsApp confirmation, a calendar booking and a reminder. Aigenetic maps the journey, tests it, and you approve before go-live."
    body = f"""{hero(with_home("How it works", path), "One customer journey", "From first contact to follow-through.", "Calls, WhatsApp, calendar bookings and follow-ups — one continuous front desk, with your team in control.")}
      <section class="section page-section">
        <div class="wrap">
          <div class="section-head">
            <div>
              <p class="eyebrow">Different channels. One continuous conversation.</p>
              <h2>A clinic enquiry, step by step.</h2>
            </div>
            <p>A clinic enquiry moves from a phone call to WhatsApp, into the calendar and on to a reminder. Your team sees what comes next.</p>
          </div>
          {journey([
            ("01 / AI CALL", "Understand the enquiry", "Capture the request and the preferred appointment time."),
            ("02 / WHATSAPP", "Confirm the details", "Share the chosen slot and keep the chat open for questions."),
            ("03 / CALENDAR", "Record the booking", "Add the appointment to the team’s connected calendar."),
            ("04 / FOLLOW-UP", "Send the reminder", "Keep the appointment on track and route changes to your team."),
          ])}
          <div class="copy-card glass">
            <h2>Sample WhatsApp chat</h2>
            <p><strong>Customer.</strong> “Kal 11:30 ka slot theek hai. Location bhi bhej dijiye.”</p>
            <p><strong>Assistant.</strong> “Ji. Aapke visit details aur clinic location yahin share kar rahe hain.”</p>
            <p><em>Slot confirmed → calendar booking → reminder scheduled.</em></p>
            <p class="small">Sample scenario, shown for illustration. Hinglish.</p>
          </div>
        </div>
      </section>
      <section class="section" id="setup">
        <div class="wrap setup">
          <div>
            <p class="eyebrow">We run it for you</p>
            <h2>Your process. Our setup. Your final say.</h2>
            <p>We map your front-desk work, configure the service and review the experience with you. Your team provides the business details, calendar rules and escalation contacts.</p>
          </div>
          {setup}
        </div>
      </section>
{related([
        ("/features.html", "AI calls, WhatsApp, booking and follow-ups"),
        ("/use-cases/healthcare-support.html", "AI receptionist for clinics in India"),
        ("/faq.html", "Practical questions before you start"),
        ("/contact.html", "Book a demo"),
      ])}"""
    render(path, title, desc, with_home("How it works", path), body, [webpage(path, title, desc)])
    pages_meta.append((path, title, desc))

    path = "/features.html"
    title = "AI Calls, WhatsApp Booking and Follow-ups | Aigenetic"
    desc = "The whole front desk, not just the phone. AI calls, WhatsApp updates, calendar booking and follow-ups, with your team in control. Book a demo."
    body = f"""{hero(with_home("Features", path), "The whole front desk. Not just the phone.", "From first contact to follow-through.", "Calls, WhatsApp, calendar bookings and follow-ups — one continuous front desk, with your team in control.")}
      <section class="section page-section">
        <div class="wrap">
          {functions}
          {coverage()}
        </div>
      </section>
{related([
        ("/how-it-works.html", "How a call becomes a booking"),
        ("/pricing.html", "Calling plans from ₹2,999 a month"),
        ("/use-cases.html", "Use cases and sample calls"),
        ("/contact.html", "Book a demo"),
      ])}"""
    render(path, title, desc, with_home("Features", path), body, [webpage(path, title, desc)])
    pages_meta.append((path, title, desc))

    path = "/pricing.html"
    title = "Public AI Front Desk Calling Plans in India | Aigenetic"
    desc = "Calling plans start at ₹2,999 a month for 500 minutes, or ₹7,999 for 1,500. Then ₹6 a minute. Book a demo to scope WhatsApp and booking in India."
    body = f"""{hero(with_home("Pricing", path), "Scope & pricing", "A clear starting point.", "Calling plans start here. WhatsApp, calendar booking and follow-ups are scoped to your workflow and added to your quote.")}
      <section class="section page-section" id="pricing">
        <div class="wrap">
          {prices}
          <p class="small pricing-note">Taxes, telephony and WhatsApp charges are confirmed in your quote. Billing and refund rules are in the <a href="/terms-of-service.html">Terms of Service</a> and the <a href="/refund-policy.html">Refund Policy</a>.</p>
        </div>
      </section>
{related([
        ("/features.html", "What the front desk includes"),
        ("/faq.html", "Questions on calendars, numbers and 24×7"),
        ("/contact.html", "Discuss a plan"),
      ])}"""
    render(path, title, desc, with_home("Pricing", path), body, [webpage(path, title, desc)])
    pages_meta.append((path, title, desc))

    path = "/faq.html"
    title = "AI Front Desk Questions and Answers | Aigenetic India"
    desc = "What Front Desk as a Service includes, how WhatsApp and calendars are set up, how reminders are controlled, and what 24×7 does and does not cover."
    faq_entities = []
    for q, a in re.findall(r"<summary>(.*?)</summary>\s*<p>(.*?)</p>", faq, re.S):
        faq_entities.append({
            "@type": "Question",
            "name": re.sub("<[^>]+>", "", q),
            "acceptedAnswer": {"@type": "Answer", "text": re.sub("<[^>]+>", "", a)},
        })
    if len(faq_entities) != 7:
        raise SystemExit(f"Expected 7 FAQs, found {len(faq_entities)}")
    body = f"""{hero(with_home("FAQ", path), "Before you get started", "A few practical questions.", "The same answers as on the homepage. Your approved rules define what the front desk handles and when your team steps in.")}
      <section class="section page-section" id="questions">
        <div class="wrap faq">
          <div class="glass faq-list" data-reveal>
            {faq.split(">", 1)[1].rsplit("</div>", 1)[0]}
          </div>
        </div>
      </section>
{related([
        ("/how-it-works.html", "How the journey is mapped"),
        ("/pricing.html", "Calling plans"),
        ("/contact.html", "Book a demo"),
      ])}"""
    render(path, title, desc, with_home("FAQ", path), body, [
        webpage(path, title, desc),
        {"@type": "FAQPage", "mainEntity": faq_entities},
    ])
    pages_meta.append((path, title, desc))

    path = "/about.html"
    title = "About Aigenetic (OPC) Pvt Ltd | AI Front Desk India"
    desc = "Aigenetic (OPC) Pvt Ltd runs an AI front desk for Indian businesses. It answers calls, replies on WhatsApp, books appointments and follows up, 24×7."
    body = f"""{hero(with_home("About", path), "Front Desk as a Service", "Aigenetic (OPC) Pvt Ltd", "Aigenetic answers your calls, replies on WhatsApp, books appointments and follows up, 24×7.")}
      <section class="section page-section">
        <div class="wrap stack">
          <article class="copy-card glass">
            <h2>What the company does</h2>
            <p>Front Desk as a Service for Indian businesses. If your day runs on bookings, Aigenetic answers every call in Hindi, English or Hinglish and books appointments on WhatsApp.</p>
            <p>The service is positioned for always-on AI handling of calls, WhatsApp enquiries, bookings and follow-ups. Human support hours, calendar availability, escalation ownership and outage procedures are agreed separately; 24×7 does not mean round-the-clock human staffing.</p>
          </article>
          <article class="copy-card glass">
            <h2>How it is run</h2>
            <p>We map your front-desk work, configure the service and review the experience with you. Your team provides the business details, calendar rules and escalation contacts. You approve before go-live.</p>
            <p>Hindi · English · Hinglish. Fully managed.</p>
          </article>
          <article class="copy-card glass">
            <h2>Published contact</h2>
            <dl class="nap">
              <div><dt>Company</dt><dd>Aigenetic (OPC) Pvt Ltd</dd></div>
              <div><dt>Address</dt><dd>Rajiv Gandhi Infotech Park, Pune, India</dd></div>
              <div><dt>Email</dt><dd><a href="mailto:connect@aigenetic.in">connect@aigenetic.in</a></dd></div>
              <div><dt>Phone</dt><dd><a href="tel:+917428497033">+91 742849 7033</a></dd></div>
            </dl>
          </article>
        </div>
      </section>
{related([
        ("/how-it-works.html", "How the front desk works"),
        ("/contact.html", "Book a demo"),
        ("/privacy-policy.html", "Privacy Policy"),
      ])}"""
    render(path, title, desc, with_home("About", path), body, [webpage(path, title, desc, "AboutPage")])
    pages_meta.append((path, title, desc))

    path = "/contact.html"
    title = "Book an Aigenetic Demo Now | AI Front Desk in India"
    desc = "Book a demo on Google Calendar, call +91 742849 7033, WhatsApp the same number, or email connect@aigenetic.in. Aigenetic is in Pune, India. Fully managed."
    body = f"""{hero(with_home("Contact", path), "Your front desk. As a service.", "Book a demo.", "Pick a time that works for you — Google Calendar takes care of the invite and the Meet link.")}
      <section class="section page-section">
        <div class="wrap">
          <article class="copy-card glass">
            <h2>Talk to Aigenetic</h2>
            <dl class="nap">
              <div><dt>Company</dt><dd>Aigenetic (OPC) Pvt Ltd</dd></div>
              <div><dt>Address</dt><dd>Rajiv Gandhi Infotech Park, Pune, India</dd></div>
              <div><dt>Phone</dt><dd><a href="tel:+917428497033">+91 742849 7033</a></dd></div>
              <div><dt>WhatsApp</dt><dd><a href="https://wa.me/917428497033?text=Hi%20Aigenetic%2C%20I%20would%20like%20a%20demo%20of%20the%20AI%20front%20desk." target="_blank" rel="noopener noreferrer">Chat on WhatsApp</a></dd></div>
              <div><dt>Email</dt><dd><a href="mailto:connect@aigenetic.in">connect@aigenetic.in</a></dd></div>
            </dl>
            <div class="actions">
              <a class="btn" href="#calendar-booking" data-open-calendar>Book a demo <span aria-hidden="true">↗</span></a>
            </div>
          </article>
        </div>
      </section>
{related([
        ("/pricing.html", "Calling plans"),
        ("/faq.html", "Practical questions"),
        ("/about.html", "About Aigenetic"),
      ])}"""
    render(path, title, desc, with_home("Contact", path), body, [webpage(path, title, desc, "ContactPage")])
    pages_meta.append((path, title, desc))

    use_cases = [
        {
            "href": "/use-cases/healthcare-support.html",
            "nav": "Clinics",
            "crumb": "Clinics",
            "title": "The AI Receptionist for Clinics in India | Aigenetic",
            "desc": "An AI receptionist for clinics in India: patient calls answered, consultations booked, reminders sent. Hear the healthcare sample and book a demo.",
            "eyebrow": "Healthcare",
            "h1": "AI receptionist for clinics in India.",
            "lede": "An AI receptionist for clinics in India: patient calls answered, consultations booked, reminders sent.",
            "steps_title": "Clinic appointment",
            "steps": [
                ("Call", "Enquiry understood", "Caller asks for tomorrow’s consultation."),
                ("WhatsApp", "Details confirmed", "Chosen slot and visit details shared in chat."),
                ("Calendar", "Appointment booked", "Tomorrow, 11:30 AM · Added to the team calendar."),
                ("Follow-up", "Reminder scheduled", "WhatsApp reminder before the appointment."),
            ],
            "audio": ("Healthcare", "Healthcare Support", "AI agent handling patient inquiries and support", "/mp3/HealthCare-onboarding_cEIUBM4Y (1).mp3"),
            "chat": True,
        },
        {
            "href": "/use-cases/salons.html",
            "nav": "Salons",
            "crumb": "Salons",
            "title": "WhatsApp Appointment Booking for Salons | Aigenetic",
            "desc": "A WhatsApp appointment booking bot that confirms the stylist and slot while your team is with clients. See the salon journey and book a demo.",
            "eyebrow": "Salons & spas",
            "h1": "WhatsApp appointment booking for salons.",
            "lede": "A WhatsApp appointment booking bot that confirms the stylist and slot while your team is with clients.",
            "steps_title": "Salon booking",
            "steps": [
                ("Call", "Enquiry understood", "Caller asks for a haircut and colour this Saturday."),
                ("WhatsApp", "Details confirmed", "Stylist, price range and slot confirmed in chat."),
                ("Calendar", "Appointment booked", "Saturday, 4:00 PM · Added to the stylist’s calendar."),
                ("Follow-up", "Reminder scheduled", "WhatsApp reminder on the morning of the visit."),
            ],
        },
        {
            "href": "/use-cases/real-estate.html",
            "nav": "Real estate",
            "crumb": "Real estate",
            "title": "AI Call Answering for Property Site Visits | Aigenetic",
            "desc": "AI call answering in Hindi and English for property enquiries, with site visits put on the sales calendar. See the sample journey and book a demo.",
            "eyebrow": "Real estate",
            "h1": "AI call answering for property enquiries.",
            "lede": "AI call answering in Hindi and English for property enquiries, with site visits put on the sales calendar.",
            "steps_title": "Property site visit",
            "steps": [
                ("Call", "Enquiry understood", "Buyer enquires about a 2 BHK and asks to see it."),
                ("WhatsApp", "Details confirmed", "Brochure, location and visit time shared in chat."),
                ("Calendar", "Site visit booked", "Sunday, 11:00 AM · Added to the sales calendar."),
                ("Follow-up", "Reminder scheduled", "WhatsApp reminder before the visit, follow-up after."),
            ],
        },
        {
            "href": "/use-cases/coaching.html",
            "nav": "Coaching",
            "crumb": "Coaching",
            "title": "AI Calls for Coaching Admissions in India | Aigenetic",
            "desc": "Admission enquiries answered after hours, demo classes booked and parents followed up on WhatsApp. See the coaching journey and book a demo.",
            "eyebrow": "Coaching & schools",
            "h1": "Admission enquiries, answered after hours.",
            "lede": "Admission enquiries answered after hours, demo classes booked and parents followed up on WhatsApp.",
            "steps_title": "Coaching demo class",
            "steps": [
                ("Call", "Enquiry understood", "Parent asks about Class 10 maths batches."),
                ("WhatsApp", "Details confirmed", "Batch timings and fee details shared in chat."),
                ("Calendar", "Demo class booked", "Thursday, 5:30 PM · Demo class added to the calendar."),
                ("Follow-up", "Reminder scheduled", "WhatsApp reminder before the demo class."),
            ],
        },
        {
            "href": "/use-cases/hospitality.html",
            "nav": "Hospitality",
            "crumb": "Hospitality",
            "title": "Hospitality Front Desk Sample Call | Aigenetic India",
            "desc": "Hear the hospitality sample: an AI agent handling front desk inquiries and support. The same service answers, books and follows up. Book a demo.",
            "eyebrow": "Hospitality",
            "h1": "Hospitality front desk sample.",
            "lede": "AI agent handling front desk inquiries and support.",
            "audio": ("Hospitality", "Hospitality Front Desk", "AI agent handling front desk inquiries and support", "/mp3/hospitality-front-desk_CVZtKlFn.mp3"),
        },
        {
            "href": "/use-cases/lead-qualification.html",
            "nav": "Lead qualification",
            "crumb": "Lead qualification",
            "title": "Edtech Lead Qualification Sample Call | Aigenetic India",
            "desc": "Hear the edtech lead qualification sample. Aigenetic answers the call, keeps the chat open and can book the next step. Book a demo in India.",
            "eyebrow": "EdTech",
            "h1": "Edtech lead qualification.",
            "lede": "Edtech lead qualification. A sample call of the AI front desk.",
            "audio": ("EdTech", "Lead Qualification", "Edtech lead qualification", "/mp3/Edtech-lead-qualification_KTkZSGKj.mp3"),
        },
        {
            "href": "/use-cases/ecommerce.html",
            "nav": "E-commerce",
            "crumb": "E-commerce",
            "title": "E-commerce Customer Support Sample | Aigenetic India",
            "desc": "Hear the e-commerce sample: AI-powered customer service for online stores. Calls, WhatsApp, booking and follow-ups stay one front desk. Book a demo.",
            "eyebrow": "E-commerce",
            "h1": "E-commerce customer support.",
            "lede": "AI-powered customer service for online stores.",
            "audio": ("E-commerce", "E-commerce Support", "AI-powered customer service for online stores", "/mp3/Ecom-customer-support_IRqJbynE.mp3"),
        },
        {
            "href": "/use-cases/payment-reminders.html",
            "nav": "Payment reminders",
            "crumb": "Payment reminders",
            "title": "Automated Payment Reminder Calls | Aigenetic India",
            "desc": "Hear the payment reminder sample: automated payment reminder calls. Follow-ups stay inside the same managed front desk. Book a demo to scope it.",
            "eyebrow": "BFSI",
            "h1": "Automated payment reminder calls.",
            "lede": "Automated payment reminder calls. A sample of the AI front desk.",
            "audio": ("BFSI", "Payment Reminders", "Automated payment reminder calls", "/mp3/BFSI-reminder_dztcIGvN.mp3"),
        },
        {
            "href": "/use-cases/recruitment.html",
            "nav": "Recruitment",
            "crumb": "Recruitment",
            "title": "AI Recruitment Screening Sample Call | Aigenetic India",
            "desc": "Hear the recruitment sample: AI-powered candidate screening and recruitment. It is a demo of the same call, WhatsApp and follow-up front desk.",
            "eyebrow": "HR Tech",
            "h1": "AI candidate screening and recruitment.",
            "lede": "AI-powered candidate screening and recruitment.",
            "audio": ("HR Tech", "Recruitment", "AI-powered candidate screening and recruitment", "/mp3/recruitment_eczAKBnf.mp3"),
        },
    ]

    hub_cards = []
    for case in use_cases:
        for step in case.get("steps", []):
            require(script if "tomorrow" not in step[2] else page + script, step[2].replace("’", "’"))
        hub_cards.append(
            f'<article class="glass"><p class="tag">{esc(case["eyebrow"])}</p>'
            f'<h2><a href="{esc(case["href"])}">{esc(case["h1"])}</a></h2>'
            f'<p>{esc(case["lede"])}</p></article>'
        )
        sections = [
            hero(with_home(case["crumb"], case["href"]), case["eyebrow"], esc(case["h1"]), esc(case["lede"]))
        ]
        if case.get("steps"):
            sections.append(f"""      <section class="section page-section">
        <div class="wrap">
          <div class="section-head">
            <div>
              <p class="eyebrow">Sample journey</p>
              <h2>{esc(case["steps_title"])}</h2>
            </div>
            <p>Shown on the homepage when this business type is selected. Sample scenario, for illustration.</p>
          </div>
          {journey(case["steps"])}
          {coverage()}
        </div>
      </section>""")
        if case.get("chat"):
            sections.append("""      <section class="section page-section">
        <div class="wrap">
          <article class="copy-card glass">
            <h2>Sample WhatsApp chat</h2>
            <p><strong>Customer.</strong> “Kal 11:30 ka slot theek hai. Location bhi bhej dijiye.”</p>
            <p><strong>Assistant.</strong> “Ji. Aapke visit details aur clinic location yahin share kar rahe hain.”</p>
            <p><em>Slot confirmed → calendar booking → reminder scheduled.</em></p>
            <p class="small">Sample scenario, shown for illustration. Hinglish.</p>
          </article>
        </div>
      </section>""")
        graph = [webpage(case["href"], case["title"], case["desc"])]
        if case.get("audio"):
            tag, audio_title, blurb, src = case["audio"]
            require(page, blurb)
            sections.append(f"""      <section class="section page-section" aria-labelledby="sample-title">
        <div class="wrap">
          <div class="section-head">
            <div>
              <p class="eyebrow">Sample calls</p>
              <h2 id="sample-title">Hear a sample call.</h2>
            </div>
          </div>
          {player(tag, audio_title, blurb, src)}
          <p class="small">Demo audio. The line under the title is the description published on the homepage.</p>
        </div>
      </section>""")
            graph.append({
                "@type": "AudioObject",
                "name": f"{audio_title} sample call",
                "description": blurb,
                "contentUrl": ORIGIN + src.replace(" ", "%20"),
                "encodingFormat": "audio/mpeg",
            })
        if not case.get("steps"):
            sections.append("""      <section class="section page-section">
        <div class="wrap">
          <article class="copy-card glass">
            <h2>Same front desk</h2>
            <p>Calls, WhatsApp, calendar bookings and follow-ups — one continuous front desk, with your team in control.</p>
""" + coverage() + """
            <p><a href="/#samples">Hear a sample call</a> from healthcare, hospitality, education, commerce, payment reminders and hiring.</p>
          </article>
        </div>
      </section>""")
        others = [(c["href"], c["h1"]) for c in use_cases if c["href"] != case["href"]][:4]
        sections.append(related([*others, ("/use-cases.html", "All use cases"), ("/contact.html", "Book a demo")]))
        render(case["href"], case["title"], case["desc"], with_home(case["crumb"], case["href"]), "\n".join(sections), graph)
        pages_meta.append((case["href"], case["title"], case["desc"]))

    path = "/use-cases.html"
    title = "Browse AI Front Desk Use Cases in India | Aigenetic"
    desc = "Clinics, salons, real estate, coaching, hospitality, edtech, e-commerce, payment reminders and recruitment. Sample journeys and calls. Book a demo."
    body = f"""{hero(with_home("Use cases", path), "Who it’s for", "An AI receptionist for appointment-led businesses.", "If your day runs on bookings, Aigenetic answers every call in Hindi, English or Hinglish and books appointments on WhatsApp.")}
      <section class="section page-section">
        <div class="wrap">
          <div class="use-grid">
            {''.join(hub_cards)}
          </div>
        </div>
      </section>"""
    render(path, title, desc, with_home("Use cases", path), body, [webpage(path, title, desc)])
    pages_meta.append((path, title, desc))

    locs = [("/", "https://aigenetic.in/")] + [(href, ORIGIN + href) for href, _, _ in pages_meta]
    locs += [
        ("/privacy-policy.html", ORIGIN + "/privacy-policy.html"),
        ("/terms-of-service.html", ORIGIN + "/terms-of-service.html"),
        ("/refund-policy.html", ORIGIN + "/refund-policy.html"),
    ]
    urlset = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for _, loc in locs:
        urlset.append(f"  <url><loc>{loc}</loc><lastmod>{TODAY}</lastmod></url>")
    urlset.append("</urlset>\n")
    (ROOT / "sitemap.xml").write_text("\n".join(urlset), encoding="utf-8")

    lines = [
        "# Aigenetic",
        "",
        "> Aigenetic is an AI front desk for Indian businesses. It answers calls, replies on WhatsApp, books appointments and follows up, 24×7.",
        "",
        "Aigenetic (OPC) Pvt Ltd provides Front Desk as a Service. The published service handles AI calls, WhatsApp chat and updates, calendar booking and follow-ups. Languages named on the site: Hindi, English and Hinglish. It is fully managed: the team maps the journey, configures and tests, and the client approves before go-live.",
        "",
        "24×7 means always-on AI handling of calls, WhatsApp enquiries, bookings and follow-ups. It does not mean round-the-clock human staffing.",
        "",
        "Calling plans published on the homepage (WhatsApp, calendar booking and follow-ups are scoped to the workflow and added to the quote):",
        "- Flex: ₹2,999 per month, 500 call minutes included, then ₹6 per minute",
        "- Pro: ₹7,999 per month, 1,500 call minutes included, then ₹6 per minute",
        "- Enterprise: volume-based pricing, discussed with the team",
        "",
        "The Terms of Service and Refund Policy also state a setup fee and a different monthly range. Those pages were not rewritten in the SEO pass. Confirm current pricing with Aigenetic before quoting it.",
        "",
        "Contact: connect@aigenetic.in, +91 742849 7033, https://wa.me/917428497033",
        "Address published on the site: Rajiv Gandhi Infotech Park, Pune, India",
        "",
        "## Pages",
    ]
    for href, loc in locs:
        lines.append(f"- {loc}")
    lines += [
        "",
        "## Not confirmed on the public site",
        "- Social profile URLs",
        "- A full street address, PIN code, or Google Business Profile",
        "- Transcripts of the sample calls",
        "- Which calendar, CRM or telephony products are already connected",
        "",
    ]
    (ROOT / "llms.txt").write_text("\n".join(lines), encoding="utf-8")

    patch_legal()
    print("pages", len(pages_meta))


def patch_legal() -> None:
    specs = {
        "privacy-policy.html": (
            "Aigenetic Privacy Policy | Calls and Customer Data",
            "How Aigenetic (OPC) Pvt Ltd collects, uses, stores and protects business, call and customer data, including recordings kept on Indian servers.",
            "Privacy Policy",
        ),
        "terms-of-service.html": (
            "Aigenetic's Terms of Service | AI Front Desk India",
            "Terms for Aigenetic (OPC) Pvt Ltd's AI front-desk and phone assistant services, including plans, client duties, billing and governing law in India.",
            "Terms of Service",
        ),
        "refund-policy.html": (
            "Aigenetic Refund Policy | Setup Fees and Subscriptions",
            "When and how Aigenetic (OPC) Pvt Ltd refunds setup fees, monthly subscriptions and per-minute call charges, and when a refund is not available.",
            "Refund Policy",
        ),
    }
    icon_block = """  <link rel="alternate" hreflang="en-in" href="{url}">
  <link rel="alternate" hreflang="x-default" href="{url}">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="Aigenetic">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{desc}">
  <meta property="og:url" content="{url}">
  <meta property="og:image" content="https://aigenetic.in/assets/og-image.png">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:image:alt" content="Aigenetic. Appointments on autopilot. Talk. Text. Follow up. Slot booking.">
  <meta property="og:locale" content="en_IN">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{title}">
  <meta name="twitter:description" content="{desc}">
  <meta name="twitter:image" content="https://aigenetic.in/assets/og-image.png">
  <meta name="twitter:image:alt" content="Aigenetic. Appointments on autopilot. Talk. Text. Follow up. Slot booking.">
  <link rel="icon" href="/favicon.ico" sizes="32x32">
  <link rel="icon" href="/favicon.svg" type="image/svg+xml">
  <link rel="apple-touch-icon" href="/assets/icons/apple-touch-icon.png">
  <link rel="manifest" href="/site.webmanifest">
"""
    for filename, (title, desc, crumb_name) in specs.items():
        print(f"/{filename} title={len(title)} desc={len(desc)}")
        path = ROOT / filename
        text = path.read_text(encoding="utf-8")
        if "og:image:width" in text:
            print(f"/{filename} already patched")
            continue
        url = f"{ORIGIN}/{filename}"
        text = re.sub(r"<title>.*?</title>", f"<title>{esc(title)}</title>", text, count=1)
        text = re.sub(
            r'<meta name="description" content=".*?">',
            f'<meta name="description" content="{esc(desc)}">',
            text,
            count=1,
        )
        canonical = f'  <link rel="canonical" href="{url}">'
        if canonical not in text:
            raise SystemExit(f"canonical missing in {filename}")
        block = icon_block.format(url=url, title=esc(title), desc=esc(desc))
        text = text.replace(
            canonical + "\n  <link rel=\"icon\" href=\"favicon.svg\" type=\"image/svg+xml\">\n  <link rel=\"icon\" href=\"logo/logo.png\" type=\"image/png\">\n  <link rel=\"apple-touch-icon\" href=\"logo/logoMedium.png\">\n",
            canonical + "\n" + block,
        )
        ld = {
            "@context": "https://schema.org",
            "@graph": [
                breadcrumb_ld([("Home", "/"), (crumb_name, "/" + filename)]),
                webpage("/" + filename, title, desc),
            ],
        }
        snippet = '  <script type="application/ld+json">\n  ' + json.dumps(ld, ensure_ascii=False, indent=2) + "\n  </script>\n"
        text = text.replace("</head>", snippet + "</head>", 1)
        crumb = crumbs([("Home", "/"), (crumb_name, "/" + filename)])
        text = text.replace(
            '<section class="legal-hero wrap">\n        <a class="back-link"',
            '<section class="legal-hero wrap">\n        ' + crumb + '\n        <a class="back-link"',
            1,
        )
        explore = """        <nav class="footer-nav footer-links" aria-label="Explore">
          <a href="/how-it-works.html">How it works</a>
          <a href="/features.html">Features</a>
          <a href="/use-cases.html">Use cases</a>
          <a href="/pricing.html">Pricing</a>
          <a href="/faq.html">FAQ</a>
          <a href="/about.html">About</a>
          <a href="/contact.html">Contact</a>
        </nav>
"""
        text = text.replace(
            '<nav class="footer-nav footer-links" aria-label="Contact and policies">',
            explore + '        <nav class="footer-nav footer-links" aria-label="Contact and policies">',
            1,
        )
        parts = text.split("<footer>", 1)
        if len(parts) == 2:
            parts[1] = parts[1].replace('decoding="async">', 'decoding="async" loading="lazy">', 1)
            text = "<footer>".join(parts)
        path.write_text(text, encoding="utf-8")


if __name__ == "__main__":
    main()
