# The journey — a cinematic corridor through `template.html`

Replaces the old photographic spine (`#hero`, the first `.bleed`, `.broken`,
`#held` — four sparse Unsplash stock frames) with one continuous scroll-driven
walk through nine photographs, on the *generic* outreach demo only. Nava's own
bespoke page (`sites/nava/index.html`) is untouched by this work.

## Image set — provenance and scope

The ten source photographs (`assets/nava/received-*`, per Mohab, 2026-07-30/31)
are AI-generated "luxury spa" imagery, confirmed with the client rather than
independently verified — see `docs/client-nava.md` for that exchange. Two
decisions follow directly from that:

1. **Nine of the ten are used here**, in `sites/_journey/`, as illustrative
   stock for the template every harvested salon receives — the same role
   Unsplash photography already played in `image-manifest.md`. One frame
   (`received-facial-room.png`) had a wall poster carrying legible fabricated
   text ("EXLCTING" / non-language gibberish, a classic diffusion-model tell)
   and was cropped to exclude it before use.
2. **The real Instagram photo is excluded from this pool.** One of the ten
   (`received-instagram-post-bench.jpeg`) is a genuine, verified post from
   `navasalon.sa`'s own account. Reusing a real business's actual interior as
   generic stock for a *different*, automatically-discovered salon's demo
   would misattribute their space — the opposite of illustrative. It stays
   out of `/_journey` entirely.

Assets live at `sites/_journey/`, **not** `assets/journey/` — Netlify's publish
directory and GitHub Pages are both configured to serve `sites/` as webroot
(see `netlify.toml`), so anything outside it is never actually deployed. Every
generated site references `/_journey/<scene>-<width>.jpg` as a root-relative
path, shared once across every salon rather than duplicated per-site the way
an inlined data URI would be.

| Width | Role |
|---|---|
| 640 / 900 / 1300 | CSS-fallback `srcset` |
| 1600 | Cinema-path WebGL texture |

## Two renderers, one data array

`JOURNEY` (in `template.html`'s behaviour script) is nine scenes — key,
native pixel size, an `fx` list (`bloom`, `curtain`), and a bilingual chapter
label. Both renderers read the same array; nothing is duplicated between them.

- **`buildCinema()`** — desktop, capable hardware, no reduced-motion
  preference. Loads Three.js, GSAP + ScrollTrigger, and Lenis from CDN (only
  here — a phone that doesn't qualify never fetches a byte of them). Nine
  textured planes on a Z-axis dolly; camera position is driven by
  `ScrollTrigger`'s scrub progress, not by GSAP's own pinning — the visual pin
  is native `position:sticky`, the exact mechanism `#held` already proved out
  (see decision 061/081 in `creative-decisions.md`) and it was reused rather
  than re-risked.
- **`buildFallback()`** — everything else, including the phone this page is
  actually opened on cold from WhatsApp. Nine real `<img>` frames with real
  `srcset`, cross-faded and Ken-Burns-drifted via the same `.rise`/`.uncover`
  idiom the rest of the page already uses. Zero WebGL, zero CDN weight.

Gate: `hasWebGL() && !prefersReducedMotion && !(pointer:coarse && width<760px)
&& !lowPower (deviceMemory<4 or cores<4) && IntersectionObserver`. Any CDN
script failing to load falls back the same as a phone would.

## What "2.5D" means here, honestly

No monocular depth estimation runs anywhere in this build — there's no ML
model available to do that in this pipeline, and claiming there was would be
the same kind of dishonesty the image-provenance question above was about.
What's actually built: nine image planes positioned along a camera path with a
small per-scene lateral offset, a shared drifting dust-particle field, and
vertex-displaced "curtain" sway on the two scenes flagged for it. It reads as
depth because the camera moves convincingly through real 3D space between
real photographs — not because any individual photograph was reconstructed
in 3D.

## The overlay

Only the arrival scene carries the salon name, tagline and primary CTA
(`.in`) — it fades past 7% scroll progress so the photography isn't fighting
a headline for eight more rooms. A small chapter kicker (`٠١ · الوصول` /
`Arrival`) is deliberately *not* inside `.in`: it's the one thing that
persists as a quiet wayfinding cue, positioned independently so it survives
the fade and doesn't collide with the fixed nav.

## The revisit grid (`#gallery`)

Repointed rather than removed: a real salon's own harvested Google Photos
(`C.photos`), when the pipeline has them, still outrank the illustrative
journey stills — evidence beats atmosphere. Only when there is no real photo
yet does the grid fall back to the same nine frames the journey walked
through.

## Bugs this build surfaced and fixed — see `creative-decisions.md` §11 for the full table

Short version: Lenis fighting native anchor links (103), a CDP
`clip`-parameter screenshot bug that looked like a rendering defect but
wasn't (104), ScrollTrigger's lazy first paint leaving the kicker blank at
rest (105), the headline overstaying its welcome (106), a CSS
`fill-mode:both` animation silently outranking a later inline style write
(108), and one **pre-existing** bug in the template unrelated to this
feature — `paint()` writing unconditionally to `#vName`, a child of the
loading veil the page already removes 2.4s after load, which threw on every
language switch after that point (109). All verified fixed, not just
patched — see the table for exactly how each was measured.
