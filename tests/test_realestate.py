"""Functional tests for the Aigenetic real-estate developer landing page.

Mirrors tests/test_healthcare.py's structure: one page load, everything
checked via subTests end-to-end rather than presence-only assertions
scattered across many separate tests.
"""

import unittest

from playwright.sync_api import expect

from utilities import WebsiteTestCase


class TestRealEstatePage(WebsiteTestCase):
    def open_realestate_page(self):
        # realestate.html now redirects to /?mode=realestate (see index.html's
        # vertical mode router); open the consolidated URL directly.
        return self.open_page("/?mode=realestate", ready_selector="h1")

    def test_realestate_html_redirects_to_consolidated_url(self):
        self.page.goto(self.page_url("realestate.html"), wait_until="load", timeout=45000)
        self.page.locator("h1").wait_for(state="visible", timeout=15000)
        self.assertIn("mode=realestate", self.page.url)
        expect(self.page.locator("h1")).to_contain_text("listings")

    def test_realestate_page(self):
        page = self.page

        with self.subTest("page loads with developer positioning"):
            response = self.open_realestate_page()
            self.assert_successful_response(response)
            self.assertIn("real estate", page.title().lower())
            expect(page.locator("h1")).to_contain_text("listings")
            expect(page.get_by_text("31+ Indian languages")).to_be_visible()

        company = page.evaluate("() => window.CONFIG.company")

        with self.subTest("email CTA is addressed to the configured inbox"):
            email = page.locator("a[data-email-link]:visible").first
            expect(email).to_be_visible()
            self.assertEqual(email.get_attribute("href"), f"mailto:{company['email']}")

        with self.subTest("live voice call button reports coming soon"):
            live_call_button = page.locator("[data-live-voice-call]")
            expect(live_call_button).to_be_visible()
            live_call_button.click()
            expect(live_call_button).to_contain_text("coming soon")

        with self.subTest("content, pricing and footer policy links are present"):
            expect(page.locator("#handles")).to_contain_text("Books the site visit")
            expect(page.locator("#limits")).to_contain_text(
                "No price negotiated on the call"
            )
            expect(page.locator("#pricing")).to_contain_text("Single project")
            page.locator("footer").scroll_into_view_if_needed()
            expect(page.get_by_role("link", name="Refund Policy")).to_be_visible()

        with self.subTest("no critical console errors after a fresh load"):
            page.reload(wait_until="domcontentloaded", timeout=45000)
            self.assert_no_console_errors()

        with self.subTest("every demo entry point opens the real booking calendar"):
            demo_links = page.locator("[data-open-calendar]:visible")
            self.assertGreaterEqual(demo_links.count(), 4)
            for index in range(demo_links.count()):
                trigger = demo_links.nth(index)
                trigger.click()

                modal = page.locator("#calendar-modal")
                expect(modal).to_be_visible()
                booking_iframe = modal.locator("iframe")
                expect(booking_iframe).to_be_visible()
                self.assertTrue(
                    (booking_iframe.get_attribute("src") or "").startswith(
                        "https://calendar.google.com/calendar/appointments/schedules/"
                    ),
                    "Book Demo should open the real Google Calendar booking page",
                )

                close_button = modal.locator("button").first
                close_button.click()
                expect(modal).not_to_be_visible()

        with self.subTest("phone CTA calls the configured number without breaking the page"):
            phone = page.locator("a[data-phone-link]:visible").first
            expect(phone).to_be_visible()
            expected_tel = f"tel:{company['phoneDial']}"
            self.assertEqual(phone.get_attribute("href"), expected_tel)
            phone.click()
            # tel: is an unsupported scheme for the browser tab itself, so the
            # click must not navigate the SPA away or throw.
            self.assertIn("mode=realestate", page.url)


class TestMainPageLinksToRealEstate(WebsiteTestCase):
    def test_use_case_card_links_to_realestate_with_its_own_label(self):
        self.open_page(ready_selector="h1.hero-title")
        # The Use Cases marquee (UseCaseMarquee in index.html) renders the card
        # list twice back-to-back for a seamless scroll loop, so two matching
        # anchors exist -- .first is the real, tab-reachable one; its duplicate
        # is aria-hidden with tabindex="-1".
        card = self.page.locator('a[href="/?mode=realestate"]').first
        expect(card).to_be_visible()
        expect(card).to_contain_text("Explore for developers")
        # Regression guard: the Real Estate card must not show the Clinics
        # card's hardcoded label (the bug fixed alongside this page).
        expect(card).not_to_contain_text("Explore for clinics")


if __name__ == "__main__":
    unittest.main(verbosity=2)
