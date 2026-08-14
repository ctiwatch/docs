# API reference

[← Documentation index](README.md) · [🇧🇷 Português](../pt/api.md) · [Runnable examples](../../examples/)

Base URL: **`https://ctiwatch.com/api/v1`**

Everything you can see on the website you can also read from the API, and **most of it needs
no authentication at all**. This page documents the endpoints as they actually behave —
every parameter listed here was verified against the live API.

---

## Quick start

```bash
# No key needed. This works right now.
curl https://ctiwatch.com/api/v1/stats
```

```json
{
  "total_iocs": 1737420,
  "total_cves": 377168,
  "total_threat_actors": 10758,
  "active_campaigns": 112,
  "total_victims": 32334,
  "kev_count": 3917,
  "sources_count": 86,
  "last_updated": "2026-08-14T06:00:50.470Z"
}
```

---

## Authentication

Most read endpoints are open. A key is required only for CSV export, the Diamond Model, Ask,
watchlists and worker health.

```bash
curl -H "X-Api-Key: ctw_your_key_here" \
     "https://ctiwatch.com/api/v1/iocs/export/csv?limit=1000"
```

- Header name is **`X-Api-Key`**. Keys look like `ctw_` followed by 64 hex characters.
- Create and revoke keys at [ctiwatch.com/settings/api-keys](https://ctiwatch.com/settings/api-keys).
- Browsers authenticated by session cookie work too — that is how the site itself calls the
  API.

Without credentials, protected endpoints return:

```json
HTTP 401  {"error": "Authentication required"}
```

---

## Conventions

### Response envelope

List endpoints return a total and an array:

```json
{ "total": 32334, "items": [ { … }, { … } ] }
```

`total` is the count **matching your filters**, not the page size. Use it to drive
pagination — and to check that a filter actually did something (see the warning below).

Aggregate endpoints (`/stats/*`, `/victims/stats`, `/honeypot/stats`, `/geopolitics`) return
named objects instead, described per endpoint.

### Pagination

| Parameter | Default | Maximum |
|---|---|---|
| `limit` | 50 | **100** |
| `offset` | 0 | **1000 without a key** — unlimited with one |

⚠️ **A `limit` above 100 is silently clamped, not rejected.** `?limit=5000` returns HTTP 200
with 100 items. If you assume you received 5,000 rows, you will silently process 2% of your
data. Always page with `offset` and stop when `offset >= total`.

**Paging past `offset=1000` requires an account.** Deeper requests without a key answer:

```json
HTTP 403  {"code": "ACCOUNT_REQUIRED", "max_anonymous_offset": 1000}
```

This one is not a trap — it is loud, and it tells you exactly what to do. The line is drawn
between *reading* and *collecting in bulk*: querying, testing and browsing stay open to
everyone with no signup, while bulk collection needs a free account so the traffic has a name
attached to it. A [free key](https://ctiwatch.com/register) removes the limit entirely.

### 🔴 Unknown parameters are silently ignored

This is the single most important thing to know about this API. A misspelled or unsupported
filter does **not** produce an error — it is dropped, and you get the unfiltered result with
HTTP 200.

```bash
# Wrong parameter name — looks successful, filters nothing
curl "…/vulnerabilities?in_kev=true&limit=1"   # total: 359241  ← whole database

# Correct parameter name
curl "…/vulnerabilities?is_kev=true&limit=1"   # total: 3913    ← actually KEV
```

**Verify every new filter by watching `total` change.** If `total` is identical with and
without your filter, the filter is not being applied.

### Errors

| Status | Body | Meaning |
|---|---|---|
| `400` | `{"error":"value is required"}` | Missing required parameter |
| `400` | `{"error":"Invalid id"}` | Malformed identifier |
| `401` | `{"error":"Authentication required"}` | Endpoint needs a key |
| `403` | `{"code":"ACCOUNT_REQUIRED"}` | Paging past `offset=1000` without a key |
| `404` | `{"error":"Not found"}` | No such record |
| `429` | `{"code":"RATE_LIMIT"}` | Daily **request** cap reached |
| `429` | `{"code":"ROW_QUOTA"}` | Daily **row** cap reached |

Read the `code` field, not the prose: the messages may be reworded, the codes will not.

### Rate limits

Read them from the response headers rather than hard-coding them:

```
ratelimit-limit: 600          # requests per 60s window, per IP
ratelimit-remaining: 579
ratelimit-reset: 46           # seconds until the window resets
x-ratelimit-limit: 150        # your scope's limit
x-ratelimit-scope: anonymous  # anonymous | api key | session
```

Key traffic is metered two ways, and **rows** is usually the one you will meet first:

| | Free | Supporter |
|---|---|---|
| Requests / day | 100 | 10,000 |
| **Rows / day** | **25,000** | **200,000** |

```
x-rowquota-limit: 25000
x-rowquota-remaining: 24890
```

Counting rows rather than requests exists because requests alone measure nothing: one CSV
export returns 5,000 rows and costs a single request. Both are anti-abuse ceilings, not sales
levers — if you have a legitimate use that needs more, ask and it gets raised.

---

## Endpoints

### Platform

| Endpoint | Returns |
|---|---|
| `GET /stats` | Headline counters |
| `GET /stats/breakdown` | `severity_distribution`, `ioc_types`, `exploit_distribution`, `recent_cves` |
| `GET /stats/geo` | Victims and actors by geography, plus timeline |
| `GET /stats/timeline` | `ioc_velocity`, `cve_monthly`, `attack_weekly` |
| `GET /health` | API, database, ingestion and feed status |
| `GET /sources` | All 86 collection sources with their last fetch time |
| `GET /whoami` | The IP the API sees you as |

### Search

```
GET /search?q=lockbit&types=ioc,vuln,actor,victim&limit=20
```

| Parameter | Notes |
|---|---|
| `q` | Required |
| `types` | Comma-separated: `ioc`, `vuln`, `actor`, `victim`. Omit for all |
| `limit` | Default 50, max 100 |

Returns `{ "query": …, "results": { … } }` grouped by entity type.

### Indicators

```
GET /iocs
```

| Parameter | Values |
|---|---|
| `type` | `ip`, `domain`, `url`, `hash_md5`, `hash_sha1`, `hash_sha256`, `email`, `cve` |
| `confidence_min` | Integer 0–100 |
| `active_only` | `true` |
| `sort` | Any sortable field; `confidence_score` and `confidence` both map to the computed score |
| `order` | `asc`, `desc` (default `desc`) |
| `limit`, `offset` | Standard pagination |

⚠️ The published OpenAPI file lists `severity` and `source` for this endpoint. **Neither is
implemented** — both are silently ignored. Use `confidence_min` instead of `severity`.

```
GET /iocs/lookup?value=1.2.3.4     ← the parameter is `value`, not `q`
GET /iocs/{id}
GET /check/{value}                 ← the same lookup behind the /check page
GET /iocs/export/csv?limit=…      ← 🔑 login required; accepts ONLY limit (max 5000)
```

`/check/{value}` returns `{ "found": bool, "value": … }` and is the friendliest of the three
for a single indicator.

### Vulnerabilities

```
GET /vulnerabilities
```

| Parameter | Values | Verified effect |
|---|---|---|
| `is_kev` | `true`, `false` | `true` → 3,913 of 359,241 |
| `severity` | `CRITICAL`, `HIGH`, `MEDIUM`, `LOW` | case-insensitive input, upper-cased internally |
| `cvss_min` | Float | `9` → 50,863 |
| `exploit_status` | e.g. `weaponized` | `weaponized` → 42 |
| `published_after` | ISO date | |
| `include_rejected` | `true` to include rejected CVEs (excluded by default) | |

⚠️ The OpenAPI file documents `in_kev` and `search` for this endpoint. **Neither exists.**
The KEV filter is `is_kev`; there is no free-text search here — use `/search` instead.

```
GET /vulnerabilities/{cve_id}           e.g. /vulnerabilities/CVE-2026-1234
GET /vulnerabilities/{cve_id}/related
GET /vulnerabilities/vendors            ← the vendor index
GET /vulnerabilities/vendor/{vendor}    ← CVEs for one vendor
```

### Threat actors

```
GET /threat-actors
```

| Parameter | Values | Verified effect |
|---|---|---|
| `source` | `ransomware`, `apt`, `malware` | `ransomware` → 475 of 10,758 |
| `country` | ISO code, e.g. `RU` | `RU` → 81 |
| `search` | Free text over name and description | `lockbit` → 48 |
| `motivation`, `sophistication`, `platform`, `active_after` | | |

```
GET /threat-actors/{id}
GET /threat-actors/by-name/{name}            ← lookup by name, case-insensitive
GET /threat-actors/by-name/{name}/victims    ← victims + top_sectors for that group
GET /threat-actors/platform-counts
```

💡 `by-name` is usually what you want. Actor names are what appear in reports; UUIDs are not.

### Victims

```
GET /victims
```

| Parameter | Matching | Verified effect |
|---|---|---|
| `country` | exact, case-insensitive | `BR` → 532 |
| `sector` | exact, case-insensitive | `Healthcare` → 1,692 |
| `group` | **substring** | `lockbit` → 3,275 |
| `source` | `ransomware.live`, `ransomlook` | |

#### 🔴 Counting one group's victims is the trap on this endpoint

Neither obvious approach is correct on its own, and both fail *silently*:

| Approach | LockBit result | Failure mode |
|---|---|---|
| `/victims?group=lockbit` | **3,275** | Substring — `group=play` also matches `playboy` |
| `/threat-actors/by-name/lockbit/victims` | **5** | Exact — misses every versioned tag |

The cause is that **leak-site group tags carry version numbers**. LockBit's footprint is
spread across `lockbit`, `lockbit2` (915), `lockbit3` (1,982) and `lockbit5` — so the exact
match returns 5 claims and under-reports by 99.8%, with no error and no warning.

**Look at the real tags before you count.** `GET /victims/stats` returns `by_group` with the
exact tag strings and their counts:

```bash
curl -s https://ctiwatch.com/api/v1/victims/stats \
  | jq -r '.by_group[] | select(.group_name | test("lockbit"; "i")) | "\(.count)\t\(.group_name)"'
```

Then decide deliberately: substring for the group's whole footprint, exact tags when you need
precision. [`examples/actor-report.py`](../../examples/actor-report.py) does this cross-check
automatically and warns you when the two numbers disagree.

```
GET /victims/{id}
GET /victims/stats     ← by_source, by_group, by_sector, by_country
```

### Campaigns

```
GET /campaigns?active=true
```

| Parameter | Values | Verified effect |
|---|---|---|
| `active` | `true` | `true` → 112 of 652 |
| `type` | `ransomware`, `apt` | |
| `impact` | impact level | |

⚠️ The OpenAPI file documents `status=active|inactive|all`. **It does not work** — the
parameter is `active=true`.

```
GET /campaigns/{id}
```

### Intel and analysis

| Endpoint | Parameters |
|---|---|
| `GET /articles` | `source`, `has_cves=true`, `priority=high\|medium`, `search`, `tag` |
| `GET /articles/sources` | — |
| `GET /geopolitics` | actors by country, victims by country, sector targeting |
| `GET /geopolitics/conflict-zones` | — |
| `GET /geopolitics/country/{code}` | — |
| `GET /markets` | Leak sites and market infrastructure |
| `GET /honeypot/stats` | `totals`, `top_countries`, `top_ports`, `top_asns`, `recent_attackers` |
| `GET /correlations/entity/{type}/{id}` | Graph edges for one entity |
| `GET /correlations/stats`, `GET /correlations/feed` | — |
| `GET /alerts`, `GET /alerts/summary` | Public alert feed |
| `GET /stream/feed` | Server-sent events, live |

### Phishing

```
GET /phishing/brands            impersonated brands, ranked
GET /phishing/hosts?class=…     hosts, by classification
GET /phishing/kits              campaigns by kit fingerprint
```

🔴 The `class` values are **`compromised_site`**, **`attacker_infra`** and
**`abused_platform`**. An unrecognised value does not error — it silently falls back to
`compromised_site`, so `class=infrastructure` returns compromised sites while looking like it
worked. Check the `class` field echoed in the response; it tells you what you actually got.

Current totals, returned in every response as `totals`:

| Class | Hosts | URLs |
|---|---|---|
| `abused_platform` | 120,791 | 191,987 |
| `attacker_infra` | 13,551 | 23,391 |
| `compromised_site` | 12,639 | 35,831 |

See [Indicators → Phishing](indicators.md#phishing--phishing-victimology) for what these
classes mean and why the third one exists.

### Supporter endpoints 🔑

| Endpoint | Requires |
|---|---|
| `GET /diamond?sector=…&country=…` | Authentication |
| `GET /diamond/options` | Authentication |
| `POST /ask` | Authentication **+ Supporter plan** |
| `GET /watchlists`, `POST /watchlists` | Authentication |
| `GET /workers/health` | Authentication |
| `GET /iocs/export/csv` | Authentication |

Note that `/ask` is **POST**, not GET — a GET returns 404.

---

## Recipes

Runnable versions of all of these live in [`examples/`](../../examples/).

### Today's KEV additions

```bash
curl -s "https://ctiwatch.com/api/v1/vulnerabilities?is_kev=true&sort=published_date&limit=10" \
  | jq -r '.items[] | "\(.cve_id)  CVSS \(.cvss_score)  \(.description[0:70])"'
```

### Is this indicator known?

```bash
curl -s "https://ctiwatch.com/api/v1/check/45.155.205.233" | jq '{found, value}'
```

### Build a high-confidence IP blocklist

The CSV endpoint is the wrong tool for this, and it is worth knowing why:

```bash
# Accepts ONLY `limit` (max 5,000). type= and confidence filters are IGNORED —
# you get the most recent indicators of every type.
curl -s -H "X-Api-Key: $CTIWATCH_KEY" \
  "https://ctiwatch.com/api/v1/iocs/export/csv?limit=5000" > all-recent.csv
```

For a filtered blocklist, page the JSON endpoint — see
[`examples/blocklist.py`](../../examples/blocklist.py), which handles the 100-row cap
correctly and needs no key at all.

### Who is hitting my sector, in my country?

```bash
curl -s "https://ctiwatch.com/api/v1/victims?country=BR&sector=Healthcare&limit=100" \
  | jq -r '.items[] | "\(.attack_date[0:10])  \(.metadata.group)  \(.name)"'
```

### Everything one group has claimed

```bash
curl -s "https://ctiwatch.com/api/v1/threat-actors/by-name/LockBit/victims?limit=100" \
  | jq '{total, top_sectors, first: .items[0].name}'
```

---

## Two habits that will save you

**1. Watch `total`, not just HTTP 200.** Because unknown parameters are dropped silently, a
successful response is not evidence that your filter worked. Compare `total` with and
without the filter the first time you use it.

**2. Re-fetch rather than cache indefinitely.** Confidence scores decay with age, and
indicators are deactivated as they go stale. A list you exported months ago no longer
reflects what the platform would tell you today.

---

## A note on the OpenAPI file

`openapi.json` is currently **out of date** in several places, all of them documented above:
`/iocs/lookup` takes `value` and not `q`; the KEV filter is `is_kev` and not `in_kev`;
`/campaigns` filters on `active` and not `status`; `search` on `/vulnerabilities` and
`severity`/`source` on `/iocs` do not exist; and the file describes 13 endpoints where the
API serves roughly fifty.

**This page reflects the live API, which was verified endpoint by endpoint.** Where the two
disagree, trust this page — and expect the spec file to be corrected.
