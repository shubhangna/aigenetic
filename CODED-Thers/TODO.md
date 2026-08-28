# TODO
# TODO LATER
- Record a real coaching-institute admission-enquiry/demo-class-booking audio sample and add the voice-sample player back into education.html (same gap as realestate.html — see newSite/template.json assets.audio.pages.education.note)

#Done
- Moved the use-case marquee carousel to the hero section of index.html, right under the call/WhatsApp/Schedule Demo/Live Call CTA buttons, so it's visible on the first screen without scrolling — done 2026-08-28: relocated the `id="use-cases"` block (header + `<UseCaseMarquee />`) from its own section further down the page into the hero, and removed the now-duplicate section lower on the page. Nav's `#use-cases` anchor and the "Perfect for Any Business" heading (checked by test_main_page.py) still resolve correctly since the id/heading moved with it.
- Removed the Salons & Spas use-case card from index.html (config.js CONFIG.useCases) — done 2026-08-28.
- Use-case carousel now moves faster with constant (linear, no easing) motion, only pausing on hover/focus — done 2026-08-28: usecase-scroll keyframe simplified to a two-stop 0%→-50% linear tween at 32s (was a 4-stop cubic-bezier ease at 60s); pause behavior via React state on hover/focus unchanged.
- move github pages test cases to smoke from main test 

-Animate the use cases cards like health care realestate etc to move right to left slowly — already implemented: index.html's UseCaseMarquee renders the CONFIG.useCases cards twice back-to-back in a `.usecase-track` that drifts via the `usecase-scroll` keyframe (translateX 0 → -50%, 60s ease-in-out, infinite loop) for a seamless right-to-left crawl. Pauses on hover/focus (React state, not `:hover`, so keyboard focus pauses it too) and disables entirely under `prefers-reduced-motion: reduce`. Verified 2026-08-28 via a headless Playwright check: `animationName: usecase-scroll`, `duration: 60s`, 8 card-wraps rendered (4 use cases × 2 for the loop).

-Create a new site for Coaching & Schools using same pattern and templates as current 2 sites healthcare and realestate — done 2026-08-28: coaching.html built after researching coaching-institute/school pain points (missed enquiry calls, no follow-up, manual fee/attendance calls), wired into index.html's mode router, config.js Use Cases card, sitemap.xml, and newSite/template.json's pages.education. See newSite/CLAUDE.md's Resolved section.

-Renamed the mode/filename from coaching to education (?mode=coaching -> ?mode=education, coaching.html -> education.html) — done 2026-08-28. The visual card on the main page ('Schools and Coaching' title, icon, copy) was left unchanged; only the underlying URL/file identifier changed.
-header and footer should be visible for policies page also so our branding is visible and it doesn't feel like a seperate page

-Fix pages back to home link for policy pages navigating back to index instead of mode page like healthcare page

-Whey do we get results for setup and tear down if its not a standard functionality can we hide the setup and tear down so we have one line in report for each test
-
passed	tests/test_smoke.py::TestSmoke::test_realestate_page_is_up	setup	0.00s	
passed	tests/test_smoke.py::TestSmoke::test_realestate_page_is_up	call	0.91s	
passed	tests/test_smoke.py::TestSmoke::test_realestate_page_is_up	teardown	0.28s	