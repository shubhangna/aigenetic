# TODO

- Bring back the use cases page with the current theme (the old vertical pages — healthcare, real estate, education — are in ___Archive/) (added 2026-11-13)
- SEO optimization — partly done 2026-11-16 (see Done). Still open: a blog and a /clinics landing page (added 2026-11-13)
- Booking modal: on short screens (under ~740px of browser height, e.g. a 1366x768 laptop) Google's booking form (a fixed ~630px dialog) still needs an inner scroll to reach Book / Cancel. Fix options: scale the iframe down to fit, or open the booking page in a new tab on short screens (added 2026-11-13)

## Needs your input before it can be built (site review, 2026-11-16)

- Booking calendar only offered 7:00pm and 7:30pm for the next day. This is set in the Google Calendar appointment schedule, not in the site code: open more daytime slots there.
- Analytics: no GA4 / Microsoft Clarity / Meta Pixel. Needs the GA4 measurement ID, Clarity project ID and Pixel ID. The privacy policy must also mention them once they are added.
- A real "try it" in the hero: "Enter your number, our AI calls you in 30 seconds" needs a backend endpoint that triggers the outbound call; a "Call the demo line" link needs a dedicated demo number. (Hero now has a "Chat on WhatsApp" button with a prefilled message to the main number.)
- Proof: client logos, testimonials, real numbers (calls answered, % booked without a human) or a founder note with name and photo. Needs real content; nothing was invented.
- Appointment-centric sample calls (Hindi dental booking, Hinglish reschedule, WhatsApp follow-up) need new recordings. Transcript toggle beside each waveform needs the transcript text of each recording.
- Pricing: an all-in "Front Desk" bundle price, or an ROI line ("one missed appointment ≈ ₹X"), needs your numbers.
- Integrations row (Google Calendar, Calendly, Practo, WhatsApp Business API, Exotel/Twilio): only list the ones that are actually supported; the FAQ currently says no calendar integration is assumed.
- Footer trust layer: GST number, CIN, "Data stays in India" and DPDP wording need the real registration numbers and a claim you can stand behind.
- Language toggle (EN / हिंदी): needs a reviewed Hindi translation of the whole page.
- "Book a demo" does not state a call length (the review said the booking is 30 minutes). Add "15-min" / "30-min" to the label once the Google schedule length is settled.
- Automated tests were not re-run after the 2026-11-16 changes (the local server could not be started in that session). Run `testsNpush.bat`.

# Done

- Samples intro no longer shows the leaked developer note — done 2026-11-16: now "Hear how it sounds in six industries…", eyebrow "Sample calls". Comment - claude moved
- "Try the autopilot" renamed to "Book a demo" on every CTA (index.html nav, mobile menu, hero, closing; header and mobile menu of the three policy pages; tests/test_smoke.py) — done 2026-11-16. Comment - claude moved
- Logo: header and footer now load logo/logo.png (133×123, 14 KB) instead of the 759×704 logoMedium.png (187 KB), with alt="Aigenetic logo", on index.html and the three policy pages — done 2026-11-16. Comment - claude moved
- Sample calls reordered front-desk first: Healthcare, Hospitality, then EdTech, E-commerce, BFSI, Recruitment — done 2026-11-16. Comment - claude moved
- "Illustrative" hedging cut from 8 places to one footnote under the WhatsApp sample ("Sample scenario, shown for illustration."); pricing intro and pricing note rewritten so they no longer undercut the plans — done 2026-11-16. Comment - claude moved
- Pro plan carries a "Recommended" badge — done 2026-11-16. Comment - claude moved
- Industry tabs (Clinic / Salon / Real estate / Coaching) on the hero journey card swap its copy; the timeline now plays step by step on load and on each tab switch (off under reduced motion) — done 2026-11-16: index.html, assets/js/home.js, assets/css/home.css. Comment - claude moved
- Footer shows the Pune address from the schema (Rajiv Gandhi Infotech Park) on index.html and the three policy pages — done 2026-11-16. Comment - claude moved
- Phones (≤760px): sticky bottom bar with Call / WhatsApp / Book a demo on the homepage — done 2026-11-16. Comment - claude moved
- SEO: new "Who it's for" section (#who) using the search phrases, FAQPage JSON-LD for the 7 existing questions, meta keywords updated — done 2026-11-16. Comment - claude moved
- Polish: feature cards' tag and title rows reserve two lines so the body copy starts level; the "→ ↗" arrows that looked like dead links were removed — done 2026-11-16. Comment - claude moved
