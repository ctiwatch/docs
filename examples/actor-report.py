#!/usr/bin/env python3
"""actor-report.py — everything CTIWatch knows about one threat group.

    ./actor-report.py LockBit
    ./actor-report.py "Akira" --limit 200

Pulls the profile, the victim list and the sector breakdown, then prints a
briefing you can paste into a ticket.

No API key required. Standard library only.

Why `by-name` and not the id endpoint: actor names are what appear in reports
and news; UUIDs are not. This endpoint is case-insensitive and also tolerates
hyphens where the name has spaces.

🔴 The trap this script exists to defuse: leak-site group tags are VERSIONED.
`by-name/lockbit/victims` matches the tag exactly and returns 5 claims, while
the group's real footprint is spread across `lockbit`, `lockbit2`, `lockbit3`,
`lockbit5` — over 3,200 claims. Exact matching silently under-reports by 99%.
So this script always cross-checks the substring search and tells you when the
two disagree.
"""
import argparse
import collections
import json
import sys
import urllib.error
import urllib.parse
import urllib.request

API = "https://ctiwatch.com/api/v1"
PAGE = 100


def fetch(path, **params):
    url = f"{API}{path}"
    if params:
        url += "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": "ctiwatch-example/1.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("name", help="group name, e.g. LockBit")
    ap.add_argument("--limit", type=int, default=100, help="victims to examine")
    args = ap.parse_args()

    quoted = urllib.parse.quote(args.name)
    try:
        data = fetch(f"/threat-actors/by-name/{quoted}/victims", limit=PAGE)
    except urllib.error.HTTPError as e:
        if e.code == 404:
            print(f"No actor named {args.name!r}.\n\n"
                  "Try an alias — the industry names the same group several ways. "
                  "Search for candidates with:\n"
                  f"  curl -s '{API}/threat-actors?search="
                  f"{quoted}&limit=10' | jq -r '.items[].name'", file=sys.stderr)
            sys.exit(1)
        raise

    actor = data.get("actor") or {}
    total = data.get("total", 0)

    print(f"== {actor.get('name', args.name)} ==")
    for label, key in (("country", "country"), ("motivation", "motivation")):
        if actor.get(key):
            print(f"{label:<12} {actor[key]}")
    print(f"{'claims':<12} {total}   (exact tag match)")

    # Cross-check: the same name as a SUBSTRING over leak-site group tags.
    # Leak-site tags carry version numbers (lockbit2, lockbit3, lockbit5), and
    # the exact match above sees none of them.
    loose = fetch("/victims", group=args.name, limit=1).get("total", 0)
    if loose > total:
        variants = [
            g["group_name"] for g in fetch("/victims/stats").get("by_group", [])
            if args.name.lower() in (g.get("group_name") or "").lower()
        ]
        print(f"\n⚠️  A substring search finds {loose} claims, not {total}.")
        print("   Leak-site group tags are versioned, and the exact match misses them.")
        if variants:
            print("   Variants seen in the data: " + ", ".join(variants[:12]))
        print(f"   For the group's full footprint use:")
        print(f"     {API}/victims?group={urllib.parse.quote(args.name)}")
        print("   ⚠️  but note substrings over-match too: group=play also matches "
              "'playboy'.")

    if actor.get("description"):
        print("\n" + actor["description"][:600].strip())

    # top_sectors comes from the server, computed over ALL victims of the group
    # — not just the page we fetched. Prefer it over counting locally.
    if data.get("top_sectors"):
        print("\nMost targeted sectors (all claims)")
        for s in data["top_sectors"]:
            print(f"  {s['count']:>5}  {s['sector']}")

    # Page through for the country breakdown, which the server does not
    # pre-compute for us.
    victims, offset = list(data.get("items", [])), PAGE
    while len(victims) < min(args.limit, total):
        page = fetch(f"/threat-actors/by-name/{quoted}/victims",
                     limit=PAGE, offset=offset)
        items = page.get("items", [])
        if not items:
            break
        victims.extend(items)
        offset += PAGE

    countries = collections.Counter(v["country"] for v in victims if v.get("country"))
    if countries:
        print(f"\nCountries (of the {len(victims)} most recent claims)")
        for name, n in countries.most_common(10):
            print(f"  {n:>5}  {name}")

    print("\nMost recent claims")
    for v in victims[:10]:
        when = (v.get("attack_date") or "—")[:10]
        print(f"  {when}  {v.get('name')}")

    print("\nEvery line above is a claim published by the group itself.")


if __name__ == "__main__":
    main()
