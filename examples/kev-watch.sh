#!/usr/bin/env bash
# kev-watch.sh — vulnerabilities that are CONFIRMED exploited (CISA KEV).
#
#   ./kev-watch.sh          # 20 most recent
#   ./kev-watch.sh 50       # 50 most recent
#
# Start your patch queue here: "confirmed exploited" beats "theoretically
# severe" every time. No API key required. Requires: curl, jq
set -euo pipefail

API="https://ctiwatch.com/api/v1"
N="${1:-20}"

# NOTE: the KEV filter is `is_kev`. The published OpenAPI file says `in_kev`,
# which does not exist — and because unknown parameters are silently ignored,
# the wrong name returns the ENTIRE database looking like a success.
resp=$(curl -sS --max-time 30 \
    "$API/vulnerabilities?is_kev=true&sort=published_date&order=desc&limit=$N")

total=$(jq -r '.total' <<<"$resp")

# Guard against the silent-filter trap: if this ever matches the unfiltered
# count, the filter stopped working and every row below is noise.
all=$(curl -sS --max-time 30 "$API/vulnerabilities?limit=1" | jq -r '.total')
if [[ "$total" == "$all" ]]; then
    echo "REFUSING TO CONTINUE: the is_kev filter returned the whole database" >&2
    echo "($total of $all). The parameter is being ignored." >&2
    exit 1
fi

echo "$total CVEs are confirmed exploited, out of $all tracked."
echo

jq -r '.items[] |
  "\(.cve_id)  CVSS \(.cvss_score // "—" | tostring | .[0:4])  \((.description // "")[0:88])"
' <<<"$resp"
