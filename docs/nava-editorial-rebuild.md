> **Superseded 2026-07-31 (same day).** The ivory editorial direction this
> file documents was rejected outright ("تيمبلت بدولار"). The final page is
> the dark-gold jewel-box documented in `docs/nava-final-direction.md` — the
> functional spine described here (finder, card, analytics, booking) carried
> over into it unchanged.

# Nava — editorial rebuild

## Pass 3 — the final global directive (2026-07-31, same day)

Targeted edits again, not a rewrite. Mohab's own addition: **nothing pure
white anywhere — every "white" role is cream** (`--ivory:#F7EEDE`,
`--green-text:#FBF4E6`).

- **Palette** → the directive's final tokens: ink `#17100C`, espresso
  `#23160F` (dark chapters), paper `#F6F0E7`, bone `#E9DDCF` (cards),
  bronze `#A87846` (rules/indexes on light), sage `#65745F`/`#53624E`.
- **Hero** → "وقتكِ، فوق ضوضاء اليوم." + supporting line + two CTAs
  (primary booking, secondary opens Ritual Finder). Brand label
  NAVA BEAUTY SALON & SPA replaces the old oversized Latin "Nava" h1.
- **The giant "١٠" screen is gone** — replaced by a compact proof strip
  right after the bridge: الطابق العاشر label + "أعلى من ضوضاء اليوم" +
  four verified facts, the service count computed from the dataset at
  runtime, never typed in.
- **Ritual Finder entry** is no longer a blank centered section: a split
  layout whose preview column renders one real question card and one real
  result (مساج استرخائي 350 ر.س, verified 50-min duration) from the same
  dataset the finder uses.
- **Analytics layer**: provider-agnostic `track()` pushing to
  `window.dataLayer` (no-op until the owner adds GA4/Pixel). Events:
  hero_primary/secondary_click, ritual_start/step/complete,
  recommendation_select, category_open, service_select, nava_card_create,
  booking_click (source-tagged), map_click, language_change.
- **Sticky mobile booking bar** after the hero, dismissible per session,
  never overlaps dialogs (they live in the top layer).
- Service names left the calligraphic display face (UI is body-face now);
  service cards gained a "عرض الخدمات" action label; new services/visit/
  experience headings per the directive's copy system.

Judgment calls against the directive, reasons on record: no skyline photo
in the proof strip (both skyline shots already carry the hero and the visit
anchor — its own no-duplicate rule wins); no separate "رتّبي يومك" chapter
(the Nava Card already does multi-service selection — a second flow would
duplicate it); no mobile menu drawer (single-column page, compact header
wins). Verified by CDP: hero copy/CTAs, proof strip (4 items, count=155
derived), RF preview renders real data, full finder flow fires the right
events in order (hero_secondary_click → ritual_start → ritual_step ×2 →
ritual_complete), sticky bar shows past the hero and dismisses, both
languages, reduced-motion static, zero errors, zero overflow.

## Pass 2 — the differentiation directive (2026-07-31, later the same day)

## Pass 2 — the differentiation directive (2026-07-31, later the same day)

Executed as targeted edits on the pass-1 file, not a rewrite. What changed:

- **Ritual Finder** (`#rf` + `#rfDlg`): the page's proprietary feature. Three
  questions (need / focus / budget) → max three results labelled
  الأقرب لاختيارك / اختيار بديل / تجربة أوسع → "بطاقة تجربتك" with exact
  services, prices, a computed total (only when every pick has one numeric
  price — ranges and "from" prices suppress the total in favour of "يؤكد
  الصالون الإجمالي"), optional day/name, and a WhatsApp handoff. Entirely
  deterministic: intention → keyword sets matched against Nava's own service
  names, quick-fix → verified durations (d≤40) and low list prices, budget →
  real price bands. No AI claim, no popularity claims, reasons state only
  list facts. `sessionStorage` restores the selection mid-session.
- **Hero transition re-sequenced**: outgoing text exits → outgoing image dims
  slightly → incoming image reveals by directional clip-path wipe at full
  opacity (the wipe edge divides the photographs; nothing ever blends) →
  incoming text enters. Grade lightened to protect only text zones; Arabic
  display lines widened 16ch→24ch to stop over-breaking.
- **Header**: real nav (التجربة / اختاري تجربتك / الخدمات / الزيارة) on
  ≥980px, theme flip measured from `#chExp.offsetTop` instead of a viewport
  multiple that flipped while the hero was still dark.
- **Bridge** after the hero (one line, dark→ivory gradient, no image) and
  **Above the City** — a typographic moment (١٠ + سطران), deliberately
  image-free because both skyline photographs already carry other chapters
  and the directive itself forbids repeating them.
- **Signature Moments**: one asymmetric composition (ritual large, treatment
  vertical, café small) with Arabic-first titles; English demoted to small
  captions.
- **Service cards**: number, Arabic name, English secondary, real per-chapter
  count (from `items.length`), verified from-price, arrow affordance.
- **Experience** 60/40 image/copy in one viewport; proof points numbered
  rows, not icon cards. **Magazine** ~61/39 split + "من داخل نافا" label +
  champagne rule. **Visit**: map became a visible ghost-button action.
- **Green tokens** per directive (`#6F8267`/`#5F7158`, text `#FFFAF2`);
  consecutive same-ground chapters share one padding breath, not two.

Verified by CDP (not assumed): finder flow end-to-end with correct filtering
(nails + under-200 → 20/30/175 ر.س items only), card total arithmetic
(30+20=50), session restore after close/reopen, both languages repainting the
open dialog, nav present on desktop / hidden on mobile, hero static +
reveals-in under reduced motion, booking handoff intact, zero console errors,
zero horizontal overflow.

## Pass 1 — the six-chapter editorial rebuild

2026-07-31, fourth pass. The seven-scene WebGL journey — built and refined
across this session's earlier passes, storyboarded and approved along the
way — was rejected outright by directive, not by preference: "the current
concept has failed... looks like a virtual gallery, not a real spatial
journey." The directive is explicit that this isn't a request to improve the
gallery; it's a replacement. This document is the planning deliverable the
directive requires before implementation, kept to what's actually decided —
not padded to look thorough.

## 1. Current-state diagnosis

The whole homepage was one `#journey` section, `height: 7×100svh`, pinned via
`position:sticky`, driven by a Three.js dolly (desktop) or a cross-fading
`<img>` stack (fallback). Three named failures, matching the directive's own
list: photographs sat as flat planes in a black void with heavy letterboxing
on portrait images at wide viewports; unrelated rooms (reception, hammam,
manicure, treatment, massage, mirror, lounge) were staged as one continuous
3D space they don't actually share; business content (services, visit info)
existed only as overlays inside that pinned section, with no ordinary page
beneath it. Booking, pricing, and the language toggle were never the
problem — those stay.

## 2. Code removal

Everything under "THE ENGINE" — `buildFallback`, `buildCinema`, `runCinema`,
the Three.js/GSAP/ScrollTrigger/Lenis CDN loads, `JOURNEY`, `setChapter`,
`setContinuous`, `fovAt`, all `#journey` CSS — is deleted, not disabled. No
WebGL context ships on this page anymore. GSAP + ScrollTrigger stay, scoped
to the three-scene hero only, loaded once, with a `matchMedia` split for
desktop/mobile timelines. No Lenis — native scroll for the whole page below
the hero is simpler and is what "return to normal document scrolling
immediately after the hero" requires.

## 3. Verified business-data preservation

`CONFIG` (name, WA number, phone display, address, maps link, Instagram, the
155-item `menu`), `T` (bilingual strings), and every function in the
"business logic" block — `nameOf`, `priceOf`, `lowOf`, `catName`, `pick`,
`paintList`, `openList`, `paintServiceChips`, `paintVisit`, `paint`, the
3-step `step()` booking state machine, `openDlg` — carry over unmodified.
Nothing here caused the rejection; the directive's own Phase 8 says preserve
the dataset and prices as-is.

## 4. Image audit

Nine photo sets exist at `journey/<key>-{640,900,1300,1600}.jpg`; all nine
get a distinct role, none dropped, none doubled:

| Key | Subject | New role | Notes |
|---|---|---|---|
| `arrival` | wide reception, golden light | Hero scene 1 | already the widest establishing shot; unsafe zone: the Nava wall sign, upper-right |
| `spa` | manicure, client + technician | Hero scene 2 | unsafe zone: hands, technician's working area, client's face |
| `massage` | treatment bed, skyline window | Hero scene 3 | unsafe zone: window/skyline — the whole point of the shot |
| `reception` | second wide lounge shot | Experience chapter | previously cut from the narrative for repeating arrival's job — as a single editorial image next to text, not a story beat, it isn't repeating anything |
| `ritual` | hammam tray, candle | Signature Moments — "The Ritual" | |
| `treatment` | treatment room | Signature Moments — "The Treatment" | |
| `cafe` | Nava café counter | Signature Moments — "The Pause" | unused since the 7-scene cut; back in play here as a distinct card, not a narrative beat |
| `beauty` | rollers, sunglasses, Nava magazine | Editorial Brand Moment | unsafe zone: face, magazine cover, hands — no pills or buttons over it, per directive #111 |
| `finale` | flower arrangement, lounge, skyline | Visit & Booking — final anchor | unsafe zone: the flower arrangement itself |

`reception-wide` in the old docs table was a naming description, not a file
key — the actual cut file is `reception-*.jpg`, sitting unused since the
seven-scene pass. It's the one image this rebuild needed that was already on
disk with nothing left to shoot or source.

## 5. Six-chapter storyboard

1. **Cinematic hero** — three scenes, one pinned viewport, ~260svh desktop /
   ~200svh mobile. Arrival (brand, architecture) → Trust (manicure, human
   care) → Held (stillness, skyline). Releases into normal flow after scene 3.
2. **Nava Experience** — ivory ground. `reception` image, editorial split,
   heading + one line of body copy + three verified proof points as text, not
   icon cards.
3. **Signature Moments** — ivory ground, three distinct compositions
   (alternating image/text sides), no identical cards, no continuous motion.
4. **Service Discovery** — five categories + one overflow group, opens the
   existing priced sheet.
5. **Editorial Brand Moment** — dark ground, `beauty` image full-bleed or
   large-format, copy beside it on desktop, stacked on mobile, one text CTA.
6. **Visit & Booking** — dark ground, `finale` image, verified address/hours/
   contact, one dominant WhatsApp CTA.

Dark→ivory→ivory→ivory→dark→dark gives three ground changes across six
chapters — enough contrast to break the "entire page is dark" failure
without turning it into an alternating stripe pattern.

## 6. Desktop composition

Hero: full-bleed image, text anchored to each scene's own negative space
(arrival: lower-start block, same position the current hero copy already
uses; trust: upper-right, clear of the manicure action; held: lower-left,
clear of the window). Experience and Editorial Brand Moment: 50/50 editorial
split, image one side, text the other. Signature Moments: alternating
60/40 image/text split per card. Service Discovery: category grid, 3-up.
Visit: same split pattern as Experience, form-style detail list opposite the
image.

## 7. Mobile composition

Hero scenes stack their text below the safe two-thirds of the frame, never
over a protected zone; shorter scroll length (~200svh vs 260svh) since three
short holds read fine at hand-scroll speed without desktop's slower pace.
Every editorial split below the hero becomes image-on-top, text-below —
mobile is not a cropped desktop layout, each section's `object-position` is
set per breakpoint, not inherited. Service category grid becomes 1-up scroll,
sheet dialogs stay full-height bottom sheets (unchanged from before).

## 8. Motion plan

One `ScrollTrigger.create` per hero scene transition (`scrub`, opacity +
small `translateY`/`scale` on the *content* inside the pinned frame, never on
the pinned element itself), gated through `gsap.matchMedia()` for the
desktop/mobile duration split. Below the hero: plain CSS
`@media(prefers-reduced-motion: no-preference)` entrance transitions
(opacity + 12px translate) triggered by `IntersectionObserver`, no GSAP —
these are one-shot reveals, not scroll-scrubbed, so ScrollTrigger isn't
needed for them. `prefers-reduced-motion: reduce` disables the hero pin
entirely (renders as three stacked static images) and skips every entrance
transition — full content, zero motion.

## 9. Service-discovery interaction plan

Homepage shows five cards: hair, skin, nails, body, lash — plus one
"المزيد من خدمات العناية" card covering micro + care (the two smallest,
most specialised chapters). Each card opens the same `#pl` priced-sheet
dialog and `openList(key)` function already built; the overflow card opens a
small chooser between micro/care first. `pick()` still hands the exact
chosen service and price into the existing `step()` booking flow unchanged.

## 10. Acceptance checklist

- [ ] No WebGL context, no Three.js/Lenis script tags.
- [ ] Hero is exactly 3 scenes, images full-scale from first paint (no
      thumbnail-to-fullscreen grow).
- [ ] Normal document scroll resumes immediately after the hero.
- [ ] Six chapters, each with one job, no image reused across chapters.
- [ ] Five service categories + one overflow group on the homepage; full
      155-item sheet and booking handoff still work.
- [ ] WhatsApp CTA uses the muted botanical green, not the neon brand green.
- [ ] `prefers-reduced-motion` yields a fully readable, fully static page.
- [ ] No console errors, no horizontal overflow, desktop + mobile + RTL + LTR.
- [ ] Booking flow composes the correct WhatsApp message end to end.
- [ ] No rating, award, client count, or unverified claim anywhere on the page.
