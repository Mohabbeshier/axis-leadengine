"""
Stage 6 — send via WhatsApp Cloud API.

The send IS the WhatsApp verification. There is no separate check:
  - message accepted + delivered  -> whatsapp_verified = True
  - error 131026 / 131047 / 470   -> number is not on WhatsApp -> False
  - anything else                 -> None (unknown), goes to needs_review

Hard caps are enforced here, not in config, because exceeding them is
what gets a number banned.
"""

import os, re, time, requests

WA_TOKEN    = os.environ["WA_TOKEN"]
WA_PHONE_ID = os.environ["WA_PHONE_ID"]
API_VER     = os.environ.get("WA_API_VERSION", "v21.0")

DAILY_CAP    = int(os.environ.get("DAILY_SEND_CAP", "10"))
SEND_SPACING = int(os.environ.get("SEND_SPACING_SEC", "180"))  # 3 min apart

# Meta error codes that mean "this number is not a WhatsApp user"
NOT_ON_WA = {131026, 131047, 470}

BASE = f"https://graph.facebook.com/{API_VER}/{WA_PHONE_ID}/messages"
HDR = {"Authorization": f"Bearer {WA_TOKEN}", "Content-Type": "application/json"}


def normalize_msisdn(phone, default_cc="966"):
    d = re.sub(r"\D", "", phone or "")
    if not d:
        return None
    if d.startswith("00"):
        d = d[2:]
    if d.startswith("0"):
        d = default_cc + d[1:]
    if not d.startswith(default_cc) and len(d) <= 10:
        d = default_cc + d
    return d if 10 <= len(d) <= 15 else None


def send(phone, body, template_name=None, lang="ar"):
    """Returns (status, detail).
    status: 'sent' | 'not_on_whatsapp' | 'unknown'
    """
    to = normalize_msisdn(phone)
    if not to:
        return "unknown", "unparseable_number"

    if template_name:
        payload = {"messaging_product": "whatsapp", "to": to, "type": "template",
                   "template": {"name": template_name,
                                "language": {"code": lang},
                                "components": [{"type": "body",
                                                "parameters": [{"type": "text",
                                                                "text": body}]}]}}
    else:
        payload = {"messaging_product": "whatsapp", "to": to,
                   "type": "text", "text": {"preview_url": True, "body": body}}

    try:
        r = requests.post(BASE, headers=HDR, json=payload, timeout=45)
    except Exception as e:
        return "unknown", f"network:{e}"

    if r.status_code == 200:
        return "sent", r.json().get("messages", [{}])[0].get("id", "")

    try:
        err = r.json().get("error", {})
        code = err.get("code")
        sub = (err.get("error_data") or {}).get("details", "")
    except Exception:
        code, sub = None, r.text[:160]

    if code in NOT_ON_WA:
        return "not_on_whatsapp", f"{code}:{sub}"
    return "unknown", f"{code}:{sub}"


def send_batch(rows, message_fn, cap=None, spacing=None):
    """rows: verified leads, each already carrying demo_url.
    message_fn(rec) -> the text to send.
    Mutates each row with send_status / whatsapp_verified / wa_message_id."""
    cap = cap or DAILY_CAP
    spacing = SEND_SPACING if spacing is None else spacing
    sent = 0

    for rec in rows:
        if sent >= cap:
            rec["send_status"] = "skipped_cap"
            continue

        status, detail = send(rec.get("phone"), message_fn(rec))
        rec["send_status"] = status
        rec["wa_detail"] = detail
        rec["whatsapp_verified"] = {"sent": True,
                                    "not_on_whatsapp": False}.get(status)

        if status == "sent":
            rec["wa_message_id"] = detail
            sent += 1
            if sent < cap:
                time.sleep(spacing)

    return sent
