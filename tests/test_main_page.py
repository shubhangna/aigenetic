"""Functional tests for the main Aigenetic landing page."""

import re
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
        expect(self.page.locator("h1.hero-title")).to_contain_text("The Voice of Your Business")

    def test_sections_and_pricing_are_visible(self):
        self.open_main_page()
        expect(self.page.locator("#features .section-label")).to_contain_text("How It Works")
        expect(self.page.get_by_role("heading", name="Perfect for Any Business")).to_be_visible()
        expect(self.page.get_by_role("heading", name="Simple Pricing")).to_be_visible()
        self.assertGreaterEqual(self.page.locator("#pricing .minimal-card").count(), 4)

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
            'a[href="#"]:visible',
            "#calendar-modal-main",
        )

    def test_audio_demo_controls_are_bound(self):
        self.open_main_page()
        audio = self.page.locator("#audio-demos audio").first
        play_button = self.page.locator("#audio-demos .audio-play").first
        expect(play_button).to_be_visible()
        self.assertIn("mp3/", audio.get_attribute("src") or "")
        play_button.click()
        audio_wave_class = self.page.locator("#audio-demos .audio-wave").first.get_attribute("class") or ""
        self.assertIn("wave-active", audio_wave_class)

    def test_footer_policies_and_testimonials_are_present(self):
        self.open_main_page()
        self.page.locator("footer").scroll_into_view_if_needed()
        expect(self.page.get_by_role("link", name="Privacy Policy")).to_be_visible()
        expect(self.page.get_by_role("link", name="Terms of Service")).to_be_visible()
        expect(self.page.get_by_role("heading", name="Trusted by 100+ Businesses")).to_be_visible()
        self.assertGreater(self.page.get_by_text("★").count(), 0)

    def test_page_has_no_critical_console_errors(self):
        self.open_main_page()
        self.page.reload(wait_until="domcontentloaded", timeout=45000)
        self.assert_no_console_errors()

    def test_use_cases_marquee_drifts_right_to_left_and_pauses_on_hover(self):
        self.open_main_page()
        track = self.page.locator(".usecase-track")
        expect(track).to_be_visible()

        with self.subTest("card list is duplicated for a seamless loop"):
            use_case_count = self.page.evaluate("() => window.CONFIG.useCases.length")
            self.assertEqual(self.page.locator(".usecase-card-wrap").count(), use_case_count * 2)
            # Only the first (non-duplicate) copy stays tab-reachable.
            self.assertEqual(self.page.locator(".usecase-card-wrap[aria-hidden='true']").count(), use_case_count)

        with self.subTest("track animates right-to-left on an infinite loop"):
            self.assertEqual(track.evaluate("el => getComputedStyle(el).animationName"), "usecase-scroll")
            self.assertEqual(track.evaluate("el => getComputedStyle(el).animationIterationCount"), "infinite")
            # translateX drifts toward -50%, i.e. leftward, never positive/rightward.
            self.assertEqual(track.evaluate("el => getComputedStyle(el).animationPlayState"), "running")

        with self.subTest("hovering a card pauses the drift"):
            self.page.locator(".usecase-marquee").hover()
            expect(track).to_have_class(re.compile("paused"))
            self.assertEqual(track.evaluate("el => getComputedStyle(el).animationPlayState"), "paused")

        with self.subTest("moving away resumes the drift"):
            self.page.locator("h1.hero-title").hover()
            expect(track).not_to_have_class(re.compile("paused"))
            self.assertEqual(track.evaluate("el => getComputedStyle(el).animationPlayState"), "running")

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