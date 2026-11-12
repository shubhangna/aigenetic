"""High-level smoke tests for the Aigenetic site.

Not a substitute for the in-depth suites (test_main_page.py,
test_mobile_nav.py). The site is now a single page; the old vertical pages
(healthcare/realestate/education) were retired to ___Archive/.
This file is a single, fast pass that answers one question per site: "is it
up and roughly right?" (200 response, correct title/H1, key CTA present).
It also carries the infra-level GitHub Pages DNS/IP checks, so the whole
"is production reachable" story lives in one place.

Run this first when triaging a deploy; run the full suites for anything
deeper.
"""

import socket
import unittest

from playwright.sync_api import expect

from utilities import EXPECTED_GITHUB_IPS, WebsiteTestCase, resolve_domain_ips

RETIRED_PAGES = ("healthcare.html", "realestate.html", "education.html", "summary.html")


class TestSmoke(WebsiteTestCase):
    def test_main_page_is_up(self):
        response = self.open_page(ready_selector="h1.hero-title")
        self.assert_successful_response(response)
        self.assertIn("Aigenetic", self.page.title())
        expect(self.page.locator("h1.hero-title")).to_contain_text("Appointments on autopilot.")
        self.assert_contact_links(
            'a[href^="tel:"]:visible',
            'a[href^="https://wa.me/"]:visible',
            'a[href^="mailto:"]:visible',
        )

    def test_policy_pages_are_up(self):
        for path in ("privacy-policy.html", "terms-of-service.html", "refund-policy.html"):
            with self.subTest(page=path):
                response = self.open_page(path, ready_selector="body")
                self.assert_successful_response(response)
                self.assertIn("Aigenetic", self.page.title())

    def test_retired_pages_are_not_served(self):
        for path in RETIRED_PAGES:
            with self.subTest(page=path):
                response = self.page.goto(self.page_url(path), wait_until="domcontentloaded", timeout=45000)
                self.assertIsNotNone(response)
                self.assertEqual(response.status, 404, f"{path} should be retired but is still served")

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
