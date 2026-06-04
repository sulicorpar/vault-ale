---
name: proposta
description: Gera proposta comercial completa a partir de transcrição de reunião, áudio ou briefing — no padrão MGTInc.
tags: [skill]
---

Gerar uma proposta comercial profissional no padrão MGTInc a partir de uma transcrição de reunião, áudio transcrito ou briefing do usuário.

## Entrada esperada

O usuário vai colar ou referenciar:
- Transcrição de reunião (Fathom ou colada)
- Áudio transcrito
- Briefing livre (descrição do lead e o que ele precisa)
- Referência a um deal existente em `deals/`

## Passo 1 — Coletar contexto

Se a entrada não tem informação suficiente, perguntar apenas o que falta:
- **Quem é o lead?** (nome, empresa, o que faz)
- **Qual o problema dele?** (o que é manual, ineficiente, travado)
- **O que ele quer?** (automação, consultoria, SaaS, agentes)
- **Orçamento/expectativa de valor?** (se mencionou)
- **Quem apresenta a proposta?** (Raicon, Marcelo, outro)
- **Data da call?** (se souber)

Verificar `pessoas/` e `deals/` para contexto existente sobre o lead.

## Passo 2 — Gerar a proposta

Seguir EXATAMENTE esta estrutura markdown:

```markdown
# Proposta — [Título do Projeto] ([Nome do Lead])

**Data:** DD/MM/YYYY
**Lead:** [[slug-pessoa|Nome]]
**Apresenta:** [Quem vai apresentar] (call [horário se souber])

---

## O Problema
[2-4 frases descrevendo a dor real do lead, usando contexto da transcrição. Ser específico — mencionar processos, ferramentas e números quando possível.]

## A Solução
[1-2 frases descrevendo o que será entregue. Usar linguagem do Marcelo: "escritório virtual de IA", "agentes", "consultoria guiada", conforme o caso.]

---

## Escopo — [Nome da Fase/Formato] ([detalhes])

### [Entregável/Agente 1]
- [Detalhe específico]
- [Detalhe específico]

### [Entregável/Agente 2]
- [Detalhe específico]
- [Detalhe específico]

[Repetir para cada entregável]

> **Fase 2 (futuro):** [Mencionar expansão possível se fizer sentido]

---

## Entregáveis
- [Lista consolidada do que o lead recebe]
- [Incluir: sessões de calibração, documentação, suporte pós-entrega]

---

## Cronograma
| Semana | Entrega |
|--------|---------|
| 1 | [Imersão/validação — sempre começar com isso] |
| 2 | [Primeiro entregável funcional] |
| ... | ... |

---

## Investimento

[Se fizer sentido, apresentar 2-3 opções de preço em tiers]

### Opção 1 — [Nome] (recomendada)
**R$[Valor]** (ou Nx de R$[parcela])

- [O que inclui]
- [O que inclui]

### Opção 2 — [Nome]
**R$[Valor]** (ou Nx de R$[parcela])

- Tudo da Opção 1
- [Extras]

[Se for valor único, usar formato simples:]

**R$[Valor]**

- [O que inclui]
- [O que inclui]

---

## Riscos e Mitigações

| Risco | Mitigação |
|-------|-----------|
| [Risco técnico ou de processo] | [Como resolver] |

[Incluir apenas se houver riscos reais identificados na conversa]

---

## Por que a MGTInc

- Marcelo Anders transforma experts em donos de SaaS e escritórios virtuais de IA — é o core do negócio
- Experiência real com automação, N8N, Claude Code e multi-agentes
- Comunidade ativa de devs e operadores (Gather)
- [1-2 bullets específicos do contexto do lead — ex: experiência com e-commerce, ads, etc.]

---

## Recomendacao para o [Closer] na call

Apresentar a **[Opção recomendada]** como âncora principal. [Estratégia de pitch em 1-2 frases.]

> "[Frase de abertura sugerida para o closer — no tom do Marcelo: direto, técnico, sem enrolação]"

**Pontos para destacar:**
- [Ponto 1 — conectar com a dor do lead]
- [Ponto 2 — diferencial vs. alternativas]
- [Ponto 3 — redução de risco]

**Objecao provavel:** "[Objeção mais provável]"
**Resposta:** "[Resposta pronta para o closer]"

**Objecao provavel:** "[Segunda objeção se relevante]"
**Resposta:** "[Resposta]"
```

## Passo 3 — Salvar e atualizar

1. Salvar a proposta em `deals/[slug-lead]-[contexto]-proposta.md`
2. Se o deal já existe em `deals/`, atualizar o status e adicionar link para a proposta
3. Se não existe, criar o deal básico em `deals/`
4. Criar ou atualizar `pessoas/` do lead se tiver info nova

## Branding — Padrão Visual MGTInc (Apple Black)

Quando gerar o site da proposta (landing page HTML), seguir EXATAMENTE este design system:

### Cores (CSS Variables)
```css
:root {
  --bg: #000000;
  --card: #0a0a0a;
  --card-hover: #111111;
  --border: #222222;
  --text: #ffffff;
  --text-secondary: #888888;
  --text-muted: #555555;
  --accent: #2997ff;          /* azul Apple — links, ícones, destaques */
  --accent-glow: rgba(41, 151, 255, 0.15);
  --green: #22c55e;           /* positivo, ganho, incluso */
  --red: #ef4444;             /* negativo, não incluso, alerta */
  --glow: rgba(255, 255, 255, 0.06);
  --radius: 14px;
  --radius-sm: 10px;
}
```

### Tipografia
```css
font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', 'Inter', 'Helvetica Neue', sans-serif;
```
- **Hero H1:** `clamp(2.2rem, 6vw, 4rem)` weight 700, letter-spacing -1.5px
- **Seções H2:** `clamp(1.75rem, 4vw, 2.6rem)` weight 700, letter-spacing -1px
- **Body:** 16px-18px weight 400, line-height 1.7
- **Labels/badges:** 13px-14px weight 500, uppercase, letter-spacing 1px
- **Pesos usados:** 300 (light), 400 (regular), 500 (medium), 600 (semibold), 700 (bold)

### Espaçamento
- **Container:** max-width 900px, margin auto, padding 0 24px
- **Hero:** padding 120px top, 80px bottom
- **Seções:** padding 80px vertical
- **Cards:** padding 32px-40px, border-radius var(--radius)
- **Gap entre cards:** 20px-32px
- **Gap entre seções internas:** 48px

### Componentes
- **Cards:** background var(--card), border 1px solid var(--border), border-radius var(--radius), transition 0.3s ease, hover border-color #333
- **Timeline:** linha vertical 2px solid #333, dots 11px circles, semanas em var(--accent)
- **Pricing card:** max-width 560px, centered, box-shadow 0 0 80px rgba(255,255,255,0.04)
- **Badges:** background var(--accent-glow), color var(--accent), padding 8px 20px, border-radius 20px
- **Botões:** background var(--accent), color #000, padding 16px 32px, border-radius 12px, font-weight 600
- **Grids:** CSS Grid — 2 colunas para problema/solução e agentes, 1 coluna no mobile (768px breakpoint)
- **Inclusões:** bullets com ✓ em var(--green)
- **Exclusões:** bullets com ✗ em var(--red)

### Estrutura HTML
```
Hero (título + subtítulo + badge data)
→ O Problema (card escuro)
→ A Solução (card escuro)
→ Escopo / Agentes (grid de cards)
→ Entregáveis (lista com ✓)
→ Cronograma (timeline vertical)
→ Investimento (pricing card centralizado ou grid de tiers)
→ Por que MGTInc (lista)
→ CTA final (botão WhatsApp ou link)
```

### Regras
- Responsivo: breakpoint 768px (2col → 1col)
- Sem imagens externas — tudo CSS puro
- Sem JavaScript obrigatório — funciona sem JS
- Fonte Inter via Google Fonts como fallback se SF Pro não disponível
- Dark mode only — nunca light mode
- Transições suaves: 0.2-0.3s ease em hovers

---

## Regras de Tom e Estilo

- Linguagem direta, sem corporativês — como o Marcelo fala
- Números específicos sempre que possível (horas, campanhas, percentuais)
- Seção "Recomendação para o Closer" é OBRIGATÓRIA — é o que o Raicon usa na call
- Objeções e respostas são OBRIGATÓRIAS — antecipar pelo menos 1-2
- A frase de pitch deve soar natural, não como template
- Usar wikilinks `[[slug]]` para pessoas referenciadas
- Investimento: preferir modelo com opções/tiers quando o escopo permitir (ancora de preço)
- Semana 1 sempre = imersão/validação (nunca pular direto pra entrega)

## Perguntar ao final

> "Quer que eu gere o site da proposta também? (landing page no padrão Apple black)"
