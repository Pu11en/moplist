"""STEP 5 — PACKAGE: turn scored leads into the thing a customer actually receives.

Two artifacts per territory:
  - a CSV they can work from
  - a plain-text email body (the free-sample pitch, or the paid weekly drop)
Output: data/delivered/<territory>-<date>.csv  and  .txt
"""
import argparse, datetime as dt
from common import DATA, read_csv, write_csv

SAMPLE_N = 3   # how many leads to give away free in a cold email


def email_body(rows, territory, paid, price='$150/mo'):
    lines = []
    if paid:
        lines.append(f'Your {territory} list for the week of {dt.date.today()}:\n')
        show = rows
    else:
        lines.append(f'Hi -- {len(rows)} businesses just opened in {territory} '
                     f'that likely do not have a commercial cleaner yet:\n')
        show = rows[:SAMPLE_N]
    for i, r in enumerate(show, 1):
        lines.append(f'{i}. {r.get("places_name") or r["taxpayer_name"]}')
        lines.append(f'   {r.get("address","")}')
        lines.append(f'   filed {r.get("sos_charter_date","")[:10]}')
        lines.append('')
    if not paid:
        lines.append(f'These are free. If useful, I send a fresh list every week for {price} '
                     f'-- no contract, reply "stop" anytime.')
        lines.append('')
        lines.append('Reply "yes" and you are on next week\'s list.')
    return '\n'.join(lines)


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--as-of', type=dt.date.fromisoformat, default=dt.date.today())
    p.add_argument('--territory', default='New Braunfels')
    p.add_argument('--min-score', type=int, default=4)
    a = p.parse_args()

    rows = [r for r in read_csv(DATA / 'verified' / f'scored-{a.as_of}.csv')
            if int(r['lead_score']) >= a.min_score]
    slug = a.territory.lower().replace(' ', '-')
    csv_out = write_csv(DATA / 'delivered' / f'{slug}-{a.as_of}.csv', rows)
    txt_out = DATA / 'delivered' / f'{slug}-{a.as_of}-sample.txt'
    txt_out.write_text(email_body(rows, a.territory, paid=False))
    print(f'STEP 5: {len(rows)} leads packaged -> {csv_out}')
    print(f'        cold-email sample body -> {txt_out}')


if __name__ == '__main__':
    main()
