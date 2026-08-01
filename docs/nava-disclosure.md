# Progressive disclosure — the Nava page (superseded)

**2026-07-31 — superseded by `docs/nava-journey.md`.** Mohab rejected this
entire layout — "a premium landing page," not what he asked for — and the
page was rebuilt from zero as a cinematic scroll journey. None of the
accordion/drawer/gallery-fold markup this document describes still exists
in `sites/nava/index.html`. Kept here as a record of what the second
version was and why, not as current documentation — read the new file for
how the page actually works today.

---

One system, four surfaces. Everything collapsible on the page is built from
the same three parts and wired through the same two functions, so a panel can
never end up with a turned chevron and a closed body.

## The primitive

```
button[aria-expanded]  →  .disc-p  →  .disc-p > .inner
```

- `disclose(btn, panel, cb)` attaches the behaviour; `setDisc(btn, panel, bool)`
  is the only thing that changes state. Nothing toggles a class directly.
- The panel opens on **`grid-template-rows: 0fr → 1fr`**, not a pixel height.
  This is deliberate: the panels hold Arabic and English at two different type
  sizes, so any hard-coded `max-height` would be wrong in one language. Engines
  without grid-row interpolation still collapse correctly — they just snap.
- `.disc-p > .inner` carries `overflow:hidden; min-height:0`. Without the
  `min-height`, the grid row refuses to go below content height and nothing
  collapses.
- Chevron rotation is driven off `[aria-expanded="true"]`, so the icon cannot
  disagree with the accessibility state.

## Where each pattern is used, and why

| Surface | Pattern | Reason |
|---|---|---|
| Services, 7 chapters | **Accordion** — one open at a time | Chapters are alternatives; two open at once is just a longer wall |
| Visit — address / hours / contact | **Independent panels** | Reference detail: a visitor may want the address *and* the hours out together |
| Gallery | **Single collapsible** — 3 frames out, 4 folded | The mosaic was the page's heaviest block below the fold |
| Index | **Off-canvas drawer**, and the same markup as a **pinned rail** ≥1100px | `showModal()` on a phone, `show()` on a desktop — no second component |

## Three levels on the services, not two

`chapter → peek (6 services + prices) → full sheet (search, all 155)`.
The peek answers "what does this chapter cost"; the sheet answers "where is the
one service I want". A peek row and a sheet row both call the same `pick()`, so
a service chosen anywhere hands the same name and price to the booking overlay.

## Rules that must survive any edit

- **`body` overflow-x stays `clip`.** An off-canvas drawer is the classic reason
  someone reaches for `hidden`; that would silently kill sticky positioning
  (see CLAUDE.md). The drawer is a `<dialog>` in the top layer, so nothing ever
  overflows the body in the first place. Verified: `scrollWidth == clientWidth`
  at 390 and at 1384.
- **The drawer slides direction-aware.** `--from: -100%` flips to `100%` under
  `html[dir="rtl"]`. Measured settled: RTL 58→390, LTR 0→332 on a 390 viewport.
- **Latin handles inside Arabic need `dir="ltr"`.** `@navasalon.sa` renders as
  `navasalon.sa@` without it. `a[dir="ltr"]` carries the isolate.
- **Open state survives a language switch.** `paint()` re-renders the menu, the
  visit and the drawer; `openChapter`, `visitOpen{}` and `galOpen` are the
  memory. Verified before/after a switch.
- No JS animation libraries; all motion is CSS and disabled under
  `prefers-reduced-motion`.

## How it was verified

`scratchpad/cdp.py` drives real Chrome over the DevTools protocol — new
headless ignores `--virtual-time-budget` on the command line and `--dump-dom`
snapshots at load, so the older dump-dom harness can no longer see anything a
timer produced. `_frame.html` is the same-origin 390×844 iframe; `probe_disc.js`
drives every surface and asserts the geometry. Anything animated must be
measured **after** the animation settles — measuring synchronously after a
`.click()` reads frame 0 and reports the panel off-screen.
