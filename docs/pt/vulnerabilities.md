# Vulnerabilidades — o que corrigir primeiro

[← Índice da documentação](README.md) · [🇬🇧 English](../en/vulnerabilities.md)

**377.168** CVEs, das quais **3.917** estão no catálogo KEV (vulnerabilidades sabidamente
exploradas) da CISA.

O objetivo desta seção não é listar vulnerabilidades — qualquer um faz isso. É te ajudar a
decidir **qual punhado delas corrigir nesta semana**.

---

## `/vulnerabilities` — Base de CVEs

**[ctiwatch.com/vulnerabilities](https://ctiwatch.com/vulnerabilities)**

### Como usar

Filtre e ordene pelos três sinais que realmente preveem risco — e que não são a mesma coisa:

| Sinal | O que ele diz | O que ele **não** diz |
|---|---|---|
| **CVSS** | Quão ruim seria se explorada | Se alguém está explorando |
| **EPSS** | Probabilidade de ser explorada nos próximos 30 dias | Se está sendo explorada *agora* |
| **CISA KEV** | Ela **está** sendo explorada, confirmado | Quão ruim ela é para *você* |

**A receita prática:** comece pelo KEV. Se uma vulnerabilidade está no KEV e você usa o
produto afetado, ela vai para o topo da lista independentemente do CVSS — "exploração
confirmada" ganha de "gravidade teórica" sempre. Depois use o EPSS para ordenar o que sobrou,
e o CVSS para desempatar.

Uma CVSS 9.8 que ninguém nunca explorou e uma CVSS 7.5 que está no KEV não são uma decisão
difícil. Corrija a 7.5.

### A página de detalhe da CVE

Abra qualquer CVE (`/vulnerabilities/CVE-2026-XXXX`) para ter:

- a **descrição oficial** do NVD;
- uma **narrativa escrita** explicando a vulnerabilidade e a classe de fraqueza dela em
  linguagem corrente;
- os **fabricantes mencionados**, extraídos da descrição;
- **Organizações atingidas por esta CVE** — vítimas que a plataforma consegue ligar à
  exploração dessa vulnerabilidade específica. É a seção que transforma uma nota abstrata em
  "isto está sendo usado contra empresas como a minha".

---

## `/vulnerabilities/vendor` — Navegar por fabricante

**[ctiwatch.com/vulnerabilities/vendor](https://ctiwatch.com/vulnerabilities/vendor)**

A mesma base, entrando pelo outro lado: **1.400+ fabricantes**, cada um com suas CVEs, notas,
situação no KEV e inteligência de exploração.

### Como usar

Esta é a página para quando você trabalha a partir de um inventário de ativos, e não a partir
da notícia. Você não se importa com "todas as CVEs críticas da semana" — você se importa com
os doze produtos que realmente usa.

Escolha seus fabricantes e confira periodicamente. Melhor ainda: coloque os nomes deles numa
[watchlist](account.md#watchlists--o-recurso-mais-útil-da-plataforma) e deixe a plataforma te avisar.

### 💡 Dica prática

Nome de fabricante em dado de CVE é bagunçado — a mesma empresa aparece como `microsoft`,
`microsoft_corporation` e dentro de strings de produto. O índice de fabricantes resolve isso a
partir do dado estruturado de CPE, e não de texto livre, então buscar o fabricante aqui é mais
confiável do que buscar o nome dele na lista de CVEs.

---

## Juntando tudo — uma rotina semanal

Um fluxo de vulnerabilidades que usa bem esta seção leva uns quinze minutos:

1. **KEV primeiro.** Filtre por CISA KEV, ordenado por data de inclusão. O que for novo e você
   usar é o trabalho da semana.
2. **Seus fabricantes.** Confira as páginas dos produtos do seu inventário — ou leia os
   alertas da watchlist que já fez isso por você.
3. **Olhe as vítimas.** Em qualquer coisa que te deixe em dúvida, abra a CVE e veja
   *Organizações atingidas por esta CVE*. Se há organizações do seu setor ali, a decisão se
   toma sozinha.

### ⚠️ Saiba disso

A cobertura de evidência de exploração é desigual, e isso corta para um lado só: **a ausência
de vítimas ligadas não é evidência de que a CVE não está sendo explorada.** Ligar uma invasão
a uma CVE específica exige que alguém publique essa conexão, e a maioria das invasões nunca
recebe esse nível de detalhe público. Use a ligação com vítimas como evidência positiva,
nunca como atestado de tranquilidade.
