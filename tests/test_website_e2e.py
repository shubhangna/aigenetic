"""
End-to-end tests for aigenetic.in website using Playwright.
Tests website functionality, content, and user interactions.
"""

import os
import unittest
from playwright.sync_api import sync_playwright, expect


class TestWebsiteE2E(unittest.TestCase):
    """End-to-end test suite for aigenetic.in website"""
    
    BASE_URL = os.environ.get('BASE_URL', 'http://localhost:8989')
    
    @classmethod
    def setUpClass(cls):
        """Set up Playwright browser for all tests"""
        cls.playwright = sync_playwright().start()
        cls.browser = cls.playwright.chromium.launch(headless=True)
        cls.context = cls.browser.new_context()
        cls.page = cls.context.new_page()
    
    @classmethod
    def tearDownClass(cls):
        """Clean up browser resources"""
        cls.page.close()
        cls.context.close()
        cls.browser.close()
        cls.playwright.stop()

    def goto_base_url(self):
        """Navigate to the configured site without waiting on slow third-party assets."""
        response = self.page.goto(
            self.BASE_URL,
            wait_until="domcontentloaded",
            timeout=45000,
        )
        self.page.locator("h1.hero-title").wait_for(state="visible", timeout=15000)
        return response
    
    def test_01_website_loads_successfully(self):
        """Verify website loads without errors"""
        response = self.goto_base_url()
        self.assertEqual(response.status, 200, "Website should load with 200 status")
        print(f"✓ Website loaded successfully (Status: {response.status})")
    
    def test_02_page_title_contains_aigenetic(self):
        """Verify page title includes AIgenetic branding"""
        self.goto_base_url()
        title = self.page.title()
        self.assertIn("AIgenetic", title, "Page title should contain 'AIgenetic'")
        print(f"✓ Page title verified: {title}")
    
    def test_03_hero_section_visible(self):
        """Verify hero section with main heading is present"""
        self.goto_base_url()
        
        # Check for main h1 heading in hero section
        hero_heading = self.page.locator("h1.hero-title").first
        expect(hero_heading).to_be_visible()
        expect(hero_heading).to_contain_text("The Voice of Your Business")
        print("✓ Hero section with main heading is visible")
        
        # Check for subheading text
        subheading = self.page.get_by_text("Never miss a customer call again")
        expect(subheading).to_be_visible()
        print("✓ Hero subheading is visible")
    
    def test_04_features_section_exists(self):
        """Verify 'How It Works' features section is present"""
        self.goto_base_url()
        
        features_label = self.page.locator("#features .section-label", has_text="How It Works")
        expect(features_label).to_be_visible()
        print("✓ 'How It Works' section is visible")
        
        # Verify key feature steps are present
        step_texts = ["Customer Calls", "AI Answers", "Understands Intent", "Takes Action", "Confirms"]
        for step in step_texts:
            element = self.page.get_by_text(step, exact=True)
            expect(element).to_be_visible()
        print(f"✓ All {len(step_texts)} feature steps are visible")
    
    def test_05_use_cases_section_present(self):
        """Verify use cases section with industry examples"""
        self.goto_base_url()
        
        use_cases_heading = self.page.get_by_role("heading", name="Perfect for Any Business")
        expect(use_cases_heading).to_be_visible()
        print("✓ Use Cases section is visible")
        
        # Check for specific use case categories
        industries = ["Clinics & Doctors", "Salons & Spas", "Real Estate", "Offices & Schools"]
        for industry in industries:
            heading = self.page.get_by_role("heading", name=industry)
            expect(heading).to_be_visible()
        print(f"✓ All {len(industries)} industry use cases are present")
    
    def test_06_pricing_section_with_cards(self):
        """Verify pricing section has pricing cards"""
        self.goto_base_url()
        
        pricing_heading = self.page.get_by_role("heading", name="Simple Pricing")
        expect(pricing_heading).to_be_visible()
        print("✓ Pricing section heading is visible")
        
        # Check for pricing cards (structure-based, content may change)
        pricing_section = self.page.locator("#pricing")
        plan_cards = pricing_section.locator(".minimal-card")
        plan_card_count = plan_cards.count()
        if plan_card_count < 3:
            grid_cards = pricing_section.locator(".grid").first.locator("> div")
            plan_card_count = grid_cards.count()
        self.assertGreaterEqual(plan_card_count, 3, "Expected at least 3 pricing cards")
        print(f"✓ Pricing section has {plan_card_count} cards")
    
    def test_07_cta_buttons_present_and_functional(self):
        """Verify CTA buttons exist with correct links"""
        self.goto_base_url()
        
        # Check Call CTA
        call_button = self.page.locator('a[href^="tel:"]:visible').first
        expect(call_button).to_be_visible()
        call_href = call_button.get_attribute("href")
        self.assertTrue(call_href.startswith("tel:"), "Call button should have tel: link")
        print(f"✓ Call CTA button is present with link: {call_href}")
        
        # Check WhatsApp CTA
        whatsapp_button = self.page.locator('a[href^="https://wa.me/"]:visible').first
        expect(whatsapp_button).to_be_visible()
        whatsapp_href = whatsapp_button.get_attribute("href")
        self.assertTrue(whatsapp_href.startswith("https://wa.me/"), "WhatsApp button should have wa.me link")
        print(f"✓ WhatsApp CTA button is present with link: {whatsapp_href}")
    
    def test_08_schedule_demo_modal_exists(self):
        """Verify schedule demo entry point opens the booking modal"""
        self.goto_base_url()

        schedule_demo = self.page.locator('a[href="#"]', has_text="Schedule Demo").first
        expect(schedule_demo).to_be_visible()
        schedule_demo.click()

        modal_heading = self.page.locator("#calendar-modal-main h2", has_text="Schedule Your Demo")
        expect(modal_heading).to_be_visible()
        calendar_frame = self.page.locator("#calendar-modal-main iframe")
        expect(calendar_frame).to_be_visible()
        print("Schedule demo modal is visible")
    
    def test_09_footer_present_with_links(self):
        """Verify footer section with company info and links"""
        self.goto_base_url()
        
        # Scroll to footer
        self.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        
        # Check for footer content
        footer_email = self.page.get_by_role("link", name="connect@aigenetic.in")
        expect(footer_email).to_be_visible()
        print("✓ Footer with contact email is visible")
        
        # Check footer links
        privacy_link = self.page.get_by_role("link", name="Privacy Policy")
        terms_link = self.page.get_by_role("link", name="Terms of Service")
        
        expect(privacy_link).to_be_visible()
        expect(terms_link).to_be_visible()
        print("✓ Footer policy links are present")
    
    def test_10_no_critical_console_errors(self):
        """Verify no critical JavaScript errors in console"""
        self.goto_base_url()
        
        # Collect console messages
        errors = []
        warnings = []
        
        def handle_console(msg):
            if msg.type == 'error' and 'favicon' not in msg.text:
                # Ignore favicon 404s as they're non-critical
                errors.append(msg.text)
            elif msg.type == 'warning':
                warnings.append(msg.text)
        
        self.page.on("console", handle_console)
        self.page.reload(wait_until="domcontentloaded", timeout=45000)
        
        # Only fail on critical errors (not favicon or CDN warnings)
        critical_errors = [e for e in errors if 'favicon' not in e.lower()]
        
        self.assertEqual(len(critical_errors), 0, 
                        f"Found {len(critical_errors)} critical console errors: {critical_errors}")
        print(f"✓ No critical console errors (Warnings: {len(warnings)}, Non-critical: {len(errors) - len(critical_errors)})")
    
    def test_11_testimonials_section_visible(self):
        """Verify testimonials section exists"""
        self.goto_base_url()
        
        testimonials_heading = self.page.get_by_role("heading", name="Trusted by 100+ Businesses")
        expect(testimonials_heading).to_be_visible()
        print("✓ Testimonials section is visible")
        
        # Check for star ratings
        stars = self.page.get_by_text("★").all()
        self.assertGreater(len(stars), 0, "Should have star ratings in testimonials")
        print(f"✓ Testimonial star ratings present ({len(stars)} stars found)")


if __name__ == '__main__':
    unittest.main(verbosity=2)
