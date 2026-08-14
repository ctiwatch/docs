# Documentação do CTIWatch

[← Voltar ao índice](../../README.md) · [🇬🇧 English](../en/README.md)

Esta documentação explica **o que cada página da plataforma faz e como usá-la**.

Se você nunca usou o CTIWatch, comece por [Primeiros passos](#primeiros-passos) e depois leia
[Indicadores](indicators.md) — a consulta de reputação é o jeito mais rápido de tirar algo
útil da plataforma em menos de um minuto.

---

## O mapa

A plataforma é organizada em quatro grupos, que são os quatro menus do topo.

### 🎯 [Ameaças](threats.md) — *quem está atacando*

| Página | O que ela responde |
|---|---|
| [`/threats`](threats.md#threats--diretório-de-atores) | Quem é esse grupo? Do que ele é conhecido? |
| [`/victims`](threats.md#victims--rastreador-de-vítimas-de-ransomware) | Quem foi atingido, por quem, quando? |
| [`/campaigns`](threats.md#campaigns--operações-ativas) | Que operações estão em curso agora? |
| [`/malware`](threats.md#malware--famílias-de-malware) | O que é essa família de malware? |

### 🔍 [Indicadores](indicators.md) — *o que bloquear e caçar*

| Página | O que ela responde |
|---|---|
| [`/check`](indicators.md#check--consulta-de-reputação-de-ip--ioc) | Esse IP / domínio / hash é perigoso? |
| [`/iocs`](indicators.md#iocs--base-de-indicadores) | Me dá os indicadores que batem com estes critérios. |
| [`/honeypot`](indicators.md#honeypot--telemetria-dos-nossos-sensores) | O que está atacando nossos sensores agora? |
| [`/phishing`](indicators.md#phishing--vitimologia-de-phishing) | Quais marcas estão sendo personificadas? |

### 🛡️ [Vulnerabilidades](vulnerabilities.md) — *o que corrigir primeiro*

| Página | O que ela responde |
|---|---|
| [`/vulnerabilities`](vulnerabilities.md#vulnerabilities--base-de-cves) | Quais CVEs importam, e com que urgência? |
| [`/vulnerabilities/vendor`](vulnerabilities.md#vulnerabilitiesvendor--navegar-por-fabricante) | O que está exposto nos produtos que eu uso? |

### 🧠 [Intel](intel.md) — *contexto e análise*

| Página | O que ela responde |
|---|---|
| [`/articles`](intel.md#articles--feed-de-notícias) | O que aconteceu em segurança nesta semana? |
| [`/reports`](intel.md#reports--relatórios-semanais) | Me dá a semana num documento só. |
| [`/geopolitics`](intel.md#geopolitics--estados-nação-e-conflitos) | Que atividade estatal afeta a minha região? |
| [`/markets`](intel.md#markets--sites-de-vazamento-e-darknet) | Onde esses grupos publicam? |
| [`/intelligence`](intel.md#intelligence--o-grafo-de-correlações) | Como essas entidades se conectam? |
| [`/diamond`](intel.md#diamond--diamond-model-of-intrusion-analysis) | Como é a ameaça para o *meu* setor e país? |
| [`/ask`](intel.md#ask--analista-de-ia) | Só responde a minha pergunta em português. |

### ⚙️ [Sua conta](account.md) — *faça a plataforma vigiar por você*

Dashboard, watchlists, alertas, chaves de API e configurações — como parar de visitar o site
e deixar que ele venha até você.

---

## Primeiros passos

### Você não precisa de conta

Todas as páginas acima são legíveis sem cadastro, e não existe paywall sobre dado.
Teste [ctiwatch.com/check](https://ctiwatch.com/check) agora com qualquer IP suspeito — sem
formulário, sem e-mail.

### O que uma conta acrescenta

A conta existe para a plataforma fazer coisas **por** você, em vez de só te mostrar coisas:

- **[Watchlists](account.md#watchlists--o-recurso-mais-útil-da-plataforma)** — diga o que te interessa (o nome da sua empresa,
  seus fornecedores, seu setor) e ela avisa quando isso aparecer em dado novo.
- **[Alertas](account.md#alerts--histórico-de-notificações)** — o histórico de notificações, com entrega por e-mail.
- **[Chaves de API](account.md#settingsapi-keys--chaves-de-api)** — acesso programático,
  100 requisições/dia no plano gratuito.

### O que o Supporter acrescenta

O [plano Supporter](https://ctiwatch.com/support) é como o projeto paga servidores, feeds e
enriquecimento por IA. Ele libera conveniência e profundidade — cota maior de API, o
[analista de IA](intel.md#ask--analista-de-ia), pivôs mais profundos no
[Diamond Model](intel.md#diamond--diamond-model-of-intrusion-analysis), exportação e
notificações push.

**Ele nunca libera dado que o visitante anônimo não possa ver.** Isso é decisão de projeto,
não descuido: inteligência de ameaça que só quem paga consegue ler protege menos gente.

---

## Como ler esse dado com responsabilidade

Três coisas valem ser internalizadas antes de agir com base em qualquer coisa daqui.

**1. Dado de site de vazamento é alegação, não confirmação.** Os registros de vítimas de
ransomware são raspados dos próprios sites de extorsão dos criminosos. Atacante infla número,
republica vazamento antigo e às vezes lista organização que nunca tocou. Trate todo registro
de vítima como *"este grupo afirma X"*.

**2. Indicador velho é indicador fraco.** Um IP que foi servidor de comando e controle há
oito meses provavelmente é a hospedagem comum de alguém hoje. É por isso que todo indicador
tem uma pontuação de confiança ponderada por recência — use essa pontuação, e tenha cuidado
ao bloquear com base em indicador já decaído pelo tempo.

**3. Ausência de evidência não é evidência de ausência.** Se um ator não tem família de
malware associada, quase sempre significa que ninguém publicou esse mapeamento em formato
legível por máquina — não que o grupo não tenha ferramental. A página do
[Diamond Model](intel.md#diamond--diamond-model-of-intrusion-analysis) mostra a cobertura
explicitamente por exatamente esse motivo.

---

## A API

Tudo que aparece no site está disponível programaticamente. São 13 endpoints públicos, com
base em `https://ctiwatch.com/api/v1/`:

```bash
# Contadores da plataforma — sem autenticação
curl https://ctiwatch.com/api/v1/stats

# Consultar um indicador
curl "https://ctiwatch.com/api/v1/iocs/lookup?value=1.2.3.4"

# Com chave de API
curl -H "X-API-Key: $CTIWATCH_KEY" \
     "https://ctiwatch.com/api/v1/vulnerabilities?is_in_kev=true&limit=20"
```

| Endpoint | Para que serve |
|---|---|
| `/stats` | Contadores da plataforma |
| `/search` | Busca entre entidades |
| `/iocs`, `/iocs/{id}`, `/iocs/lookup`, `/iocs/export/csv` | Indicadores |
| `/vulnerabilities`, `/vulnerabilities/{cve_id}` | CVEs |
| `/threat-actors`, `/threat-actors/{id}` | Atores |
| `/victims` | Vítimas de ransomware |
| `/campaigns` | Campanhas |
| `/watchlists` | Suas watchlists (autenticado) |

As chaves são criadas em [Configurações → API Keys](https://ctiwatch.com/settings/api-keys).
O plano gratuito permite 100 requisições/dia por chave.

*Uma referência dedicada da API é o próximo documento previsto para este repositório.*
