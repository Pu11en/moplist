"""STEP 3 — VERIFY: is this a real commercial premises? NO GOOGLE, NO COST, NO TOS RISK.

Rewritten 2026-09-08. The original used Google Places. Google Maps Platform terms
explicitly prohibit using their content to "create or augment ... a business listings
database, mailing list, or telemarketing list" -- which is exactly this product.
Scraping Maps is the same content with worse legal standing, so that is out too.

The registry itself carries taxpayer_address, and the address IS the signal:

    876 LOOP 337 STE 501    -> suite in a commercial building  -> REAL PREMISES
    790 GENERATIONS DR STE 410 -> suite                        -> REAL PREMISES
    814 PAMPLONA LN         -> residential street              -> home-based, skip
    1967 CLUB XING          -> residential street              -> home-based, skip

A cleaning company cannot sell a nightly janitorial contract to somebody's spare
bedroom. Filtering these out is the whole job.

Optional deeper check (step 3b, separate): crawl the business's OWN website with
crawl4ai. That is the business's public site, not Google's database -- clean.

Output: data/verified/verified-<date>.csv
"""
import argparse, datetime as dt, re
from common import DATA, read_csv, write_csv

# A unit designator means a leased space inside a larger building.
# APT is deliberately NOT here -- an apartment is a home, not a storefront.
SUITE = re.compile(r'\b(STE|SUITE|UNIT|BLDG|BUILDING|FLOOR|FLR|FRNT|REAR)\b', re.I)

# Mail drops (UPS Store, private mailbox services). An address, but no premises --
# nobody cleans a mailbox. PMB is the giveaway; so is a suite with a second number.
MAILBOX = re.compile(r'\bPMB\b|\bSTE\s*\d+[-\s]*\d{3,}\b', re.I)

# Apartments are residential no matter what else the line says.
APARTMENT = re.compile(r'\bAPT\b', re.I)

# Street types that overwhelmingly indicate a subdivision, not a commercial strip.
RESIDENTIAL = re.compile(r'\b(LN|LANE|CT|COURT|CV|COVE|XING|CROSSING|TRL|TRAIL|'
                         r'RDG|RIDGE|CIR|CIRCLE|WAY|PATH|BND|BEND|HOLW|HOLLOW|'
                         r'PASS|RUN|GLN|GLEN|MDW|MEADOW|CRK|CREEK|PARK|PL|PLACE)\b',
                        re.I)

# Commercial corridors: highways, loops, business routes, named commercial roads.
# NOTE: "LOOP 337" is a state highway. "Dove Crest Loop" is a cul-de-sac.
# Only count LOOP/HWY when a route NUMBER follows it.
COMMERCIAL = re.compile(r'\b(LOOP|HWY|HIGHWAY|STATE HIGHWAY|FM|RR|US)\s?\d+|'
                        r'\b(IH|I)[- ]?\d+\b|'
                        r'\b(EXPY|FWY|BLVD|BOULEVARD|PLAZA|COMMONS|COMMERCE|'
                        r'INDUSTRIAL|BYPASS|BROADWAY)\b|'
                        r'\bBUSINESS\s+(IH|I)[- ]?\d+\b|'
                        r'\bMAIN\s+ST', re.I)


def premises_verdict(address):
    """Return (verdict, confidence, why). No network call, no cost."""
    a = (address or '').strip()
    if not a:
        return 'unknown', 0, 'no address in registry'
    if MAILBOX.search(a):
        return 'mailbox', 0, 'private mailbox / mail drop -> no premises to clean'
    if APARTMENT.search(a):
        return 'home_based', 0, 'apartment -> residential'
    if SUITE.search(a):
        return 'commercial', 3, 'has a suite/unit number -> leased space in a building'
    if COMMERCIAL.search(a):
        return 'commercial', 2, 'on a commercial corridor'
    if RESIDENTIAL.search(a):
        return 'home_based', 0, 'residential street type -> likely run from a house'
    return 'unknown', 1, 'address type unclear -- needs a look'


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--as-of', type=dt.date.fromisoformat, default=dt.date.today())
    p.add_argument('--keep-unknown', action='store_true',
                   help='also keep addresses we could not classify')
    a = p.parse_args()

    rows = read_csv(DATA / 'raw' / f'candidates-{a.as_of}.csv')
    for r in rows:
        v, conf, why = premises_verdict(r.get('taxpayer_address'))
        r['premises'], r['premises_confidence'], r['premises_reason'] = v, conf, why

    wanted = {'commercial'} | ({'unknown'} if a.keep_unknown else set())
    keep = [r for r in rows if r['premises'] in wanted]
    out = write_csv(DATA / 'verified' / f'verified-{a.as_of}.csv', keep)

    from collections import Counter
    tally = Counter(r['premises'] for r in rows)
    print(f'STEP 3: {len(rows)} in -> {dict(tally)} -> kept {len(keep)} -> {out}')
    print('        (no API, no cost, no Google content)')


if __name__ == '__main__':
    main()
