# Sua conta — faça a plataforma vigiar por você

[← Índice da documentação](README.md) · [🇬🇧 English](../en/account.md)

Tudo que as outras seções descrevem exige que você vá lá olhar. Esta seção é sobre o
contrário: configurar a plataforma para que ela venha até você.

---

## `/dashboard` — Sua página inicial

**[ctiwatch.com/dashboard](https://ctiwatch.com/dashboard)**

Inteligência global de ameaças em tempo real — indicadores, CVEs, ransomware e atividade APT
numa visão só, com os acertos das suas watchlists em destaque.

---

## `/watchlists` — O recurso mais útil da plataforma

**[ctiwatch.com/watchlists](https://ctiwatch.com/watchlists)**

Diga à plataforma quais palavras-chave importam para você. Quando elas aparecerem em dado
novo, ela te avisa.

### O que colocar numa watchlist

| Categoria | Exemplos |
|---|---|
| **Sua organização** | Nome fantasia, razão social, o nome antigo de antes da fusão |
| **Seus fornecedores** | Os softwares que você realmente usa — é assim que CVE de fabricante chega até você |
| **Seu setor e região** | O suficiente para pegar campanhas dirigidas a organizações como a sua |
| **Suas subsidiárias e marcas** | Atacante nomeia a entidade em que caiu, seja ela qual for |

### 🔴 O erro que todo mundo comete: palavra-chave curta

As palavras-chave casam **como trecho, sem fronteira de palavra**. Uma palavra curta vai casar
dentro de palavras maiores e te soterrar.

Um exemplo real desta plataforma: a palavra-chave **`ANS`** gerou 190 falsos positivos em
trinta dias, porque casa dentro de **tr·ANS·ferência**, **r·ANS·omware** e dezenas de palavras
comuns.

**Regras que mantêm a watchlist útil:**

- Nunca use palavra-chave com menos de cinco caracteres, a não ser que ela seja realmente
  distintiva.
- Prefira o nome inteiro à sigla — `Banco Exemplo` em vez de `BEX`.
- Se uma palavra-chave te inundar, não tolere. Watchlist que grita à toa é pior do que
  watchlist nenhuma, porque ela te treina a ignorar justamente a que importa.

### 💡 Palavra-chave de fabricante rende mais do que parece

Nome de fabricante numa watchlist casa com a descrição das CVEs *e* com o dado estruturado de
produto. Colocar ali os fabricantes dos softwares que você usa é um dos cinco minutos de maior
retorno disponíveis nesta plataforma: transforma "377.168 CVEs" em "as quatro que afetam
coisas que eu rodo".

---

## `/alerts` — Histórico de notificações

**[ctiwatch.com/alerts](https://ctiwatch.com/alerts)**

Todo acerto de watchlist, com situação de entrega. Os alertas também podem chegar por
**e-mail** e — se você instalar o aplicativo — como **notificação push**.

Dispensar um alerta suprime a notificação. Não apaga o dado por trás, e o evento continua
visível no feed público.

---

## `/settings/api-keys` — Chaves de API

**[ctiwatch.com/settings/api-keys](https://ctiwatch.com/settings/api-keys)**

Crie, inspecione e revogue chaves. O plano gratuito permite **100 requisições/dia por chave**.

```bash
curl -H "X-API-Key: $CTIWATCH_KEY" \
     "https://ctiwatch.com/api/v1/victims?country=BR&limit=50"
```

As chaves aceitam data de expiração e restrição por IP. Use as duas: chave que expira é chave
que não vaza para sempre.

**Rotacione a chave imediatamente se ela já esteve num repositório, num log de CI ou numa
captura de tela.** A revogação vale na hora.

---

## `/settings/security` — Segurança da conta

**[ctiwatch.com/settings/security](https://ctiwatch.com/settings/security)**

- **Autenticação em dois fatores (TOTP)** — suportada, e vale a pena ligar.
- **Troca de senha e de e-mail** — a troca de e-mail exige confirmação nos dois endereços.
- **Exclusão de conta** — processo em duas etapas, exigindo senha *e* confirmação por e-mail.
  É deliberadamente difícil de fazer sem querer.

---

## `/settings/billing` — Assinatura

**[ctiwatch.com/settings/billing](https://ctiwatch.com/settings/billing)**

Sua assinatura [Supporter](https://ctiwatch.com/support) e suas faturas, em autoatendimento.
Cobrada em **reais** para visitantes lusófonos e em **dólares** para os demais.

---

## `/settings/privacy` — Privacidade e dados

**[ctiwatch.com/settings/privacy](https://ctiwatch.com/settings/privacy)**

O que a plataforma guarda sobre você, e os controles sobre isso.

---

## Instale como aplicativo

O CTIWatch é um **progressive web app**. Apoiadores podem instalá-lo pelo navegador e ganhar
ícone de aplicativo, acesso offline às páginas já visitadas e notificações push dos acertos de
watchlist — sem passar por loja de aplicativos.

---

## Uma configuração de cinco minutos que se paga

1. Crie uma conta.
2. Crie uma watchlist com o **nome completo da sua organização** e suas variações.
3. Crie uma segunda watchlist com **os fabricantes que você de fato usa**.
4. Ligue os alertas por e-mail.
5. Ative a autenticação em dois fatores.

É toda a configuração. Daí em diante a plataforma lê 86 fontes no seu lugar e só te
interrompe quando algo bate.
