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
    """Every place_id we've ever touched — so nothing is processed twice."""
    ids = set()
    for table in ("leads", "leads_discarded"):
        try:
            r = requests.get(f"{URL}/rest/v1/{table}", headers=H,
                             params={"select": "place_id", "limit": "50000"},
                             timeout=60)
            r.raise_for_status()
            ids |= {x["place_id"] for x in r.json() if x.get("place_id")}
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
