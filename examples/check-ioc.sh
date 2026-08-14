#!/usr/bin/env bash
# check-ioc.sh — is this IP / domain / hash known to CTIWatch?
#
#   ./check-ioc.sh 45.155.205.233
#   ./check-ioc.sh evil-domain.tld
#
# No API key required. Requires: curl, jq
set -euo pipefail

API="https://ctiwatch.com/api/v1"
VALUE="${1:-}"

if [[ -z "$VALUE" ]]; then
    echo "usage: $0 <ip|domain|url|hash>" >&2
    exit 64
fi

resp=$(curl -sS --max-time 30 "$API/check/$(printf %s "$VALUE" | jq -sRr @uri)")

if [[ "$(jq -r '.found' <<<"$resp")" != "true" ]]; then
    echo "NOT FOUND   $VALUE"
    echo
    echo "Not being in the corpus is not a clean bill of health — it means"
    echo "no source we collect has reported it. Absence of evidence only."
    exit 1
fi

jq -r '
  "FOUND       \(.value)",
  "type        \(.type // "—")",
  "confidence  \(.confidence_score // "—")",
  "first seen  \(.first_seen // "—")",
  "last seen   \(.last_seen  // "—")",
  "sources     \((.tags // []) | join(", "))"
' <<<"$resp"

echo
echo "Read the 'last seen' date before acting: an indicator last seen"
echo "many months ago is often someone else's address today."
