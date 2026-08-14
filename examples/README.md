# Runnable examples · Exemplos executáveis

[← Documentation](../README.md) · [API reference](../docs/en/api.md) · [Referência da API](../docs/pt/api.md)

Every script here was **executed against the live API before being published**. No API key is
required for any of them.

Cada script aqui foi **executado contra a API ao vivo antes de ser publicado**. Nenhum deles
exige chave de API.

| Script | What it does · O que faz | Needs |
|---|---|---|
| [`check-ioc.sh`](check-ioc.sh) | Is this IP / domain / hash known? · Esse IP / domínio / hash é conhecido? | curl, jq |
| [`kev-watch.sh`](kev-watch.sh) | CVEs confirmed exploited, newest first · CVEs com exploração confirmada | curl, jq |
| [`blocklist.py`](blocklist.py) | High-confidence blocklist, paginated correctly · Lista de bloqueio paginada | python3 |
| [`sector-watch.py`](sector-watch.py) | Pressure on your sector and country · Pressão sobre seu setor e país | python3 |
| [`actor-report.py`](actor-report.py) | Full briefing on one group · Dossiê de um grupo | python3 |

The Python scripts use the **standard library only** — no `pip install`.
Os scripts Python usam **só a biblioteca padrão** — sem `pip install`.

---

## Try them · Experimente

```bash
chmod +x *.sh *.py

./check-ioc.sh 45.155.205.233
./kev-watch.sh 10
./blocklist.py --min-confidence 90 --limit 500 > blocklist.txt
./sector-watch.py --country BR --sector Healthcare
./actor-report.py LockBit
```

---

## Each one teaches a trap · Cada um ensina uma armadilha

These are not just snippets. Each was written around a way this API will mislead you if you
call it naively — and every trap below was hit for real while writing them.

Não são só trechos de código. Cada um foi escrito em torno de um jeito pelo qual esta API te
engana se você a chamar ingenuamente — e toda armadilha abaixo foi encontrada de verdade
durante a escrita.

**`kev-watch.sh` — the silently ignored filter.** The published spec says the KEV filter is
`in_kev`; it is actually `is_kev`. Unknown parameters are dropped without an error, so the
wrong name returns all 359,241 CVEs looking like a success. The script refuses to print
anything if the filtered count equals the unfiltered count.

*O spec publicado diz que o filtro de KEV é `in_kev`; ele é `is_kev`. Parâmetro desconhecido é
descartado sem erro, então o nome errado devolve as 359.241 CVEs parecendo sucesso. O script
se recusa a imprimir se a contagem filtrada for igual à não filtrada.*

**`blocklist.py` — the silently clamped page.** `limit` is capped at 100 and the API does not
say so. Asking for 5,000 returns 100 rows with HTTP 200. The script pages with `offset` and
stops at `total`.

*O `limit` é limitado a 100 e a API não avisa. Pedir 5.000 devolve 100 linhas com HTTP 200. O
script pagina com `offset` e para no `total`.*

**`actor-report.py` — versioned group tags.** `by-name/lockbit/victims` returns **5** claims;
the group's real footprint is **3,275**, spread across `lockbit2`, `lockbit3` and `lockbit5`.
Exact matching under-reports by 99.8% without a warning. The script cross-checks both methods
and tells you when they disagree.

*O `by-name/lockbit/victims` devolve **5**; a presença real do grupo é **3.275**, espalhada
entre `lockbit2`, `lockbit3` e `lockbit5`. O casamento exato subconta 99,8% sem avisar. O
script confere os dois métodos e avisa quando discordam.*

**`sector-watch.py` — percentages off a tiny base.** Going from 1 claim to 4 is "+300%", which
looks like a trend and is arithmetic. The script refuses to print a percentage when the
comparison base is under 5.

*Ir de 1 alegação para 4 é "+300%", o que parece tendência e é aritmética. O script se recusa a
imprimir porcentagem quando a base de comparação é menor que 5.*

**`check-ioc.sh` — absence is not innocence.** A miss means no source we collect has reported
that indicator. The script says so instead of printing a reassuring "clean".

*Não achar significa que nenhuma fonte que coletamos reportou aquele indicador. O script diz
isso, em vez de imprimir um tranquilizador "limpo".*
