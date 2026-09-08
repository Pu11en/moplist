# Lead Engine

Sells weekly lists of **newly-opened local businesses** to **commercial cleaning companies**.

Two pipelines. They meet at the sale.

```
PIPELINE A — THE PRODUCT (what you sell)
========================================

  [1] SOURCE          [2] FILTER         [3] VERIFY          [4] SCORE          [5] PACKAGE
  new business    →   kill junk      →   real address?   →   worth a       →   weekly list
  filings             by name            (Places API)        cleaner?           per territory
  (TX registry)       (HOLDINGS,         address, phone,     medical/office/    CSV + email
  free, weekly        CAPITAL, ...)      category, age      restaurant = hot    body
  cron
      |                   |                   |                   |                   |
   ~2000/wk           ~800 left           ~120 left           ~40 hot            delivered
                                                                                      |
                                                                                      v
PIPELINE B — THE CUSTOMERS (who pays)                                          [6] DELIVER
=====================================                                                 |
                                                                                      |
  [B1] FIND          [B2] ENRICH        [B3] CAMPAIGN                                 |
  cleaning       →   get emails     →   Instantly       ──────── sale ────────────────+
  companies          from their          cold sequence         |
  per metro          websites            "3 free leads"        |
  (registry +                                                  v
  Maps)                                                    [7] BILL
                                                          Stripe link
                                                          → paying customer
                                                          → added to weekly
                                                            delivery list
```

## The one thing to understand

**Pipeline A is a factory. Pipeline B is the sales floor.** The factory runs on a cron every
week whether or not anyone buys. The sales floor uses the factory's output as free samples
to get people to pay. Once someone pays, they just get added to the delivery list — the
factory doesn't work any harder for customer #50 than it does for customer #1.

That's the whole reason this scales: **the cost of serving one more customer is one more
email.** The data pull is the same either way.

## Run it

```sh
./run_weekly.sh            # runs steps 1-5, writes this week's lists
python3 src/step6_deliver.py   # sends to paying customers + pushes samples to Instantly
```

## Build order (do NOT build all of it at once)

| Phase | Build | Why |
|---|---|---|
| 1 | steps 1, 2 | Free, no API keys. Proves the raw supply exists. |
| 2 | step 3 | Needs Google Places key. **This is the real work** — turns junk into leads. |
| 3 | steps 4, 5 | Cheap once 3 works. Makes it presentable. |
| 4 | B1-B3 + step 6 | Only once you have a list worth sending. |
| 5 | step 7 | Only once someone says yes. |

## Status

Scaffold only. Nothing is verified against a real buyer yet. See the research this came from:
`../reddit/research/cleaning-new-business-lead-alerts-2026-09-08.md`
