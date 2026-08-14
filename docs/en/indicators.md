# Indicators — what to block and hunt for

[← Documentation index](README.md) · [🇧🇷 Português](../pt/indicators.md)

This group is the operational half of the platform: the data you feed to a firewall, a SIEM
or a threat hunt.

---

## `/check` — IP / IOC reputation check

**[ctiwatch.com/check](https://ctiwatch.com/check)**

Paste an **IP address, domain or file hash** and get an answer checked against 1.7M+
indicators from honeypots, blocklists and OSINT feeds. Free, no signup, no form.

### How to use it

This is the fastest useful thing on the platform. An address shows up in your logs at
02:00 — paste it, get context in seconds.

You get:

- whether the indicator is known, and from which sources;
- its **confidence score** and when it was last seen;
- an **Analyst Summary** in plain language, explaining what the indicator is associated with;
- links to related actors, campaigns and CVEs where they exist.

Each check has its own URL (`/check/1.2.3.4`), so you can paste the link straight into a
ticket or a chat and the person opening it sees the same result.

### 💡 Practical tip

**Read the "last seen" date before you act.** A hit is not automatically a verdict. An IP
last seen in a scanning campaign eleven months ago is probably not the same tenant today —
cloud address space recycles fast. A hit from this week is worth acting on; a hit from last
year is worth investigating, not blocking.

---

## `/iocs` — Indicator database

**[ctiwatch.com/iocs](https://ctiwatch.com/iocs)**

The full corpus: **1,737,420** indicators of compromise — IPs, domains, URLs and file
hashes — with type, source, first and last seen, and confidence.

### How to use it

Filter by **type**, **source** and **confidence**, then export. Typical uses are building a
blocklist, seeding a hunt, or enriching data you already have.

Via the API:

```bash
# High-confidence IPs, as CSV
curl -H "X-API-Key: $CTIWATCH_KEY" \
  "https://ctiwatch.com/api/v1/iocs/export/csv?type=ip&min_confidence=80"
```

### Understanding `confidence_score`

The score is **not** copied from the source. It is computed, and it combines three things:

| Component | Meaning |
|---|---|
| **Source reliability** | A honeypot that saw the attack itself outranks a bulk aggregated list. |
| **Raw signal** | What the source itself asserted, where it asserts anything. |
| **Recency decay** | The score falls as the observation ages. |

The consequence worth remembering: **the same indicator scores lower over time without
anything new happening**. That is intentional. If you cache indicators locally, refresh them
— a list exported six months ago has drifted from what the platform would tell you today.

### ⚠️ Know this

Roughly three quarters of the corpus arrives from bulk phishing and blocklist feeds that
publish no confidence of their own. These are useful in volume and weak individually. If
you are going to block automatically rather than alert, filter on confidence.

---

## `/honeypot` — Our own sensor telemetry

**[ctiwatch.com/honeypot](https://ctiwatch.com/honeypot)**

Attacker activity captured **first-hand** by CTIWatch sensors — a dedicated T-Pot
deployment — rather than collected from someone else's feed.

### How to use it

Use it when you want to know what is being attacked **right now**, at internet scale, with
no publication delay. Because the sensors are ours, there is no lag between an attacker
touching them and the data appearing here.

It is particularly good at three questions:

- Which credentials are being sprayed this week?
- Which ports and services are drawing scanning right now?
- Where is that traffic coming from?

### 💡 Why this page matters more than its size suggests

Everything else on this platform is, ultimately, someone else's observation that we
collected and correlated. This page is *our* observation. When a honeypot indicator and a
third-party feed disagree, the honeypot saw it happen.

---

## `/phishing` — Phishing victimology

**[ctiwatch.com/phishing](https://ctiwatch.com/phishing)**

Which brands are being **impersonated** in active phishing campaigns — extracted from the
platform's own indicator corpus, without depending on any leak site.

### How to use it

Two audiences, two jobs:

- **If your brand is here**, criminals are using your name to defraud your customers. The
  page gives you the hostnames doing it, which is what a takedown request needs.
- **If you defend users**, the brand list is a ranking of what your people are most likely
  to be phished with this month.

### How the classification works — and why it has three classes, not two

Every phishing host is sorted into one of three classes, using **structural evidence in the
URL**, not guesswork:

| Class | Evidence | Meaning |
|---|---|---|
| **Compromised** | The kit sits under a CMS path (`/wp-content/`, `/wp-includes/`) | A real site that was broken into. **This organisation is a victim.** |
| **Attacker infrastructure** | The brand name is in the *hostname* | A domain registered to look like the brand. **This belongs to the criminal.** |
| **Abused platform** | Shared hosting, link shorteners, form builders | Neither victim nor criminal — a service being abused. |

The third class is the largest, and it is the one that matters most for reading the page
correctly. Without it, a hosting provider serving hundreds of phishing pages would appear as
hundreds of "victim organisations" — which would be badly wrong, and would name real
companies as breached when they were not.

### ⚠️ Know this

Each result carries a **precision tier**, shown in the interface. Read it. The brand list is
curated by hand, which means a brand nobody has added yet will not be detected — the
classification is honest about what it knows, but it cannot know everything, and new brands
appear constantly.
