"""Functional tests for the main Aigenetic landing page."""

import socket
import unittest

from playwright.sync_api import expect

from utilities import EXPECTED_GITHUB_IPS, WebsiteTestCase, assert_calendar_modal, resolve_domain_ips


class TestMainPage(WebsiteTestCase):
    def open_main_page(self):
        return self.open_page(ready_selector="h1.hero-title")

    def test_page_loads_and_contains_branding(self):
        response = self.open_main_page()
        self.assert_successful_response(response)
        self.assertIn("Aigenetic", self.page.title())
        expect(self.page.locator("h1.hero-title")).to_contain_text("Appointments on autopilot.")
        expect(self.page.get_by_text("FRONT DESK AS A SERVICE", exact=True)).to_be_visible()
        expect(self.page.get_by_text("Try the autopilot").first).to_be_visible()

    def test_sections_and_pricing_are_visible(self):
        self.open_main_page()
        expect(self.page.locator("#system")).to_contain_text("From first contact")
        expect(self.page.locator("#samples")).to_contain_text("Hear a sample call.")
        expect(self.page.locator("#pricing")).to_contain_text("A clear starting point.")
        expect(self.page.locator("#pricing")).to_contain_text("₹2,999")
        expect(self.page.locator("#pricing")).to_contain_text("₹7,999")
        self.assertEqual(self.page.locator("#pricing .price").count(), 3)

    def test_contact_ctas_have_configured_links(self):
        self.open_main_page()
        self.assert_contact_links(
            'a[href^="tel:"]:visible',
            'a[href^="https://wa.me/"]:visible',
            'a[href^="mailto:"]:visible',
        )

    def test_book_demo_modal_opens_and_closes(self):
        self.open_main_page()
        assert_calendar_modal(
            self,
            "[data-open-calendar]:visible",
            "#calendar-modal-main",
        )

    def test_audio_demo_controls_are_bound(self):
        self.open_main_page()
        player = self.page.locator("[data-player]").first
        audio = player.locator("audio")
        play_button = player.locator("[data-play]")
        expect(play_button).to_be_visible()
        self.assertIn("audio/samples/", audio.get_attribute("src") or "")
        expect(player).to_contain_text("Demo audio")
        play_button.click()
        expect(play_button).to_have_attribute("aria-pressed", "true")
        self.assertFalse(audio.evaluate("el => el.paused"))

    def test_footer_policies_and_testimonials_are_present(self):
        self.open_main_page()
        self.page.locator("footer").scroll_into_view_if_needed()
        expect(self.page.get_by_role("link", name="Privacy Policy")).to_be_visible()
        expect(self.page.get_by_role("link", name="Terms of Service")).to_be_visible()
        expect(self.page.get_by_role("link", name="Refund Policy")).to_be_visible()

    def test_page_has_no_critical_console_errors(self):
        self.open_main_page()
        self.page.reload(wait_until="domcontentloaded", timeout=45000)
        self.assert_no_console_errors()

    def test_locked_hero_copy(self):
        self.open_main_page()
        tagline = self.page.locator(".autopilot-tagline")
        expect(tagline).to_have_attribute("aria-label", "Talk. Text. Follow up. Slot booking.")
        expect(self.page.locator(".subhead")).to_contain_text(
            "Aigenetic answers your calls, replies on WhatsApp, books appointments and follows up, 24×7."
        )

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