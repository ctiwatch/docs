# Threats — who is attacking

[← Documentation index](README.md) · [🇧🇷 Português](../pt/threats.md)

This group answers the question *"who is behind this, and what have they done?"*

---

## `/threats` — Threat actor directory

**[ctiwatch.com/threats](https://ctiwatch.com/threats)**

A directory of **10,758** threat actors: APT groups, ransomware operations, malware
families and criminal crews. For each one the platform tracks attribution, motivation,
technical capability and operational patterns.

### How to use it

Search by name — including **aliases**. The industry names the same group five different
ways (a group tracked as `TA505` by one vendor is `Hive0065` to another), so every actor
page carries an **"Also Known As"** block. If a name from a report gets you nothing, try the
alias.

Open an actor to get:

- **Intelligence Assessment** — a written profile of the group, generated from the data the
  platform holds about it.
- **Also Known As** — every alias the platform has consolidated.
- **Victims** — [`/threats/<name>/victims`](https://ctiwatch.com/threats), everything
  attributed to that group.

### 💡 Practical tip

The most useful pivot here is not the actor page itself — it is the victim list. If the
group has been hitting hospitals in Latin America for six months and you run a hospital in
Latin America, that is a far stronger signal than any capability description.

### ⚠️ Know this

Actor attribution in public CTI is **noisy**. The same operation appears under different
names, groups rebrand after law-enforcement action, and affiliates of one ransomware
operation often work for three others simultaneously. The platform consolidates aliases
where it can prove they are the same group, and leaves them separate when it cannot.

---

## `/victims` — Ransomware victim tracker

**[ctiwatch.com/victims](https://ctiwatch.com/victims)**

**32,334** organisations listed on ransomware extortion sites, collected from
Ransomware.live, RansomLook and other sources, cross-correlated so the same victim published
by two sources on different days is one record and not two.

### How to use it

Filter by **group**, **country** and **sector**, and sort by date. Three common jobs:

- *"Is my organisation listed?"* — search the name. Also try the shortened trade name and
  the legal name; attackers write whatever they feel like.
- *"Is my sector under pressure right now?"* — filter by sector and look at the last 30
  days against the previous 30.
- *"Who is active in my country?"* — filter by country, and read the group column.

### 🔴 Read this before you use victim data

**These records are claims made by criminals on their own extortion sites.** They are not
confirmed breaches, and treating them as confirmed is the single most common mistake made
with this kind of data.

Attackers routinely:

- list an organisation before negotiation ends, as pressure — and remove it if paid;
- republish data from an older breach as if it were new;
- claim a subsidiary and name the parent company, or the reverse;
- occasionally list victims they never actually compromised.

Records added manually from OSINT carry an explicit **`ALLEGED · UNCONFIRMED`** badge. The
absence of that badge on a scraped record does *not* upgrade it to confirmed — it only means
it came from the group's own site.

If you are about to tell someone their company appears here, say **"a ransomware group has
published a claim naming you"**. That sentence is true. "You were breached" may not be.

---

## `/campaigns` — Active operations

**[ctiwatch.com/campaigns](https://ctiwatch.com/campaigns)**

**112** campaigns currently active. A campaign groups a threat actor's activity into a
period with a shape: who they hit, where, over what window.

Campaigns are built automatically from victim data and threat-actor intelligence, then
cross-correlated with the article feed.

### How to use it

Use it to answer *"is this still happening?"*. An actor profile tells you what a group is
capable of; a campaign tells you whether they are doing it **this month**. When a campaign
matches your sector or region, that is when an actor profile becomes worth reading in full.

### ⚠️ Know this

Campaign boundaries are inferred, not declared. Nobody publishes a start and end date for a
ransomware operation, so the platform infers activity windows from **dated evidence** —
victim publication dates and article mentions. Campaigns marked as active have evidence in
the recent window; the absence of a campaign does not mean the group is dormant, only that
it has not published recently.

---

## `/malware` — Malware families

**[ctiwatch.com/malware](https://ctiwatch.com/malware)**

**3,500+** malware families, imported from [Malpedia](https://malpedia.caad.fkie.fraunhofer.de/)
— Windows, Linux, Android and macOS — with aliases, TTPs and actor attribution where it
exists.

### How to use it

Its main job is **translation**. An incident report names a loader; you need to know what
family it belongs to, who uses it, and what it typically does next. Search the name, read
the family, follow the attribution back to [`/threats`](#threats--threat-actor-directory).

### ⚠️ Know this — the same name means different things

Malware naming collides constantly, and the collisions are dangerous because they look like
matches. Real examples from this database:

- **MEDUSA** is a rootkit here *and* the name of a ransomware operation;
- **Anubis** is an Android banking trojan *and* the name of a ransomware group;
- **Chaos** is a Linux SSH implant *and* a ransomware builder.

Before you conclude "group X uses malware Y because the names match", check that the
behaviour matches too. The platform applies exactly this test internally before linking an
actor to a family.
