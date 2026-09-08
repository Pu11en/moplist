# MopList — The Whole System on One Page

```
                        ┌────────────────────────────────────────────┐
                        │   TEXAS COMPTROLLER PUBLIC REGISTRY         │
                        │   every new business filing in the state    │
                        │   free · public · updated weekly            │
                        └───────────────────┬────────────────────────┘
                                            │
                                            │  runs every Monday, automatic (cron)
                                            ▼
  ╔═════════════════════════════════════════════════════════════════════════════════╗
  ║  PIPELINE A — THE FACTORY  (makes the product, runs whether or not anyone buys)  ║
  ╚═════════════════════════════════════════════════════════════════════════════════╝

   ┌──────────────┐      ┌──────────────┐      ┌──────────────┐      ┌──────────────┐
   │ ① SOURCE      │      │ ② FILTER      │      │ ③ VERIFY      │      │ ④ SCORE       │
   │──────────────│      │──────────────│      │──────────────│      │──────────────│
   │ pull filings │─────▶│ drop the      │─────▶│ read the     │─────▶│ rank by how  │
   │ last 30 days │      │ paper-only    │      │ REGISTRY     │      │ badly they   │
   │ for my       │      │ entities:     │      │ ADDRESS:     │      │ need a       │
   │ cities       │      │ HOLDINGS      │      │              │      │ cleaner:     │
   │              │      │ CAPITAL       │      │ STE 501 = ✅  │      │ dentist = 5  │
   │              │      │ INVESTMENTS   │      │ LOOP 337 = ✅ │      │ bakery  = 5  │
   │              │      │ VENTURES      │      │ PAMPLONA LN❌ │      │ storage = 1  │
   │              │      │ (+ keep       │      │ PMB 329   ❌ │      │              │
   │              │      │ BAKERY SALON  │      │ APT 12    ❌ │      │              │
   │              │      │ DENTAL CAFE)  │      │              │      │              │
   │ FREE         │      │ FREE          │      │ FREE, NO API │      │ FREE         │
   │ ✅ WORKS      │      │ ✅ WORKS      │      │ ✅ WORKS      │      │ ✅ WORKS     │
   └──────────────┘      └──────────────┘      └──────────────┘      └──────┬───────┘
        298                    150                    ~120                   │
      filings              candidates            with real addresses         │
                        (20 obvious wins)                                    ▼
                                                                    ┌──────────────┐
                                                                    │ ⑤ PACKAGE     │
                                                                    │──────────────│
                                                                    │ this week's  │
                                                                    │ list, per    │
                                                                    │ territory:   │
                                                                    │  · CSV       │
                                                                    │  · email body│
                                                                    │ ✅ READY     │
                                                                    └──────┬───────┘
                                                                           │
                    ┌──────────────────────────────────────────────────────┤
                    │                                                      │
           3 leads, free                                        the full list, paid
        (the bait, for cold email)                            (what customers get)
                    │                                                      │
                    ▼                                                      │
  ╔═════════════════════════════════════════════════╗                      │
  ║  PIPELINE B — THE SALES FLOOR  (finds buyers)   ║                      │
  ╚═════════════════════════════════════════════════╝                      │
                                                                           │
   ┌──────────────┐      ┌──────────────┐      ┌──────────────┐            │
   │ Ⓑ1 FIND       │      │ Ⓑ2 ENRICH     │      │ Ⓑ3 CAMPAIGN   │            │
   │──────────────│      │──────────────│      │──────────────│            │
   │ every        │─────▶│ scrape their │─────▶│ INSTANTLY    │            │
   │ cleaning co. │      │ site for an  │      │ sends the    │            │
   │ in San       │      │ email        │      │ sequence,    │            │
   │ Antonio /    │      │              │      │ handles      │            │
   │ Austin /     │      │              │      │ warmup +     │            │
   │ New Braunfels│      │              │      │ deliverability│           │
   │              │      │              │      │              │            │
   │ ❌ NOT BUILT  │      │ ❌ NOT BUILT  │      │ ⚠ needs key  │            │
   │ (have 36     │      │ (28 have     │      │              │            │
   │  by hand)    │      │  emails)     │      │              │            │
   └──────────────┘      └──────────────┘      └──────┬───────┘            │
                                                       │                    │
                                                       ▼                    │
                                        ┌──────────────────────────┐        │
                                        │  cleaning co. replies    │        │
                                        │        "yes"             │        │
                                        └────────────┬─────────────┘        │
                                                     │                      │
                                                     ▼                      │
                                        ┌──────────────────────────┐        │
                                        │  ⑦ BILL — Stripe link     │        │
                                        │  $49/mo, cancel anytime  │        │
                                        │  ❌ NOT BUILT             │        │
                                        └────────────┬─────────────┘        │
                                                     │                      │
                                                     ▼                      │
                                        ┌──────────────────────────┐        │
                                        │  customers.csv           │◀───────┘
                                        │  name · territory · $    │
                                        │                          │
                                        │  every Monday they get   │
                                        │  that week's list        │
                                        └──────────────────────────┘
                                                     │
                                                     ▼
                                              💰  RECURRING REVENUE


  ══════════════════════════════════════════════════════════════════════════════
   WHY THIS SCALES
  ══════════════════════════════════════════════════════════════════════════════

   customer #1                      customer #50
        │                                 │
        └──────────┬──────────────────────┘
                   │
                   ▼
       ┌───────────────────────┐
       │  SAME factory run.    │      Adding a customer costs you
       │  SAME data pull.      │      ONE MORE EMAIL. That is it.
       │  SAME weekly cron.    │
       └───────────────────────┘      The work does not grow with
                                      the customer count. That is
                                      the whole business.

       Adding a CITY is the only thing that costs more:
       more filings → more Places lookups → more $ in step ③.
       But a new city also means a whole new set of cleaning
       companies to sell the same list to.


  ══════════════════════════════════════════════════════════════════════════════
   BUILD ORDER  (do them in this order, do not skip ahead)
  ══════════════════════════════════════════════════════════════════════════════

   ✅ DONE  pipeline A steps ①-⑤          free, no API keys, runs today
                                          298 filings -> 19 commercial premises

   NOW ──▶ [1] PIPELINE B                 300 commercial cleaners with emails
                                          2,608 already collected, 0 have emails.
                                          THIS IS THE ONLY BLOCKER.

           [2] send                       ~30/day. copy is written.
           [3] Stripe link                only the day someone says yes
                                          ↑
                                  everything before this
                                  is worthless until this
                                  step actually happens
```

## Legend

| Mark | Meaning |
|---|---|
| ✅ WORKS | built and run against live data |
| ✅ READY | built, not yet run end-to-end |
| ⚠ needs key | built, blocked on an API key |
| ❌ NOT BUILT | doesn't exist yet |
