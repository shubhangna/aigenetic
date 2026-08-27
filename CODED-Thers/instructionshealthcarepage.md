# Instructions: Implement Missing Test Cases — Healthcare Page (`/?mode=healthcare`)

## Context

You are adding automated tests to the existing file `tests/test_healthcare.py`. It currently has:

- **Class:** `TestHealthcarePage`
- **2 test methods, 9 subTests** — all passing
- `test_healthcare_html_redirects_to_consolidated_url` — ROUTER
- `test_healthcare_page` — with SubTests 1–9 covering: Clinic Positioning, Email CTA, Audio Player, Live Voice Teaser, Scope & Policies, WhatsApp CTA, Console Errors, Demo Entry Points, Phone CTA

Additionally, `tests/test_mobile_nav.py` already covers hamburger nav for this page.

**Shared constants and helpers** are documented in the Home Page instructions file. Read that file's "Shared Infrastructure" section first — the same constants (`CONFIGURED_PHONE`, `CONFIGURED_EMAIL`, `BASE_URL`, etc.) and helper patterns apply here.

---

## Tests to Implement

Add these 14 test methods to `tests/test_healthcare.py`. You can add them as new methods on `TestHealthcarePage`, or create a new class `TestHealthcarePageExtended` in the same file.

### Test 1: `test_hero_clinic_counter`

**Category:** CONTENT  
**Priority:** High

**What to do:**
1. Navigate to `https://aigenetic.in/?mode=healthcare`
2. Locate the hero stat line above the main heading
3. Assert the text contains `"240+"` and `"clinics"`
4. The full expected text is: `"Answering for 240+ clinics right now"`
5. Assert this element is visible above the fold

---

### Test 2: `test_call_log_demo_section`

**Category:** CONTENT  
**Priority:** High

**What to do:**
1. Navigate to `https://aigenetic.in/?mode=healthcare`
2. Locate the call log demo section — look for text `"CALL LOG"` or a container with mock conversation bubbles
3. Assert these elements are present in the demo:
   - Masked phone number: `"+91 98••• ••412"`
   - Language badge: `"हिन्दी / English"`
   - Duration: `"1:12"`
   - Status: `"Handled by assistant"`
4. Assert conversation contains both `"CALLER"` and `"AIGENETIC"` labeled messages
5. Assert Hindi text is present (look for `"appointment lena tha"` or `"Dr. Rao"`)
6. Assert booking confirmation contains:
   - Patient name: `"Sunita Sharma"`
   - Time: `"11:30 AM"`
   - Type: `"Follow-up"`
   - Doctor: `"Dr. Rao"`
7. Assert integration line: `"written to Practo Ray"` (text contains)
8. Assert WhatsApp notice: `"WhatsApp confirmation delivered"`

---

### Test 3: `test_six_feature_cards_handles`

**Category:** CONTENT  
**Priority:** High

**What to do:**
1. Navigate to `https://aigenetic.in/?mode=healthcare`
2. Locate the `#handles` section or section with heading containing `"Most calls to a clinic are logistics"`
3. Assert exactly **6 feature cards**
4. Verify each card's title text:

| # | Title | Example Quote (Hindi) |
|---|-------|-----------------------|
| 01 | Books the slot | "Kal shaam ka koi time hai?" |
| 02 | Reschedules and cancels | "Aaj nahi aa paaunga, agle hafte kar dijiye." |
| 03 | Quotes fees and timings | "Root canal ka kitna charge hai?" |
| 04 | Gives directions | "Clinic metro station se kitna door hai?" |
| 05 | Reports and readiness | "Blood test ki report aa gayi kya?" |
| 06 | Screens the reps | "Sir se 5 minute mil sakte hain?" |

5. Assert each card has a numbered label (01–06), a title, a description paragraph, and a Hindi example quote in italics or a quote block

---

### Test 4: `test_three_refusal_items`

**Category:** CONTENT  
**Priority:** High

**What to do:**
1. Navigate to `https://aigenetic.in/?mode=healthcare`
2. Locate the `#limits` section or section with heading `"What it will never do"`
3. Assert section label contains `"HARD LIMITS"`
4. Assert exactly **3 refusal cards/items**:

| # | Title | Key Description Text |
|---|-------|---------------------|
| 1 | No diagnosis, no advice | "Symptoms are logged for you and the caller is offered the earliest slot" |
| 2 | No medicine names, no dosages | "Not even repeats of what you prescribed last visit" |
| 3 | No results read over the phone | "Ready for collection" is the whole answer |

5. Assert each card has both a title and a description

> **Note:** The existing SubTest 5 only checks that the text `"No diagnosis, no advice"` exists. This new test verifies all 3 refusals individually with their descriptions.

---

### Test 5: `test_emergency_escalation_notice`

**Category:** CONTENT  
**Priority:** High

**What to do:**
1. Navigate to `https://aigenetic.in/?mode=healthcare`
2. Within the limits section, locate the subsection `"And one thing it always does"`
3. Assert the description mentions these trigger conditions (any subset is fine):
   - `"chest pain"`
   - `"breathlessness"`
   - `"heavy bleeding"`
   - `"seizure"`
   - `"unresponsive patient"`
4. Assert the description mentions these actions:
   - `"emergency number"` (reads it out)
   - `"on-duty mobile"` (rings it)
5. Assert the escalation demo badge is present with text containing:
   - `"ESCALATION"`
   - `"chest pain"`
   - `"108 read aloud"`
   - `"Dr. Rao paged"`
   - `"call transferred"`

---

### Test 6: `test_setup_integrations_list`

**Category:** INTEGRATIONS  
**Priority:** High

**What to do:**
1. Navigate to `https://aigenetic.in/?mode=healthcare`
2. Locate the "SETUP" section with heading `"Keep your number. Keep your register."`
3. Assert **8 integration items** are listed. Verify each name is present:
   - `"Practo Ray"`
   - `"HealthPlix"`
   - `"Bajaj Health"`
   - `"DocPulse"`
   - `"Google Calendar"`
   - `"WhatsApp Business"`
   - `"Excel"` (may show as `"Excel / Sheets"`)
   - `"Paper register"` (may show as `"Paper register + daily list"`)
4. Integration items may be rendered as badges, chips, list items, or logo cards — match by text content

---

### Test 7: `test_specialty_tags`

**Category:** CONTENT  
**Priority:** Medium

**What to do:**
1. Navigate to `https://aigenetic.in/?mode=healthcare`
2. Locate the "TUNED PER SPECIALTY" section with heading `"The questions differ by board"`
3. Assert **9 specialty tags** are present:
   - `"Dental"`
   - `"Paediatrics"`
   - `"Dermatology"`
   - `"Orthopaedics"`
   - `"Gynaecology"`
   - `"Physiotherapy"`
   - `"Eye care"`
   - `"Diagnostic labs"`
   - `"Multi-speciality"`
4. Tags may be rendered as pills, chips, or buttons — match by text content

---

### Test 8: `test_pricing_all_three_tiers`

**Category:** CONTENT  
**Priority:** High

**What to do:**
1. Navigate to `https://aigenetic.in/?mode=healthcare`
2. Locate the `#pricing` section
3. Assert **3 pricing tiers** with these details:

| Tier | Name | Price | Key Feature | CTA |
|------|------|-------|-------------|-----|
| 1 | SOLO PRACTICE | ₹2,999 /month | One doctor, one number · 500 call minutes | Book Trial Demo |
| 2 | MULTI-DOCTOR CLINIC | ₹7,999 /month | Up to 6 doctors · 1,500 call minutes · Emergency escalation | Start Free Trial |
| 3 | HOSPITAL OR CHAIN | Let's talk | Multiple branches · Routing by specialty | Contact Sales |

4. Assert tier 2 has a `"MOST CHOSEN"` badge
5. Assert tier 2 includes `"Emergency escalation to on-duty mobile"` in its feature list
6. Assert tier 2 includes `"Waitlist fill on cancellation"` in its feature list
7. Assert tier 3 includes `"Named onboarding engineer"`

> **Note:** The existing SubTest 5 only checks `"Solo practice"` exists. This test verifies all 3 tiers fully.

---

### Test 9: `test_desktop_nav_links`

**Category:** NAV  
**Priority:** Medium

**What to do:**
1. Navigate to `https://aigenetic.in/?mode=healthcare` at **desktop viewport** (≥1024px)
2. Assert the desktop navigation bar is visible
3. Assert these nav links are present (in header, not footer):
   - `"What it handles"` (or similar)
   - `"What it won't do"` (or similar)
   - `"Setup"`
   - `"Pricing"`
   - `"Call"` (tel: link)
   - `"Book Demo"` (triggers calendar modal)
4. Click `"Pricing"` → verify page scrolls to `#pricing` section
5. Click `"Book Demo"` → verify calendar modal opens

---

### Test 10: `test_hero_feature_badges`

**Category:** CONTENT  
**Priority:** Low

**What to do:**
1. Navigate to `https://aigenetic.in/?mode=healthcare`
2. Locate the 4 feature badges below the hero CTAs
3. Assert each badge with title and description:
   - `"Live in 48–72 hours"` → `"We forward your current number"`
   - `"31+ Indian languages"` → `"Switches mid-call if the caller does"`
   - `"Answers at 2 AM"` → `"Sunday, holidays, OPD hours"`
   - `"Priced per minute"` → `"Not per receptionist seat"`

> **Note:** These differ from the Home page badges. The text is healthcare-specific.

---

### Test 11: `test_footer_data_residency`

**Category:** LEGAL  
**Priority:** Medium

**What to do:**
1. Navigate to `https://aigenetic.in/?mode=healthcare`
2. Scroll to footer
3. Assert footer tagline contains `"AI phone assistant built for Indian clinics"`
4. Assert data residency notice: `"Patient data stays in India, deleted on your schedule"`
   - **Important:** This is `"Patient data"`, NOT `"Enterprise data"` (which is the Home page). Verify the exact word.
5. Assert copyright: `"© 2026 Aigenetic (OPC) Pvt Ltd"`

---

### Test 12: `test_footer_quick_links_healthcare`

**Category:** NAV  
**Priority:** Medium

**What to do:**
1. Navigate to `https://aigenetic.in/?mode=healthcare`
2. Scroll to footer, locate "QUICK LINKS"
3. Assert **6 links** with healthcare-specific labels:
   - `"Home"` → navigates to `/` (main page, leaves healthcare mode)
   - `"What it handles"` → scrolls to handles section
   - `"What it won't do"` → scrolls to limits section
   - `"Setup"` → scrolls to setup section
   - `"Pricing"` → scrolls to pricing section
   - `"Book a Demo"` → opens calendar modal or scrolls to demo section
4. Click `"Home"` → verify URL is `https://aigenetic.in/` (no `?mode=` parameter)

---

### Test 13: `test_floating_fabs_healthcare`

**Category:** CTAS  
**Priority:** Medium

**What to do:**
1. Navigate to `https://aigenetic.in/?mode=healthcare`
2. Assert 2 floating action buttons visible at the bottom of the viewport
3. Assert WhatsApp FAB href starts with `https://wa.me/`
4. Assert Call FAB href starts with `tel:+91`
5. Scroll the page halfway down
6. Assert both FABs are still visible (position: fixed)

---

### Test 14: `test_schedule_demo_section`

**Category:** CONTENT  
**Priority:** Low

**What to do:**
1. Navigate to `https://aigenetic.in/?mode=healthcare`
2. Locate the `"SCHEDULE A DEMO"` section (near bottom, before footer)
3. Assert heading contains `"Book a personalized demo"` and `"Google Meet"`
4. Assert `"Schedule via Calendar"` link/button is present
5. Assert `"Call Now"` button is present with `tel:` href
6. Assert WhatsApp mention text is present

---

## Implementation Notes

- **Follow the existing style** in `test_healthcare.py`. The existing test uses a subTest pattern: `with self.subTest("SubTest Name"):`. You may use the same pattern or separate methods.
- **Do not modify existing tests.** Only add new methods.
- **Run:** `python -m pytest tests/test_healthcare.py -v` after each test.
- **URL:** Always navigate to `https://aigenetic.in/?mode=healthcare` (not `healthcare.html`).
- **Hindi text matching:** Use `assertIn` with a substring rather than full string match, since Hindi text may render with varying whitespace or encoding.
