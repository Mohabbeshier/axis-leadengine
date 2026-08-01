"""Storage — Supabase REST. Dedupe is enforced on place_id."""

import os, json, requests

URL = os.environ["SUPABASE_URL"].rstrip("/")
KEY = os.environ["SUPABASE_SERVICE_KEY"]
H = {"apikey": KEY, "Authorization": f"Bearer {KEY}",
     "Content-Type": "application/json"}

KEEP = ("place_id", "business_name", "category", "city", "area", "address",
        "phone", "website_url", "rating", "reviews_count", "last_review_date",
        "status", "instagram", "facebook", "maps_url", "email", "need_flag",
        "review_age_days", "last_post_age_days",
        "whatsapp_verified", "social_active", "google_reviews_active",
        "phone_reachable", "phone_is_mobile", "reviews_last_90d",
        "email_verified", "linkedin_exists", "fully_verified",
        "verification_status", "reason", "demo_url", "demo_slug",
        "send_status", "wa_message_id", "date_found")


def seen_place_ids():
    """Every place_id we've ever touched — so nothing is processed twice.

    Paginated: Supabase caps a single response at max-rows (1000 by
    default) regardless of the limit param. A single request would
    silently truncate once the pool passes that — and a truncated
    dedupe set means re-processing leads we already have."""
    ids = set()
    for table in ("leads", "leads_discarded"):
        try:
            offset, page = 0, 1000
            while True:
                r = requests.get(f"{URL}/rest/v1/{table}", headers=H,
                                 params={"select": "place_id",
                                         "limit": str(page),
                                         "offset": str(offset)},
                                 timeout=60)
                r.raise_for_status()
                rows = r.json()
                ids |= {x["place_id"] for x in rows if x.get("place_id")}
                if len(rows) < page:
                    break
                offset += page
        except Exception as e:
            print(f"  warn: could not read {table}: {e}")
    return ids


def _clean(rec):
    return {k: rec.get(k) for k in KEEP if k in rec}


def upsert_leads(rows):
    if not rows:
        return
    r = requests.post(f"{URL}/rest/v1/leads",
                      headers={**H, "Prefer": "resolution=merge-duplicates"},
                      data=json.dumps([_clean(x) for x in rows],
                                      ensure_ascii=False).encode(),
                      timeout=90)
    r.raise_for_status()


def upsert_discarded(rows):
    if not rows:
        return
    slim = [{"place_id": x.get("place_id"),
             "business_name": x.get("business_name"),
             "gate_failed": x.get("gate_failed"),
             "date_checked": x.get("date_found")} for x in rows]
    r = requests.post(f"{URL}/rest/v1/leads_discarded",
                      headers={**H, "Prefer": "resolution=merge-duplicates"},
                      data=json.dumps(slim, ensure_ascii=False).encode(),
                      timeout=90)
    r.raise_for_status()
