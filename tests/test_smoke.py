"""Smoke tests for the Aigenetic site.

The site is a single landing page plus three policy pages; the old vertical
pages (healthcare/realestate/education) were retired to ___Archive/. This file
covers all of it except mobile navigation (see test_mobile_nav.py):

* site-level: pages up, retired pages gone, sitemap, unpublished files hidden;
* main page: hero, sections, pricing, contact CTAs, demo modal, audio players;
* policy pages: shared header/footer, section index, switcher, phone layout;
* infra: GitHub Pages DNS/IP checks, so the whole "is production reachable"
  story lives in one place.
"""

import socket
import unittest
import xml.etree.ElementTree as ET
from urllib.parse import urlsplit

from playwright.sync_api import expect

from utilities import BASE_URL, EXPECTED_GITHUB_IPS, PROJECT_ROOT, WebsiteTestCase, resolve_domain_ips

RETIRED_PAGES = ("healthcare.html", "realestate.html", "education.html", "summary.html")

POLICY_PAGES = {
    "privacy-policy.html": "Privacy Policy",
    "terms-of-service.html": "Terms of Service",
    "refund-policy.html": "Refund Policy",
}

# One file from each path _config.yml excludes from the GitHub Pages build.
# They exist in the repo, so a local `python -m http.server` still serves
# them; only the real deploy can prove they're hidden.
UNPUBLISHED_PATHS = (
    "CODED-Thers/messages.html",
    "newSite/templates/vertical-page.template.html",
    "tests/issues.md",
    "localServer.bat",
    "testsNpush.bat",
)

SITEMAP_NS = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}


class TestSmoke(WebsiteTestCase):
    # --- Site-level -------------------------------------------------------

    def test_retired_pages_are_not_served(self):
        for path in RETIRED_PAGES:
            with self.subTest(page=path):
                response = self.page.goto(self.page_url(path), wait_until="domcontentloaded", timeout=45000)
                self.assertIsNotNone(response)
                self.assertEqual(response.status, 404, f"{path} should be retired but is still served")

    def test_sitemap_lists_exactly_the_live_pages(self):
        root = ET.parse(PROJECT_ROOT / "sitemap.xml").getroot()
        locs = [loc.text.strip() for loc in root.findall("sm:url/sm:loc", SITEMAP_NS)]
        paths = []
        for loc in locs:
            parts = urlsplit(loc)
            self.assertEqual(parts.netloc, "aigenetic.in", f"{loc} is not on the production domain")
            self.assertFalse(parts.query or parts.fragment, f"{loc}: sitemaps should not list ?query or #anchor URLs")
            paths.append(parts.path.lstrip("/"))

        # Every root-level HTML page except the 404 page should be listed, and nothing else.
        expected = {"" if p.name == "index.html" else p.name for p in PROJECT_ROOT.glob("*.html") if p.name != "404.html"}
        self.assertEqual(sorted(paths), sorted(expected))

        for path in paths:
            with self.subTest(page=path or "/"):
                response = self.page.request.get(self.page_url(path))
                self.assertEqual(response.status, 200, f"sitemap entry /{path} does not load")

    @unittest.skipIf(
        urlsplit(BASE_URL).hostname in {"localhost", "127.0.0.1"},
        "Jekyll's exclude list only applies to the GitHub Pages build; run with --site remote",
    )
    def test_unpublished_repo_files_are_not_served(self):
        for path in UNPUBLISHED_PATHS:
            with self.subTest(path=path):
                self.assertTrue((PROJECT_ROOT / path).exists(), f"{path} no longer exists; update UNPUBLISHED_PATHS")
                response = self.page.request.get(self.page_url(path))
                self.assertEqual(response.status, 404, f"{path} is still published on {BASE_URL}")

    # --- Main page --------------------------------------------------------

    def test_main_page(self):
        """Every homepage check, in one page load.

        Read-only checks run first, then the console check, then the
        interactions that change page state (audio playback, the booking
        modal) last, so they can't affect anything before them. Each check is
        its own subTest, so one failure doesn't hide the rest.
        """
        page = self.page
        response = self.open_page(ready_selector="h1.hero-title")
        # If the page itself didn't load, nothing below is meaningful: fail hard.
        self.assert_successful_response(response)
        self.assertIn("Aigenetic", page.title())

        with self.subTest("hero and branding"):
            expect(page.locator("h1.hero-title")).to_contain_text("Appointments on autopilot.")
            expect(page.get_by_text("FRONT DESK AS A SERVICE", exact=True)).to_be_visible()
            expect(page.get_by_text("Try the autopilot").first).to_be_visible()

        with self.subTest("locked hero copy"):
            expect(page.locator(".autopilot-tagline")).to_have_attribute(
                "aria-label", "Talk. Text. Follow up. Slot booking."
            )
            expect(page.locator(".subhead")).to_contain_text(
                "Aigenetic answers your calls, replies on WhatsApp, books appointments and follows up, 24×7."
            )

        with self.subTest("contact CTAs have configured links"):
            self.assert_contact_links(
                'a[href^="tel:"]:visible',
                'a[href^="https://wa.me/"]:visible',
                'a[href^="mailto:"]:visible',
            )

        with self.subTest("header contact buttons hide the number"):
            contact = page.locator("header .header-contact")
            expect(contact.locator('a[href="tel:+917428497033"]')).to_be_visible()
            expect(contact.locator('a[href="https://wa.me/917428497033"]')).to_be_visible()
            expect(contact.locator('a[href="mailto:connect@aigenetic.in"]')).to_be_visible()
            self.assertNotIn("742849", page.locator("body").inner_text())

        with self.subTest("sections and pricing"):
            expect(page.locator("#system")).to_contain_text("From first contact")
            expect(page.locator("#samples")).to_contain_text("Hear a sample call.")
            pricing = page.locator("#pricing")
            expect(pricing).to_contain_text("A clear starting point.")
            expect(pricing).to_contain_text("₹2,999")
            expect(pricing).to_contain_text("₹7,999")
            self.assertEqual(pricing.locator(".price").count(), 3)

        with self.subTest("footer policy links"):
            page.locator("footer").scroll_into_view_if_needed()
            for name in POLICY_PAGES.values():
                expect(page.get_by_role("link", name=name)).to_be_visible()

        with self.subTest("no console errors on load"):
            page.wait_for_load_state("load")
            self.assert_no_console_errors()

        with self.subTest("audio demo plays"):
            player = page.locator("[data-player]").first
            audio = player.locator("audio")
            play_button = player.locator("[data-play]")
            expect(play_button).to_be_visible()
            src = audio.get_attribute("src") or ""
            self.assertTrue(src.startswith("mp3/"), src)
            expect(player).to_contain_text("Demo audio")
            play_button.click()
            expect(play_button).to_have_attribute("aria-pressed", "true")
            self.assertFalse(audio.evaluate("el => el.paused"))

        with self.subTest("book-demo modal opens and closes"):
            schedule = (
                "https://calendar.google.com/calendar/appointments/schedules/"
                "AcZssZ2-oLNDtD7wJRTQhnQ4WwsQE_f0x_wePzs82A2ihrxI7WZJb-XRed0ak2ltUfH1zohb-16awYx4?gv=true"
            )
            modal = page.locator("#calendar-modal-main")
            iframe = modal.locator("iframe")
            self.assertEqual(iframe.get_attribute("src"), schedule)
            page.locator("[data-open-calendar]:visible").first.click()
            expect(modal).to_be_visible()
            expect(iframe).to_be_visible()
            page.frame_locator("#calendar-modal-main iframe").locator("body").wait_for(
                state="attached", timeout=20000
            )
            modal.locator("button").first.click()
            expect(modal).not_to_be_visible()

    # --- Policy pages -----------------------------------------------------

    def test_policy_pages(self):
        """Every policy-page check, in one load per page.

        Desktop checks run first, then the console check, then the page is
        narrowed to 320px for the phone layout and menu (no reload needed: the
        layout is pure CSS media queries). The viewport is restored before
        the next page.
        """
        page = self.page
        desktop_viewport = page.viewport_size
        for path, heading in POLICY_PAGES.items():
            with self.subTest(page=path):
                page.set_viewport_size(desktop_viewport)
                self.console_errors = []
                response = self.open_page(path, ready_selector="h1")
                # If this page didn't load, skip its checks and move to the next page.
                self.assert_successful_response(response)
                self.assertIn("Aigenetic", page.title())

                with self.subTest("shares homepage header and footer"):
                    expect(page.locator("h1")).to_have_text(heading)
                    brand = page.locator(".top .brand")
                    expect(brand).to_be_visible()
                    self.assertEqual(brand.get_attribute("href"), "/")
                    expect(page.locator("#aurora")).to_be_attached()
                    footer = page.locator("footer")
                    for name in POLICY_PAGES.values():
                        expect(footer.get_by_role("link", name=name)).to_be_visible()
                    expect(footer.locator('a[aria-current="page"]')).to_have_text(heading)

                with self.subTest("section index links resolve"):
                    hrefs = page.locator(".toc a").evaluate_all("els => els.map(a => a.getAttribute('href'))")
                    self.assertGreater(len(hrefs), 0)
                    for href in hrefs:
                        self.assertEqual(page.locator(f"section{href}").count(), 1, f"{href} has no section")

                with self.subTest("policy switch marks current page"):
                    current = page.locator('.policy-switch a[aria-current="page"]')
                    expect(current).to_have_count(1)
                    self.assertEqual(current.get_attribute("href"), path)

                with self.subTest("no console errors"):
                    page.wait_for_load_state("networkidle")
                    self.assert_no_console_errors()

                with self.subTest("phone width layout and menu"):
                    page.set_viewport_size({"width": 320, "height": 800})
                    scroll_width = page.evaluate("document.documentElement.scrollWidth")
                    client_width = page.evaluate("document.documentElement.clientWidth")
                    self.assertLessEqual(scroll_width, client_width + 1, f"overflow at 320px on {path}")
                    panel = page.locator("#mobile-nav-panel")
                    expect(panel).to_be_hidden()
                    page.locator(".nav-toggle").click()
                    expect(panel).to_be_visible()
                    expect(panel.get_by_text("Pricing", exact=True)).to_be_visible()

    # --- Infra (GitHub Pages) ---------------------------------------------

    def test_github_domain_resolves_to_expected_ips(self):
        try:
            resolved_ips = resolve_domain_ips("aigenetic.in")
        except socket.gaierror as error:
            self.fail(f"DNS resolution failed for aigenetic.in: {error}")
        self.assertEqual(resolved_ips, EXPECTED_GITHUB_IPS)

    def test_github_ips_are_accessible(self):
        for ip_address in EXPECTED_GITHUB_IPS:
            with self.subTest(ip=ip_address):
                try:
                    connection = socket.create_connection((ip_address, 443), timeout=5)
                    connection.close()
                except (socket.timeout, socket.error) as error:
                    self.fail(f"IP {ip_address} is not accessible: {error}")


if __name__ == "__main__":
    unittest.main(verbosity=2)
