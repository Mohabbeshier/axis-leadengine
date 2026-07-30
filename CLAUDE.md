# AXIS Lead Engine — Claude Code Handoff

Read this whole file before touching any code. It replaces a conversation
that took several hours — everything below is a decision that was
already made, tested, or measured. Do not re-litigate it without a
concrete reason.

## What this is

An unattended pipeline that finds Riyadh beauty salons with no working
website, builds each one a live demo site, and sends it to them on
WhatsApp. Chairman: Mohab Beshier, founder of Axis Marketing Agency.
He is non-technical-by-default here — explain plainly, act directly,
don't make him choose between options he can't evaluate.

## Architecture — two passes, not one

This is the single most important decision in the whole system, and it
was arrived at after building the wrong thing first:

```
PASS 1 — harvest.py, run ONCE per district (or a few times total)
  Apify Google Maps scrape, cheapest possible config (no reviews, no
  images, no paid filters) -> hard gates applied in code -> survivors
  written to Supabase `leads` table with a quality_score.
  This is a one-time cost. It does NOT run daily.

PASS 2 — daily.py, runs every day
  Reads the top unsent leads from the pool PASS 1 built (ordered by
  quality_score). Does the few enrichment calls that only make sense
  on a small daily batch (Claude judge, content generation, site
  build). Never touches Google Maps again.
```

**Why**: the first design re-scraped Google Maps every single day to
find "new" businesses, which is nonsensical — Riyadh's salon count
doesn't change daily, and after a week you're paying to rediscover
salons you already rejected. Measured cost difference: $36/month
(naive daily re-scrape with reviews+images) vs $2.70/month (harvest
once, enrich only the daily batch). See "Measured numbers" below for
where these figures came from.

If you ever find yourself adding a Google Maps API call inside
`daily.py`, stop — that's the mistake being described above.

## The three hard gates (in `harvest.py::keep()`)

A business enters the pool only if ALL of these are true:
1. Category is a women's salon, not a barbershop (`صالون حلاقة` and
   similar are excluded by string match — Google returns roughly 50%
   barbershops for generic "beauty salon" Arabic queries, and this
   costs nothing to filter in code vs. $0.001/place for a paid
   category filter).
2. `rating >= 4.0` and `reviews_count >= 50` — a "no reviews" listing
   is not necessarily a live business.
3. Phone is a Saudi mobile number, not a landline — landlines can't
   receive WhatsApp, so a landline-only listing is dead on arrival for
   this outreach channel.
4. **No real website.** This one has a subtlety: `has_real_website()`
   excludes only genuine own-domain sites. A salon whose "website"
   field is actually an Instagram link, a Linktree, a `wa.me` link, or
   a booking-SaaS page (Fresha, Bookr) still counts as having no real
   website and stays in the pool — those aren't a competing digital
   presence, they're exactly the gap this business is selling into.

**A past bug, already fixed**: an earlier version of `harvest.py`
computed a quality score but never actually excluded businesses with a
working website — it just scored them lower. That let real competitors
into the pool. `keep()` now hard-excludes them before scoring ever
runs. If you're reading old chat history and see this described as "a
weighted score, not a hard gate" for the website check — that was
wrong and has been corrected.

## Quality score (`harvest.py::quality_score()`)

Only computed for records that already passed `keep()`. Decides send
order, not inclusion. Weighted on what actually predicts a reply:
review volume (40) > rating (25) ≈ no-website-at-all vs. parked-social
(25) > mobile number confirmed (10). Below the hard gate threshold
(reviews<50 or rating<4.0) the function returns 0 unconditionally —
this exists because a 4.5-rating salon with 4 reviews must never
outrank a 4.0-rating salon with 500 reviews, and without the early
return the additive scoring would let that happen.

## What each file does

| File | Role |
|---|---|
| `harvest.py` | One-time discovery. Reads `harvest_queue`, runs Apify, applies the 3 gates, scores, stores. Has a **hard monthly budget check** before every run. |
| `daily.py` | The daily job. Pulls best unsent leads from the pool, does light per-lead enrichment, Claude judges, Claude writes content, builds the site, pushes to git, sends WhatsApp. |
| `pipeline.py` | Shared logic: `verify()` (channel checks against a Supabase row — NOT a fresh Apify record, see note below), `judge()` (the Claude verdict call). |
| `content.py` | Two Claude calls: `services_for()` writes a plausible service menu + prices from the salon's reviews/category, `message_for()` writes the WhatsApp outreach text. Both are Gulf/neutral Arabic, both strict JSON. |
| `sitegen.py` | Renders `template.html` with the salon's real data, writes it to `sites/<slug>/index.html`, commits, pushes. No Netlify API — Netlify is connected directly to the GitHub repo and builds on push. |
| `outreach.py` | WhatsApp Cloud API sender. **The send IS the WhatsApp verification** — there is no separate check. Delivered = number is real. Error 131026/131047/470 = not on WhatsApp. Anything else = unknown, routes to needs_review. Hard caps: `DAILY_SEND_CAP`, `SEND_SPACING_SEC` (3 min between sends) — exceeding these is what gets a WhatsApp number banned. |
| `store.py` | Supabase REST wrapper. Dedup is on `place_id`. |
| `audit.py` | Standalone, discovery-only, no writes. Run this whenever you want to sanity-check field coverage or gate pass rates before spending money on a real harvest. |
| `schema.sql` | **Reference only.** The real schema is already live in Supabase project `mjetglnmivwphxyzflsz` ("axis-os-v2"). Don't re-run this file against that project; it documents what's there. |

### Important field-source note in `pipeline.py::verify()`

`verify()` is called from `daily.py` on a **Supabase row that
`harvest.py` already wrote**, not on a live Apify record. It only
reads fields that actually exist on that row (`reviews_count`,
`rating`, `phone`, `website_url`, `instagram`). It does NOT re-check
review freshness or re-derive `phone_is_mobile` from a separate stored
field — those checks already happened once, in `harvest.py::keep()`,
before the row was ever written. Re-deriving them here would either
crash on missing fields or silently re-run a paid check for a fact
already known. If you add a new gate, decide explicitly which pass
(harvest-time, cheap, applies to the whole pool) vs. daily-time
(slightly more expensive, applies only to today's ~10-30 candidates)
it belongs to.

## Measured numbers — from real Apify runs, not estimates

Two real test scrapes were run and priced with Apify's actual
pay-per-event billing (place-scraped $0.004, review-scraped $0.0005,
image-scraped $0.0005, filter-applied $0.001/place, all measured from
live run receipts, not documentation):

**Test 1 — wrong geolocation (text "Riyadh, Saudi Arabia" resolved to
the whole province, not the city)**: pulled 40 places, 52% from a town
called Layla and 40% from Wadi ad-Dawasir — both ~600km from Riyadh
city. 50% were barbershops. Only 2.5% had any real website. Gate pass
rate: 15%. Cost: $0.474 for 40 places (reviews+images included, which
turned out to be roughly 2/3 of the bill).

**Test 2 — fixed geolocation (real lat/lng + 3.5km radius on Al
Malqa district), no reviews/images/filters**: 60/60 results correctly
in Riyadh city. 0 barbershops (category exclusion worked). 93% had no
real website (confirms the core thesis). 85% had a mobile number. Gate
pass rate: 57% (vs 15% in the broken test — the province test was
diluted by small towns with worse phone coverage). Cost: $0.2402 for
60 places.

**Conclusion baked into the current config**: `harvest.py` always uses
`customGeolocation` (a real point + radius), never a text location
string. It always sets `maxReviews: 0, maxImages: 0` at harvest time —
review/image enrichment, if ever needed, happens only on the daily
batch of ~10-30 leads, never on the full harvest pull.

**A costly mistake worth knowing about**: two orphaned Apify runs were
triggered by a synchronous API call that timed out before Make's
connector returned a response — the run had actually started on
Apify's side and kept billing ($0.156 + $0.180) even though the tool
reported a connection failure. **Lesson**: never call Apify
synchronously for anything but a trivial request. `harvest.py` always
starts async (`POST .../runs`) and polls — this is already correct in
the code, don't regress it back to a sync call for convenience.

**Current spend** (as of the last session): ~$1.29 of the $5/month
Apify free tier used, across test runs. Real balance is queryable —
see "Checking your spend" below.

## Budget guard

`harvest.py` checks `spend_this_month` (a Supabase view summing
`spend_log`) before every single run and refuses if
`MONTHLY_BUDGET_USD` (default $4.00, leaving headroom under the $5
free tier) would be exceeded. It also passes `maxTotalChargeUsd` to
Apify itself as a second, server-side backstop — even a bug in the
budget check can't cause an unbounded bill.

`PROBE_PLACES=20` and `PROBE_CAP_USD=0.10` exist specifically so that
testing a new district or a config change never costs more than 10
cents. If you're about to test something, use
`python harvest.py --probe`, not a full run.

## Known open items — in priority order

1. **`template.html` does not exist yet.** The first version was
   rejected by Mohab ("قرف") with no specifics on why — only that
   priority was data/flow first. `sitegen.py` expects a file with a
   `const CONFIG = {...};` block it can regex-replace (see
   `CONFIG_RE` in `sitegen.py` for the exact contract). Get explicit
   direction on style before building this — don't guess twice.

2. **WhatsApp Business Cloud API is not yet set up.** Needs Meta
   Business Manager verification, which takes days, not minutes. Start
   this in parallel with everything else, not after.

3. **Instagram activity check (`pipeline.py::check_social`)** depends
   on Apify's `instagram-scraper` actor, which costs real money per
   call and was never live-tested end to end in this project. Budget
   for it before turning it on for every daily batch — or reconsider
   whether it should gate at all, given only ~22% of Al Malqa salons
   even had a discoverable Instagram link (see Test 2 numbers above).
   Currently `pipeline.py::verify()` still calls it; confirm this is
   worth its cost before the first real daily run.

4. **Netlify**: connected to this GitHub repo directly (not via API
   token — Mohab's Netlify account is GitHub-SSO-linked and the
   connector token approach was abandoned for that reason). Set
   **Publish directory = `sites`** in Netlify's site settings, or
   builds will be wrong. Domain `demo.axismarketinga.com` still needs
   to be attached in Netlify's domain settings.

5. **Harvest queue has 38 cells** (19 Riyadh districts × 2 keyword
   variants) already seeded in Supabase, priority-ranked (affluent
   north/west first). Only Al Malqa has been probed so far. The rest
   are `status = 'pending'`.

## Running things

```bash
# One-time setup
pip install -r requirements.txt
cp .env.example .env   # fill in real keys, never commit this file

# Sanity check on 20 places, max $0.10 — do this before any real harvest
python harvest.py --probe

# Full harvest of the next queued district
python harvest.py

# Keep going until budget or queue runs out
python harvest.py --all

# Daily send — reads from the pool, never re-scrapes
python daily.py

# Data-quality audit — discovery only, no writes, no spend beyond one scrape
python audit.py
```

`DRY_RUN=1` on `daily.py` builds sites and writes JSON output locally
but never pushes to git or sends WhatsApp — use it to check a batch
before it goes live.

## Checking your spend

```sql
select * from spend_this_month;      -- total $ spent this calendar month
select * from harvest_queue where status != 'pending';  -- what's been run
select * from next_ten;              -- today's best unsent candidates
select * from daily_ten;             -- what actually went out today
```

Supabase project: `mjetglnmivwphxyzflsz` ("axis-os-v2"), region
eu-central-1. Reachable via the Supabase MCP connector if available in
this environment, or via `SUPABASE_URL` + `SUPABASE_SERVICE_KEY` REST
calls otherwise.

## Things that are settled — don't relitigate

- **Harvest once, send daily.** Not the other way around.
- **Website exclusion is a hard gate, not a score weight.** A salon
  with a real working site never enters the pool, full stop.
- **WhatsApp verification = the send itself.** No pre-check API exists
  that's both free and reliable; don't go looking for one.
- **Barbershops excluded by string match in code, not by a paid
  category filter.** Costs nothing, already proven to work (0/60 in
  Test 2 vs 50% before the fix).
- **Async Apify calls only.** A sync call that times out still bills
  you for a run you can't see the result of.
- **Egyptian Arabic is wrong for this audience.** All Claude-generated
  copy (salon services, outreach message) must be Gulf/neutral Arabic
  — this is enforced in the system prompts in `content.py`.
- **No email/LinkedIn requirement for a lead to qualify.** An earlier
  version required both and would have rejected ~95% of the actual
  target market — most Riyadh salons have neither. They're enrichment
  fields now, never gates.

## Mohab's working style (carry this into how you talk to him)

Direct, fast, mixes Egyptian Arabic with English technical terms.
Wants decisions made for him, not options listed. Corrects sharply and
specifically when something's off — when that happens, don't patch
around it, address the actual root cause (see the "wrong website
check" and "wrong geolocation" fixes above for the pattern: he flags a
symptom, the fix should be structural, not cosmetic). Explicitly asked
for small, cheap tests (under 10 cents) before any real spend — respect
that on every future change to `harvest.py`.


## The demo template (v23+) — non-negotiable rules

The demo each salon receives is `template.html`, rendered per salon by
`sitegen.py` (CONFIG block regex-replace). Rules that must survive any edit:

- **Arabic never gets `letter-spacing`.** Tracking lives under
  `html[lang="en"]` only; Arabic uses `word-spacing`.
- **`body` overflow-x is `clip`, never `hidden`** — hidden makes body a
  scroll container and silently kills every `position:sticky` inside
  (this produced the three-screen beige void twice).
- Plates ship `srcset` 640/900/1300/1800 + `sizes=100vw`; the pinned
  frame loads eager/high — everything else lazy.
- No JS animation libraries. Motion is scroll-driven CSS (four verbs:
  rise/uncover/drift/hold) with an IntersectionObserver fallback.
- No video in the hero: iOS Low Power Mode disables autoplay and paints a
  grey play button over it. Decided after a real screenshot; do not revisit
  without new evidence.
- Booking is the native `<dialog>` four-step overlay ending in a composed
  WhatsApp message. Saudi numbers normalised from 05/5/+9665/009665.
- Demo honesty: no invented staff, reviews, awards or availability; the
  membership figures carry an "illustrative" line on-page. See
  `docs/demo-content.md`.
- Docs are the contract: `docs/creative-decisions.md` (100 numbered council
  decisions with status) is the implementation checklist; update statuses
  there rather than re-litigating in chat.
- Verification style: nothing is called fixed from the diff. Render at
  390×844 through the harness in `scratchpad/shot2.py`-style (same-origin
  iframe, real device height, scroll-confirmed) or measure with an injected
  probe. Chrome headless clamps its viewport to 500px — never screenshot the
  page directly at phone widths.
