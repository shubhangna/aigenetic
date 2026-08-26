# TODO
- After deploy, submit /?mode=healthcare and /?mode=realestate in Google Search
  Console and request removal/301-style handling of the old /healthcare.html and
  /realestate.html URLs from the index — client-side redirects consolidate slower
  than a real server 301 would (accepted trade-off, see CLAUDE_Result.html)
- CLAUDE.md's Testing section still names tests/test_website_e2e.py, which doesn't
  exist — actual files are test_main_page.py, test_healthcare.py, test_realestate.py,
  test_mobile_nav.py, test_github_ips.py; doc drift predates this session, worth a
  cleanup pass
- Main page to have scrolling use cases
- Add animation like husky voice
- Add languages as a list somewhere on the site
- Policy pages quote ₹4,999-₹9,999 monthly range, actual plans are ₹2,999/₹7,999
- realestate.html has no voice-sample audio player — no real-estate demo clip exists
  in mp3/ yet; record one (site-visit/price-enquiry call), add under mp3/ +
  newSite/assets/, then restore the two-column callsheet-grid + sticky player layout
- realestate.html's CRM/portal chips (Zoho, Sell.Do, LeadSquared, 99acres, MagicBricks,
  Housing.com) are intentionally NOT marked active — confirm real integrations before
  marking any of them .chip.on (see newSite/template.json integrationsHonestyNote)

- Test add: verification of popup
- Tests need HEADLESS=true env var in this sandbox (headed mode flaky/slow, no display)
- tests/test_healthcare.py's whatsapp-request and console-error subtests are flaky when
  run alongside other test files (both pass alone) — one is a network-timing race, the
  other is a stray Google CSP report-only warning from the calendar iframe; neither
  reproduces in isolation, likely cross-test browser-context contention, not a site defect

# Done

- Logo fix and positioning
- Connect MCP
- Audio fix in the add
- Live add
- Create proper tests for both links
- Favicon for healthcare.html fix it as in index.html
- Fix thumbnail
- Filtered reCAPTCHA console noise from test
- Fixed healthcare.html wrong phone digit — claude moved at the end
- Pricing wording call minutes update — claude moved at the end
- healthcare.html missing meta description and Open Graph tags (index.html has them) — claude moved at the end
- healthcare.html audio player time overlapped waveform on narrow screens — claude moved at the end
- healthcare.html calendar modal close button had no positioning context — claude moved at the end
- healthcare.html had orphaned mobile CSS rules outside their media query — claude moved at the end
- healthcare.html nav links vanished under 900px with no menu replacement — claude moved at the end
- index.html resynced with healthcare.html's redesign in React/Tailwind idiom — claude moved at the end
- index.html nav links vanished under 768px with no menu replacement (worse than
  healthcare.html's old bug — main page had zero mobile nav from the start) — claude moved at the end
- Test add: mobile-width run for both pages (hamburger opens panel, no horizontal
  scroll at 390px) — tests/test_mobile_nav.py — claude moved at the end
- Real Estate use-case card on main page has no link (no realestate.html yet) —
  claude moved at the end
- index.html hardcoded "Explore for clinics →" on any linked Use Cases card,
  which would have wrongly labeled the new Real Estate card too — claude moved at the end
- Built realestate.html (developer/builder vertical page), linked from config.js's
  Real Estate use-case card, added to sitemap.xml along with healthcare.html (which
  was missing too), full test coverage in tests/test_realestate.py +
  tests/test_mobile_nav.py — claude moved at the end
- Removed stray "[V 1.19 Live]" / "· v1.19" version tags from hero badges in
  config.js, healthcare.html, realestate.html and newSite/template.json — claude
  moved at the end
- Consolidated healthcare.html/realestate.html under aigenetic.in as ?mode=
  variants via a client-side vertical mode router, so both verticals show under
  the single main-site URL instead of their own; old URLs now redirect there —
  claude moved at the end
