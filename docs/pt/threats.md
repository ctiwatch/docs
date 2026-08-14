# Ameaças — quem está atacando

[← Índice da documentação](README.md) · [🇬🇧 English](../en/threats.md)

Este grupo responde à pergunta *"quem está por trás disso, e o que já fizeram?"*

---

## `/threats` — Diretório de atores

**[ctiwatch.com/threats](https://ctiwatch.com/threats)**

Um diretório de **10.758** atores de ameaça: grupos APT, operações de ransomware, famílias
de malware e quadrilhas criminosas. Para cada um, a plataforma acompanha atribuição,
motivação, capacidade técnica e padrão operacional.

### Como usar

Busque pelo nome — inclusive por **apelidos**. A indústria batiza o mesmo grupo de cinco
maneiras diferentes (o que um fornecedor chama de `TA505`, outro chama de `Hive0065`), então
toda página de ator traz um bloco **"Also Known As"**. Se um nome que veio de um relatório
não retornar nada, tente o apelido.

Ao abrir um ator você encontra:

- **Intelligence Assessment** — um perfil escrito do grupo, gerado a partir do que a
  plataforma sabe sobre ele.
- **Also Known As** — todos os apelidos que a plataforma consolidou.
- **Vítimas** — em `/threats/<nome>/victims`, tudo que é atribuído àquele grupo.

### 💡 Dica prática

O pivô mais útil aqui não é a página do ator — é a lista de vítimas dele. Se o grupo vem
atingindo hospitais na América Latina há seis meses e você opera um hospital na América
Latina, isso é um sinal muito mais forte do que qualquer descrição de capacidade.

### ⚠️ Saiba disso

Atribuição de ator em CTI pública é **ruidosa**. A mesma operação aparece com nomes
diferentes, grupos trocam de marca depois de ação policial, e afiliados de uma operação de
ransomware costumam trabalhar para outras três ao mesmo tempo. A plataforma consolida
apelidos quando consegue provar que é o mesmo grupo, e mantém separado quando não consegue.

---

## `/victims` — Rastreador de vítimas de ransomware

**[ctiwatch.com/victims](https://ctiwatch.com/victims)**

**32.334** organizações listadas em sites de extorsão de ransomware, coletadas do
Ransomware.live, do RansomLook e de outras fontes, correlacionadas de modo que a mesma vítima
publicada por duas fontes em dias diferentes seja um registro só, e não dois.

### Como usar

Filtre por **grupo**, **país** e **setor**, e ordene por data. Três usos comuns:

- *"A minha organização está listada?"* — busque o nome. Tente também o nome fantasia e a
  razão social; atacante escreve o que quiser.
- *"O meu setor está sob pressão agora?"* — filtre por setor e compare os últimos 30 dias
  com os 30 anteriores.
- *"Quem está ativo no meu país?"* — filtre por país e leia a coluna do grupo.

### 🔴 Leia isto antes de usar dado de vítima

**Esses registros são alegações feitas por criminosos nos próprios sites de extorsão deles.**
Não são invasões confirmadas, e tratá-los como confirmados é o erro mais comum que se comete
com esse tipo de dado.

Atacantes rotineiramente:

- listam a organização antes de terminar a negociação, como pressão — e removem se receberem;
- republicam dado de um vazamento antigo como se fosse novo;
- listam uma subsidiária e nomeiam a controladora, ou o contrário;
- eventualmente listam vítimas que nunca comprometeram de fato.

Registros incluídos manualmente a partir de OSINT trazem o selo explícito
**`ALLEGED · UNCONFIRMED`**. A ausência desse selo num registro raspado **não** o promove a
confirmado — significa apenas que ele veio do site do próprio grupo.

Se você está prestes a dizer a alguém que a empresa dela aparece aqui, diga **"um grupo de
ransomware publicou uma alegação citando vocês"**. Essa frase é verdadeira. "Vocês foram
invadidos" pode não ser.

---

## `/campaigns` — Operações ativas

**[ctiwatch.com/campaigns](https://ctiwatch.com/campaigns)**

**112** campanhas ativas no momento. Uma campanha agrupa a atividade de um ator num período
com uma forma: quem ele atingiu, onde, em que janela.

As campanhas são construídas automaticamente a partir do dado de vítimas e da inteligência
sobre atores, e depois cruzadas com o feed de notícias.

### Como usar

Use para responder *"isso ainda está acontecendo?"*. O perfil do ator diz do que o grupo é
capaz; a campanha diz se ele está fazendo isso **neste mês**. Quando uma campanha bate com o
seu setor ou a sua região, aí sim vale ler o perfil do ator inteiro.

### ⚠️ Saiba disso

Os limites de uma campanha são inferidos, não declarados. Ninguém publica data de início e
fim de uma operação de ransomware, então a plataforma infere as janelas de atividade a partir
de **evidência datada** — data de publicação de vítimas e menções em artigos. Campanha marcada
como ativa tem evidência na janela recente; a ausência de campanha não significa que o grupo
está dormente, apenas que ele não publicou recentemente.

---

## `/malware` — Famílias de malware

**[ctiwatch.com/malware](https://ctiwatch.com/malware)**

**3.500+** famílias de malware, importadas do
[Malpedia](https://malpedia.caad.fkie.fraunhofer.de/) — Windows, Linux, Android e macOS —
com apelidos, TTPs e atribuição a atores onde ela existe.

### Como usar

A função principal aqui é **tradução**. Um relatório de incidente cita um loader; você
precisa saber a que família ele pertence, quem usa e o que costuma vir depois. Busque o nome,
leia a família e siga a atribuição de volta para [`/threats`](#threats--diretório-de-atores).

### ⚠️ Saiba disso — o mesmo nome significa coisas diferentes

Nome de malware colide o tempo todo, e a colisão é perigosa justamente porque parece
correspondência. Exemplos reais desta base:

- **MEDUSA** é um rootkit aqui *e* o nome de uma operação de ransomware;
- **Anubis** é um trojan bancário de Android *e* o nome de um grupo de ransomware;
- **Chaos** é um implante SSH para Linux *e* um construtor de ransomware.

Antes de concluir "o grupo X usa o malware Y porque os nomes batem", confira se o
comportamento também bate. A plataforma aplica exatamente esse teste internamente antes de
ligar um ator a uma família.
