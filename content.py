"""
Stage 4.5 — Claude writes the salon-specific content.

Two calls, both strict JSON, both temperature 0.2 (slight variation so
20 salons don't get 20 identical service lists).

Everything is written in Gulf/neutral Arabic — never Egyptian dialect.
"""

import os, re, json, requests

ANTHROPIC_KEY = os.environ["ANTHROPIC_API_KEY"]
API = "https://api.anthropic.com/v1/messages"
HDR = {"x-api-key": ANTHROPIC_KEY, "anthropic-version": "2023-06-01",
       "content-type": "application/json"}


def _call(system, user, max_tokens=800, temp=0.2):
    r = requests.post(API, headers=HDR, timeout=90, json={
        "model": "claude-sonnet-4-6", "max_tokens": max_tokens,
        "temperature": temp, "system": system,
        "messages": [{"role": "user", "content": user}]})
    r.raise_for_status()
    txt = "".join(b.get("text", "") for b in r.json()["content"]
                  if b.get("type") == "text").strip()
    return json.loads(re.sub(r"^```(?:json)?|```$", "", txt).strip())


SERVICES_SYSTEM = """You write service menus for Saudi beauty salons.

You get one salon's Google Maps data (name, category, area, review snippets).
Infer a realistic service list from what the reviews and category actually mention.

RULES
- 5 to 7 services, ordered cheapest to most expensive.
- Saudi market prices in SAR, realistic for the area given. Round numbers only.
- price: digits only (e.g. "250") — no currency word, no symbol, no "SAR"/"ر.س".
- Arabic must be Gulf/neutral — never Egyptian dialect, never transliterated English.
- Base services on evidence in the reviews where present. Do not invent a service the salon clearly does not offer (no medical/laser unless the data says so).
- desc: max 6 words, concrete, no marketing adjectives.

Output ONLY:
{"services":[{"name":str,"desc":str,"price":str}]}"""


MESSAGE_SYSTEM = """You write one short WhatsApp message from Axis to a Saudi salon owner.

Context: Axis already built the salon a website and is sending the live link. This is a first, cold message.

RULES
- Gulf/neutral Arabic. Never Egyptian dialect.
- Maximum 32 words, 3 short lines.
- Open by naming the salon, so it reads as made-for-them, not a blast.
- State plainly that a site was built and can be seen at the link.
- No price, no pitch, no agency introduction, no adjectives like رائع or مميز.
- No emoji beyond a single optional one at most.
- End with a light, low-pressure question.
- The literal token {LINK} must appear exactly once.

Output ONLY:
{"message":str}"""


def services_for(rec):
    payload = {
        "name": rec.get("business_name"),
        "category": rec.get("category"),
        "area": rec.get("area"),
        "city": rec.get("city"),
        "reviews": [r["text"] for r in (rec.get("top_reviews") or [])],
    }
    out = _call(SERVICES_SYSTEM, json.dumps(payload, ensure_ascii=False))
    svc = out.get("services", [])
    if not svc:
        raise RuntimeError("no services generated")
    return svc


def message_for(rec, link):
    payload = {"name": rec.get("business_name"), "area": rec.get("area")}
    out = _call(MESSAGE_SYSTEM, json.dumps(payload, ensure_ascii=False),
                max_tokens=300, temp=0.3)
    msg = out.get("message", "")
    if "{LINK}" not in msg:
        msg = msg.rstrip() + "\n{LINK}"
    return msg.replace("{LINK}", link)
