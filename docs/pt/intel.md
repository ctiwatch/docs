# Intel — contexto e análise

[← Índice da documentação](README.md) · [🇬🇧 English](../en/intel.md)

As páginas dos outros três grupos dizem *o quê*. Estas dizem *o que aquilo significa*.

---

## `/articles` — Feed de notícias

**[ctiwatch.com/articles](https://ctiwatch.com/articles)**

Notícias de segurança agregadas de 28 fontes — BleepingComputer, Cisco Talos, CISA, Unit 42,
Krebs, SANS ISC e outras — filtradas e etiquetadas por CVE, ator e tema.

### Como usar

Busque e filtre por **CVE**, **ator** ou palavra-chave, em vez de rolar a página. O valor do
feed não é "ler as notícias"; é *"me mostra tudo que foi publicado sobre a CVE-2026-1234"* ou
*"o que já escreveram sobre este grupo"*, em todas as fontes de uma vez.

Os artigos são ligados às entidades que mencionam, então a página de um ator mostra a
cobertura sobre ele sem você precisar buscar.

### ⚠️ Saiba disso

A ligação artigo↔entidade é casamento de texto, e casamento de texto com nome curto produz
falso positivo. A plataforma cura a lista de nomes de ator justamente para evitar isso — um
grupo cujo nome é uma palavra comum não pode ser casado com segurança só por frequência. Se
uma ligação parecer errada, ela pode estar; o artigo original é sempre a autoridade.

---

## `/reports` — Relatórios semanais

**[ctiwatch.com/reports](https://ctiwatch.com/reports)**

Um relatório escrito, gerado toda **segunda-feira** a partir do dado ao vivo da plataforma:
atividade de ransomware, vulnerabilidades críticas, destaques de atores e tendências de IOC
da semana.

### Como usar

É a página para mandar para quem não vai navegar numa plataforma de CTI. Ela é feita para a
reunião semanal de segurança, e cada relatório tem URL permanente, então dá para linkar ou
arquivar.

Se você só tem tempo para uma página por semana, que seja esta.

---

## `/geopolitics` — Estados-nação e conflitos

**[ctiwatch.com/geopolitics](https://ctiwatch.com/geopolitics)**

Atividade APT estatal por país, monitoramento de zonas de conflito (Rússia/Ucrânia,
China/Taiwan, Irã), mapas de calor de vítimas de ransomware e alvos por setor.

### Como usar

Dois usos honestos:

- **Exposição regional.** Filtre pelo seu país e leia o que de fato está caindo ali.
  Inteligência de ameaça escrita para o público americano frequentemente não descreve o que
  está atingindo o Brasil, e a diferença importa.
- **Consciência de conflito.** Quando um conflito escala, a atividade cibernética associada
  costuma se ampliar para além dos beligerantes, alcançando fornecedores e aliados. Esta
  página acompanha os informes.

### ⚠️ Saiba disso

Atribuição a Estado é **política, além de técnica**. As atribuições públicas vêm de governos
e fornecedores que têm incentivos próprios, e são contestadas com frequência. Leia esta
página como "quem é publicamente acusado do quê", e mantenha firme a distinção entre
*atribuído* e *provado*.

---

## `/markets` — Sites de vazamento e darknet

**[ctiwatch.com/markets](https://ctiwatch.com/markets)**

Monitoramento ativo de mercados da darknet, sites de vazamento de ransomware e fóruns de
crime cibernético. A infraestrutura é acompanhada via RansomLook, com atualização a cada
quatro horas.

### Como usar

Isto é inteligência de infraestrutura: **onde** esses grupos publicam, e se aquilo está no
ar. Responde "este grupo ainda está operando?" por um ângulo diferente do da lista de vítimas
— um site de vazamento que apagou costuma anteceder uma troca de marca ou uma derrubada.

### ⚠️ Saiba disso

A plataforma monitora que essa infraestrutura existe e está alcançável. Ela não transaciona,
não compra e não republica dado roubado.

---

## `/intelligence` — O grafo de correlações

**[ctiwatch.com/intelligence](https://ctiwatch.com/intelligence)**

Um grafo visual correlacionando indicadores, CVEs, atores, campanhas e vítimas — para
encontrar relações que são invisíveis numa lista.

### Como usar

Comece por uma entidade que te interessa e expanda um salto por vez. O grafo serve para
*descoberta* — "o que mais encosta nisto?" — e não para inventário. Quando ele revelar uma
aresta inesperada, confirme nas páginas das entidades antes de construir qualquer coisa em
cima.

### 🔴 Saiba disso — o grafo é esparso, e este é o estado honesto dele

A esmagadora maioria dos indicadores e CVEs da base **não tem aresta nenhuma**. Isso não é
problema de renderização; é reflexo da realidade. As relações são extraídas de texto
publicado, e quase ninguém publica "este IP pertence a esta campanha" num formato que uma
máquina leia.

Na prática: **o grafo mostra o que foi escrito, não o que é verdade.** Um nó bem conectado é
um nó bem *documentado*. Um nó isolado pode ser igualmente perigoso e apenas não documentado.
Use o grafo para achar pistas, nunca para concluir que algo é desconexo.

---

## `/diamond` — Diamond Model of Intrusion Analysis

**[ctiwatch.com/diamond](https://ctiwatch.com/diamond)**

Escolha um **setor** e um **país**. A plataforma monta o Diamond Model — adversário,
capacidade, infraestrutura e vítima — em torno daquela vitimologia, com dado ao vivo.

### Como usar

É o que existe de mais próximo, na plataforma, de *"como é a ameaça para mim?"*. Escolha seu
setor e seu país, e você recebe os quatro vértices preenchidos com os atores que de fato
atingem organizações como a sua, as capacidades ligadas a eles, a infraestrutura envolvida e
o padrão de vitimologia.

Use para apresentar a quem precisa de um retrato de ameaça, e não de um feed de dados — ela
foi desenhada para ser lida, não consultada.

| | Grátis | Supporter |
|---|---|---|
| Setores + países por pivô | 1 + 1 | 5 + 5 |
| Profundidade | Top 5 | Top 25 |
| Janela de tempo | 12 meses | 5 anos |
| Técnicas MITRE ATT&CK | — | ✅ |
| Exportação | — | ✅ |

Os quatro vértices estão presentes no plano gratuito. O Supporter alarga o pivô; ele não
destrava um vértice escondido.

### 💡 Leia o painel de cobertura

A página mostra a **cobertura** do pivô que você escolheu, e isso é deliberado. Grupos de
ransomware e famílias de malware catalogadas são populações em boa medida *disjuntas*: a
maioria das operações de ransomware não tem família de malware formalmente ligada a elas em
lugar nenhum do dado público. Em vez de desenhar um vértice vazio e deixar você supor que não
há nada ali, a página declara quanto do retrato ela realmente consegue preencher.

---

## `/ask` — Analista de IA

**[ctiwatch.com/ask](https://ctiwatch.com/ask)** · *recurso Supporter*

Faça perguntas em linguagem corrente, respondidas por uma IA fundamentada **apenas** em dado
ao vivo do CTIWatch.

### Como usar

Pergunte o que você perguntaria a um colega:

> *"Quais grupos de ransomware atingiram a saúde brasileira nos últimos seis meses?"*
>
> *"A CVE-2026-1234 está sendo explorada, e contra quem?"*
>
> *"O que se sabe sobre a infraestrutura deste grupo?"*

Ela brilha nas perguntas que, de outro modo, exigiriam você cruzar três páginas e fazer a
junção na mão.

### ⚠️ Saiba disso

O modelo responde a partir do dado da plataforma, o que limita o estrago mas não o elimina:
ele ainda pode ler errado o que recuperou, e herda todas as limitações descritas nesta
documentação — alegação de site de vazamento continua sendo alegação, grafo esparso continua
esparso.

**Para qualquer coisa que você vá agir em cima, siga a resposta de volta até a página de
origem.** A IA é um jeito rápido de achar a página certa, não um substituto para lê-la.
