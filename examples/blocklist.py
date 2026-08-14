#!/usr/bin/env python3
"""blocklist.py — build a high-confidence IP blocklist from CTIWatch.

    ./blocklist.py                                   # no key: up to 1000 rows
    export CTIWATCH_API_KEY=ctw_...                  # free key: no depth limit
    ./blocklist.py --min-confidence 95 --limit 5000 > block.txt

Standard library only.

Two traps this example exists to teach:

1. `limit` is capped at 100 and the API does NOT tell you it did. Asking for
   5000 returns 100 rows with HTTP 200, so anything that trusts its own `limit`
   silently processes 2% of the data. You have to page with `offset`.

2. Without an API key, `offset` stops at 1000 — deeper paging answers 403
   ACCOUNT_REQUIRED. That is deliberate: browsing and testing stay open to
   everyone, bulk collection is what needs a (free) account. A key removes the
   limit entirely and is one form away at https://ctiwatch.com/register.
"""
import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

API = "https://ctiwatch.com/api/v1"
PAGE = 100            # the server's hard cap; asking for more is silently clamped
ANON_MAX_OFFSET = 1000  # depth allowed without an API key


def fetch(path, api_key=None, **params):
    url = f"{API}{path}?{urllib.parse.urlencode(params)}"
    headers = {"User-Agent": "ctiwatch-example/1.0"}
    if api_key:
        headers["X-Api-Key"] = api_key
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--min-confidence", type=int, default=85,
                    help="0-100; indicators decay with age, so this is a recency filter too")
    ap.add_argument("--limit", type=int, default=1000, help="how many to collect")
    ap.add_argument("--type", default="ip", help="ip, domain, url, hash_sha256, …")
    ap.add_argument("--api-key", default=os.environ.get("CTIWATCH_API_KEY"),
                    help="or set CTIWATCH_API_KEY; lifts the 1000-row depth limit")
    args = ap.parse_args()

    seen, out = set(), []
    offset = 0

    while len(out) < args.limit:
        if not args.api_key and offset >= ANON_MAX_OFFSET:
            print(f"# stopped at {len(out)} rows: without an API key the API "
                  f"stops paging at offset {ANON_MAX_OFFSET}.\n"
                  "# A free key removes the limit: https://ctiwatch.com/register\n"
                  "# then: export CTIWATCH_API_KEY=ctw_...", file=sys.stderr)
            break
        try:
            page = fetch("/iocs", api_key=args.api_key, type=args.type,
                         confidence_min=args.min_confidence,
                         active_only="true", limit=PAGE, offset=offset)
        except urllib.error.HTTPError as e:
            # Read the body: this API says WHY in a machine-readable `code`.
            try:
                err = json.load(e)
            except Exception:
                err = {}
            if e.code == 403 and err.get("code") == "ACCOUNT_REQUIRED":
                print(f"# {err.get('error')}", file=sys.stderr)
                break
            if e.code == 429 and err.get("code") == "ROW_QUOTA":
                print(f"# daily row limit reached ({err.get('limit')} rows). "
                      "Collected so far is still valid.", file=sys.stderr)
                break
            raise

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
