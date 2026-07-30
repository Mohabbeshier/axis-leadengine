# Demo content — what is real, what is illustrative

The engine renders each salon from its own Google Maps record. Everything
else on the page is template content and must be treated as illustrative
until a salon confirms it.

## Real, per salon (from the pipeline)

- Name, city and district
- Google rating and review count
- Phone / WhatsApp number
- Address and map link
- Opening hours where Google has them
- Service names, one-line notes and starting prices (Claude-generated from
  the salon's own reviews and category — plausible, marked "تبدأ من")

## Illustrative (template copy, same for every salon until replaced)

- The ritual (الطقس) and all journey copy
- The four claims: women-only enclosure, sterilisation in view, punctual
  slots, fixed prices — **these are commitments the salon must actually make
  before the page goes beyond demo**
- Bridal chapter contents and evening attendance
- Private room and home-service availability and zones
- Membership tiers and their benefits — the page itself carries the line
  "أرقام هذه الصفحة تجريبية للعرض"
- Reply-time promise in the booking overlay
- All photography (Unsplash, licensed; see image-manifest.md) — not the
  salon's own premises

## Never fabricated, by rule

- No invented testimonials: the reviews section removes itself when the
  pipeline has none.
- No invented certifications, awards, staff names or portraits — the artists
  chapter is absent for exactly this reason.
- No fake scarcity, countdowns or booking counters anywhere.
