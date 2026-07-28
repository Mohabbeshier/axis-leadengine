"""
Data audit — discovery only. No verification calls, no deploys, no sends.

Answers the only question that matters before running anything:
does Google Maps actually carry the fields this system depends on,
and how many businesses survive each gate?

    python audit.py            # Riyadh / beauty salon
    TARGET_CATEGORY="dental clinic" python audit.py

Costs one Apify run. Nothing else.
"""

import os, json, collections, datetime as dt
import pipeline as P

SAMPLE = int(os.environ.get("AUDIT_SAMPLE", "120"))


def pct(n, d):
    return f"{(100.0 * n / d):5.1f}%" if d else "   n/a"


def bar(n, d, width=28):
    filled = int(width * n / d) if d else 0
    return "#" * filled + "." * (width - filled)


def main():
    print(f"\nAUDIT · {P.CATEGORY} · {P.CITY} · sample {SAMPLE}\n" + "=" * 62)

    P.MAX_PULL = SAMPLE
    raw = P.discover()
    recs = [P.normalize(p) for p in raw]
    recs = [r for r in recs if r.get("place_id")]
    n = len(recs)
    print(f"pulled: {n} unique listings\n")

    # ---- field coverage -------------------------------------------------
    print("FIELD COVERAGE")
    fields = [
        ("phone",            lambda r: bool(r["phone"])),
        ("phone is mobile",  lambda r: r["phone_is_mobile"] is True),
        ("website",          lambda r: bool(r["website_url"])),
        ("instagram",        lambda r: bool(r["instagram"])),
        ("facebook",         lambda r: bool(r["facebook"])),
        ("rating",           lambda r: r["rating"] is not None),
        ("reviews_count",    lambda r: bool(r["reviews_count"])),
        ("last_review_date", lambda r: bool(r["last_review_date"])),
        ("opening_hours",    lambda r: bool(r["opening_hours"])),
        ("usable reviews",   lambda r: len(r["top_reviews"]) >= 2),
        ("photos >= 3",      lambda r: len(r["photos"]) >= 3),
    ]
    for label, fn in fields:
        c = sum(1 for r in recs if fn(r))
        print(f"  {label:18} {pct(c, n)}  {bar(c, n)}  {c}/{n}")

    # ---- the gate funnel ------------------------------------------------
    print("\nGATE FUNNEL")
    reasons = collections.Counter()
    need_flags = collections.Counter()
    passed = []

    for r in recs:
        ok, flag, why = P.gate(dict(r))   # copy: gate mutates
        if ok:
            passed.append(r)
            need_flags[flag] += 1
        else:
            reasons[why] += 1

    print(f"  entered           {n}")
    for why, c in reasons.most_common():
        print(f"    rejected: {why:26} {c:4}  ({pct(c, n).strip()})")
    print(f"  passed all gates  {len(passed)}   ({pct(len(passed), n).strip()})")

    if need_flags:
        print("\n  why they need us:")
        for flag, c in need_flags.most_common():
            print(f"    {flag:24} {c:4}")

    # ---- what this means in practice ------------------------------------
    print("\nPROJECTION")
    rate = len(passed) / n if n else 0
    print(f"  gate pass rate         {rate*100:.1f}%")
    print(f"  pull needed for 10/day {int(10 / rate) if rate else '—'} listings")
    reachable = sum(1 for r in passed
                    if r["phone_is_mobile"] is True and r["instagram"])
    print(f"  of those, contactable  {reachable}/{len(passed)}"
          f"  (mobile + instagram present)")
    if rate and reachable:
        print(f"  realistic daily yield  ~{int(10 * (reachable / len(passed)))}"
              f" per 10 that clear the gates")

    # ---- eyeball the top of the list ------------------------------------
    print("\nSAMPLE (first 8 that passed)")
    for r in passed[:8]:
        print(f"  {str(r['business_name'])[:26]:28} "
              f"{str(r['rating']):4} "
              f"{str(r['reviews_count']):5}rev "
              f"{r['reviews_last_90d']:3}/90d  "
              f"{'IG' if r['instagram'] else '--'} "
              f"{'site' if r['website_url'] else 'nosite'}")

    stamp = dt.date.today().isoformat()
    with open(f"audit_{stamp}.json", "w", encoding="utf-8") as f:
        json.dump({"sample": n, "passed": len(passed),
                   "rejections": dict(reasons), "need_flags": dict(need_flags),
                   "records": recs}, f, ensure_ascii=False, indent=2, default=str)
    print(f"\nfull dump -> audit_{stamp}.json\n")


if __name__ == "__main__":
    main()
