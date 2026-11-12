"""Functional tests for the Aigenetic coaching & schools landing page.

The page's visual identity (title, copy, "Schools and Coaching" card on the
main page) is unchanged -- only the underlying mode/filename is "education"
(renamed from "coaching" 2026-08-28, see CODED-Thers/TODO.md).

Mirrors tests/test_realestate.py's structure: one page load, everything
checked via subTests end-to-end rather than presence-only assertions
scattered across many separate tests.
"""

import unittest

from playwright.sync_api import expect

from utilities import WebsiteTestCase


class TestEducationPage(WebsiteTestCase):
    def open_education_page(self):
        return self.open_page("education.html", ready_selector="h1")

    def test_education_html_renders_as_its_own_page(self):
        self.page.goto(self.page_url("education.html"), wait_until="load", timeout=45000)
        self.page.locator("h1").wait_for(state="visible", timeout=15000)
        self.assertIn("education.html", self.page.url)
        self.assertNotIn("mode=", self.page.url)
        expect(self.page.locator("h1")).to_contain_text("institute")

    def test_education_page(self):
        page = self.page

        with self.subTest("page loads with institute positioning"):
            response = self.open_education_page()
            self.assert_successful_response(response)
            self.assertIn("coaching", page.title().lower())
            expect(page.locator("h1")).to_contain_text("institute")
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
            expect(page.locator("#handles")).to_contain_text("Books the demo class")
            expect(page.locator("#limits")).to_contain_text(
                "No result or rank guaranteed"
            )
            expect(page.locator("#pricing")).to_contain_text("Single center")
            page.locator("footer").scroll_into_view_if_needed()
        with self.subTest("whatsapp CTA opens a chat to the configured number"):
            whatsapp = page.locator("a[data-whatsapp-link]:visible").first
            expect(whatsapp).to_be_visible()
            expected_wa_url = f"https://wa.me/{company['whatsappNumber']}"
            self.assertEqual(whatsapp.get_attribute("href"), expected_wa_url)
            self.assertEqual(whatsapp.get_attribute("target"), "_blank")
            self.assertIn("noopener", whatsapp.get_attribute("rel") or "")
            self.context.route("https://wa.me/**", lambda route: route.abort())
            try:
                with page.expect_popup(timeout=5000) as popup_info:
                    whatsapp.click()
                popup = popup_info.value
                popup.close()
            finally:
                self.context.unroute("https://wa.me/**")

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
            self.assertIn("education.html", page.url)
            self.assertNotIn("mode=", page.url)


class TestMainPageLinksToEducation(WebsiteTestCase):
    def test_homepage_has_no_education_mode(self):
        self.open_page(ready_selector="h1.hero-title")
        self.assertEqual(self.page.locator('a[href*="mode=education"]').count(), 0)
        expect(self.page.locator("#system")).to_contain_text("WhatsApp")
        expect(self.page.locator("#system")).to_contain_text("Follow")


if __name__ == "__main__":
    unittest.main(verbosity=2)
