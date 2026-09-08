# New-business lead alerts for commercial cleaning operators — September 8, 2026

## Decision and constraint

Drew asked what to sell to cleaning businesses specifically, after rejecting a
quoting/estimating tool (already screened out in
[the three-audience pass](three-audience-discovery-2026-09-08.md) —
Jobber's free template and QuoteWise Pro at $49/month cover that ground with
no demonstrated gap). This pass targets a narrower question: is there a
distinct, underserved need where the prospect-discovery pipeline already
built for [New Braunfels-area LLC discovery](texas-new-llc-discovery-2026-09-08.md)
is itself the sellable asset, not just research material.

No product is selected or authorized for implementation by this note. This
is findings for discussion.

## Retrieval

Used the authenticated local Reddit transport (`node bin/reddit.mjs search`)
against `r/cleaningbusiness` and `r/smallbusiness`, both by targeted query and
subreddit-scoped relevance search. An unscoped, no-subreddit search returned
unrelated general-Reddit noise and is not used as evidence. Raw run output is
saved under `research/runs/` (excluded from Git) with timestamps matching the
citations below.

## Finding: operators want to reach businesses before they open, and don't know how

**Thread:** ["Do any of you target businesses before they officially open?"](https://www.reddit.com/r/cleaningbusiness/comments/1vxfeqw/do_any_of_you_target_businesses_before_they/) — posted by a researcher (not an operator) asking the subreddit; score 8, 5 comments.

> "I heard that the spaces always need cleaning before the business moves in
> and right before they open. I just don't know how to find new businesses
> outside of driving around and looking for 'coming soon' signs."
> — u/WeCaredALot

> "What website do you use? I am really interested." — u/Straight-Emotion-761

> "Excellent source of solid leads but they need to be babied along."
> — u/EdSelkow (established operator, confirms the strategy works when leads
> are available, not just theorized)

This is three independent commenters — the original poster's premise, an
operator confirming it as a "solid" lead source, and a second operator asking
where to get one — converging on the same gap: **operators believe pre-open
businesses are good prospects, but have no systematic way to find them.** No
commenter named an existing tool or service for this.

**Corroborating cross-industry evidence (different vertical, same pattern):**
["How can I enrich a daily list of newly registered UK companies for cold email/call outreach?"](https://www.reddit.com/r/smallbusiness/comments/1lpzk6c/how_can_i_enrich_a_daily_list_of_newly_registered_uk_companies_for_cold_emailcall_outreach/) — a software/IT agency owner already pulls a daily new-incorporation
feed and wants to enrich it with contact details to reach founders "soon
after they incorporate." This confirms the new-incorporation-targeting model
is a known, working pattern in at least one adjacent service industry. It
does not by itself prove cleaning-specific demand; the cleaning-specific
threads above do that independently.

## Willingness to pay: quantified from the same subreddit

["After 1 month of using Kimi Code to build my own CMS, I went live... booked $1,500 so far"](https://www.reddit.com/r/cleaningbusiness/comments/1vwn6bh/after_1_month_of_using_kimi_code_to_build_my_own/) (score 7, 33 comments) reports concrete, operator-stated lead economics:
- Thumbtack: $400 for 7 leads (~$57/lead), 1 conversion — "most people on
  Thumbtack are just shopping for the lowest price," later dropped to ~$25/lead
  by bidding lower tiers.
- Google LSA: $150 for 5 leads (~$30/lead), 4 conversions — "the game changer
  ... ready to get a quote and put a card on file right away."

A second thread, ["Spent $1,367 on FB/IG ads... got 77 leads at $17.76 each"](https://www.reddit.com/r/cleaningbusiness/comments/1viqdw4/spent_1367_on_fbig_ads_for_my_cleaning_business/) (score 22), gives a third data point at the low end of quality/intent.

**Reading:** operators already pay $18–$70 per lead depending on buyer intent,
and explicitly rank leads by how close to "ready to buy" they are. A newly
formed business has no incumbent cleaning vendor at all — closer in kind to
the Google LSA result (high intent once contacted at the right moment) than
to a cold Thumbtack lead. This suggests per-lead pricing in the same
established range is plausible, not a novel price to justify from zero.

## Counterevidence and what does not support this

- Two other lead-source tools were named in-subreddit — **ParseStream** and
  **Conju.ai** — but both are pitched at surfacing people *currently talking
  about wanting a cleaner* (demand-signal monitoring), not newly-formed
  businesses with no vendor yet. Different mechanism, adjacent but not
  identical; do not claim these are the same competitor as this idea.
- No commenter in either subreddit named a product that delivers a
  cleaning-relevant new-business-formation feed. Absence of a named
  competitor is not proof none exists — a wider web/app-store check was not
  performed in this pass.
- The originating thread's poster is explicitly framed as researching the
  idea, not an operator with a validated business; the two confirming replies
  are the actual operator evidence, and it is two people, not a market.
- ["The worst local-service leads aren't the 'no's, it's the 'maybes'"](https://www.reddit.com/r/cleaningbusiness/comments/1unwl1s/the_worst_localservice_leads_arent_the_nos_its/) shows a related but distinct pain (follow-up tracking on existing leads);
  commenters immediately steer toward a CRM (Jobber/ZenMaid/Housecall Pro
  already compete there). Do not conflate that with the new-business-alert
  gap; it is evidence the subreddit reaches for known tools fast when the
  problem is a familiar one, which sharpens the contrast with the
  new-business-alert thread where nobody had an answer.

## What this reuses vs. requires new work

The Texas Comptroller franchise-taxpayer retrieval and cleaning-name
classification already built for
[New Braunfels-area discovery](texas-new-llc-discovery-2026-09-08.md) is the
same underlying mechanism this idea would sell access to — a recurring feed,
not a one-time list. Turning it into a sellable deliverable still requires,
and none of this is built yet:
- A recurring (not one-off) retrieval and dedup process (the existing script
  is a fixed-window research recipe, explicitly not an installed recurring
  job).
- A defined, verifiable deliverable per buyer: e.g., "N verified new
  commercial/office prospects per week within your service radius, with
  formation date, category, and best-available contact," not a raw registry
  dump.
- Confirmation the Texas data source's coverage (active franchise taxpayers,
  not real-time SOS filings) is fresh and complete enough to beat "driving
  around looking for signs" in practice — untested against a real operator's
  actual timing needs.
- A distribution/outreach route: r/cleaningbusiness requires explicit
  moderator permission for promotion (recorded in the prior pass); no
  permission sought here.

## What would change the decision

A real cleaning operator (ideally one of the two who engaged with the
original thread, or a prospect from the existing Central Texas contact list)
reviewing a small sample feed — 5–10 real newly-formed local businesses with
verified contact info — and stating whether they would pay per lead in the
established $18–$70 range, compared with what they currently get from
Thumbtack/LSA/FB ads. No sample has been shown to anyone; no price has been
proposed to a buyer.

## Conclusion for discussion

This is the first candidate in the recent research passes where operators
describe the exact gap unprompted, nobody names an incumbent, and comparable
per-lead pricing already exists in the same subreddit from the same buyers.
It still fails the final gate every prior candidate failed: no sample shown,
no price tested, no buyer commitment. Treat this as the strongest lead to
validate next, not a selected product.
