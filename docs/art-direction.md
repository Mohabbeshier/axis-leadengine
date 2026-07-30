# Art direction — لمسة سمو

The house, not the salon. Everything below is a constraint on the template, so
it holds for every salon the engine renders — not just the one being reviewed.

---

## 1 · The owned idea

**الطقس** — the ritual. Four movements, numbered, referred to by number
throughout the page and in the message that reaches the salon:

```
01  الوصول        arriving to a room that is ready
02  الاستشارة      listening before recommending
03  الجلسة         the work, and what is never seen
04  قبل المغادرة   an agreement, not an invoice
```

This is the only device the page owns. A competitor can copy a colour or a
font; they cannot copy a numbered ritual without it reading as a copy.

**Wordmark:** لمسة سمو
**Descriptor (secondary, never set large):** دار الجمال والعناية النسائية

The legal string — "صالون لمسة سمو للتزيين النسائي" — belongs in the document
title and the footer, never in the lockup.

---

## 2 · Materials

Warm stone, unpolished wood, brushed bronze, linen, still water. Nothing
reflective, nothing high-gloss, no metallic gradients. Where a surface needs
to feel touchable it gets grain, not a highlight.

Prohibited: bright gold, gold gradients, glass morphism as a theme, neon,
blush pink as a brand colour, marble as a background texture.

---

## 3 · Light

One light source, low and warm, entering from the start edge. Every frame is
graded toward that: highlights warm, shadows brown rather than grey, no cool
cast anywhere. A frame that cannot be graded into this light is rejected
regardless of its subject.

---

## 4 · Colour

| Token | Value | Role |
|---|---|---|
| `--ink` | `#17140F` | closing ground, deepest type |
| `--cocoa` | `#2B211B` | dark chapters |
| `--espresso` | `#3A2B23` | held scene ground |
| `--ivory` | `#EFE7DB` | primary page ground |
| `--porcelain` | `#FBF8F3` | the one bright band |
| `--sand` | `#E4D8C7` | alternate band |
| `--travertine` | `#D3C2AC` | plate ground before an image arrives |
| `--clay` | `#B99174` | warm accent |
| `--bronze` | `#9A704C` | rules, numerals, quiet accents |
| `--rosewood` | `#805A51` | one accent, used at most twice |
| `--sage` | `#777C68` | availability and confirmation only |
| `--pearl` | `#E8DED3` | bridal chapter only |

**Chapter rhythm** — no two adjacent bands share a ground:

```
hero        cocoa + warm frame + ivory type
statement   ivory
silent      full frame, no ground
ritual      espresso, deepening across the four lines
index       sand
space       porcelain
artists     porcelain, portrait contrast
bridal      pearl
membership  cocoa + bronze
visit       sand
closing     ink + ivory
```

Rules: body copy never below 4.5:1. Sage means available or confirmed and
nothing else. Bronze is never a fill, only a line or a numeral.

---

## 5 · Typography

| Role | Face | Notes |
|---|---|---|
| Arabic display | Amiri | tested at 320/390/430; replaced if it fails |
| Arabic UI/body | Tajawal 300/400/500 | line-height 1.85 minimum |
| Latin display | Cormorant Garamond 300/400 | numerals, ritual markers |
| Latin UI | Tajawal | avoids a fourth family |

Absolute rules:

- **No `letter-spacing` on Arabic, ever.** Tracking is scoped to
  `html[lang="en"]`. Arabic gets `word-spacing` where separation is wanted.
- Arabic headings: `line-height` ≥ 1.36; never below 1.3 at display sizes.
- Every headline has a measure in `ch` chosen so it does not orphan a word at
  390px. Measures are set per headline, not globally.
- `text-wrap: balance` on headings, `pretty` on paragraphs.
- `text-box-trim` only under `html[lang="en"]` — it clips Arabic descenders.
- Western digits in both languages. Prices in the Latin display face, tabular.
- Currency written **ريال** in Arabic, **SAR** in English. Never ر.س in
  running copy.

Scale: `clamp()` throughout. One statement crosses 120px on desktop; nothing
else does.

---

## 6 · Grid and spacing

Desktop 12 columns · tablet 8 · mobile 4.
Gutter: `clamp(1.4rem, 6vw, 7rem)`, never below 20px.
Vertical rhythm on an 8px base; chapter air is `clamp(6rem, 18vh, 14rem)`.

Composition rules:

- One dominant object per viewport.
- No two consecutive chapters share a composition.
- Exactly one composition breaks the grid — the bled frame with type across it.
- Emptiness must read as anticipation. If a screen could be mistaken for a
  failed load, it is wrong; the test is whether anything is painted in it.

---

## 7 · Photography

Ratio across the page:

| Subject | Share |
|---|---|
| hair and styling | 35% |
| nails, brows, treatment detail | 15% |
| specialists and human presence | 15% |
| interior and hospitality | 20% |
| bridal and private service | 10% |
| materials and transitions | 5% |

Hard rejects: visible third-party branding or product names, watermarks, cool
clinical light, stock smiles, uncovered portraits, bare feet, anything that
cannot take the grade, anything whose mobile crop loses its subject.

Treatment: one grade for open frames, one deeper grade for held and dark
scenes. Both defined once in CSS so a mixed library still reads as one
commission — and so a salon's own photographs drop in later without
re-grading by hand.

---

## 8 · Motion

Four verbs, and no fifth:

| Verb | Behaviour | Where |
|---|---|---|
| rise | 52px up, opacity, on entry | text blocks |
| uncover | clip-path from the bottom edge | plates |
| drift | ±4.5% against the scroll | plate wrappers |
| hold | pinned frame, content replaces itself | the ritual, once |

Curves: `cubic-bezier(.19,1,.22,1)` editorial, `cubic-bezier(.34,1.4,.64,1)`
tactile. Nothing else.

Durations: micro 180–320ms · UI 300–500ms · editorial 700–1200ms · cinematic
1000–1800ms.

Constraints: no letter-by-letter animation on Arabic. No scroll hijacking. No
element animates a property another rule also animates. Idle motion only on
the hero and held frames. Under `prefers-reduced-motion` every element is
visible at rest and no content depends on scroll to appear.

---

## 9 · The feeling

Quiet, and certain of itself. The page should feel like being shown into a
room by someone who is not in a hurry — and it should be obvious, within two
screens, that the prices are not hidden and the room is not shared.
