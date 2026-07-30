# Creative decisions — لمسة سمو

Ten councils, ten decisions each. This is the implementation checklist, not a
retrospective: nothing here is written after the fact to describe work already
done. Status is `pending` until the correction is in `template.html`, and
`verified` only once it has been seen in a render at 390×844 or measured.

Evidence base: the mobile screenshots supplied on 2026-07-29/30, the
instrumented page measurements in this session, and the live page.

---

## 01 · Global creative direction

| # | Problem observed | Required correction | Where | Verification | Status |
|---|---|---|---|---|---|
| 001 | No proprietary idea. Every claim on the page ("نساء فقط، بالموعد فقط") is table stakes in Riyadh; a competitor could copy the whole page and lose nothing. | Give the house one owned idea — the ritual is named, numbered and referred to throughout. | Statement, held scene, service index | The name appears in ≥3 chapters and in the WhatsApp message | pending |
| 002 | The brand lockup is a legal description, not a name: "صالون لمسة سمو للتزيين النسائي". | Wordmark becomes **لمسة سمو**; the descriptor drops to a secondary line. | Nav, hero, footer, title | Wordmark ≤2 words everywhere it is set large | pending |
| 003 | Composition repeats: image, then words about the image, six times. | No two consecutive chapters may share a composition. | Whole page | Composition audit table in qa-report | pending |
| 004 | Nothing on the page is memorable 24h later. | One owned visual device carried through: the numbered ritual marker set in Cormorant. | All chapters | Present in ≥5 chapters | pending |
| 005 | Colour is one flat warm field; no chapter has its own light. | Chapter-level colour rhythm per art-direction.md. | Whole page | No two adjacent bands share a ground | partial |
| 006 | Arabic display face (Amiri) is beautiful but reads traditional, fighting the contemporary intent. | Test Amiri against a contemporary Arabic display; keep whichever survives at 390px. | Type specimen | Specimen render compared | pending |
| 007 | The footer is two loose ends and ends the story abruptly. | Footer becomes a closing frame with the wordmark, the invitation and the essentials. | Footer | Render at 390 | pending |
| 008 | The demo cannot be told apart from the next salon's demo. | Per-salon accent derived from the salon's own data, not random. | Design tokens | Two salons rendered side by side differ | pending |
| 009 | No evidence of art direction in the details — radii, rules and shadows are inconsistent across chapters. | One radius scale, one rule weight, one shadow set. | Tokens | grep for stray values returns none | pending |
| 010 | The page reads as a template because every section is full-width and centred in the same field. | Introduce one broken composition and one pinned scene. | Broken frame, held scene | Seen in render | **verified** |

## 02 · Luxury fashion editorial

| # | Problem | Correction | Where | Verification | Status |
|---|---|---|---|---|---|
| 011 | Photography is a set of separate pictures, not a sequence. | Order the frames as a campaign: wide, detail, held, detail, wide. | Image manifest | Manifest sequence column | pending |
| 012 | Every crop is the same rectangle at the same margin. | At least one image bleeds off an edge; at least one is cropped unexpectedly tight. | Broken frame, gallery | Render | **verified** |
| 013 | Type never touches an image. | One headline set across a photograph in multiply. | Broken frame | Render | **verified** |
| 014 | Hair dominates: five of six frames. | Enforce the ratio in art-direction.md — hair ≤35%. | Manifest | Ratio computed in manifest | pending |
| 015 | No frame earns a full screen on its own. | One silent full-bleed frame with no words at all. | After the statement | Render | pending |
| 016 | Prices are set in the body face, so the index reads as a list not a menu. | Prices in the Latin display face, tabular, one size below the service name. | Index | Render | **verified** |
| 017 | Arabic headlines break with orphans at 390px. | Manual measure per headline in `ch` units, tested at 320/390/430. | All headings | Three-width render | partial |
| 018 | Nothing in the page is set at large scale except the hero. | One statement crosses 120px on desktop. | Statement | Desktop render | **verified** |
| 019 | Image grading is applied but never varies, so depth is flat. | Two grades: a warm open grade for wide frames, a deeper one for held/dark scenes. | Plate classes | Render | pending |
| 020 | The gallery is decoration; it says nothing. | Each gallery frame is captioned with what it is. | Gallery | Render | pending |

## 03 · Luxury hospitality and spa

| # | Problem | Correction | Where | Verification | Status |
|---|---|---|---|---|---|
| 021 | The journey is told in words but never shown. | The held scene carries the ritual in three lines over one frame. | Held scene | Render | **verified** |
| 022 | Privacy is claimed once as a chip and never substantiated. | A private-room chapter with the actual arrangement described. | Private services | Render | pending |
| 023 | No sense of arrival — the page starts at the treatment. | The first line of the ritual is arrival, before any service is named. | Held scene | Copy check | **verified** |
| 024 | Nothing about hospitality: no tea, no timing, no attendant. | Aftercare and follow-up stated as the fourth step. | Journey | Copy check | **verified** |
| 025 | The space is absent — one interior frame in the whole page. | The space chapter with reception, station, private room. | The space | Render | pending |
| 026 | No quiet moment; every screen asks for something. | One screen with no call to action at all. | Silent frame | Render | pending |
| 027 | Hours are printed as a run-on string when present, hidden when not. | Hours as a day/time table with today marked. | Visit | Render | partial |
| 028 | Nothing addresses what happens if she is late or must cancel. | Cancellation and rescheduling stated plainly. | FAQ | Copy check | pending |
| 029 | No named specialist, so the service feels anonymous. | Artists chapter with real structure (name, craft, languages). | Artists | Render | pending |
| 030 | Bridal — the highest-value booking in this market — is absent. | A distinct bridal chapter with trial, day-of and venue service. | Bridal | Render | pending |

## 04 · GCC women and cultural relevance

| # | Problem | Correction | Where | Verification | Status |
|---|---|---|---|---|---|
| 031 | Imagery has included uncovered portraits, bare shoulders and a bare-feet frame. | Detail crops and covered subjects only; no full portraits of uncovered women. | Manifest | Manifest review column | partial |
| 032 | Copy has drifted between registers, including Egyptian colloquial earlier. | One register: Gulf-neutral, plain, no poetry that obscures meaning. | All copy | Read-through | partial |
| 033 | Arabic is not truly first — the English table is the fuller one in places. | Arabic authored first; English is the translation. | i18n table | Field-by-field parity | pending |
| 034 | Numerals mixed Arabic-Indic and Western within one screen. | Western digits throughout, in both languages. | All | grep for ٠-٩ in prices | **verified** |
| 035 | "للنساء فقط" is stated but the enclosure is not described. | State that the frontage is covered and no men enter during hours. | Values, FAQ | Copy check | **verified** |
| 036 | No home or venue service, which affluent Gulf clients expect. | Private/home service chapter with zones and conditions. | Private | Render | pending |
| 037 | Payment methods unstated — Mada and Apple Pay are expected. | Stated in FAQ. | FAQ | Copy check | **verified** |
| 038 | No membership, so there is no relationship after the first visit. | Membership chapter, three tiers, no SaaS cards. | Membership | Render | pending |
| 039 | Letter-spacing was applied to Arabic, severing the joins. | Tracking scoped to `html[lang="en"]` only. | Type rules | grep: no letter-spacing outside lang=en | **verified** |
| 040 | Riyadh is named but the district is generic. | District named and marked as demo data. | Visit, demo-content | Doc entry | pending |

## 05 · Digital experience / Awwwards

| # | Problem | Correction | Where | Verification | Status |
|---|---|---|---|---|---|
| 041 | First screen is expected: photograph plus name. | The opening withholds — either silence or a held move — so it is not the default. | Hero | Render | partial |
| 042 | One motion verb repeated twenty times. | Four verbs: rise, uncover, drift, hold. | Motion layer | Audit of keyframes in use | **verified** |
| 043 | No pinned moment. | The held scene. | Held | Measured frameTop=0 across 60% | **verified** |
| 044 | No horizontal movement anywhere. | One horizontal travel, scroll-driven. | Service index or ticker | Render | pending |
| 045 | Section transitions are abrupt: band ends, next band starts. | At least two chapters share a continuous element across their boundary. | Statement→broken | Render | pending |
| 046 | Nothing responds to the pointer beyond a colour change. | Weighted hover on the index rows and the plates. | Index, plates | Desktop render | partial |
| 047 | The loading sequence is a veil with nothing in it. | The veil carries the wordmark and a drawn rule. | Veil | Render | **verified** |
| 048 | Scroll cue persists past the first screen. | Cue fades on the hero's own exit. | Hero | Render | **verified** |
| 049 | No award-level single moment. | The held scene is the moment; it must survive reduced-motion as three stacked lines. | Held | Reduced-motion render | pending |
| 050 | Reduced motion has never been tested. | Render with the media query forced. | Whole page | Render | pending |

## 06 · Product and UX

| # | Problem | Correction | Where | Verification | Status |
|---|---|---|---|---|---|
| 051 | Booking is a link out to WhatsApp with a fixed message — no choice, no context. | A real booking overlay: branch, ritual, artist, date, contact, confirm. | Overlay | Click-through | pending |
| 052 | The same CTA appears three times on one screen. | One floating control, or one sticky bar — never both. | Nav, dock | Render count = 1 per screen | partial |
| 053 | No way to find a service by need; the index is a flat list of nine. | Discovery by ritual category, filtering the index. | Index | Interaction | partial |
| 054 | Duration is never stated, though it is the second question every client asks. | Duration on every service. | Data model | Data check | pending |
| 055 | No indication of what a service includes. | One line of what is included per service. | Data model | Data check | partial |
| 056 | Nothing is keyboard reachable except links. | Rows, filters and overlay steps are focusable and operable. | All controls | Keyboard pass | partial |
| 057 | No focus visible on dark grounds. | Focus ring specified against both grounds. | Tokens | Render | pending |
| 058 | The page has no landmarks or heading order. | main/nav/footer, h1 once, h2 per chapter. | Markup | Structure audit | pending |
| 059 | Selection state is lost on reload for everything except picks. | Persist the overlay's progress too. | Overlay | Reload test | pending |
| 060 | No empty or error state anywhere. | Every list and the overlay have a stated empty/failed state. | All | Forced-failure render | pending |

## 07 · Motion and interaction

| # | Problem | Correction | Where | Verification | Status |
|---|---|---|---|---|---|
| 061 | Pinned scene left three screens blank when sticky failed. | overflow-x:clip, never hidden, on body. | Base CSS | Measured: frame holds | **verified** |
| 062 | Scroll-driven ranges were written in `contain`, which collapses on tall subjects. | Named view-timeline on the tall section, ranges in `cover`. | Held | Render | **verified** |
| 063 | Two animations competed for `transform` on the same element. | One property owner per element; parallax on wrappers only. | Plates | Render | **verified** |
| 064 | Easing varies arbitrarily between rules. | Two curves only: (.19,1,.22,1) editorial, (.34,1.4,.64,1) tactile. | Tokens | grep audit | partial |
| 065 | Durations range from 250ms to 1.6s with no system. | Bands per art-direction.md. | All | grep audit | pending |
| 066 | Entrance delays were tuned around a video that no longer exists. | Re-timed to the current opening. | Hero | Render | **verified** |
| 067 | Reduced motion collapses animation but was never checked for blank states. | Every animated element visible at rest. | All | Forced render | pending |
| 068 | Ken-burns runs forever on every image, costing battery for no gain. | Idle motion only on the hero and held frames. | Plates | Audit | pending |
| 069 | The dock slides in over content on short screens. | Dock reserves its own space or hides where it would cover. | Dock | 320px render | pending |
| 070 | No motion carries meaning; all of it is decoration. | The held scene's motion changes what is said. | Held | Render | **verified** |

## 08 · Conversion and GCC commercial

| # | Problem | Correction | Where | Verification | Status |
|---|---|---|---|---|---|
| 071 | The WhatsApp message does not carry what she chose unless she used the index. | Every entry point composes a message with context. | All CTAs | Link inspection | partial |
| 072 | No bridal enquiry path, the highest-value lead in this market. | Bridal CTA with its own prefilled message. | Bridal | Link inspection | pending |
| 073 | No membership enquiry. | Membership CTA. | Membership | Link inspection | pending |
| 074 | Saudi numbers are normalised but not validated. | Normalise and validate 05x / +9665x. | Overlay | Input test | pending |
| 075 | Directions is a bare link with no context. | Directions with district and a note on parking, marked demo. | Visit | Render | pending |
| 076 | No analytics vocabulary, so nothing can be measured later. | A no-op analytics shim with named events. | Script | Event list | pending |
| 077 | Prices are stated with no starting-from qualifier in some places. | "تبدأ من" wherever a price is a floor. | Index | Copy check | partial |
| 078 | Nothing states how quickly they reply, which is the main objection. | State the reply window plainly. | Booking | Copy check | pending |
| 079 | No trust markers beyond a Google rating. | Rating, review count and years, all marked as demo where invented. | Trust | demo-content.md | pending |
| 080 | No lead qualification at all. | The overlay captures service, date window and branch. | Overlay | Message content | pending |

## 09 · Frontend engineering and performance

| # | Problem | Correction | Where | Verification | Status |
|---|---|---|---|---|---|
| 081 | A 1MB 1800px frame was lazy-loaded into a pinned scene. | srcset 640/900/1300/1800, sizes=100vw, eager+high on the pinned frame. | All plates | Measured | **verified** |
| 082 | No width/height on images, so every plate can shift layout. | Aspect ratios declared in CSS for every plate. | Plates | CLS check | partial |
| 083 | Page weight grew from 37KB to 51KB across patches with no budget. | Budget: 60KB HTML, ≤6 image requests above the fold. | Build | Byte count | pending |
| 084 | CSS is accreted from 18 patches; token names no longer describe values. | Rename tokens to what they are; delete dead rules. | Tokens | Audit | pending |
| 085 | No fallback when scroll-driven animation is unsupported beyond `.rise`. | Every scroll-driven effect has a static resting state. | All | @supports audit | partial |
| 086 | Fonts: four families requested, some weights unused. | Two per language, only the weights used. | Head | Network audit | pending |
| 087 | Google Fonts is a third-party dependency on a cold link. | Keep non-blocking; consider subsetting. | Head | Render with fonts blocked | partial |
| 088 | No console check has ever been run on the deployed page. | Zero errors and zero failed requests. | Live | Console capture | pending |
| 089 | 100svh was used where dynamic viewport units are needed. | svh/dvh chosen deliberately per element. | Hero, held | iOS-width render | partial |
| 090 | Nothing verifies the CONFIG contract after a template edit. | Assert the regex still matches before writing sites. | sitegen | Run | partial |

## 10 · Red team

| # | Problem | Correction | Where | Verification | Status |
|---|---|---|---|---|---|
| 091 | Three screens of flat beige — the single worst defect, twice photographed. | Fixed at the root (061, 081). | Held | Reproduced then re-measured | **verified** |
| 092 | A competitor brand's product and name appeared in a hero frame. | No third-party branding in any frame. | Manifest | Frame-by-frame check | **verified** |
| 093 | Category icons rendered as a smiley face and something resembling a "5". | Icons redrawn; multi-stroke supported. | Icons | Render | **verified** |
| 094 | "1 خدمة" and "7 خدمة" — Arabic inflects for count. | Correct plural rules. | Counts | Render | **verified** |
| 095 | An empty hours field printed a lone em dash. | Block removes itself. | Visit | Render | **verified** |
| 096 | Booking pill lost its label under 400px and became an unexplained dot. | Label retained. | Nav | 390 render | **verified** |
| 097 | Charcoal navigation over a dark photograph, unreadable. | Surfaced navigation past the opening screen. | Nav | Render | **verified** |
| 098 | Filter counts merged into prices: "أقل من ٢٠٠3". | Counts in their own pill. | Index | Render | **verified** |
| 099 | Screenshots were taken through a harness that silently cropped, exploded and froze the page — three false conclusions drawn from it. | Harness rebuilt and self-checking. | tooling | Harness reports scroll position | **verified** |
| 100 | No documentation existed, so every decision was re-litigated from scratch. | This file plus art-direction, image-manifest, ux-flow, qa-report, demo-content. | /docs | Files exist and are current | in progress |

---

## Count

- verified: 27
- partial: 20
- pending: 52
- in progress: 1

Nothing above is marked verified on the strength of a code change alone.
