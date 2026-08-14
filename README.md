# CTIWatch — Documentation · Documentação

**[ctiwatch.com](https://ctiwatch.com)** — free, real-time cyber threat intelligence.
Plataforma gratuita de inteligência de ameaças cibernéticas em tempo real.

| 🇬🇧 English | 🇧🇷 Português |
|---|---|
| **[Read the documentation →](docs/en/README.md)** | **[Ler a documentação →](docs/pt/README.md)** |

---

## 🇬🇧 What is CTIWatch?

CTIWatch is a **cyber threat intelligence platform** that collects, correlates and publishes
threat data from 86 sources — honeypots we run ourselves, ransomware leak sites, blocklists,
vulnerability databases and open-source intelligence — and makes all of it searchable in one
place, for free.

As of today the platform tracks:

| | |
|---|---|
| **1,737,420** | indicators of compromise (IPs, domains, URLs, file hashes) |
| **377,168** | vulnerabilities (CVEs), of which **3,917** are in CISA KEV |
| **10,758** | threat actors, APT groups and ransomware operations |
| **32,334** | ransomware victims tracked across leak sites |
| **112** | active campaigns |
| **86** | data sources, collected continuously |

### What makes it different

**Everything is public.** There is no data paywall. Anonymous visitors see the same
indicators, CVEs, actors and victims that registered users do. The optional *Supporter*
plan pays for servers and unlocks convenience — larger API quota, AI-assisted analysis,
deeper pivots — never access to data that others cannot see.

**Some of it is first-hand.** Most CTI platforms repackage the same feeds. CTIWatch runs
its own honeypot sensors, so part of the attacker activity you see was captured directly,
not bought or re-published.

**It tells you how sure it is.** Every indicator carries an `effective_confidence` score
built from source reliability, signal strength and how recently it was seen — because a
hash first observed two years ago is not evidence in the same way one seen this morning is.

### An honest note on what this data is

Ransomware victim records come from **criminal leak sites**. That means they are *claims
made by attackers*, not confirmed breaches. Attackers exaggerate, recycle old data and
occasionally invent. The platform reproduces the claim and labels it as such — read those
pages as "this group says it hit this organization", never as established fact.

**[→ Full documentation](docs/en/README.md)** · [API reference](docs/en/api.md) · [Runnable examples](examples/)

---

## 🇧🇷 O que é o CTIWatch?

O CTIWatch é uma **plataforma de inteligência de ameaças cibernéticas** que coleta,
correlaciona e publica dados de ameaças vindos de 86 fontes — honeypots que nós mesmos
operamos, sites de vazamento de ransomware, listas de bloqueio, bases de vulnerabilidades e
inteligência de fontes abertas — e deixa tudo pesquisável num lugar só, de graça.

Hoje a plataforma acompanha:

| | |
|---|---|
| **1.737.420** | indicadores de comprometimento (IPs, domínios, URLs, hashes) |
| **377.168** | vulnerabilidades (CVEs), sendo **3.917** no catálogo KEV da CISA |
| **10.758** | atores de ameaça, grupos APT e operações de ransomware |
| **32.334** | vítimas de ransomware rastreadas em sites de vazamento |
| **112** | campanhas ativas |
| **86** | fontes de dados, coletadas continuamente |

### O que a diferencia

**Tudo é público.** Não existe paywall sobre dado. Quem entra sem conta vê os mesmos
indicadores, CVEs, atores e vítimas que um usuário registrado. O plano *Supporter*, que é
opcional, paga os servidores e libera conveniência — cota maior de API, análise assistida
por IA, pivôs mais profundos — nunca acesso a um dado que os outros não possam ver.

**Parte é de primeira mão.** A maioria das plataformas de CTI reembala os mesmos feeds. O
CTIWatch opera sensores honeypot próprios, então parte da atividade de atacante que você vê
foi capturada diretamente, não comprada nem republicada.

**Ela diz o quanto tem certeza.** Cada indicador carrega um `effective_confidence` composto
por confiabilidade da fonte, força do sinal e quão recente é a observação — porque um hash
visto pela primeira vez há dois anos não é evidência do mesmo jeito que um visto hoje de
manhã.

### Uma observação honesta sobre esse dado

Os registros de vítimas de ransomware vêm de **sites de vazamento criminosos**. Isso
significa que são *alegações feitas por atacantes*, não invasões confirmadas. Criminoso
exagera, recicla dado velho e às vezes inventa. A plataforma reproduz a alegação e a rotula
como tal — leia essas páginas como "este grupo afirma ter atingido esta organização", nunca
como fato estabelecido.

**[→ Documentação completa](docs/pt/README.md)** · [Referência da API](docs/pt/api.md) · [Exemplos executáveis](examples/)

---

## Contributing · Contribuindo

Found an error, or something that is out of date? Open an issue.
Achou um erro, ou algo desatualizado? Abra uma issue.

## License · Licença

Documentation is released under [CC BY 4.0](LICENSE) — use it, quote it, translate it,
just say where it came from.
A documentação está sob [CC BY 4.0](LICENSE) — use, cite, traduza, só diga de onde veio.
