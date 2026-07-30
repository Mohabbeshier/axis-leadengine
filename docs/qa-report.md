# QA report — 2026-07-30

Method: headless Chrome against the rendered demo (salon-09449), through the
same-origin iframe harness described in `creative-decisions.md` 099. Nothing
below is claimed from reading code; every row was measured or screenshotted.

## Instrumented sweep

| Check | 320×568 | 390×844 | 430×932 | Result |
|---|---|---|---|---|
| JS errors (window.onerror) | none | none | none | ✅ |
| document horizontal overflow | no | no | no | ✅ |
| dead images | 0 real† | 0 real† | 0 real† | ✅ |
| main script completes (index rows) | 7 | 7 | 7 | ✅ |
| gallery frames | 2 | 2 | 2 | ✅ |
| booking dialog present | yes | yes | yes | ✅ |

† the probe first reported 2: the hero frame captured mid-download under
virtual time, and the lightbox image which is legitimately empty until
opened. Neither is a defect; recorded so the number is not re-chased later.

## The pinned scene (the beige-void regression)

- `body overflow-x` measured as the sticky-killer; fixed to `clip`.
  Frame now holds `top=0` from 0%→60% of the section, then releases.
- Lines animate on a named view-timeline (`--held`) with `cover` ranges;
  screenshot at 50% depth shows exactly one line at full opacity.
- Reproduction screenshots kept: `h50.png` (broken) vs `n50.png` (fixed).

## Booking overlay (driven end-to-end in the render)

- Step 1 opens from every CTA; first tap previously threw
  `ReferenceError: SVG` — fixed, four step screenshots taken after.
- Saudi phone: `0512345678` accepted; junk blocks step 3 with the plain
  sentence, no shake.
- Final message verified to contain services+prices, total, day, name.

## Live deployment

- `https://mohabbeshier.github.io/axis-leadengine/salon-09449/` returns
  95,289 bytes; carries `#bk`, `#bridal`, `#member`; title correct.
- Serving IP is GitHub Pages (reachable from the owner's network, unlike
  Netlify, which is why Pages is the host).

## Open items (not smoothed over)

- iOS Safari with dynamic toolbars not tested on hardware — the harness is
  a fixed-height iframe. Real-device pass still owed.
- Reduced-motion render (decision 050) still owed.
- Live console/network capture is via headless dump-dom, not DevTools;
  failed-request listing on the live origin still owed.
- Lighthouse not run (not installed on this machine); page-weight budget
  tracked by byte count instead: 95KB HTML including all CSS/JS, 6 image
  requests, no JS libraries.
