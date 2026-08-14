#!/usr/bin/env python3
"""blocklist.py — build a high-confidence IP blocklist from CTIWatch.

    ./blocklist.py                      # confidence >= 85, active only
    ./blocklist.py --min-confidence 95 --limit 5000 > block.txt

No API key required (the CSV export endpoint needs one; this pages the public
JSON endpoint instead). Standard library only.

The point of this example is the pagination: the API caps `limit` at 100 and
does NOT tell you it did. Asking for 5000 returns 100 rows with HTTP 200, so
anything that trusts its own `limit` silently processes 2% of the data.
"""
import argparse
import json
import sys
import urllib.parse
import urllib.request

API = "https://ctiwatch.com/api/v1"
PAGE = 100  # the server's hard cap; asking for more is silently clamped


def fetch(path, **params):
    url = f"{API}{path}?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(url, headers={"User-Agent": "ctiwatch-example/1.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--min-confidence", type=int, default=85,
                    help="0-100; indicators decay with age, so this is a recency filter too")
    ap.add_argument("--limit", type=int, default=1000, help="how many to collect")
    ap.add_argument("--type", default="ip", help="ip, domain, url, hash_sha256, …")
    args = ap.parse_args()

    seen, out = set(), []
    offset = 0

    while len(out) < args.limit:
        page = fetch("/iocs", type=args.type, confidence_min=args.min_confidence,
                     active_only="true", limit=PAGE, offset=offset)
        items = page.get("items", [])
        if not items:
            break  # ran out of data before running out of appetite

        for it in items:
            v = it.get("value")
            if v and v not in seen:      # the corpus can hold the same value twice
                seen.add(v)
                out.append(it)
                if len(out) >= args.limit:
                    break

        offset += PAGE
        if offset >= page.get("total", 0):
            break

    print(f"# CTIWatch blocklist — type={args.type} "
          f"confidence>={args.min_confidence} count={len(out)}", file=sys.stderr)
    print("# Re-fetch regularly: confidence decays and stale indicators are "
          "deactivated.", file=sys.stderr)

    for it in out:
        print(it["value"])


if __name__ == "__main__":
    main()
