# UX flow — لمسة سمو

## The one conversion

Everything on the page funnels to a WhatsApp message the salon can price at a
glance. There is no second conversion competing with it.

```
open (WhatsApp cold link, phone)
  └─ hero ── request ─────────────► booking overlay
  └─ price index ── pick services ► picks persist ► overlay arrives pre-selected
  └─ bridal ─────────────────────► WhatsApp, bridal message
  └─ membership ─────────────────► WhatsApp, membership message
  └─ closing line ───────────────► booking overlay
```

## Booking overlay

Native `<dialog>`; four steps, one decision per screen.

| Step | Question | Validation | Escape hatch |
|---|---|---|---|
| 1 | وش تحبين نجهّز لك؟ | ≥1 service; falls back to index picks | close keeps state |
| 2 | متى يناسبك؟ | a day chosen (preference, not a slot) | back |
| 3 | عرّفينا عليك | name ≥2 chars; Saudi mobile normalised from 05/5/+9665/009665 | plain-sentence errors |
| 4 | كل شيء جاهز | — | send = wa.me with composed message |

State: `sessionStorage` per path. Closing by accident is not a reset.
Focus containment, Escape and backdrop are the platform's own.

## Navigation

- Floating, not a bar, over the opening. Withdraws on scroll-down past 60%
  of a screen; returns on scroll-up. Takes a blurred ivory surface past 85%
  so the wordmark reads over any chapter.
- Section links: الحكاية · العروس · الفهرس · المكان · الزيارة (desktop ≥1000px).
- One persistent booking affordance at a time (decision 052): the nav pill,
  and on phones the dock arrives only after the first screen is behind.

## Reading order (mobile)

hero → statement → broken frame (ch.01) → held ritual (pinned, 3 lines) →
price index → journey texts (ch.02–04) → trust line → bridal → private →
membership → gallery → visit → FAQ‑less closing → footer.

## Known interaction debts

- The FAQ chapter from earlier versions was removed in the editorial rebuild
  and has not been reinstated; cancellation policy currently lives only in
  the journey text (decision 028 pending).
- Artists chapter deliberately absent — no real staff data (029).
- Filters on the index were removed in the editorial pass; category discovery
  is pending (053 partial).
