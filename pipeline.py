"""
Axis Lead Engine — stage 1-3
Discovery -> hard gates -> channel verification -> Claude verdict

Nothing here requires a human. Every check is an API call.
A check that errors returns None ("unknown") and routes to needs_review.
It never silently passes.
"""

import os, re, json, smtplib, datetime as dt
from urllib.parse import urlparse
import requests

APIFY_TOKEN    = os.environ["APIFY_TOKEN"]
ANTHROPIC_KEY  = os.environ["ANTHROPIC_API_KEY"]
GOOGLE_CSE_KEY = os.environ.get("GOOGLE_CSE_KEY", "")
GOOGLE_CSE_ID  = os.environ.get("GOOGLE_CSE_ID", "")
PAGESPEED_KEY  = os.environ.get("PAGESPEED_KEY", "")

CITY           = os.environ.get("TARGET_CITY", "Riyadh")
CATEGORY       = os.environ.get("TARGET_CATEGORY", "beauty salon")
MAX_PULL       = int(os.environ.get("MAX_PULL", "120"))
ENABLE_IG_CHECK = os.environ.get("ENABLE_IG_CHECK", "0") == "1"

MIN_RATING       = 4.0
MIN_REVIEWS      = 50
REVIEW_MAX_AGE_D = 90
MIN_REVIEWS_90D  = 5      # real ongoing flow, not one stray review
SOCIAL_MAX_AGE_D = 30
MOBILE_SCORE_MIN = 0.60

TIMEOUT = 20
UA = {"User-Agent": "Mozilla/5.0 (compatible; AxisLeadEngine/1.0)"}
APIFY = "https://api.apify.com/v2/acts"


def _now():
    return dt.datetime.now(dt.timezone.utc)


def _age_days(iso):
    if not iso:
        return None
    try:
        d = dt.datetime.fromisoformat(str(iso).replace("Z", "+00:00"))
        if not d.tzinfo:
            d = d.replace(tzinfo=dt.timezone.utc)
        return (_now() - d).days
    except Exception:
        return None


def _actor(slug, payload, timeout=600):
    r = requests.post(f"{APIFY}/{slug}/run-sync-get-dataset-items"
                      f"?token={APIFY_TOKEN}", json=payload, timeout=timeout)
    r.raise_for_status()
    return r.json()


# ------------------------------------------------------------ stage 1
def discover():
    return _actor("compass~crawler-google-places", {
        "searchStringsArray": [CATEGORY],
        "locationQuery": CITY,
        "language": "ar",
        "maxCrawledPlacesPerSearch": MAX_PULL,
        "skipClosedPlaces": True,
        "scrapeReviewsPersonalData": False,
        "maxReviews": 20,
        "reviewsSort": "newest",   # critical: default sort is by relevance,
                                   # which makes "last review date" meaningless
    })


def normalize(p):
    imgs = p.get("imageUrls")
    phone = re.sub(r"[^\d+]", "", p.get("phone") or "")
    return {
        "place_id":         p.get("placeId"),
        "business_name":    p.get("title"),
        "category":         p.get("categoryName"),
        "city":             CITY,
        "area":             p.get("neighborhood") or p.get("street"),
        "address":          p.get("address"),
        "phone":            phone,
        "phone_is_mobile":  is_saudi_mobile(phone),
        "website_url":      p.get("website"),
        "rating":           p.get("totalScore"),
        "reviews_count":    p.get("reviewsCount"),
        "last_review_date": _pick_last_review(p),
        "reviews_last_90d": _recent_review_count(p, 90),
        "status":           "closed" if p.get("permanentlyClosed") else "open",
        "instagram":        _social(p, "instagram"),
        "facebook":         _social(p, "facebook"),
        "maps_url":         p.get("url"),
        "opening_hours":    _hours(p),
        "top_reviews":      _reviews(p),
        "photos":           imgs[:6] if isinstance(imgs, list) else [],
        "date_found":       _now().date().isoformat(),
    }


def is_saudi_mobile(phone):
    """Landlines have no WhatsApp. Saudi mobiles are 05x / +9665x.
    None = genuinely can't tell (foreign or malformed)."""
    d = re.sub(r"\D", "", phone or "")
    if not d:
        return False
    if d.startswith("00"):
        d = d[2:]
    if d.startswith("966"):
        rest = d[3:]
        if len(rest) == 9:
            return rest.startswith("5")
        return None
    if d.startswith("0") and len(d) in (9, 10):
        return d.startswith("05")      # 011/012/013... = landline
    return None


def _recent_review_count(p, days):
    """How many of the sampled reviews landed in the last N days.
    This is the real 'in demand' signal — freshness alone is not."""
    n = 0
    for r in (p.get("reviews") or []):
        a = _age_days(r.get("publishedAtDate"))
        if a is not None and a <= days:
            n += 1
    return n


def _pick_last_review(p):
    ds = [r.get("publishedAtDate") for r in (p.get("reviews") or [])
          if r.get("publishedAtDate")]
    return max(ds) if ds else None


def _social(p, kind):
    pools = [(p.get("additionalInfo", {}) or {}).get("links", []) or [],
             p.get("socialMedias") or []]
    for pool in pools:
        for u in pool:
            if kind in str(u).lower():
                return str(u)
    return None


def _hours(p):
    oh = p.get("openingHours") or []
    return "، ".join(f"{d.get('day','')} {d.get('hours','')}".strip()
                     for d in oh if isinstance(d, dict))[:300]


def _reviews(p):
    out = []
    for r in (p.get("reviews") or [])[:6]:
        t = (r.get("text") or "").strip()
        if 40 <= len(t) <= 240 and (r.get("stars") or 0) >= 4:
            out.append({"text": t, "who": (r.get("name") or "عميلة")[:18]})
    return out[:3]


# ------------------------------------------------------------ stage 2
def gate(rec):
    """Returns (passed, need_flag, reason)."""

    # Gate 0 — reachable at all. Without a mobile number there is no
    # outreach, so this is discarded before we spend any API call on it.
    if not rec.get("phone"):
        return False, None, "no_phone"
    if rec.get("phone_is_mobile") is False:
        return False, None, "landline_no_whatsapp"

    # Gate 1 — alive
    if rec["status"] != "open":
        return False, None, "permanently_closed"
    if not rec["rating"] or rec["rating"] < MIN_RATING:
        return False, None, "rating_below_min"
    if not rec["reviews_count"] or rec["reviews_count"] < MIN_REVIEWS:
        return False, None, "reviews_below_min"

    # Gate 2 — in demand. Freshness alone is weak: one recent review can
    # come from a dying salon. Volume in the window is the real signal.
    age = _age_days(rec["last_review_date"])
    if age is None:
        return False, None, "no_review_date"
    if age > REVIEW_MAX_AGE_D:
        return False, None, f"last_review_{age}d"
    if rec.get("reviews_last_90d", 0) < MIN_REVIEWS_90D:
        return False, None, f"only_{rec.get('reviews_last_90d',0)}_reviews_90d"
    rec["review_age_days"] = age

    # Gate 3 — actually needs us
    site = rec["website_url"]
    if not site:
        return True, "no_website", "ok"

    host = urlparse(site).netloc.lower()
    if any(s in host for s in ("instagram.", "facebook.", "linktr.ee", "wa.me",
                               "twitter.", "x.com", "tiktok.", "snapchat.")):
        return True, "social_as_website", "ok"

    h = site_health(site)
    rec["site_health"] = h
    if h["reachable"] is False:
        return True, "broken_site", "ok"
    if h["mobile_score"] is not None and h["mobile_score"] < MOBILE_SCORE_MIN:
        return True, "not_mobile_friendly", "ok"
    return False, None, "has_working_site"


def site_health(url):
    out = {"reachable": None, "status_code": None, "mobile_score": None}
    try:
        r = requests.get(url, timeout=TIMEOUT, headers=UA, allow_redirects=True)
        out["status_code"] = r.status_code
        out["reachable"] = r.status_code < 400
    except Exception:
        out["reachable"] = False
        return out
    if PAGESPEED_KEY:
        try:
            ps = requests.get(
                "https://www.googleapis.com/pagespeedonline/v5/runPagespeed",
                params={"url": url, "strategy": "mobile",
                        "key": PAGESPEED_KEY, "category": "performance"},
                timeout=90).json()
            out["mobile_score"] = ps["lighthouseResult"]["categories"]["performance"]["score"]
        except Exception:
            pass
    return out


# ------------------------------------------------------------ stage 3
def verify(rec):
    """Channel checks for the DAILY job, operating on a Supabase row that
    harvest.py already wrote — not on a fresh Apify record. Only reads
    fields that actually exist on that row.

    phone_reachable and google_reviews_active are re-derived from stored
    fields rather than re-fetched, since harvest.py already gated on
    rating>=4.0 and reviews_count>=50 before this row ever entered the
    pool. Re-checking them here would just repeat a paid Apify call for
    a fact we already know.

    social_active is enrichment-only and does NOT gate leads in or out.
    The paid Apify Instagram scraper is skipped unless ENABLE_IG_CHECK=1
    is set in the environment — by default social_active is None.
    """
    phone = re.sub(r"\D", "", rec.get("phone") or "")
    is_mobile = phone.startswith("9665") or (phone.startswith("05") and len(phone) == 10)

    return {
        "phone_reachable":       is_mobile and bool(phone),
        "google_reviews_active": (rec.get("reviews_count") or 0) >= MIN_REVIEWS,
        "social_active":         check_social(rec) if ENABLE_IG_CHECK else None,
        "whatsapp_verified":     None,          # set by the send receipt
        # enrichment only, never gates a lead out
        "email_verified":        check_email(rec),
        "linkedin_exists":       check_linkedin(rec),
    }


def check_social(rec):
    """Last Instagram post within 30 days, via Apify IG scraper."""
    ig = rec.get("instagram")
    if not ig:
        return False if not rec.get("facebook") else None
    handle = ig.rstrip("/").split("/")[-1].split("?")[0]
    if not handle:
        return None
    try:
        items = _actor("apify~instagram-scraper", {
            "directUrls": [f"https://www.instagram.com/{handle}/"],
            "resultsType": "posts",
            "resultsLimit": 3,
            "addParentData": False,
        }, timeout=300)
    except Exception:
        return None
    ts = [i.get("timestamp") for i in items if i.get("timestamp")]
    if not ts:
        return None
    age = _age_days(max(ts))
    if age is None:
        return None
    rec["last_post_age_days"] = age
    return age <= SOCIAL_MAX_AGE_D


EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
JUNK = ("example.", "sentry.", "wixpress.", "@2x", ".png", ".jpg", "godaddy")


def check_email(rec):
    site = rec.get("website_url")
    if not site or rec.get("site_health", {}).get("reachable") is not True:
        return False
    try:
        html = requests.get(site, timeout=TIMEOUT, headers=UA).text
    except Exception:
        return None
    found = [e for e in EMAIL_RE.findall(html)
             if not any(j in e.lower() for j in JUNK)]
    if not found:
        return False
    email = sorted(set(found), key=len)[0]
    rec["email"] = email
    return smtp_probe(email)


def smtp_probe(email):
    """250 = deliverable, 550 = dead, anything else = unknown (None)."""
    try:
        import dns.resolver
        domain = email.split("@")[1]
        mx = sorted(dns.resolver.resolve(domain, "MX"),
                    key=lambda r: r.preference)[0].exchange.to_text()
    except Exception:
        return None
    try:
        s = smtplib.SMTP(timeout=15)
        s.connect(mx, 25)
        s.helo("axismarketinga.com")
        s.mail("verify@axismarketinga.com")
        code, _ = s.rcpt(email)
        s.quit()
        if code == 250:
            return True
        if code in (550, 551, 553):
            return False
        return None
    except Exception:
        return None


def check_linkedin(rec):
    """Existence only — no activity scraping (ToS)."""
    if not (GOOGLE_CSE_KEY and GOOGLE_CSE_ID):
        return None
    try:
        r = requests.get("https://www.googleapis.com/customsearch/v1",
                         params={"key": GOOGLE_CSE_KEY, "cx": GOOGLE_CSE_ID,
                                 "q": f'site:linkedin.com/company "{rec["business_name"]}"'},
                         timeout=TIMEOUT).json()
        return int(r.get("searchInformation", {}).get("totalResults", 0)) > 0
    except Exception:
        return None


# ------------------------------------------------------------ stage 4
JUDGE_SYSTEM = """You are a lead-verification judge for Axis. You receive one business record with channel checks already computed upstream. You have no external access — never re-verify, never infer a missing value.

DECIDING FIELDS (these two only)
- phone_reachable
- google_reviews_active

RULES
- fully_verified = true ONLY if BOTH deciding fields (phone_reachable, google_reviews_active) are true.
- Any null among them = fully_verified false, status "needs_review".
- whatsapp_verified is resolved later at send time — ignore it.
- social_active is enrichment/context only. NEVER let it fail a lead — a salon with weak or no social presence is exactly the profile we want.
- email_verified and linkedin_exists are enrichment only. NEVER let either
  one fail a lead. A salon with no email and no LinkedIn is normal and is
  exactly the profile we want.
- Raise name_mismatch_flag only if the business name and the website/email
  domain clearly belong to different businesses. An Arabic name that does
  not transliterate to the domain is NOT a mismatch.
- Never round "probably" up to true.

Output ONLY this JSON. No markdown, no prose outside "reason".
{"place_id":str,"business_name":str,"fully_verified":bool,"verification_status":"verified"|"needs_review","name_mismatch_flag":bool,"reason":str}"""


def judge(rec, checks):
    slim = {k: rec.get(k) for k in
            ("place_id", "business_name", "website_url", "email",
             "instagram", "need_flag", "review_age_days",
             "last_post_age_days", "reviews_last_90d", "phone_is_mobile")}
    body = {"model": "claude-sonnet-4-6", "max_tokens": 300, "temperature": 0,
            "system": JUDGE_SYSTEM,
            "messages": [{"role": "user",
                          "content": json.dumps({**slim, **checks}, ensure_ascii=False)}]}
    r = requests.post("https://api.anthropic.com/v1/messages",
                      headers={"x-api-key": ANTHROPIC_KEY,
                               "anthropic-version": "2023-06-01",
                               "content-type": "application/json"},
                      json=body, timeout=60)
    r.raise_for_status()
    txt = "".join(b.get("text", "") for b in r.json()["content"]
                  if b.get("type") == "text").strip()
    txt = re.sub(r"^```(?:json)?|```$", "", txt).strip()
    return json.loads(txt)
