# Your account — make the platform watch for you

[← Documentation index](README.md) · [🇧🇷 Português](../pt/account.md)

Everything described in the other sections requires you to go and look. This section is
about the opposite: configuring the platform so it comes to you.

---

## `/dashboard` — Your starting page

**[ctiwatch.com/dashboard](https://ctiwatch.com/dashboard)**

Global threat intelligence in real time — indicators, CVEs, ransomware and APT activity, in
one view, with your watchlist matches surfaced.

---

## `/watchlists` — The most useful feature on the platform

**[ctiwatch.com/watchlists](https://ctiwatch.com/watchlists)**

Tell the platform which keywords matter to you. When they appear in new data, it tells you.

### What to put in a watchlist

| Category | Examples |
|---|---|
| **Your organisation** | The trade name, the legal name, the old name from before the merger |
| **Your vendors** | The software you actually run — this is how vendor CVEs reach you |
| **Your sector and region** | Enough to catch campaigns aimed at organisations like yours |
| **Your subsidiaries and brands** | Attackers name whichever entity they landed on |

### 🔴 The one mistake everybody makes: short keywords

Keywords are matched **as substrings, without word boundaries**. A short keyword will match
inside longer words and bury you.

A real example from this platform: the keyword **`ANS`** produced 190 false positives in
thirty days, because it matches inside **tr·ANS·fer**, **r·ANS·omware**, and dozens of
ordinary words.

**Rules that keep watchlists useful:**

- Never use a keyword shorter than five characters unless it is genuinely distinctive.
- Prefer the full name over the acronym — `Banco Exemplo` rather than `BEX`.
- If a keyword floods you, do not tolerate it. A watchlist that cries wolf is worse than no
  watchlist, because it trains you to ignore the one that matters.

### 💡 Vendor keywords work harder than you would expect

A vendor name in a watchlist matches CVE descriptions *and* the structured product data,
so putting your actual software vendors in a watchlist is one of the highest-value five
minutes available on this platform. It turns "377,168 CVEs" into "the four that affect
things I run".

---

## `/alerts` — Notification history

**[ctiwatch.com/alerts](https://ctiwatch.com/alerts)**

Every watchlist match, with delivery status. Alerts can also arrive by **email**, and — if
you install the app — as **push notifications**.

Dismissing an alert suppresses the notification. It does not delete the underlying data, and
the event remains visible in the public feed.

---

## `/settings/api-keys` — API keys

**[ctiwatch.com/settings/api-keys](https://ctiwatch.com/settings/api-keys)**

Create, inspect and revoke keys. The free tier allows **100 requests/day per key**.

```bash
curl -H "X-API-Key: $CTIWATCH_KEY" \
     "https://ctiwatch.com/api/v1/victims?country=BR&limit=50"
```

Keys can be given an expiry date and restricted by IP. Use both: a key that expires is a key
that cannot leak forever.

**Rotate a key immediately if it has ever been in a repository, a CI log or a screenshot.**
Revocation takes effect at once.

---

## `/settings/security` — Account security

**[ctiwatch.com/settings/security](https://ctiwatch.com/settings/security)**

- **Two-factor authentication (TOTP)** — supported, and worth enabling.
- **Password and email changes** — an email change requires confirmation on both addresses.
- **Account deletion** — a two-step process requiring your password *and* email
  confirmation. It is deliberately hard to do by accident.

---

## `/settings/billing` — Subscription

**[ctiwatch.com/settings/billing](https://ctiwatch.com/settings/billing)**

Your [Supporter](https://ctiwatch.com/support) subscription and invoices, self-service.
Priced in **BRL** for Portuguese-speaking visitors and **USD** for everyone else.

---

## `/settings/privacy` — Privacy and data

**[ctiwatch.com/settings/privacy](https://ctiwatch.com/settings/privacy)**

What the platform stores about you, and the controls over it.

---

## Install it as an app

CTIWatch is a **progressive web app**. Supporters can install it from the browser and get an
app icon, offline access to pages already visited, and push notifications for watchlist
matches — without going through an app store.

---

## A five-minute setup that pays for itself

1. Create an account.
2. Add a watchlist with **your organisation's full name** and its variants.
3. Add a second watchlist with **the vendors you actually run**.
4. Turn on email alerts.
5. Enable two-factor authentication.

That is the whole configuration. From then on the platform reads 86 sources on your behalf
and only interrupts you when something matches.
