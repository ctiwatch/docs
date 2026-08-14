# CTIWatch Documentation

[← Back to index](../../README.md) · [🇧🇷 Português](../pt/README.md)

This documentation explains **what every page of the platform does and how to use it**.

If you have never used CTIWatch, start with [Getting started](#getting-started) below and
then read [Indicators](indicators.md) — the reputation check is the fastest way to get
something useful out of the platform in under a minute.

---

## The map

The platform is organised into four groups, which are the four menus in the top navigation.

### 🎯 [Threats](threats.md) — *who is attacking*

| Page | What it answers |
|---|---|
| [`/threats`](threats.md#threats--threat-actor-directory) | Who is this group? What are they known for? |
| [`/victims`](threats.md#victims--ransomware-victim-tracker) | Who has been hit, by whom, when? |
| [`/campaigns`](threats.md#campaigns--active-operations) | What operations are running right now? |
| [`/malware`](threats.md#malware--malware-families) | What is this malware family? |

### 🔍 [Indicators](indicators.md) — *what to block and hunt for*

| Page | What it answers |
|---|---|
| [`/check`](indicators.md#check--ip--ioc-reputation-check) | Is this IP / domain / hash dangerous? |
| [`/iocs`](indicators.md#iocs--indicator-database) | Give me indicators matching these criteria. |
| [`/honeypot`](indicators.md#honeypot--our-own-sensor-telemetry) | What is attacking our sensors right now? |
| [`/phishing`](indicators.md#phishing--phishing-victimology) | Which brands are being impersonated? |

### 🛡️ [Vulnerabilities](vulnerabilities.md) — *what to patch first*

| Page | What it answers |
|---|---|
| [`/vulnerabilities`](vulnerabilities.md#vulnerabilities--cve-database) | Which CVEs matter, and how urgently? |
| [`/vulnerabilities/vendor`](vulnerabilities.md#vulnerabilitiesvendor--browse-by-vendor) | What is exposed in the products I run? |

### 🧠 [Intel](intel.md) — *context and analysis*

| Page | What it answers |
|---|---|
| [`/articles`](intel.md#articles--intel-feed) | What happened in security this week? |
| [`/reports`](intel.md#reports--weekly-threat-reports) | Give me the week in one document. |
| [`/geopolitics`](intel.md#geopolitics--nation-state-and-conflict) | Which nation-state activity affects my region? |
| [`/markets`](intel.md#markets--leak-sites-and-darknet) | Where do these groups publish? |
| [`/intelligence`](intel.md#intelligence--the-correlation-graph) | How are these entities connected? |
| [`/diamond`](intel.md#diamond--diamond-model-of-intrusion-analysis) | What does the threat look like for *my* sector and country? |
| [`/ask`](intel.md#ask--ai-analyst) | Just answer my question in plain language. |

### ⚙️ [Your account](account.md) — *make it watch for you*

Dashboard, watchlists, alerts, API keys and settings — how to stop visiting the site and
let it come to you instead.

---

## Getting started

### You do not need an account

Every page listed above is readable without signing up, and there is no data paywall.
Try [ctiwatch.com/check](https://ctiwatch.com/check) with any suspicious IP address right
now — no form, no email.

### What an account adds

An account exists so the platform can do things **for** you rather than just show you
things:

- **[Watchlists](account.md#watchlists--the-most-useful-feature-on-the-platform)** — tell it what you care about (your company name,
  your vendors, your sector) and it notifies you when that appears in new data.
- **[Alerts](account.md#alerts--notification-history)** — the notification history, with email delivery.
- **[API keys](account.md#settingsapi-keys--api-keys)** — programmatic access, 100 requests/day on the free
  tier.

### What Supporter adds

The [Supporter plan](https://ctiwatch.com/support) is how the project pays for servers,
feeds and AI enrichment. It unlocks convenience and depth — a larger API quota, the
[AI analyst](intel.md#ask--ai-analyst), deeper [Diamond Model](intel.md#diamond--diamond-model-of-intrusion-analysis)
pivots, exports, and push notifications.

**It never unlocks data that anonymous visitors cannot see.** That is a deliberate design
decision, not an oversight: threat intelligence that only paying people can read protects
fewer people.

---

## Reading this data responsibly

Three things are worth internalising before you act on anything you find here.

**1. Leak-site data is a claim, not a confirmation.** Ransomware victim records are scraped
from the criminal groups' own extortion sites. Attackers inflate numbers, republish old
breaches and sometimes list organisations they never touched. Treat every victim record as
*"this group claims X"*.

**2. Old indicators are weak indicators.** An IP address that was a command-and-control
server eight months ago is very likely someone's ordinary web host today. This is why every
indicator carries a confidence score weighted by recency — use it, and be careful about
blocking on age-decayed indicators.

**3. Absence of evidence is not evidence of absence.** If an actor has no malware families
linked, it usually means nobody has published that mapping in a machine-readable form — not
that the group has no tooling. The [Diamond Model](intel.md#diamond--diamond-model-of-intrusion-analysis)
page shows coverage explicitly for exactly this reason.

---

## The API

Everything visible on the site is available programmatically. There are 13 public
endpoints, base URL `https://ctiwatch.com/api/v1/`:

```bash
# Platform-wide counters — no authentication needed
curl https://ctiwatch.com/api/v1/stats

# Look up a single indicator
curl "https://ctiwatch.com/api/v1/iocs/lookup?value=1.2.3.4"

# With an API key
curl -H "X-API-Key: $CTIWATCH_KEY" \
     "https://ctiwatch.com/api/v1/vulnerabilities?is_in_kev=true&limit=20"
```

| Endpoint | Purpose |
|---|---|
| `/stats` | Platform counters |
| `/search` | Cross-entity search |
| `/iocs`, `/iocs/{id}`, `/iocs/lookup`, `/iocs/export/csv` | Indicators |
| `/vulnerabilities`, `/vulnerabilities/{cve_id}` | CVEs |
| `/threat-actors`, `/threat-actors/{id}` | Actors |
| `/victims` | Ransomware victims |
| `/campaigns` | Campaigns |
| `/watchlists` | Your watchlists (authenticated) |

Keys are created at [Settings → API Keys](https://ctiwatch.com/settings/api-keys). The free
tier allows 100 requests/day per key.

*A dedicated API reference is the next document planned for this repository.*
