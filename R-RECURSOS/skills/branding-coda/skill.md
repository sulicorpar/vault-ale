# Skill: branding-coda — Capas, Banners e Posts no Padrão CODA

Gera capa, post Instagram, banner ou thumb seguindo o branding CODA (Dark, Light ou Editorial Halftone) via NanoBanana (Gemini 3.1 Flash Image).

## Quando invocar

`/branding-coda <tema> <formato> [variante]` — ou "use a skill branding-coda pra criar capa de X".

Marcelo usa pra: capas de carrossel IG, capas de módulo, banners de live, thumbs YouTube, manifestos visuais.

## Variantes de branding

### A) CODA Dark (default — produto premium)
- BG preto puro `#000000`
- Accent laranja `#FF5000`
- Branco puro `#FFFFFF`
- Display: Space Grotesk Bold uppercase
- 3D glossy plastic blocks como elementos visuais (asterisco 3D)
- Asterisco geométrico perfeito 8 pontas
- **Quando usar:** capas Higgsfield-style, manifestos de live, carrosséis premium 3D
- **Referência:** `conteudo/higgsfield-mcp-2026-04-28/slides/`

### B) CODA Editorial Halftone (Marcelo AMA — gold standard atual)
- BG preto `#000000`
- Accent laranja `#FF5000`
- Halftone print preto-e-branco em fotos/objetos (1960s newspaper print)
- Asterisco brushy hand-painted (NÃO 3D glossy, NÃO geométrico perfeito)
- Display: Helvetica Black/Space Grotesk Bold uppercase
- Mono: JetBrains Mono italic pra lede/labels
- Pills com border laranja
- Grid sutil `#1a1a1a` (graph paper)
- **Quando usar:** capas magazine, posts editoriais IG, manifestos, banners checkout, capas live, emails
- **Receita visual** (Marcelo elogiou): objeto concreto halftone (relógio, laptop, chave, etc) + asterisco brushy laranja sobreposto + tipografia editorial gigante (branco + palavra-chave laranja) + sub mono italic
- **Referência:** `conteudo/live-2026-04-30/email-hero-hoje-halftone.png`, `conteudo/live-2026-04-30/menu-carrossel-v2/`

### C) CODA Light (institucional)
- BG `#F5F5F5`
- Accent verde `#749E15`
- Pra: comunidadecoda.com, dashboards, comunicação clean

## Formatos

| Formato | Pixels | Uso |
|---|---|---|
| Carrossel IG vertical | 1080×1350 (4:5) | Posts educacionais |
| Post IG quadrado | 1080×1080 | Quotes, anúncios |
| Story IG | 1080×1920 | Stories |
| Thumb YouTube | 1280×720 (16:9) | Thumb de vídeo |
| Banner email/checkout | 1200×600 (2:1) | Hero email, banner Cakto |
| Banner LP hero | 1920×1080 | Hero de landing page |

## Fluxo de execução

1. **Confirmar inputs** — tema, formato, variante (default: Editorial Halftone)
2. **Definir hierarquia visual:**
   - Pill mono no topo (label/categoria)
   - Visual halftone central (objeto concreto)
   - Asterisco brushy laranja sobreposto
   - Headline editorial split (linha branca + linha laranja)
   - Lede mono italic
   - Body / bullets (se densidade pedagógica)
   - Footer mono uppercase
3. **Construir prompt pro NanoBanana** seguindo template abaixo
4. **Chamar API Gemini 3.1 Flash Image** (`gemini-3.1-flash-image-preview`)
5. **Salvar PNG** no path apropriado da pasta do projeto
6. **Mostrar preview** pro usuário aprovar / regerar

## Template de prompt NanoBanana (Editorial Halftone)

```
Premium editorial collage [FORMATO] image in CODA Dark Editorial Halftone brand style. Pure black #000000 background. Aspect ratio [X:Y].

Background: subtle thin grid lines in very dark grey (#1a1a1a). Sparse small orange #FF5000 sparkle particles in corners.

CRITICAL TEXT INSTRUCTIONS:
- All text in Brazilian Portuguese — DO NOT translate
- Render EXACTLY: [TEXTO ESPECÍFICO]
- Portuguese accents (Ã, Õ, Á, É) correct
- LARGE and READABLE

LAYOUT:
- Top-left: small orange asterisco watermark (~50px) + monospace pill "[LABEL]"
- Center: HALFTONE-PRINTED illustration of [OBJETO CONCRETO] in pure monochrome BLACK AND WHITE halftone dot pattern (1960s newspaper print, NOT 3D glossy). To upper-right: HAND-DRAWN BRUSHY orange (#FF5000) 8-pointed asterisk (~140px), painted with imperfect brush strokes (NOT geometric perfect, NOT digital).
- Bottom 40%: editorial typography
  - Headline 2 lines: line 1 WHITE "[H1]", line 2 ORANGE (#FF5000) "[H2]". Bold condensed sans-serif uppercase, ~120px, letter-spacing negative.
  - Thin orange divider line ~80px
  - Sub: monospace italic light gray (#9CA3AF) ~26px "[LEDE]"
  - Footer: small uppercase orange mono "[FOOTER]"

Style: editorial premium magazine-poster, dark mood with bright orange punctuation, halftone printing on illustrated objects (1960s newspaper print, NOT photorealistic, NOT 3D render). NYT Magazine cover / A24 movie poster vibe.

ONLY exact text specified. NO English translation, NO extra labels, NO logos.
```

## API call

Modelo: `gemini-3.1-flash-image-preview`
Endpoint: `https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-flash-image-preview:generateContent`
API Key: `os.environ["GEMINI_API_KEY"]`

```python
import json, base64, urllib.request, os
API_KEY = os.environ["GEMINI_API_KEY"]
URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-flash-image-preview:generateContent"

payload = {
    "contents": [{"role": "user", "parts": [{"text": PROMPT}]}],
    "generationConfig": {"responseModalities": ["TEXT", "IMAGE"], "candidateCount": 1, "temperature": 0.7}
}
req = urllib.request.Request(URL, data=json.dumps(payload).encode("utf-8"),
    headers={"Content-Type": "application/json", "x-goog-api-key": API_KEY})
resp = json.loads(urllib.request.urlopen(req, timeout=180).read())
for part in resp["candidates"][0]["content"]["parts"]:
    if "inlineData" in part:
        with open(OUT_PATH, "wb") as f:
            f.write(base64.b64decode(part["inlineData"]["data"]))
```

## Objetos concretos halftone que funcionam (catálogo)

- **Tempo:** stopwatch analógico, relógio de parede vintage, ampulheta
- **Trabalho:** typewriter, laptop aberto, gears/engrenagens
- **Mensagem:** envelope com motion lines, speech bubble + envelope
- **Decisão:** dado 6-faces mid-air com motion blur, chave esquelética
- **Riqueza:** notas de R$ caindo, cofre, caixa registradora
- **Movimento:** foguete subindo, escada, esteira/conveyor belt
- **Obstáculo:** figura silhueta parada na escada (representa travado)

## Regras

1. **Editorial Halftone é o branding default** (Marcelo confirmou que ama)
2. **Asterisco SEMPRE brushy hand-painted** quando Editorial — nunca geométrico perfeito 3D
3. **Texto direto e literal** — Gemini renderiza exato o que você escreve, sem inferir
4. **Português correto** — sempre acentos certos, sem traduzir
5. **Após gerar:** salvar no path do projeto, abrir Finder, perguntar se aprova
6. **Em paralelo:** múltiplos slides podem rodar em background simultâneos (3-4 paralelos OK)

## Referência canônica completa

`referencias/branding/branding-manifesto-coda-dark.md` (CODA Dark)
`referencias/branding/branding-coda-editorial-halftone.md` (Editorial Halftone — default Marcelo)
