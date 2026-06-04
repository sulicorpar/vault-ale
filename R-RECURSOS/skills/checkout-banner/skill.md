# Skill: checkout-banner — Banner de Checkout Cakto

Gera banner de checkout (1280×720) e mockup de produto (1920×1080 hero) pro Cakto/landing page, no padrão CODA Editorial Halftone.

## Quando invocar

`/checkout-banner <produto>` — ou "cria banner do checkout do produto X".

Marcelo usa pra: banner do Cakto (página de pagamento) + mockup de produto pra hero da LP.

## Outputs

| Tipo | Pixels | Ratio | Onde usa |
|---|---|---|---|
| Banner Cakto | 1280×720 | 16:9 | Topo da página de checkout Cakto |
| Hero LP | 1920×1080 | 16:9 | Hero da landing (zoom no laptop/iPhone) |
| Mockup produto | 1080×1080 | 1:1 | Card "produto" em LP, anúncios |

## Inputs esperados

1. **Nome do produto** + 1 frase de promessa
2. **Ticket** (R$ X) e modelo (assinatura/one-shot)
3. **Branding:** CODA Editorial Halftone (default)
4. **DESIGN.md** se aplicável (paleta + tipo do produto específico)

## Estrutura do banner Cakto (1280×720)

```
┌────────────────────────────────────┐
│ [pill mono]                        │ ← top-left: nome do produto
│                                    │
│   HEADLINE EDITORIAL               │ ← linha branca + linha laranja
│   PROMESSA.*                       │
│                                    │
│   ▬▬▬                              │ ← divider laranja
│   sub mono italic                  │
│                                    │
│ [HALFTONE produto/laptop/visual] [BRUSHY ASTERISK]
│                                    │
│ R$ XX/MÊS · COMECE AGORA →         │ ← footer mono uppercase
└────────────────────────────────────┘
```

## Estrutura do mockup de produto (1080×1080)

```
┌────────────────────────────────────┐
│            [LAPTOP HALFTONE]       │
│       /                    \       │
│      /  TELA do app/site    \      │
│     /   rodando, halftone    \     │
│    /__________________________\    │
│              ╲___╱                 │
│                                    │
│   [BRUSHY ASTERISK ORANGE]         │
│                                    │
│  CODA · NOME DO PRODUTO            │
└────────────────────────────────────┘
```

## Template prompt NanoBanana — Banner Cakto

```
Premium editorial banner HORIZONTAL 1280x720 image in CODA Dark Editorial Halftone brand style. Pure black #000000 background. Aspect ratio 16:9.

Background: subtle thin grid lines (#1a1a1a). Sparse small orange #FF5000 sparkle particles in corners.

CRITICAL TEXT (Portuguese, exact rendering):
- All text Brazilian Portuguese, NO translation
- Render exactly what specified

LAYOUT (split horizontal):

LEFT 50% (text block):
- Top: rectangular pill with thin orange #FF5000 border, dark transparent fill, monospace uppercase white text "[PRODUTO]" inside, ~24px
- Headline 2 lines, bold condensed sans-serif uppercase, ~120px:
  - Line 1 WHITE "[HEADLINE_1]"
  - Line 2 ORANGE #FF5000 "[HEADLINE_2]" + brushy orange asterisk small after period
- Thin orange #FF5000 divider line ~120px wide
- Sub: monospace italic light gray (#9CA3AF) ~24px "[SUB]"
- Bottom row: orange #FF5000 monospace ~22px "R$ [PRECO]/MÊS · COMECE AGORA →"

RIGHT 50% (visual):
- HALFTONE-PRINTED illustration of [OBJETO/PRODUTO] in pure monochrome BLACK AND WHITE halftone dot pattern (1960s newspaper print, NOT 3D glossy). To the upper-right: HAND-DRAWN BRUSHY orange (#FF5000) 8-pointed asterisk (~140px), painted with imperfect brush strokes (NOT geometric, NOT 3D).

Style: editorial premium magazine cover, dark mood, bright orange punctuation, halftone illustration. NYT Magazine / A24 poster vibe. NO photorealistic 3D. NO glossy plastic.

ONLY exact text specified. NO extra labels, NO English, NO logos.
```

## Template prompt NanoBanana — Mockup de produto

```
Premium editorial PRODUCT MOCKUP image, SQUARE 1080x1080, in CODA Dark Editorial Halftone brand style. Pure black #000000 background. Aspect ratio 1:1.

Background: subtle thin grid lines (#1a1a1a). Sparse small orange #FF5000 sparkle particles in corners.

CRITICAL TEXT (Portuguese, exact):
- Render exactly what specified

LAYOUT:

CENTER (~70% of vertical, y=120 to y=820):
A HALFTONE-PRINTED illustration of [LAPTOP / iPHONE / DEVICE] in 3/4 isometric view, with the screen showing a stylized mockup of [PRODUTO]: [DESCRIÇÃO DO QUE APARECE NA TELA]. The device and screen rendered in pure monochrome BLACK AND WHITE halftone dot pattern (1960s newspaper print, NOT 3D glossy render).
To upper-right of device: HAND-DRAWN BRUSHY orange (#FF5000) 8-pointed asterisk (~150px), hand-painted brush strokes.

BOTTOM (y=890 to y=1020):
- Bold sans-serif uppercase WHITE text "[PRODUTO]" centered, ~70px, letter-spacing negative
- Below in monospace orange #FF5000 ~18px centered: "CODA · COMUNIDADECODA.COM"

Style: editorial premium magazine product photography, dark mood with orange punctuation, halftone illustration print. NOT photorealistic 3D, NOT glossy.

ONLY exact text specified.
```

## Headlines que funcionam (catálogo)

Pra **assinatura SaaS/app** (R$19-97/mês):
- "100 FUNCIONÁRIOS." + "POR R$X/MÊS." (volume + ticket baixo)
- "1 PROMPT." + "TUDO ISSO." (simplicidade)
- "ENQUANTO VOCÊ DORME." + "VENDE." (passive income hook)
- "CHEGA DE [DOR]." + "AGORA TEM ISSO." (alívio)

Pra **one-shot** (R$197-997):
- "LANÇAMENTO." + "[PRODUTO]." (frame de marco)
- "ACABOU." + "[O QUE ANTES ERA RUIM]." (transformação)
- "100% [BENEFÍCIO]." + "0% [DOR]." (math editorial)

## Variáveis a coletar antes de gerar

```yaml
produto: <nome do app/SaaS>
promessa: <1 frase, max 15 palavras>
ticket: <R$ X, modelo>
publico_alvo: <ICP em 1 frase>
visual_central: <halftone object — laptop/iphone/specific item>
headline_l1: <linha branca>
headline_l2: <linha laranja, com final period>
sub: <lede mono italic max 80 chars>
```

## Output paths

- Banner Cakto: `<projeto>/checkout-banner.png`
- Hero LP: `<projeto>/hero-mockup.png`
- Mockup produto: `<projeto>/produto-mockup.png`

## Regras

1. **Editorial Halftone é o default** — ama esse branding
2. **Asterisco brushy** sempre, NUNCA 3D glossy
3. **Texto curto** no banner — mais de 4 linhas vira ruim em diffusion model
4. **R$ no banner** sempre que aplicável (cria âncora de preço)
5. **Após gerar:** abrir Finder + perguntar pro Marcelo aprovar
6. **Variantes:** se ele não gostar, mudar o objeto halftone (catálogo na skill `/branding-coda`)

## Workflow combinado

Quando user pedir "banner de checkout + mockup pra LP", gerar **AMBOS em paralelo** (1 call cada, async). Dá pra rodar via background bash com 2 scripts.
