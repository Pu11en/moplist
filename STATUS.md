# MopList — STATUS, read this first

Last updated 2026-09-08 by a Claude session. Written so a fresh agent can pick this
up with zero prior context.

## What this business is

Sell **weekly lists of newly-registered local businesses** to **commercial cleaning
companies**, who use them as first-mover sales leads. A business that filed its LLC
three weeks ago has no cleaning vendor and has been called by nobody.

Positioning, in customers' own words: *"not a lead five other companies already called."*

Price hypothesis: **$49/mo flat, no contract, first 3 leads free.** Never tested on a
buyer. Anchored on operators' stated spend ($400 Thumbtack → 1 job; $150 Google LSA → 4 jobs).

## Everything you need is in this repo

**`docs/`** — all committed, read these before building anything:

| File | What it gives you |
|---|---|
| `docs/why-this-business.md` | the Reddit evidence this is built on, plus counterevidence |
| `docs/data-rights-ruling.md` | **⚠ read before touching step 3** — why Google Places is banned |
| `docs/competitors.md` | AlphaLeads at $19.99 and why our edge is qualification, not volume |
| `docs/brand-and-offer.md` | MopList, $49/mo, positioning |
| `docs/email-copy.md` | 5 cold email variants + follow-ups |
| `docs/customer-journey.md` | reply → free trial → Stripe, with scripts for every branch |

**`data/prospects/`** — gitignored, local only (third-party contact data, not for a
public repo):

| File | What |
|---|---|
| `core-cleaning-candidates.csv` | **2,608 cleaning businesses already collected.** 398 janitorial-coded. No emails — that's pipeline B's job. |
| `public-business-contacts.csv` | 36 hand-enriched, 28 with email |
| `send-list-batch1.csv` | the 17 that actually do commercial work and have a live mail domain |

Original research lives in the reddit repo, but you do not need it — everything
above is a copy.

## Pipeline A — the product

| Step | File | State | Notes |
|---|---|---|---|
| ① SOURCE | `src/step1_source.py` | ✅ **works** | TX Comptroller API, free, no key |
| ② FILTER | `src/step2_filter.py` | ✅ **works** | drops HOLDINGS/CAPITAL/etc by name |
| ③ VERIFY | `src/step3_verify.py` | ✅ **works** | registry address → commercial vs home/mailbox. **No Google.** |
| ④ SCORE | `src/step4_score.py` | ❌ **BROKEN** | still scores on Google Places `types`/review count, which no longer exist. Rewire to registry signals: name category, `premises_confidence`, charter recency. |
| ⑤ PACKAGE | `src/step5_package.py` | ⚠ untested | should work once ④ is fixed |
| ⑥ DELIVER | `src/step6_deliver.py` | ⚠ needs key | `INSTANTLY_API_KEY` + campaign id. Has `--dry-run`. |

Verified live run (45 days, New Braunfels + Seguin + San Marcos):
```
298 filings → 150 candidates → 19 commercial premises
                               45 home-based · 3 mailboxes · 83 unclear (dropped)
cost: $0 · API calls: 0
```

Run it: `./run_weekly.sh 2026-09-08`  (env `CITIES="NEW BRAUNFELS,SEGUIN,SAN MARCOS"`)

## Pipeline B — the customers

**DISCOVERY IS ALREADY DONE. This is an ENRICHMENT job, not a collection job.**

`data/prospects/core-cleaning-candidates.csv` already holds **2,608 cleaning businesses** (Austin 948, San Antonio 670,
Round Rock 94, Pflugerville 79, New Braunfels 56). Of those, **398 are classified
`janitorial_housekeeping_industry` (NAICS 561720)** — that is the commercial-cleaning
subset and the highest-value targets. **Do not re-collect these.**

**Zero of the 2,608 have an email.** The registry does not carry contact details.
That is the whole job:

```
have:  business name + city + NAICS      (2,608 rows, done)
need:  website URL  →  email address     ← build this
```

- `Ⓑ2a` name + city → find the business's website. This is the hard half; the registry
  has no URL. the reddit repo's `research/scripts/inspect-cleaning-websites.py` exists but requires
  manually seeded URLs, which is why only 36 were ever enriched.
- `Ⓑ2b` website → scrape a contact email. crawl4ai is available and legally clean for
  this — it is the business's own public site, not a third-party database.
- `Ⓑ3` load into Instantly.

**Start with the 398 janitorial-coded rows**, not all 2,608. They are the commercial
buyers; most of the remaining 2,210 are name-matched residential maid services who do
not want commercial-premises leads.

Prior hand-built batch: 36 companies, 28 with email, of which only **17** actually do
commercial work and have a live mail domain — see `data/prospects/send-list-batch1.csv`. 17 is too small to prove anything at a 2% reply rate.

## Also not built

- **Billing.** No Stripe. If someone says yes today there is no way to charge them.
- **Weekly cron.** `run_weekly.sh` exists but nothing schedules it.

## ⛔ Hard rules

1. **Never put Google Maps/Places content in a delivered list.** Their terms explicitly
   ban using Maps content to build a "business listings database, mailing list, or
   telemarketing list." Scraping Maps is the same violation. See the data-rights ruling.
2. Attribute the Texas Comptroller on delivered lists.
3. Nothing gets emailed to a real cleaning company without Drew's say-so.
4. r/cleaningbusiness requires mod permission to promote — the copy is for **cold email**,
   not for posting there.

## Next tasks, in order

1. Fix `step4_score.py` (registry-based scoring)
2. Run ①→⑤ end to end, eyeball the packaged list
3. Build Ⓑ1 + Ⓑ2 (need ~300 cleaning companies, not 36)
4. Load Instantly, dry-run first
5. Stripe link — only needed the day someone says yes

Phases 1–2 produce zero revenue. The only step that proves anything is a real send.

---

## Brand (added 2026-09-08)

- **Name:** MopList · **Domain:** moplist.com (available, Drew to purchase)
- **Price:** **$49/mo**, no contract, 3 free leads first.
  Revised down from $150 — see `research/competitor-scan-2026-09-08.md` in the
  reddit repo. AlphaLeads sells raw filings at $19.99/mo, so $150 is indefensible.
- **The one argument:** competitors sell volume (5,400 filings/day). 93% of that is
  houses, mailboxes and holding companies. *"They send you 5,400 filings a day.
  We send you the 19 with a floor to mop."*
- **Email copy to use:** `business/moplist-brand-and-email-2026-09-08.md` in the
  reddit repo. Do NOT use the earlier v1 copy — it quotes $150.
