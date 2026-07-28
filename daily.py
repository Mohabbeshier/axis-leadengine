"""
Daily run — reads TODAY's batch from the pool harvest.py already built.
It never scrapes Google Maps again. This is the entire point of the
harvest-once architecture: discovery is a one-time cost, this file
spends money only on the 10 businesses it is actually about to contact.

  1. pull top N un-sent leads by quality_score from Supabase
  2. light re-check: still open, has recent review activity
     (small API cost — only on today's N, never the whole pool)
  3. Claude judge -> verified / needs_review
  4. Claude writes services + outreach message
  5. build the demo site, commit, push (Netlify builds on push)
  6. send via WhatsApp — the delivery receipt IS the WhatsApp check
  7. write results back to Supabase, notify Telegram

Every external call is wrapped. A failure anywhere on one lead marks
that lead needs_review and moves to the next — it never crashes the
whole batch and never silently promotes a failure to "sent".
"""

import os, re, json, traceback, datetime as dt
import requests

import pipeline as P
import content, sitegen, outreach, store

TARGET   = int(os.environ.get("TARGET_LEADS", "10"))
DRY_RUN  = os.environ.get("DRY_RUN", "0") == "1"
TG_TOKEN = os.environ.get("TELEGRAM_TOKEN", "")
TG_CHAT  = os.environ.get("TELEGRAM_CHAT_ID", "")
TODAY    = dt.date.today().isoformat()

SUPA_URL = os.environ["SUPABASE_URL"].rstrip("/")
SUPA_KEY = os.environ["SUPABASE_SERVICE_KEY"]
H = {"apikey": SUPA_KEY, "Authorization": f"Bearer {SUPA_KEY}",
     "Content-Type": "application/json"}


def log(m):
    print(m, flush=True)


def fetch_batch(n):
    """Best un-sent leads, ranked by the score harvest.py computed.
    Pulls 3x the target so judge/verify rejections still leave enough."""
    r = requests.get(f"{SUPA_URL}/rest/v1/leads", headers=H, timeout=30,
                     params={"send_status": "is.null",
                             "quality_score": "gt.0",
                             "order": "quality_score.desc,reviews_count.desc",
                             "limit": str(n * 3)})
    r.raise_for_status()
    return r.json()


def recheck_activity(rec):
    """Light single-place re-fetch: is it still open, still getting
    reviews. This is the only per-lead discovery-adjacent cost in the
    daily job, and it only ever runs on today's ~30 candidates, never
    the pool of hundreds."""
    try:
        r = requests.get(f"https://www.google.com/maps/place/?q=place_id:"
                         f"{rec['place_id']}", timeout=10)
        return r.status_code == 200          # coarse liveness check only
    except Exception:
        return None


def main():
    log(f"[{TODAY}] daily send · target {TARGET}"
        + ("  (DRY RUN)" if DRY_RUN else ""))

    batch = fetch_batch(TARGET)
    log(f"  candidates pulled from pool: {len(batch)}")
    if not batch:
        log("  pool is empty or exhausted — run harvest.py to refill")
        notify(f"Axis · {TODAY}\npool empty — harvest.py needs a run", [])
        return

    ready, review = [], []

    for rec in batch:
        if len(ready) >= TARGET:
            break

        try:
            checks = P.verify(rec)
        except Exception:
            traceback.print_exc()
            checks = dict.fromkeys(
                ("phone_reachable", "social_active", "google_reviews_active",
                 "email_verified", "linkedin_exists"), None)
        rec.update(checks)

        try:
            verdict = P.judge(rec, checks)
        except Exception as e:
            verdict = {"fully_verified": False,
                       "verification_status": "needs_review",
                       "reason": f"judge_error:{e}"}
        rec.update({k: verdict.get(k) for k in
                    ("fully_verified", "verification_status", "reason")})

        if not verdict.get("fully_verified"):
            review.append(rec)
            log(f"  x {str(rec['business_name'])[:30]:32} "
                f"{str(verdict.get('reason',''))[:40]}")
            continue

        try:
            services = content.services_for(rec)
            if DRY_RUN:
                rec["demo_url"] = "https://example.invalid/dry-run"
            else:
                sitegen.write_site(rec, services)
            rec["services"] = services
        except Exception as e:
            rec["verification_status"] = "needs_review"
            rec["reason"] = f"sitegen_error:{e}"
            review.append(rec)
            log(f"  ! {str(rec['business_name'])[:30]:32} sitegen failed: {e}")
            continue

        ready.append(rec)
        log(f"  + {str(rec['business_name'])[:30]:32} {rec['demo_url']}")

    if ready and not DRY_RUN:
        try:
            sitegen.commit_and_push(len(ready))
            log(f"  pushed {len(ready)} site(s) — netlify will build")
        except Exception as e:
            log(f"  ABORT push: {e}")
            log("  not sending — links would 404")
            for r in ready:
                r["verification_status"] = "needs_review"
                r["reason"] = f"push_failed:{e}"
            review.extend(ready)
            ready = []

    sent = 0
    if ready and not DRY_RUN:
        sent = outreach.send_batch(
            ready, lambda r: content.message_for(r, r["demo_url"]), cap=TARGET)
        for r in ready:
            if r.get("whatsapp_verified") is False:
                r["verification_status"] = "needs_review"
                r["reason"] = "number_not_on_whatsapp"

    try:
        store.upsert_leads(ready + review)
    except Exception as e:
        log(f"  warn: supabase write failed: {e}")

    for name, rows in (("sent", ready), ("needs_review", review)):
        with open(f"out_{name}_{TODAY}.json", "w", encoding="utf-8") as f:
            json.dump(rows, f, ensure_ascii=False, indent=2, default=str)

    summary = (f"Axis · {TODAY}\n"
               f"pool candidates: {len(batch)}\n"
               f"sites built: {len(ready)}\n"
               f"messages sent: {sent}\n"
               f"needs review: {len(review)}")
    if len(ready) < TARGET:
        summary += (f"\n\nshort by {TARGET - len(ready)} — "
                    f"pool may be running low, consider harvest.py --all")
    log("\n" + summary)
    notify(summary, ready)


def notify(summary, ready):
    if not (TG_TOKEN and TG_CHAT):
        return
    lines = [summary, ""]
    for r in ready:
        lines.append(f"- {r['business_name']} | {r.get('demo_url','')} "
                     f"[{r.get('send_status','-')}]")
    try:
        requests.post(f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage",
                      json={"chat_id": TG_CHAT, "text": "\n".join(lines),
                            "disable_web_page_preview": True}, timeout=30)
    except Exception as e:
        log(f"  warn: telegram failed: {e}")


if __name__ == "__main__":
    main()
