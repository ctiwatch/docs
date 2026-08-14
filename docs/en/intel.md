# Intel — context and analysis

[← Documentation index](README.md) · [🇧🇷 Português](../pt/intel.md)

The pages in the other three groups tell you *what*. These tell you *what it means*.

---

## `/articles` — Intel feed

**[ctiwatch.com/articles](https://ctiwatch.com/articles)**

Cybersecurity news aggregated from 28 sources — BleepingComputer, Cisco Talos, CISA, Unit
42, Krebs, SANS ISC and others — filtered and tagged by CVE, actor and topic.

### How to use it

Search and filter by **CVE**, **threat actor** or keyword rather than scrolling. The feed's
value is not "read the news"; it is *"show me everything published about CVE-2026-1234"* or
*"what has been written about this group"*, across all sources at once.

Articles are linked to the entities they mention, so an actor page shows the coverage about
that actor without you searching for it.

### ⚠️ Know this

Article-to-entity linking is text matching, and text matching on short names produces false
positives. The platform curates the actor name list specifically to prevent this — a group
whose name is a common English word cannot be matched safely by frequency alone. If a link
looks wrong, it may be; the underlying article is always the authority.

---

## `/reports` — Weekly threat reports

**[ctiwatch.com/reports](https://ctiwatch.com/reports)**

A written report generated every **Monday** from live platform data: ransomware activity,
critical vulnerabilities, threat actor highlights and IOC trends for the week.

### How to use it

This is the page to send to someone who is not going to browse a CTI platform. It is
built for the weekly security meeting, and each report has a permanent URL you can link or
archive.

If you only have time for one page per week, make it this one.

---

## `/geopolitics` — Nation-state and conflict

**[ctiwatch.com/geopolitics](https://ctiwatch.com/geopolitics)**

Nation-state APT activity by country, conflict-zone monitoring (Russia/Ukraine,
China/Taiwan, Iran), ransomware victim heatmaps and sector targeting.

### How to use it

Two honest uses:

- **Regional exposure.** Filter to your country and read what is actually landing there.
  Threat intelligence written for a US audience often does not describe what is hitting
  Brazil, and the difference matters.
- **Conflict awareness.** When a conflict escalates, the associated cyber activity tends to
  broaden beyond the belligerents to their suppliers and allies. This page tracks the
  briefs.

### ⚠️ Know this

Nation-state **attribution is political as well as technical**. Public attributions come
from governments and vendors who each have their own incentives, and they are frequently
contested. Read this page as "who is publicly accused of what", and keep the distinction
between *attributed* and *proven* firmly in mind.

---

## `/markets` — Leak sites and darknet

**[ctiwatch.com/markets](https://ctiwatch.com/markets)**

Active monitoring of darknet markets, ransomware leak sites and cybercrime forums.
Infrastructure is tracked via RansomLook, refreshed every four hours.

### How to use it

This is infrastructure intelligence: **where** these groups publish, and whether that
infrastructure is up. It answers "is this group still operating?" from a different angle
than the victim list — a leak site that has gone dark often precedes a rebrand or a
takedown.

### ⚠️ Know this

The platform monitors that this infrastructure exists and is reachable. It does not
transact, does not purchase, and does not republish stolen data.

---

## `/intelligence` — The correlation graph

**[ctiwatch.com/intelligence](https://ctiwatch.com/intelligence)**

A visual graph correlating indicators, CVEs, actors, campaigns and victims — for finding
relationships that are invisible in a list.

### How to use it

Start from an entity you care about and expand outward one hop at a time. The graph is for
*discovery* — "what else touches this?" — not for inventory. When it surfaces an unexpected
edge, verify it on the entity pages before building anything on it.

### 🔴 Know this — the graph is sparse, and that is the honest state of it

The overwhelming majority of indicators and CVEs in the database have **no edges at all**.
This is not a rendering problem; it reflects reality. Relationships are extracted from
published text, and almost nobody publishes "this IP belongs to this campaign" in a form a
machine can read.

What this means practically: **the graph shows what has been written about, not what is
true.** A well-connected node is a well-*documented* node. An isolated node may be equally
dangerous and simply undocumented. Use the graph to find leads, never to conclude that
something is unconnected.

---

## `/diamond` — Diamond Model of Intrusion Analysis

**[ctiwatch.com/diamond](https://ctiwatch.com/diamond)**

Pick a **sector** and a **country**. The platform builds the Diamond Model — adversary,
capability, infrastructure, victim — around that victimology, from live data.

### How to use it

This is the closest thing on the platform to *"what does the threat look like for me?"*.
Choose your sector and your country, and you get the four vertices populated with the actors
actually hitting organisations like yours, the capabilities linked to them, the
infrastructure involved and the victim pattern.

Use it to brief people who need a threat picture rather than a data feed — it is designed to
be read, not queried.

| | Free | Supporter |
|---|---|---|
| Sectors + countries per pivot | 1 + 1 | 5 + 5 |
| Depth | Top 5 | Top 25 |
| Time window | 12 months | 5 years |
| MITRE ATT&CK techniques | — | ✅ |
| Export | — | ✅ |

All four vertices are present on the free tier. Supporter widens the pivot; it does not
unlock a hidden vertex.

### 💡 Read the coverage panel

The page shows **coverage** for the pivot you selected, and this is deliberate. Ransomware
groups and catalogued malware families are largely *disjoint populations*: most ransomware
operations have no malware family formally linked to them anywhere in public data. Rather
than draw an empty vertex and let you assume there is nothing there, the page states how
much of the picture it can actually fill.

---

## `/ask` — AI analyst

**[ctiwatch.com/ask](https://ctiwatch.com/ask)** · *Supporter feature*

Ask questions in plain language, answered by an AI grounded **only** in live CTIWatch data.

### How to use it

Ask the question you would ask a colleague:

> *"Which ransomware groups have hit Brazilian healthcare in the last six months?"*
>
> *"Is CVE-2026-1234 being exploited, and against whom?"*
>
> *"What do we know about the infrastructure of this group?"*

It is at its best for questions that would otherwise require you to cross three pages and
do the joining yourself.

### ⚠️ Know this

The model answers from platform data, which bounds the damage but does not eliminate it: it
can still misread what it retrieves, and it inherits every limitation described elsewhere in
this documentation — leak-site claims are still claims, sparse graph edges are still sparse.

**For anything you are going to act on, follow the answer back to the underlying page.** The
AI is a fast way to find the right page, not a replacement for reading it.
