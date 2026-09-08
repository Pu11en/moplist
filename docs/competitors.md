# R2 — Competitor scan: who already sells this — September 8, 2026

## Verdict

**Both halves of the idea are already sold by someone, and the raw data is nearly free.
The $150/mo price hypothesis does not survive contact with this. The one thing that is
NOT commoditised is the part we discovered by accident: premises qualification.**

## Direct competitors — new-business-filing feeds

| Vendor | What they sell | Price |
|---|---|---|
| [AlphaLeads](https://alphaai-leads.com/) | ~5,400 fresh filings/business day, 11 states **incl. Texas**, AI-classified by niche, contact-enriched | **from $19.99/mo** |
| [DayOneLead](https://dayonelead.com/new-llc-filing-business-leads) | every new registration in 6 states + verified owner name, phone, email, website | flat monthly, 200 leads/day export |
| [NewFilings](https://newfilingalerts.com/) | daily new LLC/corp alerts, 10 states | not published |
| [Apify filings scraper](https://apify.com/splendorous_astrolabe_xs9/new-business-filings) | raw filings, pay per result | **$0.004/record** (~$20 for 5,000) |
| [Salesgenie / Data Axle](https://www.salesgenie.com/lists/new-business-list/) | "New Business" database, ~4M US businesses <1yr old | $99–$149/mo |

**AlphaLeads at $19.99/mo covers Texas, enriches contacts, and classifies by niche.**
That is our product with more states and more enrichment, at 13% of our proposed price.
Apify at $0.004/record means the underlying data has effectively zero cost — there is no
supply-side moat whatsoever.

## Direct competitors — lead gen sold *to cleaning companies*

| Vendor | What they sell |
|---|---|
| [Salesgenie janitorial leads](https://www.salesgenie.com/leads/commercial-janitorial-leads/) | lead lists targeted at commercial cleaning |
| [UpLead](https://www.uplead.com/commercial-cleaning-leads/) | SIC-code targeted lists + verified decision-maker contacts |
| [Abstrakt Marketing Group](https://www.abstraktmg.com/industries/commercial-cleaning/) | **sales-ready appointments**, outsourced sales team |
| [CallingAgency](https://callingagency.com/lead-generation-services/get-commercial-cleaning-leads/) | **verified on-site meetings** with facility/property managers |
| [leadsforcommercialcleaning.com](https://www.leadsforcommercialcleaning.com/) | outsourced janitorial sales team, appointment setting |

So the buyer is already being sold to, and the premium end sells **appointments**, not lists.

## Does the Reddit evidence still hold?

Yes, but it means something different than we thought. Operators said *"I don't know how
to find new businesses outside of driving around"* and *"What website do you use?"* — those
are real quotes. But now we know the answer to their question is "AlphaLeads, $19.99."

**That is an awareness gap, not an unmet need.** Awareness gaps are real and monetisable,
but they are not defensible: the moment a competitor markets into r/cleaningbusiness, it
closes. Do not mistake it for a moat.

## Where we are actually different (the one real edge)

Every competitor above sells **volume**. AlphaLeads brags about 5,400 filings *per day*.
Our own run says what that volume actually contains:

```
298 filings  →  150 after junk-name filter  →  19 real commercial premises
                45 home-based · 3 private mailboxes · 83 unclassifiable
```

**93% of new business filings are useless to a cleaning company.** They are people's
houses, UPS Store mailboxes, holding companies and consultancies. A cleaning operator
handed 5,400 filings/day has been given a second job, not a lead list.

Nobody in the table above filters for *"does this business have floors, restrooms and a
door someone unlocks in the morning."* That question is specific to cleaning, and it is
the only question that matters to this buyer.

**Positioning that follows:** not "more leads." *Fewer* leads.

> "AlphaLeads sends you 5,400 filings a day. We send you the 19 with a floor to mop."

## What this does to pricing (Hypothesis, revised)

$150/mo is not defensible against a $19.99 competitor **on list-vs-list terms**. Options:

1. **Compete on curation at a modest premium** — $49–79/mo. Justified only if we can show
   the junk-removal rate against a raw feed side by side. Weak moat, easily copied.
2. **Move up to the outcome** — qualified/contacted leads, or appointments, like Abstrakt
   and CallingAgency. Much higher price, much higher delivery cost, no longer a data
   business. This is where the real money is and where the real work is.
3. **Hyper-local + done-for-you** — one metro, hand-checked, cleaning-specific, sold to a
   handful of operators per city at $99–149. Defensible by attention, not technology.

Recommendation: **price at $49/mo for a first paying customer, treat it as buying evidence,
not revenue.** Do not defend $150 against a $19.99 incumbent in a cold email — that
argument is lost before it starts. Get one paying user, then find out whether they would
pay more for qualification or for appointments.

## What would change this assessment

- Buy one month of AlphaLeads ($19.99) for Texas, run their output through our step ②③
  filter, and measure what fraction is home-based/mailbox junk. If it is ~90%, the
  curation claim is proven with a competitor's own data and becomes the entire sales pitch.
- Ask an operator directly: would you rather have 500 filings or 19 qualified premises?

## Honest summary

The idea is not novel and the data is not scarce. The specific insight that *is* ours —
that cleaning companies need premises qualification, not filing volume — was discovered
while fixing the Google problem, and it is the only part of this worth building around.
