# MOJO Salon — working brief (self-written, v2)

## The instruction that produced this file
"افتكر كل اللي عملناه في نافا والموشن واللايف — ويبسايت يبقى عايش كدا وبيتحرك.
راجع كل تفاصيل نافا، مش عايزه ناقص حاجة. ولو في زيادات زود. الشكل لازم يبقى مبهر."

So: **full feature parity with Nava**, then additions. Not a simpler sibling —
the same calibre of build, wearing Mojo's identity.

## Non-negotiables carried from CLAUDE.md + the Nava build
- Arabic never gets `letter-spacing`. Tracking lives under `html[lang="en"]` only.
- `body` overflow-x is `clip`, never `hidden` (hidden kills every `position:sticky`).
- No pure black, no pure white anywhere.
- No JS animation libraries beyond GSAP + ScrollTrigger (already the Nava stack).
- No video in the hero (iOS Low Power Mode paints a grey play button over it).
- `prefers-reduced-motion` must leave everything readable and operable.
- Real data only. No invented prices, staff, reviews, ratings, or availability.
  Mojo has published **no prices** → every service CTA goes to WhatsApp instead.
- Verify by rendering at 390×844, never by reading the diff.

## Mojo's real facts (already confirmed — do not re-research)
- صالون موجو النسائي / MOJO Salon — موجو للتزيين النسائي
- طريق الملك خالد، حي الجامعيين، المجمعة ١٥٣٦٥
- WhatsApp 966557715152 · also listed 0551122972
- Daily 1:00 PM – 10:00 PM, all seven days
- Instagram mojo_salon (2,794 followers) · Snapchat mojo_salon · TikTok · YouTube
- Loyalty: ٣٠٠→٢٠٪ (max ٢٠٠ ر.س) · ٦٠٠→٣٠٪ (٣٠٠) · ٩٠٠→٤٠٪ (٤٠٠) · ١٢٠٠→٥٠٪ (٥٠٠)
- Student discount ١٥٪ code MOJO15 · group ٣٠٪ for 3+ · Tabby & Tamara
- Categories: شعر · أظافر · بشرة · حمّام مغربي · مكياج
- 7 real photos: storefront, reception-wide, reception-close, hair-wash,
  nail-wall, treatment-room, candle

## Nava feature inventory → Mojo parity plan

| Nava | Mojo |
|---|---|
| 3-scene GSAP pinned hero, clip-path wipes | same, scenes = storefront → reception → treatment room |
| statement/proof band with count-up numerals | count-up on the real 7 / 5 / 1–10 figures |
| full-bleed immersive chapter | full-bleed "الأجواء" chapter on reception-wide |
| Ritual Finder (3-question deterministic) | **دليل موجو** — 3 questions → category, no prices, ends at WhatsApp |
| horizontal pinned journey (desktop) + scroll-snap gallery + dots (mobile) | same, 5 signature moments = the 5 categories |
| rAF pixel-math services ticker | same, single row, category names + "استفسري" |
| draggable / auto-drifting card river | same over the 7 real photos |
| Arabic-aware fuzzy search + synonyms | search over categories (no price sheet — no prices exist) |
| price sheet dialog with filters | **replaced** by a category sheet → WhatsApp per category |
| booking dialog, 4 steps, time bands, name memory, animated tick | same, bands built from the real 1–10 PM window |
| floating index FAB + page map | same |
| scroll-progress hairline | same |
| skip link, PWA manifest, print stylesheet, share button | same |
| splash intro, once per tab | already built, keep |
| AR/EN toggle incl. direction flip | already built, extend to all new strings |
| live open/closed chip from real hours | already built, keep |

### Additions beyond Nava (the "زود" part)
1. **Loyalty tier calculator** — pick a spend, see which tier it lands in. Mojo
   has this data and Nava never did; it is the most persuasive thing they own.
2. **Offers band** — student / group / Tabby-Tamara as a live rotating strip.
3. **Gold-leaf hairline motion** on section rules (draws on reveal).

## Motion system (four verbs, identical to Nava)
rise · uncover · drift · hold — all scroll-driven CSS, IntersectionObserver
fallback, `.fx` opt-in class so a script failure can never blank the photos.

## Verification checklist before showing anything
- 390×844 render, scroll-confirmed, every control clicked
- zero JS errors, zero horizontal overflow, zero broken images
- no touch target under 44px
- reduced-motion pass: everything visible and operable
- EN pass: no Arabic letter-spacing leak, direction flips
- live URL serves the new build (poll until the marker string appears)
