# Vulnerabilities — what to patch first

[← Documentation index](README.md) · [🇧🇷 Português](../pt/vulnerabilities.md)

**377,168** CVEs, of which **3,917** are in CISA's Known Exploited Vulnerabilities catalog.

The point of this section is not to list vulnerabilities — anyone can do that. It is to
help you decide **which handful of them to fix this week**.

---

## `/vulnerabilities` — CVE database

**[ctiwatch.com/vulnerabilities](https://ctiwatch.com/vulnerabilities)**

### How to use it

Filter and sort by the three signals that actually predict risk, which are not the same
thing:

| Signal | What it tells you | What it does *not* tell you |
|---|---|---|
| **CVSS** | How bad it would be if exploited | Whether anyone is exploiting it |
| **EPSS** | Probability it will be exploited in the next 30 days | Whether it is being exploited *now* |
| **CISA KEV** | It **is** being exploited, confirmed | How bad it is for *you* |

**The practical recipe:** start with KEV. If a vulnerability is in KEV and you run the
affected product, it goes to the top of the list regardless of its CVSS score — "confirmed
exploited" beats "theoretically severe" every time. Then use EPSS to rank what is left, and
CVSS to break ties.

A CVSS 9.8 that nobody has ever exploited and a CVSS 7.5 that is in KEV are not a close
call. Patch the 7.5.

### The CVE detail page

Open any CVE (`/vulnerabilities/CVE-2026-XXXX`) to get:

- the **official description** from NVD;
- a **written narrative** explaining the vulnerability and its weakness class in plain
  language;
- **mentioned vendors**, extracted from the description;
- **Organizations Hit via This CVE** — victims the platform can link to exploitation of this
  specific vulnerability. This is the section that turns an abstract score into "this is
  being used against companies like mine".

---

## `/vulnerabilities/vendor` — Browse by vendor

**[ctiwatch.com/vulnerabilities/vendor](https://ctiwatch.com/vulnerabilities/vendor)**

The same database, entered from the other side: **1,400+ vendors**, each with its CVEs,
scores, KEV status and exploitation intelligence.

### How to use it

This is the page to use when you are working from an asset inventory rather than from the
news. You do not care about "all critical CVEs this week" — you care about the twelve
products you actually run.

Pick your vendors, and check them on a schedule. Better still, put those vendor names in a
[watchlist](account.md#watchlists--the-most-useful-feature-on-the-platform) and let the platform tell you.

### 💡 Practical tip

Vendor names in CVE data are messy — the same company appears as `microsoft`,
`microsoft_corporation` and inside product strings. The vendor index resolves this from the
structured CPE data rather than from free text, so searching the vendor here is more
reliable than searching the vendor name in the CVE list.

---

## Putting it together — a weekly routine

A vulnerability workflow that uses this section well takes about fifteen minutes:

1. **KEV first.** Filter for CISA KEV, sorted by date added. Anything new that you run is
   this week's work.
2. **Your vendors.** Check the vendor pages for the products in your inventory — or read
   the watchlist alerts that did it for you.
3. **Check the victims.** On anything you are unsure about, open the CVE and look at
   *Organizations Hit via This CVE*. If organisations in your sector are on that list, the
   decision makes itself.

### ⚠️ Know this

Coverage of exploitation evidence is uneven, and this cuts one way: **the absence of linked
victims is not evidence that a CVE is not being exploited.** Linking a breach to a specific
CVE requires someone to publish that connection, and most breaches never get that level of
public detail. Use victim links as positive evidence, never as an all-clear.
