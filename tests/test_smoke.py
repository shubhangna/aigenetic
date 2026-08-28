"""High-level smoke tests for the Aigenetic site.

Not a substitute for the per-page suites (test_main_page.py,
test_healthcare.py, test_realestate.py) -- those cover each page in depth.
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


class TestSmoke(WebsiteTestCase):
    def test_main_page_is_up(self):
        response = self.open_page(ready_selector="h1.hero-title")
        self.assert_successful_response(response)
        self.assertIn("Aigenetic", self.page.title())
        expect(self.page.locator("h1.hero-title")).to_contain_text("The Voice of Your Business")
        self.assert_contact_links(
            'a[href^="tel:"]:visible',
            'a[href^="https://wa.me/"]:visible',
            'a[href^="mailto:"]:visible',
        )

    def test_healthcare_page_is_up(self):
        response = self.open_page("/?mode=healthcare", ready_selector="h1")
        self.assert_successful_response(response)
        self.assertIn("clinic", self.page.title().lower())
        expect(self.page.locator("h1")).to_contain_text("clinic")
        expect(self.page.locator("a[data-email-link]:visible").first).to_be_visible()

    def test_realestate_page_is_up(self):
        response = self.open_page("/?mode=realestate", ready_selector="h1")
        self.assert_successful_response(response)
        self.assertIn("real estate", self.page.title().lower())
        expect(self.page.locator("h1")).to_contain_text("listings")
        expect(self.page.locator("a[data-email-link]:visible").first).to_be_visible()

    def test_education_page_is_up(self):
        response = self.open_page("/?mode=education", ready_selector="h1")
        self.assert_successful_response(response)
        self.assertIn("coaching", self.page.title().lower())
        expect(self.page.locator("h1")).to_contain_text("institute")
        expect(self.page.locator("a[data-email-link]:visible").first).to_be_visible()

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
