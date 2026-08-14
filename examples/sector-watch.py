#!/usr/bin/env python3
"""sector-watch.py — who is attacking my sector, in my country?

    ./sector-watch.py --country BR
    ./sector-watch.py --country BR --sector Healthcare --days 90

Answers the only question most people actually have: is pressure on
organisations like mine going up or down, and who is applying it?

No API key required. Standard library only.

⚠️ Every record here is a CLAIM published by a ransomware group on its own
extortion site — not a confirmed breach. Groups exaggerate, recycle old data
and occasionally invent. Report these as "group X claims to have hit Y".
"""
import argparse
import collections
import datetime as dt
import json
import urllib.parse
import urllib.request

API = "https://ctiwatch.com/api/v1"
PAGE = 100


def fetch(path, **params):
    url = f"{API}{path}?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(url, headers={"User-Agent": "ctiwatch-example/1.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def collect(country, sector, cap=1000):
    """Page through victims, honouring the server's 100-row cap."""
    filters = {"limit": PAGE}
    if country:
        filters["country"] = country
    if sector:
        filters["sector"] = sector

    rows, offset = [], 0
    while len(rows) < cap:
        page = fetch("/victims", offset=offset, **filters)
        items = page.get("items", [])
        if not items:
            break
        rows.extend(items)
        offset += PAGE
        if offset >= page.get("total", 0):
            break
    return rows, page.get("total", len(rows))


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--country", help="ISO code, e.g. BR")
    ap.add_argument("--sector", help="e.g. Healthcare")
    ap.add_argument("--days", type=int, default=90, help="window for the trend (default 90)")
    args = ap.parse_args()

    rows, total = collect(args.country, args.sector)
    scope = " / ".join(x for x in (args.country, args.sector) if x) or "everything"
    print(f"{total} claimed victims matching {scope} "
          f"({len(rows)} most recent examined)\n")

    now = dt.datetime.now(dt.timezone.utc)
    cur = prev = 0
    groups = collections.Counter()
    sectors = collections.Counter()

    for v in rows:
        raw = v.get("attack_date")
        if not raw:
            continue
        when = dt.datetime.fromisoformat(raw.replace("Z", "+00:00"))
        age = (now - when).days
        if age <= args.days:
            cur += 1
            groups[(v.get("metadata") or {}).get("group") or "—"] += 1
            if v.get("sector"):
                sectors[v["sector"]] += 1
        elif age <= args.days * 2:
            prev += 1

    line = f"Last {args.days}d: {cur} claims  |  previous {args.days}d: {prev}"
    if prev == 0:
        print(f"{line}  |  no earlier window to compare")
    elif prev < 5:
        # A percentage off a base of 1 or 2 is arithmetic, not a trend: one
        # extra victim reads as "+300%". Refuse to dress noise up as a signal.
        print(f"{line}  |  base too small for a trend")
    else:
        change = (cur - prev) / prev * 100
        print(f"{line}  |  {'UP' if change > 0 else 'DOWN'} {abs(change):.0f}%")

    if groups:
        print(f"\nMost active groups (last {args.days}d)")
        for name, n in groups.most_common(10):
            print(f"  {n:>4}  {name}")

    if sectors and not args.sector:
        print(f"\nMost affected sectors (last {args.days}d)")
        for name, n in sectors.most_common(10):
            print(f"  {n:>4}  {name}")

    print("\nThese are attacker claims, not confirmed breaches.")


if __name__ == "__main__":
    main()
