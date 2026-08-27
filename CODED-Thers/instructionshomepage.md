# Instructions: Implement Missing Test Cases — Home Page (`/`)

## Context

You are adding automated tests to the existing Aigenetic test suite. The project already has:

- `tests/test_main_page.py` — Class `TestMainPage` with 9 passing test methods
- `tests/test_healthcare.py` — Class `TestHealthcarePage`
- `tests/test_realestate.py` — Classes `TestRealEstatePage` & `TestMainPageLinksToRealEstate`
- `tests/test_mobile_nav.py` — Mobile navigation tests

The test runner is **pytest** with **Playwright** (Chromium headless). Tests use Python's `unittest`-style subTests where multiple assertions are grouped.

## Shared Infrastructure (read this first)

Before implementing page-specific tests, ensure these common utilities exist. If they don't, create them in a shared file like `tests/conftest.py` or `tests/helpers.py`:

### Fixtures / Constants

```python
BASE_URL = "https://aigenetic.in"
CONFIGURED_PHONE = "+917428497033"
CONFIGURED_WHATSAPP_URL = "https://wa.me/917428497033"
CONFIGURED_EMAIL = "connect@aigenetic.in"
COMPANY_NAME = "Aigenetic (OPC) Pvt Ltd"
COPYRIGHT_YEAR = "2026"
```

### Shared Assertions (used across all 3 pages)

These patterns repeat on every page. Implement them as reusable helpers:

1. **Footer Legal Links** — Assert Privacy Policy, Terms of Service, and Refund Policy links exist in `footer` under "LEGAL" heading. Each should be an `<a>` tag with a navigable `href`.

2. **Footer Contact Block** — Assert `connect@aigenetic.in` (mailto:), `+91 742849 7033` (tel:), and WhatsApp Support (wa.me/) links are present in the footer.

3. **Floating Action Buttons (FABs)** — Assert 2 fixed-position buttons at viewport bottom: WhatsApp (href starts with `https://wa.me/`) and Call (href starts with `tel:`). Verify they remain visible after scrolling.

4. **Console Error Check** — The existing `test_page_has_no_critical_console_errors` pattern: reload page, listen for `console` events, filter benign iframe errors, assert zero errors.

5. **Data Residency Notice** — Each page has a different notice in the footer:
   - Home: "Enterprise data stays in India, deleted on your schedule"
   - Healthcare: "Patient data stays in India, deleted on your schedule"
   - Real Estate: "Your Client data stays in India, deleted on your schedule"

---

## Tests to Implement

Add these 15 test methods to `tests/test_main_page.py` inside the `TestMainPage` class (or a new class in the same file).

### Test 1: `test_hero_stats_counters_render`

**Category:** CONTENT  
**Priority:** High

**What to do:**
1. Navigate to `https://aigenetic.in/`
2. Locate the stats section below the hero (look for elements containing counter numbers)
3. Assert exactly **4 stat counters** are visible
4. Verify these exact values exist in the section:
   - `"10,000+"` with label containing `"CALLS HANDLED"`
   - `"95%"` with label containing `"BOOKING SUCCESS"`
   - `"2 min"` with label containing `"AVG CALL DURATION"`
   - `"100+"` with label containing `"HAPPY BUSINESSES"`

**Selectors to try:** Look for a stats container after the hero. The counters may use `.stat-item`, `.counter`, or similar. Use `text_content()` to match the values.

---

### Test 2: `test_how_it_works_five_steps`

**Category:** CONTENT  
**Priority:** High

**What to do:**
1. Navigate to `https://aigenetic.in/`
2. Locate the section with label text `"HOW IT WORKS"`
3. Assert the heading contains `"A simple, reliable flow"`
4. Query all step items within the section
5. Assert exactly **5 steps** exist
6. Verify step titles in order:
   - Step 1: `"Customer Calls"`
   - Step 2: `"AI Answers"`
   - Step 3: `"Understands Intent"`
   - Step 4: `"Takes Action"`
   - Step 5: `"Confirms"`
7. Verify each step has a description paragraph below its title

---

### Test 3: `test_use_case_cards_render`

**Category:** CONTENT  
**Priority:** High

**What to do:**
1. Navigate to `https://aigenetic.in/`
2. Locate the "USE CASES" section with heading `"Perfect for Any Business"`
3. Assert **4 use case cards** are rendered
4. Verify card titles:
   - `"Clinics & Doctors"`
   - `"Real Estate"`
   - `"Salons & Spas"`
   - `"Offices & Schools"`
5. Assert cards 3 and 4 (Salons, Offices) display `"COMING SOON"` badge text
6. Assert cards 1 and 2 have explore links:
   - Card 1: text contains `"Explore for clinics"`, href = `/?mode=healthcare`
   - Card 2: text contains `"Explore for developers"`, href = `/?mode=realestate`
7. Verify each card lists **3 feature bullets** (✓ items)

---

### Test 4: `test_use_case_card_links_to_healthcare`

**Category:** CROSS-LINK  
**Priority:** High

**What to do:**

> **Note:** The existing suite has `test_use_case_card_links_to_realestate_with_its_own_label` in `test_realestate.py`. This is the mirror test for healthcare.

1. Navigate to `https://aigenetic.in/`
2. Find the link with `href="/?mode=healthcare"`
3. Assert it exists and is visible
4. Assert its text contains `"Explore for clinics"`
5. **Regression guard:** Assert it does NOT contain `"Explore for developers"`
6. Click the link and verify URL changes to contain `/?mode=healthcare`

---

### Test 5: `test_audio_demos_all_six_present`

**Category:** AUDIO  
**Priority:** High

**What to do:**

> **Note:** The existing `test_audio_demo_controls_are_bound` checks that audio controls work. This new test checks that all **6 industry demos** are present with correct labels.

1. Navigate to `https://aigenetic.in/`
2. Locate `#audio-demos` section with heading `"Hear Our AI Agents in Action"`
3. Query all audio demo items in the section
4. Assert exactly **6** demos exist
5. Verify labels (case-insensitive match):
   - `"Healthcare"` or `"HEALTHCARE"`
   - `"E-commerce"` or `"E-COMMERCE"`
   - `"BFSI"`
   - `"Edtech"` or `"EDTECH"`
   - `"HR Tech"` or `"HR TECH"`
   - `"Hospitality"` or `"HOSPITALITY"`
6. For each demo, assert:
   - An `<audio>` element exists with `src` containing `mp3/`
   - A play button element is visible
   - A time display shows `"0:00"`

---

### Test 6: `test_pricing_tier_details`

**Category:** CONTENT  
**Priority:** High

**What to do:**
1. Navigate to `https://aigenetic.in/`
2. Locate `#pricing` section
3. Assert **3 pricing tiers** with these exact details:

| Tier | Name | Price | Included Minutes | CTA Text |
|------|------|-------|-----------------|----------|
| 1 | FLEX | ₹2,999/month | 500 call minutes | Get Started |
| 2 | PRO | ₹7,999/month | 1,500 call minutes | Get Started |
| 3 | ENTERPRISE | Custom | (volume-based) | Contact Sales |

4. Assert PRO tier has a `"Most Popular"` badge/label
5. Assert each tier has a checklist of ✓ features (at least 4 items per tier)
6. Assert overage rate `"₹6/minute"` appears on FLEX and PRO tiers

---

### Test 7: `test_why_choose_us_features`

**Category:** CONTENT  
**Priority:** Medium

**What to do:**
1. Navigate to `https://aigenetic.in/`
2. Locate section with heading `"Why Choose Aigenetic"`
3. Assert subtitle `"Fully managed AI phone service designed for Indian businesses"`
4. Assert **4 feature cards**:
   - `"Fully Managed"` — `"We handle everything from setup to maintenance"`
   - `"31+ Languages"` — `"Understands major Indian languages and accents"`
   - `"Works 24/7"` — `"Never miss a call, even on holidays"`
   - `"Affordable"` — `"Pay-per-use pricing for small businesses"`

---

### Test 8: `test_testimonials_content`

**Category:** CONTENT  
**Priority:** Medium

**What to do:**
1. Navigate to `https://aigenetic.in/`
2. Locate the "TESTIMONIALS" section
3. Assert **3 testimonial cards** rendered
4. For each testimonial, verify:
   - **Card 1:** Name `"Dr. Priya Sharma"`, role contains `"Skin Clinic, Mumbai"`, 5 stars
   - **Card 2:** Name `"Rahul Desai"`, role contains `"Salon Owner, Pune"`, 5 stars
   - **Card 3:** Name `"Anjali Reddy"`, role contains `"Real Estate Agency, Bangalore"`, 5 stars
5. Assert each card contains a quote (text inside quotation marks or a quote element)
6. Assert each card has an avatar initial circle (first letter of name)

---

### Test 9: `test_desktop_nav_links_scroll`

**Category:** NAV  
**Priority:** High

**What to do:**
1. Navigate to `https://aigenetic.in/` at **desktop viewport** (≥1024px wide)
2. Assert the desktop navigation bar is visible (not hamburger menu)
3. Locate nav links. Expect at least: `"Features"`, `"Use Cases"`, `"Pricing"`
4. For each nav link:
   - Click the link
   - Wait briefly for scroll animation
   - Assert that the corresponding section is now in the viewport (use `is_visible()` or check scroll position)
5. Specifically verify:
   - Clicking `"Pricing"` scrolls to the `#pricing` section

---

### Test 10: `test_hero_cta_buttons`

**Category:** CTAS  
**Priority:** High

**What to do:**
1. Navigate to `https://aigenetic.in/`
2. Locate the hero section
3. Assert **3 CTA buttons** in the hero:
   - `"Call Now"` — href starts with `tel:+91`
   - `"WhatsApp Us"` — href starts with `https://wa.me/`
   - `"Schedule Demo"` — clicking opens the calendar modal (`#calendar-modal-main`)
4. For the Schedule Demo button: click it, assert modal is visible, close it

---

### Test 11: `test_floating_action_buttons`

**Category:** CTAS  
**Priority:** Medium

**What to do:**
1. Navigate to `https://aigenetic.in/`
2. Locate 2 fixed-position floating buttons at the bottom of the viewport
3. Assert one links to `https://wa.me/...` (WhatsApp icon 💬)
4. Assert one links to `tel:+91...` (Phone icon 📞)
5. Scroll down to the middle of the page
6. Assert both FABs are **still visible** in the viewport
7. Verify FABs have CSS `position: fixed` (use `evaluate` to check computed style)

---

### Test 12: `test_footer_quick_links`

**Category:** NAV  
**Priority:** Medium

**What to do:**
1. Navigate to `https://aigenetic.in/`
2. Scroll to footer, locate "QUICK LINKS" section
3. Assert **5 links** present: `"Home"`, `"How It Works"`, `"Use Cases"`, `"Pricing"`, `"Book a Demo"`
4. Click `"How It Works"` → verify page scrolls up to that section
5. Click `"Book a Demo"` → verify calendar modal opens or page scrolls to demo section

---

### Test 13: `test_footer_contact_and_company`

**Category:** CONTENT  
**Priority:** Medium

**What to do:**
1. Navigate to `https://aigenetic.in/`
2. Scroll to footer
3. Assert company name `"Aigenetic (OPC) Pvt Ltd"` is visible
4. Assert email `"connect@aigenetic.in"` with `mailto:` link
5. Assert phone `"+91 742849 7033"` with `tel:` link
6. Assert `"WhatsApp Support"` with `wa.me/` link
7. Assert copyright text `"© 2026 Aigenetic (OPC) Pvt Ltd. All rights reserved."`
8. Assert data residency notice: `"Enterprise data stays in India, deleted on your schedule."`

---

### Test 14: `test_live_voice_assistant_teaser`

**Category:** CTAS  
**Priority:** Medium

**What to do:**
1. Navigate to `https://aigenetic.in/`
2. Locate the `"Live Call to Voice Assistant"` button (look for `[data-live-voice-call]` or button text match)
3. Assert the button is visible
4. Click the button
5. Assert either:
   - A "coming soon" notification/toast flashes briefly, OR
   - A call flow is initiated (tel: link)
6. Assert the page did not navigate away (URL is still `https://aigenetic.in/`)

---

### Test 15: `test_quick_setup_badges`

**Category:** CONTENT  
**Priority:** Low

**What to do:**
1. Navigate to `https://aigenetic.in/`
2. Locate the 4 feature badges below the hero CTA buttons
3. Assert each badge has a title and description:
   - `"Quick setup"` → `"Get started in 48-72 hours"`
   - `"31+ Languages"` → `"Understands local accents"`
   - `"Works 24/7"` → `"Never miss a call"`
   - `"Pay per use"` → `"Affordable pricing"`

---

## Implementation Notes

- **Follow the existing code style** in `test_main_page.py`. Use `self.page.goto()`, `self.page.locator()`, `expect()`, and `with self.subTest()` patterns.
- **Do not modify existing tests.** Add new methods below the existing ones.
- **Run `python -m pytest tests/test_main_page.py -v`** after adding each test to verify it passes.
- **Selectors:** Prefer `data-*` attributes if available. Fall back to CSS selectors like `#section-id .class-name`. Use `text=` selectors for heading/label matching.
- **Timeouts:** Use Playwright's default timeout. For scroll animations, add a short `page.wait_for_timeout(500)` after clicking nav links.
- **Console error filter:** Reuse the existing benign-error filter from `test_page_has_no_critical_console_errors`.
