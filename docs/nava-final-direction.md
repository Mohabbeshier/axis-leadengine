# Nava — the final direction (autonomous)

## FULL-SITE REVIEW — 100 decisions (2026-08-01, the whole-look pass)

**Hero (1–12):** 1 scene-2/3 lines were pinned to the bottom edge with weak
contrast on light bedding — now glass captions (blur + warm scrim, radius
16) lifted higher. 2 headline gets a drop-shadow safety net for any photo.
3 molten gradient kept at 12s. 4 word-rise stagger kept. 5 frame draw kept.
6 both CTAs confirmed (green=WA, ghost=finder). 7 fine print at 78% cream
confirmed. 8 scroll cue cream confirmed. 9 LCP preload confirmed. 10 wipe
sequencing untouched. 11 static fallback re-checked. 12 h1 15ch cap kept.

**Statement band (13–20):** 13 stmt in Alexandria ink confirmed. 14 stats
rose numerals confirmed. 15 count-up once confirmed. 16 bilingual stat
labels stay. 17 band stays cream. 18 no facts list (deduped earlier) —
right call, stands. 19 spacing tightened earlier, stands. 20 no rule
between stmt and stats (hairline only above stats).

**Kickers/mood (21–28):** 21 every kicker now opens with the rose ✦ — one
brand rhythm across all chapters. 22 kickers rose-deep on cream, blush on
photos, confirmed. 23 the finder's Latin kicker keeps its tracking.
24 Arabic never tracked (law, re-verified). 25 gold reserved for
labels/prices/numerals. 26 sage reserved for WA. 27 rose is the one accent
family. 28 footer credit carries the ✦ too.

**Experience/immersive (29–36):** 29 full-bleed image chapter confirmed.
30 shade protects only text zones. 31 numbered facts on-image confirmed
legible. 32 track blush on photo. 33 reveal stagger fine. 34 no numeral
here (calm) — kept. 35 proof rows max-width 560 kept. 36 image eager-safe
via walk check.

**Finder (37–44):** 37 blush panel + rose gradient border confirmed.
38 interactive preview chips (tap = answered) confirmed working. 39 result
card real data confirmed. 40 rose CTA + browse link confirmed. 41 dialog
steps rose. 42 sheet drag-handle present. 43 aria-pressed rose fills.
44 finder logic untouched.

**Moments (45–52):** 45 horizontal pin desktop / stack mobile confirmed.
46 mobile numerals live ON the photo (cream + shadow) — reads deliberate.
47 captions gutter-padded. 48 heading clears the glass header. 49 images
edge-to-edge mobile. 50 EN rebuild of the pin on toggle confirmed. 51 no
auto-motion inside panels. 52 kicker gets the ✦ like everyone.

**Cards river (53–62):** 53 photo cards over rows — confirmed the right
call. 54 drift 26px/s calm. 55 drag + click-suppression verified. 56 RTL
anchor fix documented. 57 gradient scrim bottom-heavy for names. 58 go2
glass circle affordance. 59 num cream top-start. 60 reduced = native
scroll, 6 cards. 61 search field gains a drawn search glyph (affordance).
62 more-results opens the best-matching category (bug fixed earlier,
stands).

**Ticker (63–70):** 63 single line confirmed. 64 pixel-math engine
confirmed on-view moving. 65 pauses offscreen/hidden. 66 edge fades as
overlays (iOS-safe). 67 Alexandria 600 presence. 68 ✦ separators rose.
69 reduced = one static centered segment. 70 borders champagne-alpha.

**Editorial + Visit (71–84):** 71 editorial full-bleed + overlay confirmed.
72 rose-light text-cta confirmed. 73 glow drift both deep chapters.
74 bento three-hue system stands. 75 today-row logic verified again.
76 chips real anchors. 77 copy pill stable. 78 booking panel is the
closer. 79 under-560 stacking (wrap fix) stands. 80 icons hue-matched.
81 open-chip state colors. 82 no black anywhere re-verified. 83 footer
clearance for the FAB. 84 map ghost beside WA.

**System (85–100):** 85 index FAB cream circle both grounds. 86 panel
numbers rose. 87 sticky bar deep glass; hides at visit. 88 dialogs share
the material. 89 press states everywhere interactive. 90 reveals one
bezier. 91 focus rings rose. 92 selection rose. 93 grain 4%. 94 no new
fonts/libraries. 95 walk re-run after edits. 96 flows re-run (booking/
search/finder). 97 EN parity re-run. 98 reduced matrix re-run. 99 zero
errors / zero overflow gates. 100 this list written before the edits it
describes — the contract.

## VISIT CHAPTER — 100 decisions (2026-08-01, "مش عايز دي حتة واحدة")

**A. Anatomy (1–10):** 1 the monolith dies — one dl-slab becomes four
units. 2 unit one: heading + live chip. 3 unit two: a bento of three fact
cards. 4 unit three: a booking panel with its own ground. 5 unit four:
photograph stays the chapter's opening. 6 address card is full-width.
7 hours + contact share a row (2-up) on every viewport wide enough.
8 stack gracefully under 360px. 9 the bento sits inside the text column,
not spanning the photo. 10 DOM ids/data-t hooks unchanged — the language
engine never knows.

**B. Card material (11–20):** 11 radius 16. 12 each card its own tint,
not one shared grey. 13 address = rose tint. 14 hours = champagne tint.
15 contact = sage tint. 16 borders 1px of the same hue at low alpha.
17 icon chip inherits the card hue. 18 labels take the card hue too.
19 values stay cream for reading. 20 press state: card compresses
(scale .985) + tint deepens.

**C. Address card (21–30):** 21 the address text is the maps link —
whole value tappable. 22 copy pill lives inside the card, end-aligned.
23 copy → "اتنسخ ✓" for 1.8s (already wired). 24 pin icon chip rose.
25 two-line clamp, no overflow. 26 tower + floor stay on their own line.
27 no district repetition beyond the verified string. 28 external-link
affordance: small ↗ after the address. 29 map ghost button remains in the
booking panel (two routes to maps is fine — different moments). 30 rtl/ltr
mirroring by logical properties only.

**D. Hours card (31–40):** 31 hours split into two structured rows, not a
<br> string. 32 TODAY's row is highlighted — computed from Riyadh time.
33 highlight = rose dot + cream-strong + 600 weight. 34 the other row dims
to 55%. 35 Friday logic exact (row B on day 5). 36 clock icon champagne.
37 the live chip stays at the heading — the card doesn't repeat
open/closed state. 38 tabular numerals. 39 line-height 1.7 for Arabic
numerals. 40 EN mirrors the same structure.

**E. Contact card (41–50):** 41 the number is a large tappable wa.me
link. 42 under it, two action chips: WhatsApp + Instagram. 43 chips carry
brand hues (sage / rose). 44 chips are real anchors ≥44px. 45 phone icon
sage. 46 the number keeps LTR isolation. 47 IG handle shortened to
@navasalon.sa. 48 chips get press states. 49 no third-party icons beyond
the existing WA glyph + a drawn camera glyph. 50 track() on both chips.

**F. Booking panel (51–60):** 51 its own surface: blush-on-mocha gradient
with rose top hairline. 52 radius 20, padding generous. 53 one line of
honest reassurance (the no-app/no-signup line, reused). 54 WA CTA stays
green — the one green on the page. 55 map ghost sits beside it. 56 both
full-width stacked under 420px. 57 sheen stays on the WA CTA only.
58 panel enters with the same reveal as everything else. 59 panel is the
chapter's last word before the footer. 60 no extra links competing inside.

**G. Color discipline (61–70):** 61 three hues only: rose, champagne,
sage. 62 all three already exist in the system — nothing new invented.
63 tint formula uniform: 14–18% bg, 35–40% border. 64 icon chip = same
hue at 20%. 65 cream text everywhere for values. 66 chip hue = state
(green open / rose closed) unchanged. 67 gold reserved for labels +
numerals. 68 glow stays behind everything (z-0). 69 no pure white, no
black. 70 contrast ≥4.5:1 for values, ≥3:1 for labels.

**H. Motion (71–80):** 71 cards reveal staggered 60ms via existing
system. 72 press compress 120ms. 73 chip dot keeps its 2.2s pulse.
74 copy pill morphs color only — no layout shift. 75 today-dot pulses in
sync with the chip. 76 no hover-lift on touch. 77 desktop hover: border
brightens, nothing moves. 78 reduced-motion: zero animation, all content.
79 no parallax here — it's the reading room. 80 glow untouched (26s).

**I. Layout maths (81–90):** 81 bento gap .8rem. 82 card padding 1.1rem.
83 icon chip 38px. 84 label .7rem. 85 value .95–1rem. 86 hours/contact
minmax(0,1fr) each. 87 address value max 2 lines then wraps naturally.
88 the panel clears the index FAB (existing footer clearance covers it).
89 total chapter height shrinks vs the monolith. 90 zero horizontal
overflow at 320px.

**J. Verification (91–100):** 91 today-highlight asserted for the actual
Riyadh weekday at test time. 92 chips tappable → correct hrefs. 93 copy
verified again post-refactor. 94 EN full parity screenshot. 95 reduced
static + complete. 96 booking + map flows from the panel. 97 zero console
errors. 98 zero overflow 390/1440. 99 eyeball pass on the final render
before showing. 100 documented here before implementation — this list.

## THE ROSE PIVOT — 2026-07-31, after Mohab's phone review

Verdict on the jewel-box: the ambience read as noise not wow ("ازعاج اكتر
من ابهار"), the marquee stalled and looked dated, the site is dark with
black while **Nava's own logo is dusty rose** — the brand color the site
ignored. Plus: a collapsible index arrow, a smart service-selection
section, and trend research. Research done (Colorlib/Figma/Envato/Fireart
2026 roundups): expressive type on heroes only, bento-informed modules,
bold personality color, fewer-but-better interactions; kinetic gimmicks
that run everywhere are the thing that reads dated.

### 20 decisions × 10

**D1 — The brand's rose is the palette's anchor.** 1 rose `#B08585` from
the logo itself. 2 deep rose `#8E6163` for hover/strong. 3 blush surface
`#EFDFD8`. 4 cream ground `#F7F0E8`. 5 no pure white. 6 champagne `#C9A875`
survives only as hairline/numeral jewelry. 7 sage stays exclusively on
WhatsApp actions. 8 muted text `#8F7A72`. 9 selection/focus recolored rose.
10 theme-color meta updated.

**D2 — Black is banned; depth is rose-mocha.** 1 deep chapters `#40312C`.
2 raised-on-deep `#4C3B36`. 3 text ink `#3B2A25` — warm, never #000.
4 grep-verified: no #000/#0C0805 remains. 5 hero grade warm smoke, not
black veils. 6 dialog sheets rose-mocha. 7 shadows are rose-tinted.
8 borders from rose at low alpha. 9 image vignettes warm. 10 the OG/meta
descriptions unchanged — color is presentation, not facts.

**D3 — Cream is the ground; deep is the accent.** 1 base page cream.
2 hero (photo-led) + editorial + visit are the only deep chapters.
3 ~65/35 light-to-deep rhythm. 4 header flips cream-glass after the hero.
5 proof band cream. 6 finder blush-on-cream. 7 menu cream. 8 moments
cream→blush wash. 9 footer cream. 10 sticky bar deep glass on mobile.

**D4 — Typography modernized; the calligraphic era ends.** 1 Aref Ruqaa
removed everywhere. 2 display = Alexandria (modern Arabic geometric).
3 body stays Almarai. 4 Latin jewelry stays Marcellus. 5 El Messiri
retired. 6 weights pruned (300/400/500/700). 7 hero clamp 2.4→5rem.
8 h2 clamp 1.8→2.8rem. 9 no letter-spacing on Arabic (law). 10 fallbacks
warm serif for Latin, system Arabic sans otherwise.

**D5 — Kinetic type on the hero only (trend reality-check).** 1 word-rise
stagger kept. 2 champagne-cream shimmer gradient kept but slowed. 3 no
kinetic anywhere else. 4 re-split on language toggle kept. 5 static under
reduced motion. 6 no letter splits (Arabic shaping). 7 scenes 2/3 lines
plain cream. 8 CLS-safe (transforms only). 9 crawlable text intact.
10 hero label Marcellus tracked (Latin only).

**D6 — Ambient noise deleted.** 1 gold-dust canvas removed. 2 marquee
removed. 3 rosette SVG removed. 4 grain kept at 4% (texture ≠ noise).
5 sheen kept on primary CTAs only. 6 breathing scroll cue kept. 7 no
looping background animation elsewhere. 8 dialogs unchanged motion.
9 fewer IO reveals (blur removed — cleaner). 10 the deleted code is gone,
not display:none.

**D7 — Motion budget: fewer, better.** 1 reveals = rise+fade only.
2 stagger caps at 3 children. 3 hover states do one thing each. 4 cursor
glow kept, rose, desktop only. 5 magnetic CTAs kept ≤6px. 6 count-ups
kept. 7 horizontal journey kept (scrub, no snap). 8 frame-draw kept on
hero card, rose stroke. 9 everything transform/opacity. 10 reduced-motion
matrix re-verified.

**D8 — The index (الفهرس): a floating arrow that opens the map.** 1 fixed
pill bottom-start, all viewports. 2 arrow rotates 180° on toggle.
3 panel lists the six chapters, numbered. 4 smooth clip reveal.
5 aria-expanded + aria-controls wired. 6 Esc and outside-click close it.
7 current chapter highlighted on open (scroll position). 8 links smooth-
scroll and close. 9 never overlaps dialogs (z below top layer). 10 label
"الفهرس" / "Index" via the existing T engine.

**D9 — Smart service selection.** 1 an inline search field in the services
chapter — type anything, matches across all 155 AR+EN names live.
2 results show name + chapter + exact price. 3 tapping a result goes
straight into booking with that service (existing pick()). 4 empty query
shows nothing (no noise). 5 ≤6 results shown, "+N أكثر" opens the sheet.
6 a "مش متأكدة؟" chip opens Ritual Finder. 7 keyboard: arrows + Enter.
8 category rows stay below as the browse path. 9 tracked as service_search
events. 10 zero new data — same CONFIG the sheet uses.

**D10 — Menu rows stay typographic, recolored.** 1 names ink on cream.
2 prices deep-rose Marcellus. 3 hover sweep rose. 4 numerals champagne.
5 EN echoes muted. 6 counts muted. 7 arrow rose. 8 hairlines rose-alpha.
9 hover background blush tint. 10 same DOM contract (paintServiceGrid
untouched).

**D11 — Horizontal journey kept, humanized.** 1 stays desktop-only pin.
2 panels on cream with blush wash. 3 numerals champagne outline.
4 captions ink. 5 image grade brightened. 6 RTL/EN rebuild kept.
7 vertical stack mobile/reduced. 8 heading kicker rose. 9 no auto-motion
inside panels. 10 progress unchanged (scrub position is the progress).

**D12 — Hero photography breathes again.** 1 brightness veil lifted
(.82→.9). 2 grade tint rose-warm not gold-brown. 3 text zones protected
by local gradients only. 4 frame stroke rose. 5 card padding tightened.
6 CTAs: WA green primary + rose ghost secondary. 7 fine print cream 70%.
8 scene lines cream, larger, no calligraphy. 9 LCP priority kept.
10 wipe engine untouched.

**D13 — Statement band on cream.** 1 stmt line Alexandria ink. 2 stats
rose numerals. 3 bilingual stat labels kept. 4 facts row with rose ✦.
5 hairlines rose-alpha. 6 count-up kept. 7 tighter padding (was airy).
8 no lead duplication — proofLbl/Em kept as one quiet line. 9 cream bg.
10 same IDs (paint hooks).

**D14 — Finder = blush jewel on cream.** 1 panel blush, rose gradient
border. 2 preview cards cream. 3 selected chip rose. 4 result prices
deep-rose. 5 CTA rose (not green — it's not WhatsApp). 6 browse text-link
rose. 7 dialog steps rose. 8 aria-pressed rose fills. 9 reasons stay
muted. 10 logic byte-identical.

**D15 — Editorial chapter deep rose-mocha.** 1 bg `#40312C`. 2 headline
cream Alexandria. 3 label champagne. 4 image full-bleed brightened.
5 shade gradient warm. 6 text-cta rose-light. 7 one chapter, one image
(unchanged). 8 no black overlay. 9 numeral removed here (calmer). 10 copy
unchanged.

**D16 — Visit chapter deep, conversion-first.** 1 bg deep mocha. 2 heading
Alexandria cream. 3 labels champagne. 4 WA CTA green + map ghost rose.
5 rows hairline cream-alpha. 6 image brightened. 7 footer back to cream.
8 sticky bar deep glass. 9 phone/IG links cream. 10 schema untouched.

**D17 — Dialogs join the new material.** 1 sheets rose-mocha. 2 borders
warm. 3 titles cream. 4 selected states rose. 5 prices champagne.
6 search caret rose. 7 steps rose. 8 WA sends stay green. 9 close targets
44px. 10 zero logic edits.

**D18 — Image grade v2.** 1 light-page images: saturate 1.05, no sepia
veil. 2 rose soft-light tint 12%. 3 hero keeps stronger grade for text.
4 no image on cream gets darkened. 5 aspect ratios unchanged (CLS 0).
6 srcset pipeline unchanged. 7 alt hooks unchanged. 8 editorial/visit
images slightly deeper. 9 grain global 4%. 10 no new assets — same nine
photographs.

**D19 — Performance & a11y hold the line.** 1 fonts: 3 families (Ruqaa+
Messiri out, Alexandria in). 2 canvas gone = one less rAF. 3 marquee gone
= one less compositor layer. 4 index/search JS ≈ 2KB. 5 contrast: ink on
cream 10:1, cream on mocha 9:1, rose-deep on cream 4.6:1. 6 focus rings
rose. 7 keyboard walk re-tested. 8 touch targets ≥44px. 9 reduced-motion
full matrix. 10 no new libraries.

**D20 — Verified, not assumed.** 1 CDP full-flow suite re-run. 2 search:
type→result→booking verified with a real service. 3 index open/close/jump
verified. 4 no-black grep. 5 both languages. 6 mobile 390. 7 reduced
motion. 8 zero console errors. 9 zero overflow. 10 screenshots reviewed
before reporting.


2026-07-31. Mohab's verdict on the directive-driven builds: "شغل عادي وتافه
اشتريه بدولار — دا تيمبلت." Mandate: stop executing briefs, make ~200 real
decisions myself, use the model's judgment, review the whole project record,
understand him psychologically/intellectually/practically, build a map, then
execute. This is the last revision. This document is that map.

## I — The read

**The record.** Across two projects (template.html + Nava) he rejected, in
order: minimal ivory editorial ("كويس بس مش مبهر"), generic dark-gold over
raw stock ("صامت وعادي، ملوش مود ولا روح"), the WebGL gallery ("gallery with
text overlays"), the ivory editorial rebuild ("moodboard"), and now the
final ivory-dominant product page ("تيمبلت بدولار"). The ONE direction he
approved — built hands-on, documented in memory — was template.html v3:
**jewel-box dark+gold, one forced warm color-grade unifying every image,
typography-as-spectacle (huge Arabic display with molten-gold shimmer),
bespoke ornament, and a page that feels alive while idle.** His words for
the target: **مبهر، مود، روح.**

**Psychologically.** He judges in the first three seconds by feeling, not
by information architecture: "هل ده غالي؟ هل ده مبهر؟" The ChatGPT
directives he forwards optimize for UX correctness — ivory clarity, quiet
luxury, Baymard citations. That is a web designer's taste, not his and not
his buyer's. His buyer is a Jeddah salon owner opening the link on her
phone at night: a dark screen where her own salon glows in gold reads as
"البروشور بتاع الريتز" — that sells. Cream information design reads as a
Squarespace theme — that gets him one dollar.

**Intellectually.** He is not against function — he demanded the finder,
prices, booking stay real. He is against function *wearing* the design.
The design must be the spectacle and the function must live inside it.

**Practically.** He sells demos. The demo must be demonstrable in 20
seconds of thumb-scrolling in front of a client: an opening that stuns,
motion that feels alive, gold everywhere disciplined, then "وده كله شغال —
دوسي هنا واحجزي."

**Forecast.** Ship another tasteful-quiet page → rejected. Ship drama
without the working spine → "فاضي". Ship the v3 jewel-box formula, scaled
up, wrapped around the working product → this is the version he shows
people.

**Connectors.** Checked and deliberately not used: Higgsfield could
generate new imagery, but demo honesty + the client's approved photo set
rule it out; Figma/Canva add a round-trip for a deliverable that is code.
The nine approved photographs + CSS art direction are the raw material.

## II — 200 decisions

### A. Brand & world (1–20)
1. One world: a dark gold jewel-box, edge to edge — no ivory chapters at all.
2. The approved v3 formula is the law: grade, spectacle type, ambient life.
3. Positioning line stays "وقتكِ، فوق ضوضاء اليوم" — it earned its place.
4. The tenth floor is treated as scenography (glow above a dark city), not a stat card.
5. Photography is the second voice, typography is the first.
6. Every image passes one forced warm-gold grade — no photo may break the palette.
7. Gold is light, not paint: it appears as glow, shimmer, hairline — never flat fills.
8. Cream replaces every white (Mohab's standing order).
9. Green stays only on WhatsApp actions — it is a signal, not a brand color.
10. No section exists without a job: stun, prove, guide, list, or book.
11. Arabic leads everywhere; Latin is jewelry (labels, numerals, captions).
12. The page must feel alive while idle: dust, shimmer, marquee, breathing cues.
13. No invented facts survive: no ratings, no "الأكثر طلبًا", no outcomes.
14. The 155-service dataset, finder, card, booking, analytics: untouched logic.
15. The demo is phone-first in feel, desktop-first in spectacle.
16. Reduced motion gets a still jewel-box, never a broken one.
17. One scroll story: arrival → world → guidance → menu → editorial → visit.
18. Nothing pinned after the hero except the signature horizontal chapter.
19. Ornament is bespoke (drawn SVG rosette), never emoji, never stock flourishes.
20. The wordmark "Nava" in the header stays quiet — the hero owns the spectacle.

### B. Color system (21–40)
21. Ground `--noir #0C0805` — near-black with warmth, not #000.
22. Chapter alt `--esp #16"0E"08` espresso for tonal breathing between sections.
23. Raised surfaces `--raise #221509` (dialogs, cards, menu hovers).
24. Primary type `--cream #F2E7D4`; emphasis `--cream-strong #FBF3E3`.
25. Gold `--gold #D3A95C` for accents; `--gold-deep #9C7434` for strokes/outlines.
26. Muted type `--sand #A8977E` — captions, meta, fine print.
27. Hairlines: gold at 16% opacity — visible discipline, not decoration.
28. WhatsApp green deepened to `#75866B`, text cream — no neon on this ground.
29. The molten-gold text gradient: deep→bright→deep animated at 8s.
30. Image overlay tint: gold soft-light at 18% over every photograph.
31. Image filter: sepia .25, saturate 1.15, brightness .9, contrast 1.06 — one grade.
32. Focus rings gold, 2px, offset 3px — luxury must still be keyboard-visible.
33. Selection: gold background, noir text.
34. Scrollbar left native — custom scrollbars read as gimmick.
35. Dialogs share the raise surface + gold hairline — one material system.
36. The sticky bar is espresso glass (blur) with cream type.
37. No pure #FFF anywhere in the file — verified by grep before ship.
38. No grey anywhere — every neutral carries warmth.
39. Errors/empty states use sand, never red — nothing on this page is an error.
40. Grain overlay stays at 5% — texture, not noise.

### C. Typography (41–60)
41. Display Arabic: **Aref Ruqaa** — the face Mohab approved for spectacle.
42. Aref Ruqaa is reserved for the hero headline + chapter statements only.
43. Secondary display: **El Messiri** for section h2 — presence with legibility.
44. Body/UI Arabic: **Almarai** 300/400/700 — prices, lists, buttons, forms.
45. Latin display: **Marcellus** — the luxury-hotel face, for labels + numerals.
46. Hero headline: clamp(2.8rem → 6rem), Aref Ruqaa, molten-gold gradient.
47. Arabic never letter-spaced (project law); Latin labels tracked +0.3em.
48. Word-level reveal on the hero headline only — Arabic shaping forbids letter splits.
49. Section h2: El Messiri clamp(1.9rem → 3.2rem), cream, no gradient (hierarchy).
50. Giant chapter numerals: Marcellus, outline stroke gold-deep, 8–11rem, behind content.
51. Body copy: 1rem/1.85 Almarai 300, max 50ch.
52. Prices: Marcellus, tabular, gold, LTR-isolated — every price identical treatment.
53. Fine print .72rem sand — one size, everywhere.
54. Menu row names: El Messiri large (1.4→2.1rem) — the menu IS typography.
55. English echoes under Arabic names: Marcellus .78rem sand.
56. No centered long paragraphs; centered only single-line statements.
57. Line-height 1.4 minimum on Aref Ruqaa (tall ascenders clip below that).
58. The marquee uses El Messiri + Marcellus alternating AR/EN names.
59. Numerals Latin everywhere (prices, counts) — matches the price cards.
60. data-t/data-t-alt hooks preserved exactly — the language engine is untouched.

### D. Hero (61–80)
61. The 3-scene pinned cinema engine survives verbatim — proven, tested code.
62. Scene photos get the forced grade + a stronger cinematic vignette.
63. The text block sits inside a self-drawing gold SVG frame (stroke-dash animation on load).
64. Behind the text: a faint bespoke 8-fold gold rosette, rotating at 120s, opacity 6%.
65. Headline "وقتكِ، فوق ضوضاء اليوم." in molten-gold animated gradient.
66. Label above: NAVA BEAUTY SALON & SPA — Marcellus, tracked, gold.
67. Supporting line + two CTAs stay (booking primary, finder secondary ghost).
68. CTA sheen: a light sweep crosses the primary CTA every 6s.
69. Words of the headline rise in staggered — re-split safely on language toggle.
70. Scene 2/3 lines keep Aref Ruqaa at reduced scale — same voice, quieter.
71. Grade tuned so the Nava wall sign still reads in scene 1 — brand proof.
72. Scroll cue: a breathing gold line, bottom start — not an arrow icon.
73. Hero height ratios unchanged (260/200svh) — pacing was already right.
74. Wipe transitions unchanged — no double exposure regression.
75. Reduced motion: three static framed scenes, frame pre-drawn, no shimmer.
76. The gold frame is decorative → aria-hidden, zero layout shift.
77. Dust canvas begins in the hero and persists page-long, fixed, behind content.
78. 70 particles max, 1px–2.5px, upward drift + twinkle — jewel dust, not snow.
79. Canvas pauses on document.hidden and under reduced motion.
80. LCP protection: scene-1 image eager/high priority; canvas initialized post-load.

### E. The living layer (81–100)
81. Marquee strip after the hero: all 7 category names AR ✦ EN, infinite drift.
82. Marquee is dir=ltr internally, language-independent (both names always shown).
83. Marquee pauses on hover and under reduced motion.
84. Separators are gold ✦ — the one ornament glyph allowed in text.
85. Reveal-on-scroll: rise 24px + blur(6px)→0 + opacity, 0.9s luxury bezier.
86. Reveals stagger children automatically (nth-child delays capped at 6).
87. Count-up numerals (10 / 155 / 7) animate once in view, 1.2s easeOut.
88. Magnetic CTAs: primary buttons lean ≤6px toward the cursor (pointer:fine only).
89. Custom cursor glow: a soft gold radial dot, screen-blend, lerped follow.
90. Cursor grows over any interactive element; never replaces the native cursor.
91. Menu rows sweep a gold gradient underline start→end on hover.
92. Category row hover lifts the arrow and brightens the name — two cues, one motion.
93. Image containers scale imgs 1.06→1 on reveal — photos breathe in.
94. The proof band's gold hairlines draw themselves (scaleX) on reveal.
95. Shimmer sweep crosses the molten headline every 9s (background-position).
96. Section numerals parallax slower than content (translateY at 0.4 ratio) — desktop only.
97. All motion transform/opacity/filter only — nothing animates layout.
98. Every idle animation ≤ 2 properties, ≥ 6s period — alive, not busy.
99. prefers-reduced-motion kills: dust, marquee drift, shimmer, magnetic, cursor, parallax.
100. No Lenis, no smooth-scroll lib — native scroll + CSS smooth for anchors.

### F. Chapters & layout (101–140)
101. Order: hero → marquee → statement → experience → finder → horizontal signature → menu → editorial → visit.
102. The ivory proof strip becomes a dark **statement band**: بريدج line + three count-up stats (10/155/7) + 4 verified facts.
103. The bridge gradient (dark→ivory) dies — the world never leaves the dark.
104. Experience chapter: asymmetric 7/5 grid, image right, text overlapping, numeral 01 behind.
105. Proof points stay numbered rows (verified facts only) — now gold-on-dark.
106. Finder chapter: a raised jewel panel with an animated gold gradient border.
107. Finder preview (real question + real result) restyled dark — kept, it sells the tool.
108. Finder heading in El Messiri; "NAVA RITUAL FINDER" label in Marcellus gold.
109. Signature moments become a **horizontal pinned journey** (desktop): 3 full panels sliding.
110. Each panel: graded image, huge outline numeral, Arabic title + one line.
111. Horizontal drive: GSAP scrub, direction-aware (RTL translates positive).
112. Rebuilt on language toggle (kill + recreate trigger) — no stale distances.
113. Mobile/reduced/no-GSAP: the same panels stack vertically — no pin, full content.
114. Menu = fashion-house service list: six full-width rows, not cards.
115. Row anatomy: numeral · Arabic name (large) · EN echo · count · from-price · arrow.
116. Row hover: gold sweep hairline + arrow slide — restrained, repeatable.
117. The "المزيد" row keeps the overflow chooser dialog — logic untouched.
118. Search/sheet/booking dialogs restyle via tokens only — zero logic edits.
119. Editorial chapter: full-bleed graded beauty image, headline overlapping bottom-start.
120. Editorial keeps "من داخل نافا" label + the approved two-line copy.
121. Visit chapter: split — skyline image left, details right, both CTAs (WA + map ghost).
122. Visit heading "موعدكِ فوق المدينة." in Aref Ruqaa — the closing statement.
123. vrows: gold labels, cream values, hairline separators — a menu of facts.
124. Footer: one line, sand, minimal — the page ends quietly after the CTA.
125. Sticky mobile bar survives (conversion) — espresso glass restyle.
126. Section spacing: clamp(5rem→9rem); consecutive same-ground handled by rhythm not rule.
127. Max content width 1360px; gutters clamp(1.25rem→4.5rem).
128. The huge numerals are aria-hidden and non-selectable — pure scenography.
129. No card grids anywhere on the page — rows, panels, and full-bleeds only.
130. Every image container overflow:hidden with 2px radius — knife-edge frames.
131. Image aspect ratios fixed per role — zero CLS from photography.
132. The rosette SVG appears twice max (hero, visit) — ornament stays rare.
133. Header: transparent → espresso glass at 40px; never light (no on-light state).
134. Nav links cream at 78%, gold on hover; active state skipped (single page).
135. All chapters keep existing section IDs — nav anchors + JS hooks unbroken.
136. #proof-strip ID retained on the statement band (header measure + paint hook).
137. .ch-light class dies in markup; light-ground CSS removed entirely.
138. Dialogs open over dust/cursor layers (top layer wins by spec) — verified.
139. svc grid container becomes .svc-list but keeps id svcGrid — JS untouched.
140. Footer year via existing #yr script — no duplicate logic.

### G. The finder & conversion (141–160)
141. Finder logic untouched — deterministic rules are correct and tested.
142. Finder dialog restyles to raise surface + gold steps — same DOM contract.
143. Result labels gold; reasons stay sand — facts quiet, choices bright.
144. The Nava Card keeps its total logic (numeric-only totals) — honesty rule.
145. WA message templates unchanged — they were approved content.
146. Analytics events unchanged and complete — the owner-value story stands.
147. Sticky bar copy stays "موعدك برسالة واحدة" — best line written for it.
148. Hero primary CTA = booking; secondary = finder — proven mapping.
149. ebmCta smooth-scrolls to the menu — kept.
150. Map ghost button kept — secondary action visible, not buried.
151. Booking dialog steps recolor gold — progress reads on dark.
152. Price sheet rows: name cream, price gold Marcellus — scannable at speed.
153. Search input: noir field, gold caret, cream text.
154. The 35 SAR nail-tools footnote + lash/hair notes survive — real card facts.
155. aria-pressed states get gold fills — selection is unmissable.
156. Dialog close × enlarged to 44px touch target.
157. Finder entry CTA gets the sheen sweep — the money button glows.
158. rf preview cards borrow the result-card anatomy — one design, two uses.
159. Overflow chooser buttons full-width rows — thumb-friendly.
160. Nothing asks for data beyond optional name/day — trust by restraint.

### H. Performance & a11y (161–180)
161. Same 4-size srcset pipeline; hero eager, all else lazy.
162. Fonts: 4 families, weights pruned (Ruqaa 400/700, Messiri 400/600, Almarai 300/400/700, Marcellus 400).
163. display=swap on fonts; system fallbacks tuned warm (Georgia/serif for display).
164. Canvas dust: one rAF loop, integer math, devicePixelRatio capped at 1.5.
165. Cursor + magnetic share the same rAF — one loop, three effects.
166. No will-change anywhere global; transforms promoted implicitly.
167. Horizontal pin uses one ScrollTrigger; killed cleanly on language rebuild.
168. Grain + tint overlays are pseudo-elements — zero extra requests.
169. The rosette is inline SVG — no fetch, no layout shift.
170. Total added JS ≈ 6KB unminified — no new libraries.
171. Focus-visible gold on every interactive element — tested by keyboard walk.
172. Dialogs already focus-trap via showModal + Esc — retained.
173. Touch targets ≥44px on all mobile controls (rows, chips, ×).
174. Contrast: cream on noir 12:1; gold on noir 7:1; sand reserved for ≥.72rem meta.
175. aria-hidden on all scenography (numerals, rosette, frame, dust canvas).
176. Marquee content duplicated with aria-hidden on the clone.
177. reduced-motion audited path-by-path, not blanket-only.
178. No autoplay media, no sound, no video — stills + light only.
179. overflow-x clip on body (project law — sticky survives).
180. Print gets default styles — not a target, not broken either.

### I. Verification (181–200)
181. Every claim below verified in real Chrome via CDP, not assumed.
182. Desktop 1440×900: hero frame draws, shimmer runs, dust visible, zero console errors.
183. Scene transitions: text-out → wipe → text-in sequence intact after restyle.
184. Marquee scrolls; pauses on hover.
185. Count-ups fire once; values 10/155/7 match dataset-derived numbers.
186. Horizontal chapter pins and completes; releases into menu chapter.
187. RTL horizontal direction correct; EN toggle rebuilds it without breakage.
188. Menu rows open the priced sheet; 155 items intact; search works.
189. Finder full path: 3 answers → 3 real results → card → WA message correct.
190. Analytics events fire in order through the full flow.
191. Booking dialog end-to-end composes the correct WA message.
192. Language toggle repaints every hook including hero split-text.
193. Mobile 390×844: stacked signature panels, sticky bar shows/dismisses.
194. No horizontal overflow at 390/1440; scrollWidth == clientWidth.
195. Reduced motion: static hero, no dust/marquee/shimmer, all content readable.
196. Grep-verified: no #FFF, no letter-spacing on Arabic selectors.
197. Screenshots of all six chapters reviewed visually before reporting.
198. LCP element confirmed = scene-1 image (not the canvas or fonts).
199. Docs updated (this file + editorial-rebuild pointer) before the report.
200. Report states what was decided FOR him, not what was asked OF him — that is the assignment.
