"""Shared Playwright and unittest helpers for the Aigenetic website tests."""

from __future__ import annotations

import os
import socket
import unittest
from pathlib import Path

from playwright.sync_api import Page, expect, sync_playwright


PROJECT_ROOT = Path(__file__).resolve().parents[1]
BASE_URL = os.environ.get("BASE_URL", "http://localhost:8989").rstrip("/")
HEADLESS = os.environ.get("HEADLESS", "").strip().lower() in {"1", "true", "yes"}


class WebsiteTestCase(unittest.TestCase):
    """Base class that gives each test an isolated browser page."""

    @classmethod
    def setUpClass(cls):
        cls.playwright = sync_playwright().start()
        cls.browser = cls.playwright.chromium.launch(headless=HEADLESS)
        cls.context = cls.browser.new_context()

    @classmethod
    def tearDownClass(cls):
        cls.context.close()
        cls.browser.close()
        cls.playwright.stop()

    def setUp(self):
        self.page = self.context.new_page()
        self.console_errors = []
        self.page.on("console", self._collect_console_error)

    def tearDown(self):
        self.page.close()

    def _collect_console_error(self, message):
        if message.type == "error" and "favicon" not in message.text.lower():
            self.console_errors.append(message.text)

    def page_url(self, relative_path=""):
        return f"{BASE_URL}/{relative_path.lstrip('/')}"

    def open_page(self, relative_path="", ready_selector="body"):
        response = self.page.goto(
            self.page_url(relative_path),
            wait_until="domcontentloaded",
            timeout=45000,
        )
        self.page.locator(ready_selector).wait_for(state="visible", timeout=15000)
        return response

    def assert_successful_response(self, response):
        self.assertIsNotNone(response, "The page navigation should return a response")
        self.assertEqual(response.status, 200, "The page should load with HTTP 200")

    def assert_contact_links(self, phone_selector, whatsapp_selector, email_selector=None):
        phone = self.page.locator(phone_selector).first
        whatsapp = self.page.locator(whatsapp_selector).first
        expect(phone).to_be_visible()
        expect(whatsapp).to_be_visible()
        self.assertTrue((phone.get_attribute("href") or "").startswith("tel:"))
        self.assertTrue((whatsapp.get_attribute("href") or "").startswith("https://wa.me/"))

        if email_selector:
            email = self.page.locator(email_selector).first
            expect(email).to_be_visible()
            self.assertTrue((email.get_attribute("href") or "").startswith("mailto:"))

    def assert_no_console_errors(self):
        self.assertEqual(
            self.console_errors,
            [],
            f"Unexpected browser console errors: {self.console_errors}",
        )


def assert_calendar_modal(test_case, trigger_selector, modal_selector):
    """Open and close a calendar modal, including its embedded scheduler."""
    trigger = test_case.page.locator(trigger_selector).first
    expect(trigger).to_be_visible()
    trigger.click()

    modal = test_case.page.locator(modal_selector)
    expect(modal).to_be_visible()
    expect(modal.locator("iframe")).to_be_visible()

    close_button = modal.locator("button").first
    expect(close_button).to_be_visible()
    close_button.click()
    expect(modal).not_to_be_visible()


EXPECTED_GITHUB_IPS = {
    "185.199.108.153",
    "185.199.109.153",
    "185.199.110.153",
    "185.199.111.153",
}


def resolve_domain_ips(domain):
    return set(socket.gethostbyname_ex(domain)[2])