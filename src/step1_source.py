"""STEP 1 — SOURCE: pull new business filings from the Texas registry.

Free, public, no key. This is the raw net-drag: everything, junk included.
Output: data/raw/filings-<date>.csv
"""
import argparse, datetime as dt
from common import DATA, get_json, write_csv

API = 'https://data.texas.gov/resource/9cir-efmm.json'
FIELDS = ('taxpayer_number,taxpayer_name,taxpayer_address,taxpayer_city,taxpayer_state,taxpayer_zip,'
          'taxpayer_organizational_type,secretary_of_state_sos_or_coa_file_number,'
          'sos_charter_date,_621111')


def sql(v):
    return "'" + v.replace("'", "''") + "'"


def pull(cities, since, until):
    where = (f"taxpayer_state='TX' AND taxpayer_organizational_type='CL' "
             f"AND upper(taxpayer_city) in({','.join(map(sql, cities))}) "
             f"AND sos_charter_date >= '{since}T00:00:00' "
             f"AND sos_charter_date < '{until}T00:00:00'")
    rows, offset = [], 0
    while True:
        page = get_json(API, {'$select': FIELDS, '$where': where,
                              '$order': 'sos_charter_date DESC',
                              '$limit': '1000', '$offset': str(offset)})
        rows += page
        if len(page) < 1000:
            return rows
        offset += 1000


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--cities', default='NEW BRAUNFELS',
                   help='comma-separated, e.g. "NEW BRAUNFELS,SEGUIN,SAN MARCOS"')
    p.add_argument('--days', type=int, default=30, help='look-back window')
    p.add_argument('--as-of', type=dt.date.fromisoformat, default=dt.date.today())
    a = p.parse_args()

    cities = [c.strip().upper() for c in a.cities.split(',')]
    since = (a.as_of - dt.timedelta(days=a.days)).isoformat()
    rows = pull(cities, since, a.as_of.isoformat())
    out = write_csv(DATA / 'raw' / f'filings-{a.as_of}.csv', rows)
    print(f'STEP 1: {len(rows)} filings, {since} .. {a.as_of} -> {out}')


if __name__ == '__main__':
    main()
