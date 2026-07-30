# Image manifest

Every frame currently referenced by `template.html`, with its licence basis and
how it is used. Sourced through the Unsplash API with a key supplied by the
project owner; the Unsplash Licence permits commercial use without
attribution, though the photographer is recorded here anyway.

Curation method: 14 searches across the beauty vocabulary returned 420 results.
Those were filtered on Unsplash's own dominant-colour value — saturation ≤0.42,
lightness 0.18–0.92 — leaving 136 warm neutrals, which were rendered as two
contact sheets at 520px and reviewed by eye. 20 were shortlisted, 6 chosen.
Every rejection reason is recorded in `creative-decisions.md` 031 and 092.

Delivery: each plate ships `srcset` at 640/900/1300/1800 with `sizes=100vw`, so
a 390px phone fetches ~900px. The pinned frame loads eagerly at high priority
because it occupies a full screen; everything else is lazy.


| # | Role | Photographer | Unsplash ID | Dominant | Licence | Focal point | Grade |
|---|---|---|---|---|---|---|---|
| 0 | hero / opening plate | K8 | `photo-1613323885789-e2212e15c326` | `#735940` | Unsplash Licence — commercial use permitted | upper third (hair mass) | warm open |
| 1 | chapter 01 — the ritual, detail | Marek Piwnicki | `photo-1755344953503-6911565dd387` | `#402626` | Unsplash Licence — commercial use permitted | centre | warm open |
| 2 | held scene — pinned frame | Paul Siewert | `photo-1560264641-1b5191cc63e2` | `#402626` | Unsplash Licence — commercial use permitted | centre-left | warm open |
| 3 | chapter 02 — brows, detail | Lana Graves | `photo-1692221307059-8819db116d92` | `#d9c0c0` | Unsplash Licence — commercial use permitted | centre | warm open |
| 4 | gallery 01 | Crystal Clark | `photo-1682450285233-1fb10d4a4616` | `#d9d9c0` | Unsplash Licence — commercial use permitted | centre | warm open |
| 5 | gallery 02 | Kajetan Sumila | `photo-1613057388812-029549dc3d39` | `#734040` | Unsplash Licence — commercial use permitted | centre | warm open |

## Ratio check

| Subject | Target | Actual |
|---|---|---|
| hair and styling | 35% | 67% (4 of 6) — **over budget** |
| nails / brows / treatment detail | 15% | 33% (2 of 6) |
| specialists | 15% | 0% — **missing** |
| interior and hospitality | 20% | 0% — **missing** |
| bridal and private | 10% | 0% — **missing** |
| materials | 5% | 0% |

The set is currently hair-heavy and has no interior, no specialist and no
bridal frame. Those chapters do not exist yet; the manifest is the checklist
for sourcing them, and decision 014 stays `pending` until the ratio is met.

## Rejected, and why

- A frame carrying another company's product and brand name in full view
  (decision 092). Removed on sight.
- Uncovered portraits and a bare-feet frame — wrong for this market
  (decision 031).
- 64 Openverse candidates: a Flickr and Commons archive, not an editorial
  library. Contact sheet showed spiders on walls, county courthouses, churches
  and vintage cars. None usable.
- 28 Mixkit video candidates: all but one was dated spa stock. The one that
  was not — cream cloth under warm light — was used and then removed, because
  iOS disables autoplay entirely in Low Power Mode and paints its own play
  control over the frame.

## Sources not used, and why

Pexels and Unsplash's own search pages both refuse requests from this machine
(403 and 401). No asset has been taken from a competitor site, a luxury brand
campaign, Pinterest, Instagram, Behance or Google Images; those were consulted
as creative reference only.
