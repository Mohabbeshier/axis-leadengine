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
- Also give a natural English rendering of each name and desc (name_en, desc_en) — the demo site has an English mode. Translate the meaning, do not transliterate the Arabic.

Output ONLY:
{"services":[{"name":str,"name_en":str,"desc":str,"desc_en":str,"price":str}]}"""


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


EN_SYSTEM = """You localise one Saudi salon's own details into English.

The demo site has an Arabic/English switch, so every visible field needs an
English counterpart. This is the salon's real identity — be faithful, not
creative.

RULES
- salon_name_en: the salon's name as it would appear on an English sign.
  Transliterate proper names (لمسة سمو -> Lamsat Sumow), translate the
  descriptive part (للتزيين النسائي -> Ladies Beauty Salon).
- city_en / address_en: standard English spellings of Saudi places
  (الرياض -> Riyadh, الياسمين -> Al Yasmin, طريق الملك عبدالعزيز -> King
  Abdulaziz Rd).
- hours_en: English days and 12-hour times. Empty string if the input is empty.
- tagline_en: translate each segment, keep the same " · " separator.
- whatsapp_msg_en: the English equivalent of the Arabic booking message.
- Never invent a field that has no Arabic input — return "" for it.

Output ONLY:
{"salon_name_en":str,"city_en":str,"address_en":str,"hours_en":str,"tagline_en":str,"whatsapp_msg_en":str}"""


def en_fields_for(cfg):
    """English counterparts for the Arabic fields already in a site CONFIG.

    Failure here must never block a send — the template falls back to the
    Arabic string for any key that comes back empty or missing.
    """
    payload = {k: cfg.get(k, "") for k in
               ("salon_name", "city", "address", "hours", "tagline", "whatsapp_msg")}
    try:
        out = _call(EN_SYSTEM, json.dumps(payload, ensure_ascii=False),
                    max_tokens=600, temp=0)
    except Exception:
        return {}
    return {k: v for k, v in out.items() if isinstance(v, str) and v.strip()}


def message_for(rec, link):
    payload = {"name": rec.get("business_name"), "area": rec.get("area")}
    out = _call(MESSAGE_SYSTEM, json.dumps(payload, ensure_ascii=False),
                max_tokens=300, temp=0.3)
    msg = out.get("message", "")
    if "{LINK}" not in msg:
        msg = msg.rstrip() + "\n{LINK}"
    return msg.replace("{LINK}", link)
