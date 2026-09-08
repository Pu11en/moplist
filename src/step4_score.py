"""STEP 4 — SCORE: which verified businesses actually need a commercial cleaner?

A dentist's office needs a nightly cleaner. A tattoo parlor might. A self-storage
facility barely does. Score them so the weekly list leads with the best ones.
Output: data/verified/scored-<date>.csv
"""
import argparse, datetime as dt
from common import DATA, read_csv, write_csv

# Google Places "types" -> how badly they typically need recurring commercial cleaning.
HOT = {'dentist', 'doctor', 'hospital', 'physiotherapist', 'veterinary_care',
       'beauty_salon', 'hair_care', 'spa', 'gym', 'restaurant', 'cafe', 'bakery',
       'bar', 'meal_takeaway', 'school', 'child_care', 'lawyer', 'accounting',
       'real_estate_agency', 'insurance_agency', 'bank'}
WARM = {'store', 'clothing_store', 'furniture_store', 'shoe_store', 'book_store',
        'florist', 'pet_store', 'car_dealer', 'lodging', 'church', 'local_government_office'}


def score(row):
    types = set((row.get('types') or '').split('|'))
    pts, why = 0, []
    if types & HOT:
        pts += 3; why.append('high-traffic premises')
    elif types & WARM:
        pts += 2; why.append('retail premises')
    else:
        pts += 1; why.append('premises type unclear')
    if row.get('looks_new') == 'yes':
        pts += 2; why.append('no reviews yet = likely just opened')
    if row.get('filter_verdict') == 'keep_physical_hint':
        pts += 1; why.append('name implies a physical place')
    if (row.get('business_status') or 'OPERATIONAL') != 'OPERATIONAL':
        pts -= 3; why.append('not operational')
    return pts, '; '.join(why)


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--as-of', type=dt.date.fromisoformat, default=dt.date.today())
    a = p.parse_args()

    rows = read_csv(DATA / 'verified' / f'verified-{a.as_of}.csv')
    for r in rows:
        r['lead_score'], r['score_reason'] = score(r)
    rows.sort(key=lambda r: -int(r['lead_score']))
    out = write_csv(DATA / 'verified' / f'scored-{a.as_of}.csv', rows)
    top = sum(1 for r in rows if int(r['lead_score']) >= 5)
    print(f'STEP 4: {len(rows)} scored, {top} scoring 5+ (lead with these) -> {out}')


if __name__ == '__main__':
    main()
