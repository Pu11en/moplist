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

## Where the research lives (do not duplicate it)

`/home/drewp/main-projects/reddit/.worktrees/wt-1546681327871336560/`

| File | What it gives you |
|---|---|
| `research/cleaning-new-business-lead-alerts-2026-09-08.md` | why this idea, with Reddit evidence + counterevidence |
| `research/data-rights-ruling-2026-09-08.md` | **⚠ read before touching step 3** — why Google is banned |
| `business/cleaning-lead-offer-copy-2026-09-08.md` | the offer, cold email copy, objections |
| `planning/RESEARCH-PLAN.md` | task order across both folders |
| `research/cleaning-prospects/2026-09-08-100mi/public-business-contacts.csv` | 36 cleaning companies, 28 with email — the first send list |

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

**❌ NOT BUILT.** Needs:
- `Ⓑ1` find every cleaning company in a metro (registry + web)
- `Ⓑ2` enrich with an email from their own website (crawl4ai is available and is
  legally clean here — it's their own public site)
- `Ⓑ3` load into Instantly

Currently there are 36 companies collected by hand, 28 with emails. That's one small
batch — enough for a first test, not enough to find a buyer reliably.

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
