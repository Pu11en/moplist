# R1 — Data rights ruling: can we sell this data? — September 8, 2026

## Verdict

**Google Places: NO. Texas registry: yes, with a caveat. Pipeline redesigned; it is now
better, free, and faster than the Google version.**

## Google Maps Platform — disqualified for this product

Google's terms prohibit, in their words:

> "you shall not sell, resell, sublicense, transfer, or distribute the Google Maps Content"

> "using Google Maps to create or augment any other mapping-related dataset (including a
> mapping or navigation dataset, **business listings database, mailing list, or
> telemarketing list**) for use in a service that is a substitute for, or a substantially
> similar service to, Google Maps"

[Places API policies](https://developers.google.com/maps/documentation/places/web-service/policies) ·
[Maps Platform terms](https://cloud.google.com/maps-platform/terms)

"Business listings database, mailing list" is a literal description of this product. Also
relevant: lat/long may only be cached 30 days; only `place_id` may be stored indefinitely.

**Scraping Maps instead does not help.** Same content, same restriction, minus any
contractual footing, plus bot-detection breakage. Rejected on business-risk grounds, not
squeamishness: a product whose supply can be cut off, and whose data a customer's counsel
could challenge, is not a sellable asset.

## Texas Comptroller registry — usable, one open question

- Publisher: Texas Comptroller of Public Accounts. Dataset marked public; API `rights: [read]`.
- **No explicit license or redistribution grant is stated in the dataset metadata.**
- Strong supporting position: business registration records are *facts*, and facts are not
  copyrightable in the US (*Feist v. Rural Telephone*). Compiled factual government records
  are the weakest possible basis for a redistribution claim against us.
- **Still to confirm:** the Comptroller's own open-data/terms page, and whether resale (vs.
  free redistribution) is addressed. Treat as low-risk-but-unconfirmed, not settled.
- Attribution to the Comptroller should appear on delivered lists regardless.

## What replaced Google — and why it is better

The registry already carries `taxpayer_address`. We never used it. **The address itself is
the qualifier**, and it answers a question Google could not:

```
876 LOOP 337 STE 501        suite in a commercial building  -> REAL PREMISES  ✅
790 GENERATIONS DR STE 410  suite                           -> REAL PREMISES  ✅
814 PAMPLONA LN             residential street              -> home-based     ❌
1967 CLUB XING              residential street              -> home-based     ❌
201 THORPE LN STE 105 PMB   private mailbox / UPS Store     -> no premises    ❌
677 CREEKSIDE WAY APT 12    apartment                       -> residential    ❌
```

A cleaning company cannot sell a nightly janitorial contract to a spare bedroom or a
mailbox. Google Places would happily have returned a "verified address" for all of them.

Live result on 45 days of New Braunfels / Seguin / San Marcos filings:

```
298 filings -> 150 candidates -> 19 commercial premises
                                 45 home-based, 3 mailboxes, 83 unclear (dropped)
```

Cost: **$0**. API calls: **none**. TOS exposure: **none**.

## Consequences for the build

- `lead-engine/src/step3_verify.py` rewritten; no key needed. Verified working.
- `step1_source.py` now pulls `taxpayer_address`.
- ⚠️ **`step4_score.py` is now broken** — it scored on Google Places `types` and review
  counts, which no longer exist. Must be rewired to score on registry signals: name
  category (bakery/dental/salon), premises confidence, charter recency.
- Optional depth later: crawl the business's **own website** (crawl4ai) to confirm it is
  trading. That is the business's public site, not Google's database — clean.

## Remaining Phase 0

- **R2** competitor + price scan (Data Axle, InfoUSA, LeadsPlease, new-mover list vendors)
- **R3** brand name + domain + one-line promise
