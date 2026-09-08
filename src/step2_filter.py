"""STEP 2 — FILTER: kill obvious non-targets by name. Free, instant, no API.

A holding company has no floor to mop. This is the cheapest cut you will ever make,
so make it before you spend money on Places lookups in step 3.
Output: data/raw/candidates-<date>.csv
"""
import argparse, datetime as dt, re
from common import DATA, read_csv, write_csv

# Entities that exist on paper but have no cleanable premises.
JUNK = re.compile(r'\b('
    r'HOLDINGS?|CAPITAL|INVESTMENTS?|VENTURES?|EQUITY|PARTNERS|FUND|TRUST|'
    r'REALTY|REAL ESTATE|PROPERTIES|PROPERTY|LAND|RANCH|FARMS?|'
    r'FINANCIAL|INSURANCE|MORTGAGE|LENDING|CONSULTING|CONSULTANTS?|'
    r'TRUCKING|TRANSPORT|LOGISTICS|HAULING|LAWN|LANDSCAP\w*|ROOFING|'
    r'CONSTRUCTION|CONTRACTING|PLUMBING|ELECTRIC\w*|HVAC|'
    r'ENTERPRISES?|SOLUTIONS|GROUP|MANAGEMENT|MGMT|SERVICES'
    r')\b', re.I)

# Bare personal names ("DUY HUYNH LLC", "HEIDI HOLMES, LLC") are usually one-person
# entities with no storefront. Two capitalized words + LLC and nothing else.
PERSONAL = re.compile(r'^[A-Z]+ [A-Z]+,? (LLC|L\.L\.C\.|LIMITED LIABILITY COMPANY)$', re.I)

# Names that suggest an actual physical place with floors, restrooms and traffic.
PHYSICAL_HINT = re.compile(r'\b('
    r'CLINIC|MEDICAL|DENTAL|DENTIST|HEALTH|WELLNESS|THERAPY|COUNSELING|CHIRO\w*|'
    r'SALON|SPA|BARBER|NAILS?|LASH|BEAUTY|'
    r'CAFE|COFFEE|BAKERY|RESTAURANT|KITCHEN|GRILL|BAR|BREWING|TAQUERIA|PIZZA|'
    r'GYM|FITNESS|STUDIO|YOGA|PILATES|DANCE|MARTIAL|'
    r'ACADEMY|SCHOOL|LEARNING|DAYCARE|CHILDCARE|MONTESSORI|'
    r'BOUTIQUE|SHOP|STORE|MARKET|RETAIL|GALLERY|'
    r'OFFICE|SUITES|CENTER|CENTRE|LOUNGE|CLUB|INN|HOTEL|SUITE'
    r')\b', re.I)


def verdict(name):
    if PERSONAL.match(name.strip()):
        return 'drop_personal_name'
    if PHYSICAL_HINT.search(name):
        return 'keep_physical_hint'   # strong signal, keep even if JUNK also matches
    if JUNK.search(name):
        return 'drop_no_premises'
    return 'keep_unknown'             # no signal either way -> step 3 decides


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--as-of', type=dt.date.fromisoformat, default=dt.date.today())
    a = p.parse_args()

    rows = read_csv(DATA / 'raw' / f'filings-{a.as_of}.csv')
    for r in rows:
        r['filter_verdict'] = verdict(r['taxpayer_name'])
    kept = [r for r in rows if r['filter_verdict'].startswith('keep')]
    out = write_csv(DATA / 'raw' / f'candidates-{a.as_of}.csv', kept)

    hot = sum(1 for r in kept if r['filter_verdict'] == 'keep_physical_hint')
    print(f'STEP 2: {len(rows)} in -> {len(kept)} kept ({hot} with a physical hint) -> {out}')


if __name__ == '__main__':
    main()
