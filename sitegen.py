"""
Stage 5 — build the demo site.

No Netlify API, no NETLIFY_TOKEN. The runner writes each salon into
sites/<slug>/index.html and commits. Netlify is already connected to the
repo, so the push triggers the build.

Inside GitHub Actions the commit uses the built-in GITHUB_TOKEN, which is
generated per run and expires with it — nothing to store, nothing to leak.
"""

import os, re, json, hashlib, subprocess, unicodedata

TEMPLATE  = os.environ.get("TEMPLATE_PATH", "template.html")
SITES_DIR = os.environ.get("SITES_DIR", "sites")
BASE_URL  = os.environ.get("DEMO_BASE_URL", "https://demo.axismarketinga.com").rstrip("/")

CONFIG_RE = re.compile(r"const CONFIG = \{.*?\n\};", re.S)


def slugify(name, place_id):
    """Stable and unique. md5 (not hash()) because hash() is salted
    per process — a re-run would otherwise create a second folder."""
    ascii_name = unicodedata.normalize("NFKD", name or "").encode("ascii", "ignore").decode()
    ascii_name = re.sub(r"[^a-zA-Z0-9]+", "-", ascii_name).strip("-").lower() or "salon"
    tag = hashlib.md5(place_id.encode()).hexdigest()[:5]
    return f"{ascii_name[:32]}-{tag}"


def build_config(rec, services):
    wa = re.sub(r"\D", "", rec.get("phone") or "")
    if wa.startswith("00"):
        wa = wa[2:]
    if wa.startswith("0"):
        wa = "966" + wa[1:]
    return {
        "salon_name":    rec.get("business_name") or "",
        "city":          " · ".join(x for x in [rec.get("city"), rec.get("area")] if x),
        "tagline":       " · ".join(s["name"] for s in services[:4]),
        "rating":        str(rec.get("rating") or ""),
        "reviews_count": str(rec.get("reviews_count") or ""),
        "phone":         rec.get("phone") or "",
        "whatsapp":      wa,
        "whatsapp_msg":  "السلام عليكم، أبغى أحجز موعد",
        "address":       rec.get("address") or "",
        "hours":         rec.get("opening_hours") or "",
        "maps_url":      rec.get("maps_url") or "",
        "services":      services,
        "photos":        rec.get("photos") or [],
        "reviews":       rec.get("top_reviews") or [],
    }


def render(rec, services):
    with open(TEMPLATE, encoding="utf-8") as f:
        html = f.read()
    cfg = json.dumps(build_config(rec, services), ensure_ascii=False, indent=2)
    out, n = CONFIG_RE.subn(f"const CONFIG = {cfg};", html)
    if n != 1:
        raise RuntimeError("CONFIG block not found in template.html")
    return out


def write_site(rec, services):
    """Write the file. Returns the public URL it will live at."""
    slug = slugify(rec.get("business_name"), rec["place_id"])
    path = os.path.join(SITES_DIR, slug)
    os.makedirs(path, exist_ok=True)
    with open(os.path.join(path, "index.html"), "w", encoding="utf-8") as f:
        f.write(render(rec, services))
    rec["demo_slug"] = slug
    rec["demo_url"] = f"{BASE_URL}/{slug}"
    return rec["demo_url"]


def commit_and_push(count):
    """One commit for the whole batch. No-op locally if git isn't configured."""
    def git(*a):
        return subprocess.run(["git", *a], check=True,
                              capture_output=True, text=True)
    try:
        git("config", "user.name", "axis-lead-engine")
        git("config", "user.email", "bot@axismarketinga.com")
        git("add", SITES_DIR)
        status = subprocess.run(["git", "status", "--porcelain", SITES_DIR],
                                capture_output=True, text=True).stdout.strip()
        if not status:
            return False
        git("commit", "-m", f"sites: add {count} demo(s)")
        git("push")
        return True
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"git push failed: {e.stderr[:300]}")
