"""STEP 4 — SCORE: which verified businesses actually need a commercial cleaner?

Rewritten 2026-09-08. The old version scored on Google Places `types` and
`user_ratings_total`, which step 3 stopped producing when it moved off Google
(see step3_verify.py). Everything scored 0. This version scores only on what
the registry + step 3 give us:

  1. Name category (0-3). A dental clinic or bakery in the name tells a cleaner
     what the place IS and where to drive. "SILVER KING MANAGMENT CONVERSE, LLC"
     tells them nothing actionable, so it scores 0 on this axis no matter what.
  2. Premises confidence from step 3 (0-3). Suite = 3, commercial corridor = 2.
  3. Charter recency (0-2). Newer = better; a brand-new place has no cleaner yet.

Max score 8. Output: data/verified/scored-<date>.csv
"""
import argparse, datetime as dt, re
from common import DATA, read_csv, write_csv

# HIGH: dirty/high-traffic premises a cleaner immediately recognizes as their ICP.
HIGH = re.compile(r'\b('
    r'DENTAL|DENTIST|MEDICAL|CLINIC|CHIRO\w*|PHYSICAL THERAPY|PEDIATRIC|OPTOMETRY|'
    r'ORTHODONT\w*|VETERINARY|VET|URGENT CARE|'
    r'SALON|SPA|BARBER|NAILS?|LASH|BROW|WAXING|'
    r'CAFE|COFFEE|BAKERY|RESTAURANT|KITCHEN|GRILL|BAR & GRILL|TAQUERIA|'
    r'PIZZA|BREWING|BREWERY|DELI|BISTRO|'
    r'GYM|FITNESS|CROSSFIT|YOGA|PILATES|'
    r'DAYCARE|CHILDCARE|MONTESSORI|PRESCHOOL'
    r')\b', re.I)

# MID: probably a real premises, but less obviously janitorial-heavy.
MID = re.compile(r'\b('
    r'STUDIO|ACADEMY|SCHOOL|LEARNING|TUTORING|'
    r'BOUTIQUE|SHOP|STORE|MARKET|RETAIL|GALLERY|'
    r'LOUNGE|BAR|CLUB|'
    r'WELLNESS|THERAPY|COUNSELING|HEALTH|BEAUTY|AESTHETIC|'
    r'DANCE|MARTIAL|KARATE|JIU|'
    r'OFFICE|SUITES|CENTER|CENTRE|HOTEL|INN'
    r')\b', re.I)

# Opaque names a cleaner cannot act on. Bare "FIRST LAST LLC" or short all-caps
# entity with no descriptor. If HIGH/MID matched, this is ignored.
OPAQUE_BARE_PERSONAL = re.compile(
    r'^[A-Z][A-Z\'\-]+(?:\s+[A-Z])?\s+[A-Z][A-Z\'\-]+,?\s+'
    r'(LLC|L\.L\.C\.|INC|CORP|LIMITED LIABILITY COMPANY)\.?$',
    re.I)


def name_score(name):
    n = (name or '').strip()
    if HIGH.search(n):
        return 3, 'name says what the place is (high-traffic ICP)'
    if MID.search(n):
        return 2, 'name implies a physical place'
    if OPAQUE_BARE_PERSONAL.match(n):
        return 0, 'opaque personal-name LLC -- no signal to a cleaner'
    return 1, 'name gives no category; premises signal only'


def recency_score(charter_date_str, as_of):
    if not charter_date_str:
        return 0, ''
    try:
        d = dt.date.fromisoformat(charter_date_str[:10])
    except ValueError:
        return 0, ''
    age = (as_of - d).days
    if age <= 7:
        return 2, f'chartered {age}d ago (fresh)'
    if age <= 14:
        return 1, f'chartered {age}d ago'
    return 0, f'chartered {age}d ago'


def score(row, as_of):
    pts, reasons = 0, []
    ns, nr = name_score(row.get('taxpayer_name'))
    pts += ns; reasons.append(nr)

    try:
        pc = int(row.get('premises_confidence') or 0)
    except ValueError:
        pc = 0
    pts += pc
    reasons.append(row.get('premises_reason') or 'no premises reason')

    rs, rr = recency_score(row.get('sos_charter_date'), as_of)
    pts += rs
    if rr:
        reasons.append(rr)

    return pts, '; '.join(reasons)


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--as-of', type=dt.date.fromisoformat, default=dt.date.today())
    a = p.parse_args()

    rows = read_csv(DATA / 'verified' / f'verified-{a.as_of}.csv')
    for r in rows:
        r['lead_score'], r['score_reason'] = score(r, a.as_of)
    rows.sort(key=lambda r: -int(r['lead_score']))
    out = write_csv(DATA / 'verified' / f'scored-{a.as_of}.csv', rows)
    top = sum(1 for r in rows if int(r['lead_score']) >= 5)
    print(f'STEP 4: {len(rows)} scored, {top} scoring 5+ (lead with these) -> {out}')


if __name__ == '__main__':
    main()
