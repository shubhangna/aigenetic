# Instructions: Implement Missing Test Cases — Real Estate Page (`/?mode=realestate`)

## Context

You are adding automated tests to the existing file `tests/test_realestate.py`. It currently has:

- **Class:** `TestRealEstatePage` — 2 test methods, 8 subTests (all passing)
  - `test_realestate_html_redirects_to_consolidated_url` — ROUTER
  - `test_realestate_page` — SubTests 1–8: Developer Positioning, Email CTA, Live Voice Teaser, Scope & Limits, WhatsApp CTA, Console Errors, Demo Entry Points, Phone CTA
- **Class:** `TestMainPageLinksToRealEstate` — 1 test method
  - `test_use_case_card_links_to_realestate_with_its_own_label` — CROSS-LINK

Additionally, `tests/test_mobile_nav.py` already covers hamburger nav for this page.

**Shared constants and helpers** are documented in the Home Page instructions file. Read that file's "Shared Infrastructure" section first.

---

## Important Parity Gaps

Before implementing the new tests, note these asymmetries between the Healthcare and Real Estate suites that should be addressed:

1. **Audio Player:** Healthcare has SubTest 3 testing the audio player. Real Estate has an identical audio player section but **no test for it**. This is test #3 below.

2. **Refund Policy link:** Healthcare SubTest 5 explicitly checks the Refund Policy link in the footer. Real Estate SubTest 4 does NOT check it. This is test #12 below.

---

## Tests to Implement

Add these 13 test methods to `tests/test_realestate.py`. You can add them to `TestRealEstatePage` or create `TestRealEstatePageExtended`.

### Test 1: `test_hero_developer_counter`

**Category:** CONTENT  
**Priority:** High

**What to do:**
1. Navigate to `https://aigenetic.in/?mode=realestate`
2. Locate the hero stat line above the main heading
3. Assert text contains `"120+"` and `"developer"`
4. The full expected text is: `"Answering for 120+ developer sales teams right now"`
5. Assert visible above the fold

---

### Test 2: `test_call_log_demo_realestate`

**Category:** CONTENT  
**Priority:** High

**What to do:**
1. Navigate to `https://aigenetic.in/?mode=realestate`
2. Locate the call log demo section (text `"CALL LOG"`)
3. Assert these elements:
   - Masked phone: `"+91 98••• ••771"`
   - Language: `"हिन्दी / English"`
   - Duration: `"1:24"`
   - Status: `"Handled by assistant"`
4. Assert conversation contains both `"CALLER"` and `"AIGENETIC"` messages
5. Assert property-specific details are present:
   - Project name: `"Skyline Residency"`
   - Unit type: `"2BHK"`
   - Price: `"₹78 lakh"`
   - Area: `"685 sq ft"`
   - Tower: `"Tower B"`
6. Assert RERA info: `"December 2027"` possession date
7. Assert booking confirmation:
   - Buyer: `"Rohit Verma"`
   - Time: `"Sat 11:00 AM"`
   - Type: `"Sample flat visit"`
8. Assert CRM integration: text contains `"written to your CRM"`
9. Assert WhatsApp: text contains `"WhatsApp brochure delivered"`

---

### Test 3: `test_audio_player_realestate`

**Category:** AUDIO  
**Priority:** High

**What to do:**

> **PARITY GAP:** This test mirrors Healthcare SubTest 3 (Audio Player). The Real Estate page has an identical audio sample section ("Hear the assistant") but the existing RE suite does not test it.

1. Navigate to `https://aigenetic.in/?mode=realestate`
2. Locate the audio sample section — look for text `"Hear the assistant"` or `[data-call-player]`
3. Assert an `<audio>` element exists with `src` containing `mp3/`
4. Assert a play button (▶) is visible — look for `[data-play-audio]` or a button with play icon
5. Click the play button
6. Assert the audio container toggles a `playing` class (or equivalent active state)
7. Assert the page did not navigate away

---

### Test 4: `test_six_feature_cards_realestate`

**Category:** CONTENT  
**Priority:** High

**What to do:**
1. Navigate to `https://aigenetic.in/?mode=realestate`
2. Locate the section with heading containing `"Most enquiries ask the same six questions"`
3. Assert exactly **6 feature cards**
4. Verify each card:

| # | Title | Example Quote (Hindi) |
|---|-------|-----------------------|
| 01 | Books the site visit | "Weekend mein visit ho sakti hai kya?" |
| 02 | Shares price & floor plan | "2BHK ka rate kya hai?" |
| 03 | Confirms possession & RERA status | "RERA number aur possession date bhej sakte ho?" |
| 04 | Qualifies the lead | "Loan pre-approved hai, kab visit kar sakte hain?" |
| 05 | Gives directions & landmarks | "Site office ka location kya hai?" |
| 06 | Screens channel partners | "Co-broking available hai kya?" |

5. Assert each card has numbered label (01–06), title, description, and Hindi example quote

---

### Test 5: `test_three_rera_refusal_cards`

**Category:** CONTENT  
**Priority:** High

**What to do:**
1. Navigate to `https://aigenetic.in/?mode=realestate`
2. Locate the `#limits` section with heading `"What it will never do"`
3. Assert label `"HARD LIMITS"` is present
4. Assert **3 RERA-specific refusal cards**:

| # | Title | Key Description Text |
|---|-------|---------------------|
| 1 | No price negotiated on the call | "Shares the listed price and standard payment plans only. Final negotiation goes to your sales team." |
| 2 | No guaranteed returns or rental yield promised | "RERA prohibits it, and so do we" |
| 3 | No possession date beyond what's filed | "Reads only the RERA-registered timeline. Never invents an earlier date" |

5. Assert each card has a title and description

> **Note:** These differ completely from healthcare refusals. Healthcare says "No diagnosis", RE says "No price negotiated". Verify the RE-specific RERA language.

---

### Test 6: `test_hot_lead_escalation_notice`

**Category:** CONTENT  
**Priority:** High

**What to do:**
1. Navigate to `https://aigenetic.in/?mode=realestate`
2. Locate subsection `"And one thing it always does"` within the limits section
3. Assert the description mentions:
   - `"ready to book"` or `"token amount"`
   - `"sales lead's mobile"` — rings until someone picks up
4. Assert the escalation demo badge contains:
   - `"ESCALATION"`
   - `"caller ready to pay token amount"`
   - `"Sales lead paged"`
   - `"call transferred in 11s"`

> **Note:** Healthcare escalation triggers on medical emergencies (chest pain). RE escalation triggers on hot leads (token payment). Verify the RE-specific language.

---

### Test 7: `test_setup_integrations_realestate`

**Category:** INTEGRATIONS  
**Priority:** High

**What to do:**
1. Navigate to `https://aigenetic.in/?mode=realestate`
2. Locate "SETUP" section with heading `"Keep your number. Keep your CRM."`
   - **Note:** Healthcare says `"Keep your register."` — RE says `"Keep your CRM."` — verify correct heading
3. Assert **9 integration items**:
   - `"Google Calendar"`
   - `"WhatsApp Business"`
   - `"Zoho CRM"`
   - `"Sell.Do"`
   - `"LeadSquared"`
   - `"99acres"`
   - `"MagicBricks"`
   - `"Housing.com"`
   - `"Excel"` (may show as `"Excel / Sheets"`)
4. Assert RE-specific integrations that are NOT on healthcare: `"Zoho CRM"`, `"Sell.Do"`, `"LeadSquared"`, `"99acres"`, `"MagicBricks"`, `"Housing.com"`

---

### Test 8: `test_project_type_tags`

**Category:** CONTENT  
**Priority:** Medium

**What to do:**
1. Navigate to `https://aigenetic.in/?mode=realestate`
2. Locate "TUNED PER PROJECT TYPE" section with heading `"The questions differ by project"`
3. Assert **6 project type tags**:
   - `"Residential apartments"`
   - `"Luxury villas"`
   - `"Affordable housing"`
   - `"Commercial"` (may show as `"Commercial / office space"`)
   - `"Plotted development"`
   - `"Mixed-use"` (may show as `"Mixed-use / township"`)

> **Note:** This mirrors healthcare's 9 specialty tags structure, but has 6 RE-specific project types.

---

### Test 9: `test_pricing_all_three_tiers_realestate`

**Category:** CONTENT  
**Priority:** High

**What to do:**
1. Navigate to `https://aigenetic.in/?mode=realestate`
2. Locate `#pricing` section
3. Assert **3 pricing tiers**:

| Tier | Name | Price | Key Feature | CTA |
|------|------|-------|-------------|-----|
| 1 | SINGLE PROJECT | ₹2,999 /month | One project, one number · 500 call minutes | Book Trial Demo |
| 2 | MULTI-PROJECT DEVELOPER | ₹7,999 /month | Up to 6 live projects · 1,500 call minutes · Hot-lead escalation | Start Free Trial |
| 3 | DEVELOPER GROUP / TOWNSHIP | Let's talk | Multiple projects · Routing by project | Contact Sales |

4. Assert tier 2 has `"MOST CHOSEN"` badge
5. Assert tier 2 includes `"Hot-lead escalation to sales lead"` (differs from healthcare's `"Emergency escalation to on-duty mobile"`)
6. Assert tier 2 includes `"Channel-partner call screening"` (RE-specific feature)
7. Assert tier 3 includes `"Named onboarding engineer"`

> **Note:** Existing SubTest 4 only checks `"Single project"`. This test verifies all 3 tiers with RE-specific vocabulary.

---

### Test 10: `test_desktop_nav_links_realestate`

**Category:** NAV  
**Priority:** Medium

**What to do:**
1. Navigate to `https://aigenetic.in/?mode=realestate` at **desktop viewport** (≥1024px)
2. Assert desktop nav is visible with links:
   - `"What it handles"`
   - `"What it won't do"`
   - `"Setup"`
   - `"Pricing"`
   - `"Call"` (tel: link)
   - `"Book Demo"` (triggers modal)
3. Click `"Pricing"` → verify scrolls to `#pricing`
4. Click `"Book Demo"` → verify calendar modal opens

---

### Test 11: `test_footer_data_residency_realestate`

**Category:** LEGAL  
**Priority:** Medium

**What to do:**
1. Navigate to `https://aigenetic.in/?mode=realestate`
2. Scroll to footer
3. Assert tagline contains `"AI phone assistant built for Indian real estate developers"`
4. Assert data residency: `"Your Client data stays in India, deleted on your schedule"`
   - **Important:** This says `"Your Client data"` — NOT `"Enterprise data"` (Home) and NOT `"Patient data"` (Healthcare). Verify the exact wording.
5. Assert copyright: `"© 2026 Aigenetic (OPC) Pvt Ltd"`

---

### Test 12: `test_refund_policy_link_realestate`

**Category:** LEGAL  
**Priority:** Medium

**What to do:**

> **PARITY GAP:** Healthcare SubTest 5 explicitly checks `"Refund Policy"` link exists in footer. Real Estate SubTest 4 checks scope & limits content but does NOT verify the Refund Policy link. This test closes that gap.

1. Navigate to `https://aigenetic.in/?mode=realestate`
2. Scroll to footer, locate "LEGAL" section
3. Assert 3 legal links present:
   - `"Privacy Policy"`
   - `"Terms of Service"`
   - `"Refund Policy"`
4. Assert `"Refund Policy"` link has a valid `href` (not empty, not `#`)
5. Optionally: click the link and verify it loads a page (doesn't 404)

---

### Test 13: `test_hero_feature_badges_realestate`

**Category:** CONTENT  
**Priority:** Low

**What to do:**
1. Navigate to `https://aigenetic.in/?mode=realestate`
2. Locate the 4 feature badges below the hero CTAs
3. Assert each badge with title and description:
   - `"Live in 48–72 hours"` → `"We forward your current number"`
   - `"31+ Indian languages"` → `"Switches mid-call if the caller does"`
   - `"Answers at 9 PM"` → `"Weekends and the hours buyers actually call"`
   - `"Priced per minute"` → `"Not per site-office seat"`

> **Key differences from Healthcare badges:**
> - Healthcare says `"Answers at 2 AM"` / `"Sunday, holidays, OPD hours"` — RE says `"Answers at 9 PM"` / `"Weekends and the hours buyers actually call"`
> - Healthcare says `"Not per receptionist seat"` — RE says `"Not per site-office seat"`
> These are intentional domain-specific copy differences that should be tested.

---

## Implementation Notes

- **Follow the existing style** in `test_realestate.py`. Use the same `self.page.goto()`, `self.page.locator()`, and `with self.subTest()` patterns.
- **Do not modify existing tests.** Only add new methods.
- **Run:** `python -m pytest tests/test_realestate.py -v` after each test.
- **URL:** Always navigate to `https://aigenetic.in/?mode=realestate` (not `realestate.html`).
- **Cross-page verification:** When a test notes a difference from healthcare (pricing vocabulary, escalation triggers, data residency wording), assert the RE-specific text and optionally assert the healthcare text is NOT present.
- **Hindi text matching:** Use substring matching (`assertIn`) for Hindi text to handle whitespace and encoding variations.
