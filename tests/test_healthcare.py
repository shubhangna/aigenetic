"""Functional tests for the Aigenetic healthcare landing page.

All checks run inside a single test case (one page load) so behavior is
verified end-to-end via subTests rather than presence-only assertions
scattered across many separate tests.
"""

import unittest

from playwright.sync_api import expect

from utilities import WebsiteTestCase


class TestHealthcarePage(WebsiteTestCase):
    def open_healthcare_page(self):
        # healthcare.html now redirects to /?mode=healthcare (see index.html's
        # vertical mode router); open the consolidated URL directly.
        return self.open_page("/?mode=healthcare", ready_selector="h1")

    def test_healthcare_html_redirects_to_consolidated_url(self):
        self.page.goto(self.page_url("healthcare.html"), wait_until="load", timeout=45000)
        self.page.locator("h1").wait_for(state="visible", timeout=15000)
        self.assertIn("mode=healthcare", self.page.url)
        expect(self.page.locator("h1")).to_contain_text("clinic")

    def test_healthcare_page(self):
        page = self.page

        with self.subTest("page loads with clinic positioning"):
            response = self.open_healthcare_page()
            self.assert_successful_response(response)
            self.assertIn("clinic", page.title().lower())
            expect(page.locator("h1")).to_contain_text("clinic")
            expect(page.get_by_text("31+ Indian languages")).to_be_visible()

        company = page.evaluate("() => window.CONFIG.company")

        with self.subTest("email CTA is addressed to the configured inbox"):
            email = page.locator("a[data-email-link]:visible").first
            expect(email).to_be_visible()
            self.assertEqual(email.get_attribute("href"), f"mailto:{company['email']}")

        with self.subTest("audio player has a real source and toggles playback"):
            player = page.locator("[data-call-player]")
            audio = player.locator("[data-audio-player]")
            expect(player.locator("[data-play-audio]")).to_be_visible()
            self.assertIn("mp3/", audio.get_attribute("src") or "")
            player.locator("[data-play-audio]").click()
            self.assertIn("playing", player.get_attribute("class") or "")

        with self.subTest("live voice call button reports coming soon"):
            live_call_button = page.locator("[data-live-voice-call]")
            expect(live_call_button).to_be_visible()
            live_call_button.click()
            expect(live_call_button).to_contain_text("coming soon")

        with self.subTest("content, pricing and footer policy links are present"):
            expect(page.locator("#handles")).to_contain_text("Books the slot")
            expect(page.locator("#limits")).to_contain_text("No diagnosis, no advice")
            expect(page.locator("#pricing")).to_contain_text("Solo practice")
            page.locator("footer").scroll_into_view_if_needed()
            expect(page.get_by_role("link", name="Refund Policy")).to_be_visible()

        with self.subTest("whatsapp CTA opens a chat to the configured number"):
            # WhatsApp links have no JS handler and no target="_blank" -- clicking
            # one really navigates the tab away, so the page is restored via
            # open_healthcare_page() straight after regardless of what runs next.
            whatsapp = page.locator("a[data-whatsapp-link]:visible").first
            expect(whatsapp).to_be_visible()
            expected_wa_url = f"https://wa.me/{company['whatsappNumber']}"
            self.assertEqual(whatsapp.get_attribute("href"), expected_wa_url)
            page.route("https://wa.me/**", lambda route: route.abort())
            try:
                with page.expect_request("https://wa.me/**", timeout=5000) as request_info:
                    whatsapp.click()
                self.assertEqual(request_info.value.url, expected_wa_url)
            finally:
                page.unroute("https://wa.me/**")
                self.open_healthcare_page()

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
            self.assertIn("mode=healthcare", page.url)


if __name__ == "__main__":
    unittest.main(verbosity=2)
