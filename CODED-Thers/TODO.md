# TODO
- Main page to have scrolling use cases
- Add animation like husky voice
- Add languages as a list somewhere on the site
- Policy pages quote ₹4,999-₹9,999 monthly range, actual plans are ₹2,999/₹7,999
- Real Estate use-case card on main page has no link (no realestate.html yet)
- index.html not yet resynced with healthcare.html's 2026-08-23 redesign (sticky nav
  .scrolled state, hamburger nav panel, card-style stat rail, rounded card grids,
  dark closing CTA panel, .reveal/.stagger entrances) — root CLAUDE.md requires
  main/child look-and-feel parity, so index.html needs the same treatment in Tailwind
- healthcare.html has no mobile nav on index.html's pattern to copy from — decide whether
  index.html adopts the .nav-toggle/.nav-panel markup or gets its own React equivalent

- Test add: verification of popup
- Test add: mobile-width run (hamburger opens panel, no horizontal scroll at 390px)
- Tests need HEADLESS=true env var in this sandbox (headed mode flaky/slow, no display)

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
