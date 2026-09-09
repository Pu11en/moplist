"""STEP 3b — ENRICH: for rows step 3 could not decide from the address alone,
find any public web mention of the business and read what it says.

  Jina Search (s.jina.ai)  ->  top 5 results  ->  classify title + snippet
  ->  optional homepage fetch if we found the biz's own site.

Why we look at directories: brand-new LLCs often have no website of their
own yet, but they may have a Yelp / Facebook / Google page. Those pages
still carry the category signal ("Bakery", "Nail Salon"), which is what
step 4 actually needs. We tier the confidence: own-site > directory-page.

Hard-rule check: search results are a discovery signal, not the delivered
list. What ships in the CSV is registry data. The `web_*` columns are
internal metadata we use to decide whether to keep a row.

Output: rewrites verified-<date>.csv with columns
  web_url, web_title, web_desc, web_verdict, web_reason
and promotes unknowns that turned out to have a real premises. Unknowns
that reveal themselves as home-based / mobile / no-web-presence are dropped.
"""
import argparse, datetime as dt, html, json, os, re, subprocess, time, urllib.parse
from collections import Counter
from common import DATA, ROOT, read_csv, write_csv

CACHE = DATA / 'cache' / 'enrichment.json'
UA = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36'


def load_env():
    env = ROOT / '.env'
    if env.exists():
        for line in env.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                k, v = line.split('=', 1)
                os.environ.setdefault(k.strip(), v.strip())


load_env()
JINA_KEY = os.environ.get('JINA_API_KEY', '')

# Directory / social hosts. Not skipped anymore — used to tier confidence.
DIRECTORY = re.compile(
    r'(^|\.)(facebook|linkedin|instagram|tiktok|twitter|x|youtube|pinterest|'
    r'yelp|yellowpages|bbb|mapquest|foursquare|nextdoor|google|maps|'
    r'bizapedia|opencorporates|buzzfile|dnb|zoominfo|apollo|rocketreach|'
    r'chamberofcommerce|manta|hotfrog|superpages|whitepages|spokeo|'
    r'reddit|quora|medium|wikipedia|amazon|ebay|etsy|airbnb|vrbo|expedia|'
    r'goodhire|glassdoor|indeed|ziprecruiter|apollo)\.[a-z.]+$', re.I)

# Hosts that add no signal even in a snippet — always skip.
GARBAGE = re.compile(
    r'(^|\.)(tx\.gov|texas\.gov|irs\.gov|sos\.state\.tx\.us|comptroller\.texas)\.[a-z.]+$', re.I)

HIGH = re.compile(r'\b(dental|dentist|medical|clinic|chiro\w*|physical therapy|'
    r'pediatric|optometry|orthodont\w*|veterinary|urgent care|'
    r'salon|salons|spa|barber\w*|nail\w*|lash\w*|brow bar|hairsty\w*|hair\s+studio|'
    r'cafe|coffee|bakery|bakeries|restaurant|kitchen|grill|taqueria|pizza|pizzeria|'
    r'brewing|brewery|deli|bistro|gastropub|steakhouse|'
    r'gym|fitness|crossfit|yoga|pilates|daycare|childcare|montessori|preschool)\b', re.I)

MID = re.compile(r'\b(studio|studios|academy|school|learning|tutoring|boutique|shop|'
    r'store|market|retail|gallery|lounge|club|wellness|therapy|counseling|'
    r'beauty|aesthetic|dance|martial|office|suites|showroom|dispensary|'
    r'hotel|inn|tattoo|piercing|photograph\w*|printing|print\s+shop|'
    r'auto\s+repair|body\s+shop|mechanic\s+shop|welding\s+shop|'
    r'church|chapel|ministry|ministries)\b', re.I)

PERSONAL = re.compile(r'\b(freelance|freelancer|independent contractor|'
    r'personal portfolio|solopreneur|life coach|virtual assistant|'
    r'work from home|home[- ]based|by appointment only|'
    r'mobile service|we come to you|mobile detailing|mobile mechanic|'
    r'airbnb|vrbo|short.?term rental|vacation rental)\b', re.I)

# Corporate suffixes to strip from queries.
CORP_SUFFIX = re.compile(
    r'[,\s]+(LLC|L\.L\.C\.|LLP|LTD|INC|INCORPORATED|CORP|CORPORATION|CO|'
    r'PLLC|P\.L\.L\.C\.|PC|P\.C\.|COMPANY|LIMITED|LIMITED LIABILITY COMPANY)\.?\s*$',
    re.I)


def clean_name(name):
    n = name.strip()
    # Strip corporate suffix repeatedly (handles ", LLC.")
    for _ in range(3):
        m = CORP_SUFFIX.search(n)
        if not m:
            break
        n = n[:m.start()].strip().rstrip(',')
    return n


def curl(url, timeout=20, headers=None):
    cmd = ['curl', '--silent', '--max-time', str(timeout), '-A', UA, '-L']
    for k, v in (headers or {}).items():
        cmd += ['-H', f'{k}: {v}']
    cmd.append(url)
    try:
        r = subprocess.run(cmd, capture_output=True, timeout=timeout + 5)
        return r.stdout.decode('utf-8', errors='ignore')
    except Exception:
        return ''


def jina_search(query, timeout=30):
    if not JINA_KEY:
        raise SystemExit('JINA_API_KEY not set. Put it in .env.')
    url = 'https://s.jina.ai/?q=' + urllib.parse.quote(query)
    body = curl(url, timeout=timeout, headers={
        'Authorization': f'Bearer {JINA_KEY}',
        'Accept': 'application/json',
        'X-Respond-With': 'no-content',
    })
    try:
        d = json.loads(body or '{}')
    except json.JSONDecodeError:
        return []
    if d.get('code') != 200:
        return []
    return [(it.get('url') or '', it.get('title') or '', it.get('description') or '')
            for it in (d.get('data') or [])]


def host(url):
    try:
        return (urllib.parse.urlparse(url).hostname or '').lower()
    except ValueError:
        return ''


def title_desc(url):
    raw = curl(url, timeout=12)
    t = re.search(r'<title[^>]*>([^<]+)</title>', raw, re.I | re.S)
    d = (re.search(r'<meta[^>]+name=["\']description["\'][^>]+content=["\']([^"\']+)', raw, re.I)
         or re.search(r'<meta[^>]+content=["\']([^"\']+)["\'][^>]+name=["\']description["\']', raw, re.I))
    return (html.unescape((t.group(1) if t else '').strip())[:200],
            html.unescape((d.group(1) if d else '').strip())[:400])


def classify_text(text):
    if PERSONAL.search(text):  return 'home_based', 0
    if HIGH.search(text):      return 'has_premises_high', 3
    if MID.search(text):       return 'has_premises_mid', 2
    return 'unclear', 1


STREET_TYPE = re.compile(
    r'\b(st|street|ave|avenue|rd|road|blvd|dr|drive|ln|ct|way|hwy|highway|'
    r'loop|circle|cir|trail|trl|pkwy|parkway|place|pl|lane)\b', re.I)

# URL paths that mean "this LLC owns a short-term rental listing" -> home-based.
STR_LISTING = re.compile(
    r'/(room|rooms|listing|listings|property|properties|rental|rentals|cabin|'
    r'suite|villa|home)/', re.I)


def pick_best(hits, biz_name, biz_city):
    """From Jina hits, pick the one that best represents this business.
    Score: own-site > directory-page-that-mentions-the-name > directory generic.

    Reject a match unless the biz's city ALSO appears in the result — otherwise
    a namesake in another state gets picked up (TCConline.tv church in PA, etc.).
    """
    cleaned = clean_name(biz_name)
    name_toks = [t.lower() for t in re.split(r'\W+', cleaned) if len(t) > 2]
    non_street = [t for t in name_toks if not STREET_TYPE.match(t)]
    strict_name = len(non_street) >= 2 or (len(non_street) == 1 and len(non_street[0]) >= 6)
    city = (biz_city or '').lower().strip()
    # First token of city ("NEW BRAUNFELS" -> "new"/"braunfels"); accept either.
    city_toks = [t for t in re.split(r'\W+', city) if len(t) > 3]

    scored = []
    for (url, title, desc) in hits:
        h = host(url)
        if not h or GARBAGE.search(h):
            continue
        text = f'{title} {desc}'.lower()
        url_l = url.lower()
        matches = sum(1 for t in non_street if t in text or t in url_l)
        name_hit = matches >= max(1, min(2, len(non_street)))
        if name_hit and not strict_name:
            name_hit = False
        # City must appear somewhere in the result (title, desc, or URL).
        city_hit = any(ct in text or ct in url_l for ct in city_toks)
        if name_hit and not city_hit:
            name_hit = False
        is_directory = bool(DIRECTORY.search(h))
        is_str = bool(STR_LISTING.search(url))
        tier = (0 if not is_directory and name_hit else
                1 if is_directory and name_hit else
                2 if not is_directory else
                3)
        scored.append((tier, url, title, desc, is_directory, name_hit, is_str))
    scored.sort(key=lambda x: x[0])
    return scored[0] if scored else None


def enrich(row, cache, sleep):
    key = row.get('taxpayer_number') or row['taxpayer_name']
    if key in cache:
        return cache[key], True
    cleaned = clean_name(row['taxpayer_name'])
    query = f'{cleaned} {row.get("taxpayer_city","")} TX'
    hits = jina_search(query)
    best = pick_best(hits, row['taxpayer_name'], row.get('taxpayer_city', ''))
    if not best:
        result = {'web_url': '', 'web_title': '', 'web_desc': '',
                  'web_verdict': 'no_site_found',
                  'web_reason': f'no city-matching result for "{query}"'}
    else:
        tier, url, jt, jd, is_directory, name_hit, is_str = best
        title, desc = jt[:200], jd[:400]
        if not is_directory and name_hit:
            pt, pd = title_desc(url)
            if pt or pd:
                title, desc = pt, pd
        verdict, _ = classify_text(f'{title} {desc}')
        if is_str:
            verdict = 'home_based'  # LLC owns a rental listing, not a premises to clean
        if not name_hit:
            verdict = 'unclear_no_name_match'
        elif is_directory and verdict.startswith('has_premises'):
            verdict = verdict + '_directory'
        reason = (f'{host(url)} says: {(title or desc)[:120]}'
                  if (title or desc) else f'{host(url)}: no readable text')
        result = {'web_url': url, 'web_title': title, 'web_desc': desc,
                  'web_verdict': verdict, 'web_reason': reason}
    cache[key] = result
    time.sleep(sleep)
    return result, False


PROMOTE = {
    'has_premises_high':           (3, 'high-traffic ICP per own site'),
    'has_premises_mid':            (2, 'physical premises per own site'),
    'has_premises_high_directory': (2, 'high-traffic ICP per directory listing'),
    'has_premises_mid_directory':  (1, 'physical premises per directory listing'),
}
# Any verdict NOT in PROMOTE means: drop the row from the delivered list.


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--as-of', type=dt.date.fromisoformat, default=dt.date.today())
    p.add_argument('--max', type=int, default=200,
                   help='cap on live Jina lookups this run (cache hits do not count)')
    p.add_argument('--sleep', type=float, default=0.3)
    p.add_argument('--rerun', action='store_true',
                   help='drop cache and requery everyone')
    a = p.parse_args()

    path = DATA / 'verified' / f'verified-{a.as_of}.csv'
    rows = read_csv(path)
    cache = {} if a.rerun else load_cache()

    unknowns = [r for r in rows if r.get('premises') == 'unknown']
    print(f'STEP 3b: {len(unknowns)} unknown rows to enrich (live cap {a.max})')

    live = 0
    for r in unknowns:
        if live >= a.max:
            break
        e, cached = enrich(r, cache, a.sleep)
        r.update(e)
        if e['web_verdict'] in PROMOTE:
            conf, why = PROMOTE[e['web_verdict']]
            r['premises'] = 'commercial'
            r['premises_confidence'] = str(conf)
            r['premises_reason'] = f'{why} ({host(e["web_url"])})'
        if not cached:
            live += 1
            if live % 10 == 0:
                save_cache(cache)

    save_cache(cache)

    keep = [r for r in rows if r.get('premises') == 'commercial']
    write_csv(path, keep)

    verdicts = Counter(r.get('web_verdict', '') for r in unknowns if r.get('web_verdict'))
    print(f'STEP 3b: verdicts={dict(verdicts)}, kept {len(keep)} '
          f'({len(rows)-len(keep)} dropped, {live} live queries)')


def load_cache():
    return json.loads(CACHE.read_text()) if CACHE.exists() else {}


def save_cache(c):
    CACHE.parent.mkdir(parents=True, exist_ok=True)
    CACHE.write_text(json.dumps(c, indent=2))


if __name__ == '__main__':
    main()
