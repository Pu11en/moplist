"""STEP 6 — DELIVER: samples go to Instantly (prospects), paid lists go to customers.

Instantly does the sending, warmup and deliverability -- that is why we use it rather
than sending ourselves. This script only pushes leads into a campaign.

Needs: INSTANTLY_API_KEY. Docs: https://developer.instantly.ai/
Output: appends to data/delivered/sent-log.csv
"""
import argparse, datetime as dt, json, os, subprocess
from common import DATA, ROOT, read_csv, write_csv

INSTANTLY = 'https://api.instantly.ai/api/v2/leads'


def push(campaign_id, prospect, body, key):
    payload = {'campaign': campaign_id,
               'email': prospect['public_email'],
               'company_name': prospect['business_name'],
               'personalization': body}
    r = subprocess.run(['curl', '--fail', '--silent', '--show-error', '-X', 'POST', INSTANTLY,
                        '-H', f'Authorization: Bearer {key}',
                        '-H', 'Content-Type: application/json',
                        '-d', json.dumps(payload)], capture_output=True)
    if r.returncode:
        raise RuntimeError(r.stderr.decode()[:300])
    return json.loads(r.stdout or '{}')


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--as-of', type=dt.date.fromisoformat, default=dt.date.today())
    p.add_argument('--territory', default='New Braunfels')
    p.add_argument('--campaign-id', required=True, help='Instantly campaign to load into')
    p.add_argument('--prospects', required=True, help='CSV of cleaning companies to pitch')
    p.add_argument('--dry-run', action='store_true')
    a = p.parse_args()

    key = os.environ.get('INSTANTLY_API_KEY')
    if not key and not a.dry_run:
        raise SystemExit('Set INSTANTLY_API_KEY (or use --dry-run).')

    slug = a.territory.lower().replace(' ', '-')
    body = (DATA / 'delivered' / f'{slug}-{a.as_of}-sample.txt').read_text()
    prospects = [r for r in read_csv(a.prospects) if r.get('public_email')]

    sent = []
    for pr in prospects:
        if a.dry_run:
            print(f'[dry-run] would push {pr["business_name"]} <{pr["public_email"]}>')
        else:
            push(a.campaign_id, pr, body, key)
        sent.append({'date': str(a.as_of), 'territory': a.territory,
                     'business': pr['business_name'], 'email': pr['public_email'],
                     'campaign': a.campaign_id, 'dry_run': a.dry_run})
    write_csv(DATA / 'delivered' / 'sent-log.csv', sent)
    print(f'STEP 6: {len(sent)} prospects {"simulated" if a.dry_run else "pushed to Instantly"}')


if __name__ == '__main__':
    main()
