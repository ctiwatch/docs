# Referência da API

[← Índice da documentação](README.md) · [🇬🇧 English](../en/api.md) · [Exemplos executáveis](../../examples/)

URL base: **`https://ctiwatch.com/api/v1`**

Tudo que você vê no site também dá para ler pela API, e **a maior parte não exige
autenticação nenhuma**. Esta página documenta os endpoints como eles realmente se comportam
— cada parâmetro listado aqui foi verificado contra a API ao vivo.

---

## Comece por aqui

```bash
# Sem chave. Isto funciona agora.
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

## Autenticação

A maioria dos endpoints de leitura é aberta. A chave só é necessária para exportação CSV,
Diamond Model, Ask, watchlists e saúde dos workers.

```bash
curl -H "X-Api-Key: ctw_sua_chave_aqui" \
     "https://ctiwatch.com/api/v1/iocs/export/csv?limit=1000"
```

- O nome do cabeçalho é **`X-Api-Key`**. As chaves têm o formato `ctw_` seguido de 64
  caracteres hexadecimais.
- Crie e revogue chaves em [ctiwatch.com/settings/api-keys](https://ctiwatch.com/settings/api-keys).
- Navegador autenticado por cookie de sessão também funciona — é assim que o próprio site
  chama a API.

Sem credencial, os endpoints protegidos respondem:

```json
HTTP 401  {"error": "Authentication required"}
```

---

## Convenções

### Envelope da resposta

Os endpoints de listagem devolvem um total e um vetor:

```json
{ "total": 32334, "items": [ { … }, { … } ] }
```

O `total` é a contagem **que casa com os seus filtros**, não o tamanho da página. Use para
paginar — e para conferir se o filtro realmente fez alguma coisa (veja o aviso abaixo).

Endpoints agregados (`/stats/*`, `/victims/stats`, `/honeypot/stats`, `/geopolitics`)
devolvem objetos nomeados, descritos endpoint a endpoint.

### Paginação

| Parâmetro | Padrão | Máximo |
|---|---|---|
| `limit` | 50 | **100** |
| `offset` | 0 | — |

⚠️ **`limit` acima de 100 é silenciosamente truncado, não recusado.** `?limit=5000` devolve
HTTP 200 com 100 itens. Se você supuser que recebeu 5.000 linhas, vai processar 2% dos seus
dados sem perceber. Sempre pagine com `offset` e pare quando `offset >= total`.

### 🔴 Parâmetro desconhecido é ignorado em silêncio

Esta é a coisa mais importante a saber sobre esta API. Um filtro com nome errado ou não
suportado **não** dá erro — ele é descartado, e você recebe o resultado sem filtro, com
HTTP 200.

```bash
# Nome errado — parece sucesso, não filtra nada
curl "…/vulnerabilities?in_kev=true&limit=1"   # total: 359241  ← a base inteira

# Nome certo
curl "…/vulnerabilities?is_kev=true&limit=1"   # total: 3913    ← KEV de verdade
```

**Confirme todo filtro novo vendo o `total` mudar.** Se o `total` é idêntico com e sem o seu
filtro, o filtro não está sendo aplicado.

### Erros

| Status | Corpo | Significado |
|---|---|---|
| `400` | `{"error":"value is required"}` | Falta parâmetro obrigatório |
| `400` | `{"error":"Invalid id"}` | Identificador malformado |
| `401` | `{"error":"Authentication required"}` | Endpoint exige chave |
| `404` | `{"error":"Not found"}` | Registro inexistente |

### Limites de requisição

Leia dos cabeçalhos da resposta, em vez de fixar no código:

```
ratelimit-limit: 600          # requisições por janela de 60s, por IP
ratelimit-remaining: 579
ratelimit-reset: 46           # segundos até a janela reiniciar
x-ratelimit-limit: 150        # o limite do seu escopo
x-ratelimit-scope: anonymous  # anonymous | chave de API | sessão
```

Chaves de API no plano gratuito têm ainda um teto de **100 requisições/dia**. É um limite
antiabuso, não uma alavanca comercial — se você tem um uso legítimo que precisa de mais,
peça.

---

## Endpoints

### Plataforma

| Endpoint | Devolve |
|---|---|
| `GET /stats` | Contadores principais |
| `GET /stats/breakdown` | `severity_distribution`, `ioc_types`, `exploit_distribution`, `recent_cves` |
| `GET /stats/geo` | Vítimas e atores por geografia, mais linha do tempo |
| `GET /stats/timeline` | `ioc_velocity`, `cve_monthly`, `attack_weekly` |
| `GET /health` | Situação da API, do banco, da ingestão e dos feeds |
| `GET /sources` | As 86 fontes de coleta com o horário da última busca |
| `GET /whoami` | O IP com que a API te enxerga |

### Busca

```
GET /search?q=lockbit&types=ioc,vuln,actor,victim&limit=20
```

| Parâmetro | Observações |
|---|---|
| `q` | Obrigatório |
| `types` | Separado por vírgula: `ioc`, `vuln`, `actor`, `victim`. Omita para todos |
| `limit` | Padrão 50, máximo 100 |

Devolve `{ "query": …, "results": { … } }` agrupado por tipo de entidade.

### Indicadores

```
GET /iocs
```

| Parâmetro | Valores |
|---|---|
| `type` | `ip`, `domain`, `url`, `hash_md5`, `hash_sha1`, `hash_sha256`, `email`, `cve` |
| `confidence_min` | Inteiro de 0 a 100 |
| `active_only` | `true` |
| `sort` | Campo ordenável; `confidence_score` e `confidence` mapeiam para a pontuação calculada |
| `order` | `asc`, `desc` (padrão `desc`) |
| `limit`, `offset` | Paginação padrão |

⚠️ O arquivo OpenAPI publicado lista `severity` e `source` para este endpoint. **Nenhum dos
dois existe** — ambos são ignorados em silêncio. Use `confidence_min` no lugar de `severity`.

```
GET /iocs/lookup?value=1.2.3.4     ← o parâmetro é `value`, não `q`
GET /iocs/{id}
GET /check/{value}                 ← a mesma consulta que está por trás da página /check
GET /iocs/export/csv?limit=…      ← 🔑 exige login; aceita SÓ limit (máx. 5000)
```

O `/check/{value}` devolve `{ "found": bool, "value": … }` e é o mais amigável dos três para
consultar um indicador só.

### Vulnerabilidades

```
GET /vulnerabilities
```

| Parâmetro | Valores | Efeito verificado |
|---|---|---|
| `is_kev` | `true`, `false` | `true` → 3.913 de 359.241 |
| `severity` | `CRITICAL`, `HIGH`, `MEDIUM`, `LOW` | aceita minúscula, é convertido internamente |
| `cvss_min` | Decimal | `9` → 50.863 |
| `exploit_status` | ex.: `weaponized` | `weaponized` → 42 |
| `published_after` | Data ISO | |
| `include_rejected` | `true` para incluir CVEs rejeitadas (excluídas por padrão) | |

⚠️ O arquivo OpenAPI documenta `in_kev` e `search` para este endpoint. **Nenhum dos dois
existe.** O filtro de KEV é `is_kev`; não há busca textual aqui — use `/search`.

```
GET /vulnerabilities/{cve_id}           ex.: /vulnerabilities/CVE-2026-1234
GET /vulnerabilities/{cve_id}/related
GET /vulnerabilities/vendors            ← o índice de fabricantes
GET /vulnerabilities/vendor/{vendor}    ← CVEs de um fabricante
```

### Atores de ameaça

```
GET /threat-actors
```

| Parâmetro | Valores | Efeito verificado |
|---|---|---|
| `source` | `ransomware`, `apt`, `malware` | `ransomware` → 475 de 10.758 |
| `country` | Código ISO, ex.: `RU` | `RU` → 81 |
| `search` | Texto livre sobre nome e descrição | `lockbit` → 48 |
| `motivation`, `sophistication`, `platform`, `active_after` | | |

```
GET /threat-actors/{id}
GET /threat-actors/by-name/{nome}            ← consulta por nome, sem diferenciar maiúsculas
GET /threat-actors/by-name/{nome}/victims    ← vítimas + top_sectors do grupo
GET /threat-actors/platform-counts
```

💡 O `by-name` costuma ser o que você quer. Nome de ator é o que aparece em relatório; UUID
não.

### Vítimas

```
GET /victims
```

| Parâmetro | Casamento | Efeito verificado |
|---|---|---|
| `country` | exato, sem diferenciar maiúsculas | `BR` → 532 |
| `sector` | exato, sem diferenciar maiúsculas | `Healthcare` → 1.692 |
| `group` | **trecho** | `lockbit` → 3.275 |
| `source` | `ransomware.live`, `ransomlook` | |

#### 🔴 Contar as vítimas de um grupo é a armadilha deste endpoint

Nenhuma das duas abordagens óbvias está certa sozinha, e as duas falham *em silêncio*:

| Abordagem | Resultado p/ LockBit | Como falha |
|---|---|---|
| `/victims?group=lockbit` | **3.275** | Trecho — `group=play` também casa com `playboy` |
| `/threat-actors/by-name/lockbit/victims` | **5** | Exato — perde toda etiqueta versionada |

A causa é que **as etiquetas de grupo do leak site carregam número de versão**. A presença do
LockBit está espalhada entre `lockbit`, `lockbit2` (915), `lockbit3` (1.982) e `lockbit5` —
então o casamento exato devolve 5 e subconta em 99,8%, sem erro e sem aviso.

**Olhe as etiquetas reais antes de contar.** O `GET /victims/stats` devolve `by_group` com as
strings exatas e as contagens:

```bash
curl -s https://ctiwatch.com/api/v1/victims/stats \
  | jq -r '.by_group[] | select(.group_name | test("lockbit"; "i")) | "\(.count)\t\(.group_name)"'
```

Depois decida conscientemente: trecho para a presença inteira do grupo, etiqueta exata quando
precisar de precisão. O [`examples/actor-report.py`](../../examples/actor-report.py) faz essa
checagem cruzada sozinho e avisa quando os dois números discordam.

```
GET /victims/{id}
GET /victims/stats     ← by_source, by_group, by_sector, by_country
```

### Campanhas

```
GET /campaigns?active=true
```

| Parâmetro | Valores | Efeito verificado |
|---|---|---|
| `active` | `true` | `true` → 112 de 652 |
| `type` | `ransomware`, `apt` | |
| `impact` | nível de impacto | |

⚠️ O arquivo OpenAPI documenta `status=active|inactive|all`. **Não funciona** — o parâmetro
é `active=true`.

```
GET /campaigns/{id}
```

### Intel e análise

| Endpoint | Parâmetros |
|---|---|
| `GET /articles` | `source`, `has_cves=true`, `priority=high\|medium`, `search`, `tag` |
| `GET /articles/sources` | — |
| `GET /geopolitics` | atores por país, vítimas por país, alvos por setor |
| `GET /geopolitics/conflict-zones` | — |
| `GET /geopolitics/country/{código}` | — |
| `GET /markets` | Sites de vazamento e infraestrutura de mercados |
| `GET /honeypot/stats` | `totals`, `top_countries`, `top_ports`, `top_asns`, `recent_attackers` |
| `GET /correlations/entity/{tipo}/{id}` | Arestas do grafo para uma entidade |
| `GET /correlations/stats`, `GET /correlations/feed` | — |
| `GET /alerts`, `GET /alerts/summary` | Feed público de alertas |
| `GET /stream/feed` | Server-sent events, ao vivo |

### Phishing

```
GET /phishing/brands            marcas personificadas, ranqueadas
GET /phishing/hosts?class=…     hosts, por classificação
GET /phishing/kits              campanhas por impressão digital de kit
```

🔴 Os valores de `class` são **`compromised_site`**, **`attacker_infra`** e
**`abused_platform`**. Um valor não reconhecido **não dá erro** — ele cai silenciosamente em
`compromised_site`, então `class=infrastructure` devolve sites comprometidos parecendo que
funcionou. Confira o campo `class` ecoado na resposta; ele diz o que você recebeu de fato.

Totais atuais, devolvidos em toda resposta no campo `totals`:

| Classe | Hosts | URLs |
|---|---|---|
| `abused_platform` | 120.791 | 191.987 |
| `attacker_infra` | 13.551 | 23.391 |
| `compromised_site` | 12.639 | 35.831 |

Veja [Indicadores → Phishing](indicators.md#phishing--vitimologia-de-phishing) para entender
o que essas classes significam e por que a terceira existe.

### Endpoints de apoiador 🔑

| Endpoint | Exige |
|---|---|
| `GET /diamond?sector=…&country=…` | Autenticação |
| `GET /diamond/options` | Autenticação |
| `POST /ask` | Autenticação **+ plano Supporter** |
| `GET /watchlists`, `POST /watchlists` | Autenticação |
| `GET /workers/health` | Autenticação |
| `GET /iocs/export/csv` | Autenticação |

Repare que o `/ask` é **POST**, não GET — um GET devolve 404.

---

## Receitas

Versões executáveis de todas elas estão em [`examples/`](../../examples/).

### As entradas de KEV mais recentes

```bash
curl -s "https://ctiwatch.com/api/v1/vulnerabilities?is_kev=true&sort=published_date&limit=10" \
  | jq -r '.items[] | "\(.cve_id)  CVSS \(.cvss_score)  \(.description[0:70])"'
```

### Este indicador é conhecido?

```bash
curl -s "https://ctiwatch.com/api/v1/check/45.155.205.233" | jq '{found, value}'
```

### Montar uma lista de bloqueio de IPs de alta confiança

O endpoint de CSV é a ferramenta errada para isso, e vale saber por quê:

```bash
# Aceita SÓ `limit` (máx. 5.000). type= e filtros de confiança são IGNORADOS —
# você recebe os indicadores mais recentes de todos os tipos.
curl -s -H "X-Api-Key: $CTIWATCH_KEY" \
  "https://ctiwatch.com/api/v1/iocs/export/csv?limit=5000" > recentes.csv
```

Para uma lista de bloqueio filtrada, pagine o endpoint JSON — veja
[`examples/blocklist.py`](../../examples/blocklist.py), que trata o teto de 100 linhas
corretamente e não precisa de chave nenhuma.

### Quem está atingindo o meu setor, no meu país?

```bash
curl -s "https://ctiwatch.com/api/v1/victims?country=BR&sector=Healthcare&limit=100" \
  | jq -r '.items[] | "\(.attack_date[0:10])  \(.metadata.group)  \(.name)"'
```

### Tudo que um grupo já reivindicou

```bash
curl -s "https://ctiwatch.com/api/v1/threat-actors/by-name/LockBit/victims?limit=100" \
  | jq '{total, top_sectors, first: .items[0].name}'
```

---

## Dois hábitos que vão te poupar

**1. Olhe o `total`, não só o HTTP 200.** Como parâmetro desconhecido é descartado em
silêncio, resposta bem-sucedida não é prova de que o seu filtro funcionou. Compare o `total`
com e sem o filtro na primeira vez que usar.

**2. Rebusque em vez de guardar indefinidamente.** As pontuações de confiança decaem com o
tempo, e indicadores são desativados conforme envelhecem. Uma lista exportada meses atrás já
não reflete o que a plataforma diria hoje.

---

## Uma observação sobre o arquivo OpenAPI

O `openapi.json` está **desatualizado** em vários pontos, todos documentados acima: o
`/iocs/lookup` recebe `value` e não `q`; o filtro de KEV é `is_kev` e não `in_kev`; o
`/campaigns` filtra por `active` e não por `status`; `search` em `/vulnerabilities` e
`severity`/`source` em `/iocs` não existem; e o arquivo descreve 13 endpoints onde a API
serve cerca de cinquenta.

**Esta página reflete a API ao vivo, verificada endpoint a endpoint.** Onde as duas
discordarem, confie nesta página — e conte com a correção do arquivo de spec.
