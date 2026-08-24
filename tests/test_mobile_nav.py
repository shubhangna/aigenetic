"""Mobile-viewport nav checks, shared across index.html and healthcare.html.

Both pages replace their desktop nav links with a hamburger (`.nav-toggle`)
below their respective mobile breakpoints, opening a panel with the same
links plus the call/book-demo CTAs. This verifies that pattern actually
works at a real phone width, rather than just that the desktop nav renders.
"""

import unittest

from playwright.sync_api import expect

from utilities import WebsiteTestCase

MOBILE_VIEWPORT = {"width": 390, "height": 844}


class MobileNavTestCase(WebsiteTestCase):
    """Same setup as WebsiteTestCase, but every page opens at phone width."""

    def setUp(self):
        self.page = self.context.new_page()
        self.page.set_viewport_size(MOBILE_VIEWPORT)
        self.console_errors = []
        self.page.on("console", self._collect_console_error)

    def assert_no_horizontal_overflow(self):
        scroll_width = self.page.evaluate("document.documentElement.scrollWidth")
        client_width = self.page.evaluate("document.documentElement.clientWidth")
        self.assertLessEqual(
            scroll_width,
            client_width + 1,  # 1px tolerance for sub-pixel rounding
            f"Horizontal scroll at {MOBILE_VIEWPORT['width']}px: "
            f"scrollWidth={scroll_width} > clientWidth={client_width}",
        )


class TestMainPageMobileNav(MobileNavTestCase):
    def test_hamburger_opens_and_closes_on_index(self):
        self.open_page(ready_selector="h1.hero-title")
        self.assert_no_horizontal_overflow()

        toggle = self.page.locator(".nav-toggle")
        expect(toggle).to_be_visible()

        panel = self.page.locator("#mobile-nav-panel")
        expect(panel).to_be_hidden()

        toggle.click()
        expect(panel).to_be_visible()
        expect(panel.get_by_text("Pricing", exact=True)).to_be_visible()

        panel.get_by_text("Pricing", exact=True).click()
        expect(panel).to_be_hidden()
        self.assertIn("#pricing", self.page.url)


class TestHealthcareMobileNav(MobileNavTestCase):
    def test_hamburger_opens_and_closes_on_healthcare(self):
        self.open_page("healthcare.html", ready_selector="h1")
        self.assert_no_horizontal_overflow()

        toggle = self.page.locator("#nav-toggle")
        expect(toggle).to_be_visible()

        panel = self.page.locator("#nav-panel")
        expect(panel).not_to_have_class("open")

        toggle.click()
        expect(panel).to_have_class("nav-panel open")
        expect(panel.get_by_text("Pricing", exact=True)).to_be_visible()

        panel.get_by_text("Pricing", exact=True).click()
        expect(panel).not_to_have_class("open")


class TestRealEstateMobileNav(MobileNavTestCase):
    def test_hamburger_opens_and_closes_on_realestate(self):
        self.open_page("realestate.html", ready_selector="h1")
        self.assert_no_horizontal_overflow()

        toggle = self.page.locator("#nav-toggle")
        expect(toggle).to_be_visible()

        panel = self.page.locator("#nav-panel")
        expect(panel).not_to_have_class("open")

        toggle.click()
        expect(panel).to_have_class("nav-panel open")
        expect(panel.get_by_text("Pricing", exact=True)).to_be_visible()

        panel.get_by_text("Pricing", exact=True).click()
        expect(panel).not_to_have_class("open")


if __name__ == "__main__":
    unittest.main(verbosity=2)
