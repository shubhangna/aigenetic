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
            self.assertIn("mode=healthcare", page.url)

    def test_healthcare_page_extended_content(self):
        """Content coverage beyond test_healthcare_page's happy path, folded
        into a single page load as subTests (see module docstring) rather
        than as 14 separate test methods with 14 separate navigations.

        One originally proposed test (floating FABs) was dropped: this page
        has no floating action buttons anywhere in its markup.
        """
        page = self.page
        self.page.set_viewport_size({"width": 1280, "height": 900})
        self.open_healthcare_page()

        with self.subTest("hero clinic counter is visible above the fold"):
            counter = page.get_by_text("Answering for 240+ clinics right now")
            expect(counter).to_be_visible()
            expect(counter).to_contain_text("240+")
            expect(counter).to_contain_text("clinics")
            self.assertLess(counter.bounding_box()["y"], page.viewport_size["height"])

        with self.subTest("call log demo section shows the full mock conversation"):
            demo = page.locator(".callsheet-sec .sheet")
            expect(demo).to_contain_text("+91 98••• ••412")
            expect(demo).to_contain_text("हिन्दी / English")
            expect(demo).to_contain_text("1:12")
            expect(demo).to_contain_text("Handled by assistant")
            turns = demo.locator(".turn")
            turn_text = " ".join(turns.nth(i).inner_text().lower() for i in range(turns.count()))
            self.assertIn("caller", turn_text)
            self.assertIn("aigenetic", turn_text)
            self.assertIn("appointment lena tha", turn_text)
            self.assertIn("dr. rao", turn_text)
            expect(demo).to_contain_text("Sunita Sharma")
            expect(demo).to_contain_text("11:30 AM")
            expect(demo).to_contain_text("Follow-up")
            expect(demo).to_contain_text("Dr. Rao")
            expect(demo).to_contain_text("written to Practo Ray")
            expect(demo).to_contain_text("WhatsApp confirmation delivered")

        with self.subTest("six feature cards under handles"):
            handles = page.locator("#handles")
            cards = handles.locator(".cell")
            self.assertEqual(cards.count(), 6)
            expected_titles = [
                "Books the slot",
                "Reschedules and cancels",
                "Quotes fees and timings",
                "Gives directions",
                "Reports and readiness",
                "Screens the reps",
            ]
            for index, title in enumerate(expected_titles):
                with self.subTest(card=title):
                    card = cards.nth(index)
                    expect(card).to_contain_text(f"{index + 1:02d}")
                    expect(card).to_contain_text(title)
                    expect(card.locator(".quote")).to_be_visible()

        with self.subTest("three refusal items under limits"):
            limits = page.locator("#limits")
            expect(limits).to_contain_text("Hard limits", ignore_case=True)
            items = limits.locator(".limit-list li")
            self.assertEqual(items.count(), 3)
            expected_refusals = {
                "No diagnosis, no advice": "earliest slot",
                "No medicine names, no dosages": "Not even repeats",
                "No results read over the phone": "Ready for collection",
            }
            for title, snippet in expected_refusals.items():
                with self.subTest(refusal=title):
                    item = limits.locator(".limit-list li", has_text=title)
                    expect(item).to_contain_text(snippet)

        with self.subTest("emergency escalation notice"):
            escalate = page.locator("#limits .escalate")
            expect(escalate).to_contain_text("And one thing it always does")
            for trigger in ("chest pain", "breathlessness", "heavy bleeding", "seizure", "unresponsive patient"):
                expect(escalate).to_contain_text(trigger)
            expect(escalate).to_contain_text("emergency number")
            expect(escalate).to_contain_text("on-duty mobile")
            escalation_line = escalate.locator(".line")
            expect(escalation_line).to_contain_text("ESCALATION")
            expect(escalation_line).to_contain_text("chest pain")
            expect(escalation_line).to_contain_text("108 read aloud")
            expect(escalation_line).to_contain_text("Dr. Rao paged")
            expect(escalation_line).to_contain_text("call transferred")

        with self.subTest("setup integrations list has all 8 entries"):
            setup = page.locator("#setup")
            for integration in (
                "Practo Ray", "HealthPlix", "Bajaj Health", "DocPulse",
                "Google Calendar", "WhatsApp Business", "Excel", "Paper register",
            ):
                expect(setup).to_contain_text(integration)

        with self.subTest("specialty tags list has all 9 entries"):
            setup = page.locator("#setup")
            for specialty in (
                "Dental", "Paediatrics", "Dermatology", "Orthopaedics", "Gynaecology",
                "Physiotherapy", "Eye care", "Diagnostic labs", "Multi-speciality",
            ):
                expect(setup).to_contain_text(specialty)

        with self.subTest("pricing section has all three tiers"):
            pricing = page.locator("#pricing")
            plans = pricing.locator(".plan")
            self.assertEqual(plans.count(), 3)

            solo = plans.nth(0)
            expect(solo).to_contain_text("Solo practice", ignore_case=True)
            expect(solo).to_contain_text("2,999")
            expect(solo).to_contain_text("Book Trial Demo")

            multi = plans.nth(1)
            expect(multi).to_contain_text("Multi-doctor clinic", ignore_case=True)
            expect(multi).to_contain_text("most chosen", ignore_case=True)
            expect(multi).to_contain_text("7,999")
            expect(multi).to_contain_text("Emergency escalation to on-duty mobile")
            expect(multi).to_contain_text("Waitlist fill on cancellation")
            expect(multi).to_contain_text("Start Free Trial")

            hospital = plans.nth(2)
            expect(hospital).to_contain_text("Hospital or chain", ignore_case=True)
            expect(hospital).to_contain_text("Let's talk")
            expect(hospital).to_contain_text("Named onboarding engineer")
            expect(hospital).to_contain_text("Contact Sales")

        with self.subTest("desktop nav links are present and Pricing scrolls into view"):
            nav = page.locator("#site-nav .nav-links")
            expect(nav).to_be_visible()
            for label in ("What it handles", "What it won't do", "Setup", "Pricing"):
                expect(nav.get_by_text(label, exact=True)).to_be_visible()
            nav.get_by_text("Pricing", exact=True).click()
            expect(page.locator("#pricing")).to_be_in_viewport()

        with self.subTest("hero feature badges"):
            rail = page.locator(".rail")
            expected_badges = {
                "Live in 48–72 hours": "We forward your current number",
                "31+ Indian languages": "Switches mid-call if the caller does",
                "Answers at 2 AM": "Sunday, holidays, OPD hours",
                "Priced per minute": "Not per receptionist seat",
            }
            for title, description in expected_badges.items():
                with self.subTest(badge=title):
                    expect(rail).to_contain_text(title)
                    expect(rail).to_contain_text(description)

        with self.subTest("footer data residency and legal notices"):
            footer = page.locator("footer")
            footer.scroll_into_view_if_needed()
            expect(footer).to_contain_text("AI phone assistant built for Indian clinics")
            expect(footer).to_contain_text("Patient data stays in India, deleted on your schedule")
            expect(footer).to_contain_text("© 2026 Aigenetic (OPC) Pvt Ltd")

        with self.subTest("footer quick links stay within healthcare mode"):
            footer = page.locator("footer")
            for label in ("Home", "What it handles", "What it won't do", "Setup", "Pricing", "Book a Demo"):
                expect(footer.get_by_role("link", name=label, exact=True)).to_be_visible()
            # "Home" intentionally stays in ?mode=healthcare and scrolls to
            # #top rather than leaving the vertical (see index.html's
            # loadModeContent comment on deliberately not rewriting this link).
            footer.get_by_role("link", name="Home", exact=True).click()
            self.assertIn("mode=healthcare", page.url)
            expect(page.locator("#top")).to_be_in_viewport()

        with self.subTest("schedule a demo section"):
            demo_section = page.locator("#demo")
            expect(demo_section).to_contain_text("Book a personalized demo")
            expect(demo_section).to_contain_text("Google Meet")
            expect(demo_section).to_contain_text("Schedule via Calendar")
            expect(demo_section.locator("[data-open-calendar]")).to_be_visible()
            call_now = demo_section.locator("[data-phone-link]")
            expect(call_now).to_be_visible()
            expect(call_now).to_contain_text("Call Now")
            self.assertTrue((call_now.get_attribute("href") or "").startswith("tel:"))
            expect(demo_section).to_contain_text("WhatsApp")


if __name__ == "__main__":
    unittest.main(verbosity=2)
