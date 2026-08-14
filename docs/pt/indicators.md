# Indicadores — o que bloquear e caçar

[← Índice da documentação](README.md) · [🇬🇧 English](../en/indicators.md)

Este grupo é a metade operacional da plataforma: o dado que você joga num firewall, num SIEM
ou numa caçada de ameaças.

---

## `/check` — Consulta de reputação de IP / IOC

**[ctiwatch.com/check](https://ctiwatch.com/check)**

Cole um **IP, domínio ou hash de arquivo** e receba uma resposta conferida contra mais de 1,7
milhão de indicadores vindos de honeypots, listas de bloqueio e feeds de OSINT. Grátis, sem
cadastro, sem formulário.

### Como usar

É a coisa útil mais rápida da plataforma. Um endereço apareceu no seu log às 2 da manhã —
cole aqui e tenha contexto em segundos.

Você recebe:

- se o indicador é conhecido, e por quais fontes;
- a **pontuação de confiança** e quando ele foi visto pela última vez;
- um **Analyst Summary** em linguagem corrente, explicando a que o indicador está associado;
- links para atores, campanhas e CVEs relacionados, quando existem.

Cada consulta tem URL própria (`/check/1.2.3.4`), então dá para colar o link direto num
chamado ou numa conversa, e quem abrir vê o mesmo resultado.

### 💡 Dica prática

**Leia a data de "visto pela última vez" antes de agir.** Um acerto não é automaticamente um
veredito. Um IP visto numa campanha de varredura há onze meses provavelmente não é o mesmo
inquilino hoje — faixa de nuvem recicla rápido. Acerto desta semana merece ação; acerto do ano
passado merece investigação, não bloqueio.

---

## `/iocs` — Base de indicadores

**[ctiwatch.com/iocs](https://ctiwatch.com/iocs)**

O corpus completo: **1.737.420** indicadores de comprometimento — IPs, domínios, URLs e
hashes — com tipo, fonte, primeira e última observação, e confiança.

### Como usar

Filtre por **tipo**, **fonte** e **confiança**, e exporte. Os usos típicos são montar lista
de bloqueio, semear uma caçada, ou enriquecer dado que você já tem.

Pela API:

```bash
# Exportação CSV — qualquer conta logada, até 5.000 linhas
curl -H "X-Api-Key: $CTIWATCH_KEY" \
  "https://ctiwatch.com/api/v1/iocs/export/csv?limit=5000" > iocs.csv
```

⚠️ O endpoint de CSV aceita **só `limit`** — ele sempre devolve os indicadores mais recentes
de todos os tipos. Para filtrar por tipo ou confiança, pagine o endpoint JSON (veja
[`examples/blocklist.py`](../../examples/blocklist.py)).

### Entendendo o `confidence_score`

A pontuação **não** é copiada da fonte. Ela é calculada, e combina três coisas:

| Componente | Significado |
|---|---|
| **Confiabilidade da fonte** | Um honeypot que viu o ataque acontecer vale mais que uma lista agregada a granel. |
| **Sinal bruto** | O que a própria fonte afirmou, quando ela afirma alguma coisa. |
| **Decaimento por recência** | A pontuação cai conforme a observação envelhece. |

A consequência que vale lembrar: **o mesmo indicador pontua menos com o tempo sem que nada de
novo aconteça**. Isso é intencional. Se você guarda indicadores em cache local, atualize —
uma lista exportada há seis meses já se afastou do que a plataforma diria hoje.

### ⚠️ Saiba disso

Cerca de três quartos do corpus chega de feeds de phishing e listas de bloqueio a granel, que
não publicam confiança própria. Eles são úteis em volume e fracos individualmente. Se a
intenção é bloquear automaticamente, e não alertar, filtre por confiança.

---

## `/honeypot` — Telemetria dos nossos sensores

**[ctiwatch.com/honeypot](https://ctiwatch.com/honeypot)**

Atividade de atacante capturada **de primeira mão** por sensores do CTIWatch — uma instalação
dedicada de T-Pot — em vez de coletada do feed de outra pessoa.

### Como usar

Use quando quiser saber o que está sendo atacado **agora**, em escala de internet, sem atraso
de publicação. Como os sensores são nossos, não existe intervalo entre o atacante encostar
neles e o dado aparecer aqui.

Ela é especialmente boa em três perguntas:

- Que credenciais estão sendo testadas em massa nesta semana?
- Que portas e serviços estão atraindo varredura agora?
- De onde vem esse tráfego?

### 💡 Por que esta página importa mais do que o tamanho dela sugere

Todo o resto da plataforma é, no fim das contas, observação de outra pessoa que nós coletamos
e correlacionamos. Esta página é observação **nossa**. Quando um indicador de honeypot e um
feed de terceiro discordam, o honeypot viu acontecer.

---

## `/phishing` — Vitimologia de phishing

**[ctiwatch.com/phishing](https://ctiwatch.com/phishing)**

Quais marcas estão sendo **personificadas** em campanhas de phishing ativas — extraído do
próprio corpus de indicadores da plataforma, sem depender de nenhum site de vazamento.

### Como usar

Dois públicos, dois usos:

- **Se a sua marca está aqui**, criminosos estão usando o seu nome para fraudar os seus
  clientes. A página te dá os hostnames que fazem isso, que é o que um pedido de derrubada
  precisa.
- **Se você defende usuários**, a lista de marcas é um ranking do que a sua gente tem mais
  chance de receber como isca neste mês.

### Como a classificação funciona — e por que ela tem três classes, não duas

Todo host de phishing cai numa de três classes, por **evidência estrutural na URL**, não por
palpite:

| Classe | Evidência | Significado |
|---|---|---|
| **Comprometido** | O kit está sob caminho de CMS (`/wp-content/`, `/wp-includes/`) | Um site de verdade que foi invadido. **Esta organização é vítima.** |
| **Infraestrutura do atacante** | O nome da marca está no *hostname* | Domínio registrado para parecer a marca. **Isto é do criminoso.** |
| **Plataforma abusada** | Hospedagem compartilhada, encurtador, construtor de formulário | Nem vítima nem criminoso — um serviço sendo abusado. |

A terceira classe é a maior, e é a que mais importa para ler a página corretamente. Sem ela,
um provedor de hospedagem servindo centenas de páginas de phishing apareceria como centenas
de "organizações vítimas" — o que seria gravemente errado, e nomearia empresas reais como
invadidas sem que tivessem sido.

### ⚠️ Saiba disso

Cada resultado carrega um **nível de precisão**, mostrado na interface. Leia. A lista de
marcas é curada à mão, o que significa que uma marca que ninguém cadastrou ainda não será
detectada — a classificação é honesta sobre o que conhece, mas não tem como conhecer tudo, e
marca nova aparece o tempo inteiro.
