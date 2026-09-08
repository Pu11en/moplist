"""Shared helpers. Keep this boring."""
import csv, json, subprocess, urllib.parse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'data'


def fetch(url, timeout=45):
    """GET via system curl. Python's TLS store failed on this host; curl works."""
    r = subprocess.run(
        ['curl', '--fail', '--silent', '--show-error', '--max-time', str(timeout), url],
        capture_output=True)
    if r.returncode:
        raise RuntimeError(f'fetch failed: {url.split("?")[0]}: {r.stderr.decode()[:300]}')
    return r.stdout


def get_json(base, params):
    return json.loads(fetch(base + '?' + urllib.parse.urlencode(params)))


def read_csv(path):
    with open(path, newline='') as f:
        return list(csv.DictReader(f))


def write_csv(path, rows):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text('')
        return path
    # Socrata omits null fields, so row 1 is not authoritative. Union all keys,
    # first-seen order, and fill blanks -- otherwise DictWriter raises.
    fields = list(dict.fromkeys(k for r in rows for k in r))
    rows = [{k: r.get(k, '') for k in fields} for r in rows]
    with path.open('w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)
    return path
