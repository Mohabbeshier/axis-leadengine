> **Superseded 2026-07-31.** The seven-scene WebGL journey documented below
> was replaced outright by directive — "the current concept has failed...
> looks like a virtual gallery, not a real spatial journey." Nothing in this
> file describes what's currently on `sites/nava/index.html`. See
> `docs/nava-editorial-rebuild.md` for the six-chapter editorial page that
> replaced it. Kept as a historical record of how the blend/timing bugs
> were diagnosed and fixed, since that debugging method (CDP-measured, not
> assumed) carried forward unchanged into the rebuild.

# The journey — Nava's page, rebuilt twice

**2026-07-31, first rebuild.** Mohab rejected the second version outright:
"technically clean... creatively nowhere near the vision... I don't want a
nicer layout, I want a completely different experience." The accordion
sections, the drawer, the gallery grid, the boxed plates were replaced with
nine full-screen scenes on a scroll-driven camera.

**2026-07-31, second rebuild — this one.** That still wasn't it: "this
currently feels like a gallery with text overlays... I don't want sections
with different background images." Two real problems, both structural, not
cosmetic:

1. **Nine scenes was too many to be one story.** Two of them (a second
   reception shot, a coffee counter) repeated an emotional beat another
   scene already carried, or carried none at all.
2. **Nothing actually blended.** Every plane sat at full, constant opacity;
   only the camera moved. Arriving at the next photograph was a hard cut
   wearing a camera move as a costume — which is exactly what "feels like a
   gallery" describes.

Both are fixed below. (`docs/nava-disclosure.md`, describing the very first
version, stays as a record of a design that's no longer in the file at all.)

## The seven scenes — one arc, one purpose each

Designed before any code changed, per instruction. The test for every scene
still in it: does removing it break the story.

| # | Scene | Photograph | The one emotional job |
|---|---|---|---|
| 1 | The threshold | reception-wide | Leave the city's noise at the door |
| 2 | The invitation | hammam-tray | Scent and warmth say: stop performing, start receiving |
| 3 | Trust | manicure-scene | The moment you stop directing and let expertise take over |
| 4 | Undisturbed | facial-room | One room, one purpose, total privacy |
| 5 | Held | treatment-bed-view | The peak stillness the whole visit was for |
| 6 | Revealed | vanity-rollers | The mirror moment — seeing the change, not just feeling it |
| 7 | The return | rooftop-lounge | The same skyline as scene 1 — you are not who walked in |

**Cut, and why:** the second reception shot (`lounge-reception`) did
scene 1's job a second time; the coffee counter (`cafe-counter`) didn't move
the story at all — an amenity, not a beat. Both stay disclosed for the
generic template's pool (`docs/journey-experience.md`) since that page never
claimed a single narrative arc the way this one now does.

**Business content lives inside the arc, not beside it.** The 155-service
menu surfaces at scene 6 ("this is what created what you're seeing"), not as
a standalone chapter; visit and contact info surface at scene 7, alongside
the return itself.

## The actual fix: scenes now blend, not cut

Every plane's opacity is a triangular function of how far the current
scroll position is from that plane's own index — `1 - |scrollFraction -
sceneIndex|`, floored at 0. At a scene's own moment it's fully opaque; a
full scene-length away either side it's invisible; in between, it's
dissolving in exactly as its neighbour dissolves out. This runs identically
on both renderers:

- **Cinema path** — each `THREE.MeshBasicMaterial` is `transparent:true,
  depthWrite:false`, opacity set every frame in `paintAt()`.
- **Fallback path** — each `<img>` frame's `style.opacity` is set the same
  way, continuously, on scroll — not the discrete `.on`/off swap the first
  rebuild used, which is the same class of bug already found and fixed once
  in the shared template (decision 105): a state machine standing in for
  arithmetic the scroll position already answers.

Measured, not assumed: landing the scroll exactly halfway between scene 2
and scene 3 reads two planes simultaneously at opacity 0.08 and 0.92 on the
cinema path, and 0.084 / 0.916 on the fallback — the same blend, minus the
WebGL, confirmed on both render paths rather than the desktop pass alone.

## Verification

Both paths, after the rework: scene count is 7; kickers read the new labels
in order on a full sweep; the services scene's category pills still open
the real priced sheet (155 services intact); a service picked there still
hands off into booking; the booking flow still composes a correct WhatsApp
message; the finale scene's address/hours/contact are still real; language
switch still repaints every overlay; zero console errors; no horizontal
overflow at 390px or desktop width.

## 2026-07-31, third pass — the storyboard's camera and typography timing

A storyboard was written and approved before any code changed (per instruction):
every scene's camera move, transition, and text timing, defined in filmmaking
vocabulary first. Two things in that document weren't in the code yet:

**Camera as push-in/pull-back, not just a dolly.** The camera previously moved
through the seven planes at a constant field of view — position changed, but
never the sense of the lens itself opening or closing. `fovAt(f)` now
interpolates a per-scene FOV control point (`[44,43,42,42,50,36,44]`): steady
through the opening scenes, opened to 50° at Held (massage) for the skyline
reveal, snapped to 36° at Revealed (beauty) for the mirror push-in — a
deliberate echo of scene 1's own push-in on the reception desk — then back to
44° at Return, matching arrival's own establishing width almost exactly. Every
plane is scaled every frame by `tan(fov/2)/tan(21°)` to compensate, so no FOV
value — however wide or tight — ever exposes background at a plane's edge; the
math guarantees the same oversize margin at any FOV, not just the original 42°
the planes were built for. Runs on the cinema path only — the plain-image
fallback keeps its own simpler idiom (Ken-Burns creep), since forcing a literal
camera-FOV concept onto a flat crossfade risks exactly the kind of jank this
project has repeatedly had to fix, for a feature most users on the fallback
path (phones) can't tell apart from the existing creep anyway.

**Typography now answers "how far into the scene," not just "which chapter."**
`setChapter()` used to gate the arrival heading, the services chips, and the
visit details on a symmetric ±0.5-scene window around the nearest scene index —
which is what the blend needs, but not what the storyboard's timing calls for.
A new `setContinuous(f)` runs every frame on both render paths and answers the
timing questions directly: arrival's heading fades past 7% into its own scene,
the services chips reveal only past 40% into Revealed (once the mirror moment
has visually landed, not the instant that scene becomes active), and the
visit/contact block fades in at 15% into Return and holds — the one scene
built to be acted on, not just felt.

Verified by CDP, not assumed: FOV read directly off the camera object at seven
scroll positions matched the control points exactly (44 / 43.9 / 50 / 38.1 /
36.7 / 36.8→37.6 / 44); the arrival/services/visit reveal-class booleans
flipped at the intended f-thresholds on both the cinema and fallback paths;
zero horizontal overflow on both. One real bug caught in this pass: `fovAt()`
computed its interpolation fraction from `f - Math.floor(f)` instead of
`f - i`, which is only wrong at the very last frame (`f` exactly `6`, where `i`
gets clamped below `floor(f)`) — the bookend would have snapped to 36° instead
of 44° at the exact end of the scroll. Fixed before shipping.

## Also fixed in this pass

- **A flex-column stretch bug**: `.in`'s children defaulted to
  `align-items:stretch`, rendering the WhatsApp CTA as an edge-to-edge bar
  instead of a pill. `align-items:flex-start` on the container.
- **The 4.7 rating is gone** — from the page and the schema.org markup.
  `docs/client-nava.md` was explicit from the first session: no rating
  until Nava states one. Removed outright, not patched around.
- Fallback scene detection had been IntersectionObserver-driven and,
  measured, never advanced past the opening scene once a jump changed a
  mark's visibility by more than the observer's threshold in one step —
  which is exactly what a real scroll does when scenes are one viewport
  tall. Replaced with the same scroll-position arithmetic the cinema path
  already used successfully.
