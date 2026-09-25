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

# Bare personal names ("DUY HUYNH LLC", "LUIS JESUS MARRUPE GRUEIRO LLC") are usually
# one-person entities with no storefront. Two to four capitalized words + LLC and nothing
# else -- the old two-word-only rule let four-word Hispanic and compound surnames through,
# which is how LUIS JESUS MARRUPE GRUEIRO LLC reached a delivered list.
#
# Widening this is only safe because verdict() now checks for a physical hint first: a name
# like "MARY JANE DENTAL LLC" matches this pattern too, and dropping it would be worse than
# the bug being fixed.
PERSONAL = re.compile(
    r'^[A-Z]+( [A-Z]+){1,3},? (LLC|L\.L\.C\.|LIMITED LIABILITY COMPANY)$', re.I
)

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
    # Ordered by how much each pattern actually knows. PHYSICAL_HINT is positive evidence
    # of a place with floors. JUNK matches an explicit word like HOLDINGS or CAPITAL. Only
    # PERSONAL is a guess, made from the shape of a name, so it goes last -- which is both
    # what makes widening it safe and what keeps "BLUEBONNET HOLDINGS GROUP LLC" reported
    # as a holding company rather than as somebody's name.
    if PHYSICAL_HINT.search(name):
        return 'keep_physical_hint'
    if JUNK.search(name):
        return 'drop_no_premises'
    if PERSONAL.match(name.strip()):
        return 'drop_personal_name'
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
