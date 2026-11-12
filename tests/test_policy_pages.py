"""Checks for the three policy pages (privacy, terms, refund).

They share the homepage's header, footer and aurora theme (home.css + legal.css
+ home.js), so these tests guard that shared chrome, the in-page section index,
and phone-width layout, on top of test_smoke.py's "is it up" check.
"""

import unittest

from playwright.sync_api import expect

from utilities import WebsiteTestCase

POLICY_PAGES = {
    "privacy-policy.html": "Privacy Policy",
    "terms-of-service.html": "Terms of Service",
    "refund-policy.html": "Refund Policy",
}


class TestPolicyPages(WebsiteTestCase):
    def test_pages_share_homepage_header_and_footer(self):
        for path, heading in POLICY_PAGES.items():
            with self.subTest(page=path):
                response = self.open_page(path, ready_selector="h1")
                self.assert_successful_response(response)
                self.assertIn("Aigenetic", self.page.title())
                expect(self.page.locator("h1")).to_have_text(heading)
                expect(self.page.locator(".top .brand")).to_be_visible()
                expect(self.page.locator("#aurora")).to_be_attached()
                footer = self.page.locator("footer")
                for name in POLICY_PAGES.values():
                    expect(footer.get_by_role("link", name=name)).to_be_visible()
                expect(footer.locator('a[aria-current="page"]')).to_have_text(heading)
                self.assertEqual(self.page.locator(".top .brand").get_attribute("href"), "/")

    def test_section_index_links_resolve(self):
        for path in POLICY_PAGES:
            with self.subTest(page=path):
                self.open_page(path, ready_selector="h1")
                hrefs = self.page.locator(".toc a").evaluate_all("els => els.map(a => a.getAttribute('href'))")
                self.assertGreater(len(hrefs), 0)
                for href in hrefs:
                    self.assertEqual(self.page.locator(f"section{href}").count(), 1, f"{href} has no section")

    def test_policy_switch_marks_current_page(self):
        for path in POLICY_PAGES:
            with self.subTest(page=path):
                self.open_page(path, ready_selector="h1")
                current = self.page.locator('.policy-switch a[aria-current="page"]')
                expect(current).to_have_count(1)
                self.assertEqual(current.get_attribute("href"), path)

    def test_pages_have_no_console_errors(self):
        for path in POLICY_PAGES:
            with self.subTest(page=path):
                self.console_errors = []
                self.open_page(path, ready_selector="h1")
                self.page.wait_for_load_state("networkidle")
                self.assert_no_console_errors()

    def test_phone_width_layout_and_menu(self):
        for path in POLICY_PAGES:
            with self.subTest(page=path):
                self.page.set_viewport_size({"width": 320, "height": 800})
                self.open_page(path, ready_selector="h1")
                scroll_width = self.page.evaluate("document.documentElement.scrollWidth")
                client_width = self.page.evaluate("document.documentElement.clientWidth")
                self.assertLessEqual(scroll_width, client_width + 1, f"overflow at 320px on {path}")
                panel = self.page.locator("#mobile-nav-panel")
                expect(panel).to_be_hidden()
                self.page.locator(".nav-toggle").click()
                expect(panel).to_be_visible()
                expect(panel.get_by_text("Pricing", exact=True)).to_be_visible()


if __name__ == "__main__":
    unittest.main(verbosity=2)
