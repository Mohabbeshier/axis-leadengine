"""
Harvest — run once per district, then never again.

Discovery is a one-time cost. The daily job reads from the pool this
builds; it does not scrape to find new businesses.

Cheap by design:
  - no reviews, no images, no paid filters in this pass  ($0.004/place)
  - geolocation is a real circle, not a place name, so results stay in Riyadh
  - barbershops are dropped in code (free) instead of by a paid filter
  - hard budget check before every single run

    python harvest.py            # process the next pending cell
    python harvest.py --all      # keep going until budget or queue runs out
"""

import os, re, sys, json, time, requests

APIFY_TOKEN = os.environ["APIFY_TOKEN"]
SUPA_URL    = os.environ["SUPABASE_URL"].rstrip("/")
SUPA_KEY    = os.environ["SUPABASE_SERVICE_KEY"]

MONTHLY_BUDGET_USD = float(os.environ.get("MONTHLY_BUDGET_USD", "4.00"))
MAX_PER_CELL       = int(os.environ.get("MAX_PLACES_PER_CELL", "120"))

# A probe answers "is this cell worth harvesting" — it does not need volume.
# 20 places * $0.004 = $0.08. Hard ceiling, not a suggestion.
PROBE_PLACES   = int(os.environ.get("PROBE_PLACES", "20"))
PROBE_CAP_USD  = float(os.environ.get("PROBE_CAP_USD", "0.10"))

P_PLACE = 0.004          # measured from a live run
ACTOR   = "compass~crawler-google-places"

H = {"apikey": SUPA_KEY, "Authorization": f"Bearer {SUPA_KEY}",
     "Content-Type": "application/json"}

# Google returns men's barbershops for almost any salon query in Arabic.
# Dropping them here costs nothing; a paid category filter would cost
# $0.001 per place scraped.
EXCLUDE_CATEGORIES = ("صالون حلاقة", "حلاق", "barber")
EXCLUDE_NAME_HINTS = ("حلاق", "للحلاقة", "للحلاقه", "barber")


# ---------------------------------------------------------------- budget
def spent_this_month():
    r = requests.get(f"{SUPA_URL}/rest/v1/spend_this_month",
                     headers=H, timeout=30)
    r.raise_for_status()
    rows = r.json()
    return float(rows[0]["spent_usd"]) if rows else 0.0


def budget_left():
    return MONTHLY_BUDGET_USD - spent_this_month()


def log_spend(run_id, purpose, places, cost):
    requests.post(f"{SUPA_URL}/rest/v1/spend_log", headers=H, timeout=30,
                  data=json.dumps({"run_id": run_id, "purpose": purpose,
                                   "places": places, "cost_usd": round(cost, 4)}))


# ---------------------------------------------------------------- queue
def next_cell():
    r = requests.get(f"{SUPA_URL}/rest/v1/harvest_queue", headers=H, timeout=30,
                     params={"status": "eq.pending", "order": "priority.asc,id.asc",
                             "limit": "1"})
    r.raise_for_status()
    rows = r.json()
    return rows[0] if rows else None


def mark(cell_id, **fields):
    requests.patch(f"{SUPA_URL}/rest/v1/harvest_queue", headers=H, timeout=30,
                   params={"id": f"eq.{cell_id}"},
                   data=json.dumps(fields))


# ---------------------------------------------------------------- apify
def run_actor(cell, probe=False):
    """Async start, then poll. Sync endpoints time out on long scrapes
    and still bill you for the run you never got back."""
    limit = PROBE_PLACES if probe else MAX_PER_CELL
    cap   = PROBE_CAP_USD if probe else round(min(budget_left(), 1.0), 2)
    # Apify rejects maxTotalChargeUsd below $0.50 (400: max-total-charge-usd-
    # below-minimum). The REAL cost control is maxItems (20 * $0.004 = $0.08
    # on a probe); this server-side cap is only the disaster backstop, so
    # raising its floor to Apify's minimum does not change expected spend.
    cap   = max(cap, 0.50)
    payload = {
        "searchStringsArray": [cell["keyword"]],
        "language": "ar",
        "maxCrawledPlacesPerSearch": limit,
        # a real circle — 'Riyadh, Saudi Arabia' as text resolves to the
        # whole province and returns towns 600km away
        "customGeolocation": {
            "type": "Point",
            "coordinates": [float(cell["lng"]), float(cell["lat"])],
            "radiusKm": float(cell["radius_m"]) / 1000.0,
        },
        # everything below is deliberately off — each one is billed per place
        "maxReviews": 0,
        "maxImages": 0,
        "scrapeReviewsPersonalData": False,
        "skipClosedPlaces": False,
    }
    start = requests.post(
        f"https://api.apify.com/v2/acts/{ACTOR}/runs",
        params={"token": APIFY_TOKEN, "maxTotalChargeUsd": cap,
                "maxItems": limit},
        json=payload, timeout=60)
    start.raise_for_status()
    run = start.json()["data"]
    run_id, ds_id = run["id"], run["defaultDatasetId"]
    print(f"    run {run_id}  (limit {limit}, cap ${cap})")

    for _ in range(90):                      # up to ~15 min
        time.sleep(10)
        try:
            st = requests.get(f"https://api.apify.com/v2/actor-runs/{run_id}",
                              params={"token": APIFY_TOKEN}, timeout=30).json()["data"]
        except Exception:
            # transient network blip while POLLING must not orphan the run —
            # the run keeps going (and billing) on Apify's side regardless.
            # Just poll again; the 90-iteration cap still bounds us.
            continue
        if st["status"] in ("SUCCEEDED", "FAILED", "ABORTED", "TIMED-OUT"):
            return run_id, ds_id, st["status"], float(st.get("usageTotalUsd") or 0)
    return run_id, ds_id, "TIMEOUT", 0.0


def fetch(ds_id):
    r = requests.get(f"https://api.apify.com/v2/datasets/{ds_id}/items",
                     params={"token": APIFY_TOKEN, "clean": "true", "limit": 1000},
                     timeout=120)
    r.raise_for_status()
    return r.json()


# ---------------------------------------------------------------- filter
def has_real_website(p):
    """True only if the website field is an actual own site — not a
    social link, booking-SaaS page, or click-to-chat wrapper.
    These businesses already have a functioning digital front door
    and are not a fit; they must never enter the pool at all."""
    site = (p.get("website") or "").lower()
    if not site:
        return False
    parked = ("instagram.", "facebook.", "linktr.ee", "wa.me", "snapchat.",
              "twitter.", "x.com", "tiktok.", "fresha.com", "bookr.co")
    return not any(s in site for s in parked)


def need_flag_for(p):
    site = (p.get("website") or "").lower()
    if not site:
        return "no_website"
    if any(s in site for s in ("instagram.", "facebook.", "linktr.ee",
                               "wa.me", "snapchat.", "twitter.", "x.com",
                               "tiktok.")):
        return "social_as_website"
    if any(s in site for s in ("fresha.com", "bookr.co")):
        return "booking_saas_only"
    return None


def _extract_instagram(website):
    """Google Maps (on this plan) has no dedicated social field — an
    Instagram profile only shows up when the salon put it in the
    'website' slot. This is the only place to recover it from."""
    if website and "instagram." in website.lower():
        return website
    return None


def keep(p):
    cat = (p.get("categoryName") or "")
    name = (p.get("title") or "")
    if any(x in cat for x in EXCLUDE_CATEGORIES):
        return False
    if any(x in name for x in EXCLUDE_NAME_HINTS):
        return False
    if p.get("permanentlyClosed"):
        return False
    # the hard gates that make this business a lead at all
    if has_real_website(p):
        return False                        # already has a real site — not our market
    if (p.get("totalScore") or 0) < 4.0:
        return False
    if (p.get("reviewsCount") or 0) < 50:
        return False
    phone = re.sub(r"\D", "", p.get("phone") or "")
    is_mobile = phone.startswith("9665") or (phone.startswith("05") and len(phone) == 10)
    if not is_mobile:
        return False
    return True


def quality_score(p):
    """0-100. Decides who gets contacted first, not who gets kept.

    Weighted on what actually predicts a reply:
      volume of reviews  = a real business with real customers
      rating             = they care about reputation
      no website at all  = the gap is obvious to them, not a debate
      mobile number      = we can actually reach them
    """
    rev = p.get("reviewsCount") or 0
    rating = p.get("totalScore") or 0
    # below the gate the score is meaningless — a 4.5 rating on 4 reviews
    # is noise, and must never outrank a 4.0 on 500
    if rev < 50 or rating < 4.0:
        return 0

    score = 0
    if   rev >= 500: score += 40
    elif rev >= 250: score += 32
    elif rev >= 100: score += 24
    elif rev >=  50: score += 14

    if   rating >= 4.5: score += 25
    elif rating >= 4.2: score += 20
    elif rating >= 4.0: score += 14

    site = (p.get("website") or "").lower()
    if not site:                                   score += 25   # cleanest pitch
    elif any(s in site for s in ("instagram", "snapchat",
                                 "linktr", "wa.me")):  score += 20
    elif any(s in site for s in ("fresha", "bookr")):   score += 10
    else:                                          score += 0    # has a real site

    phone = re.sub(r"\D", "", p.get("phone") or "")
    if phone.startswith("9665") or phone.startswith("05"):
        score += 10
    return min(score, 100)


def store(places, cell):
    rows = []
    for p in places:
        if not p.get("placeId"):
            continue
        rows.append({
            "place_id":      p["placeId"],
            "business_name": p.get("title"),
            "category":      p.get("categoryName"),
            "city":          p.get("city") or cell["city"],
            "area":          p.get("neighborhood") or cell["district"],
            "address":       p.get("address"),
            "phone":         (p.get("phone") or "").replace(" ", ""),
            "website_url":   p.get("website"),
            "instagram":     _extract_instagram(p.get("website")),
            "rating":        p.get("totalScore"),
            "reviews_count": p.get("reviewsCount"),
            "maps_url":      p.get("url"),
            "status":        "open",
            "need_flag":     need_flag_for(p),
            "quality_score": quality_score(p),
            "verification_status": "needs_review",   # nothing verified yet
        })
    if not rows:
        return 0
    r = requests.post(f"{SUPA_URL}/rest/v1/leads",
                      headers={**H, "Prefer": "resolution=ignore-duplicates"},
                      data=json.dumps(rows, ensure_ascii=False).encode(), timeout=120)
    if not r.ok:
        # surface the PostgREST error body — a bare 400 once cost a debugging
        # round-trip (constraint violation was invisible)
        raise RuntimeError(f"supabase store failed {r.status_code}: {r.text[:300]}")
    return len(rows)


# ---------------------------------------------------------------- main
def harvest_one(probe=False):
    left = budget_left()
    if left <= 0.05:
        print(f"  STOP: monthly budget exhausted (${MONTHLY_BUDGET_USD} cap)")
        return False

    cell = next_cell()
    if not cell:
        print("  queue empty — Riyadh is fully harvested")
        return False

    print(f"  {cell['district']} / {cell['keyword']}  "
          f"(budget left ${left:.2f})")
    mark(cell["id"], status="running")

    try:
        run_id, ds_id, status, cost = run_actor(cell, probe=probe)
        if status != "SUCCEEDED":
            mark(cell["id"], status="failed", error=status)
            print(f"    {status}")
            return True

        raw = fetch(ds_id)
        kept = [p for p in raw if keep(p)]
        n = store(kept, cell)
        cost = cost or len(raw) * P_PLACE
        log_spend(run_id, "harvest", len(raw), cost)
        mark(cell["id"], status="done", places_found=n,
             cost_usd=round(cost, 4), last_run_at="now()")
        print(f"    pulled {len(raw)}, kept {len(kept)}, stored {n}, "
              f"${cost:.3f}")
        return True

    except Exception as e:
        mark(cell["id"], status="failed", error=str(e)[:300])
        print(f"    ERROR {e}")
        return True


if __name__ == "__main__":
    probe = "--probe" in sys.argv
    if "--all" in sys.argv:
        while harvest_one():
            pass
    else:
        harvest_one(probe=probe)
    print(f"\n  spent this month: ${spent_this_month():.2f} / ${MONTHLY_BUDGET_USD}")
