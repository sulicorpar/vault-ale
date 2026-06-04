---
name: gpt-image
description: Gera slides e imagens via GPT Image 2 (OpenAI) — roda no fal.ai até a API oficial abrir em maio/2026. Usa branding e conteúdo das pastas do projeto. Suporta multi-turn edit sem drift.
tags: [skill]
---

Gera imagens/slides usando **GPT Image 2** (modelo `gpt-image-2` da OpenAI). Paralela à skill `/nanobanana` — use esta quando precisar de:
- **Texto dentro da imagem** (slides, infográficos, thumbs com headline)
- **Multi-turn edit** sem perder identidade (personagem/cena consistente em várias versões)
- **100+ elementos** na mesma cena sem virar sopa
- **2K nativo** com reasoning (modo "thinking")

Pra gerações estéticas rápidas/pixel art CODA, `/nanobanana` continua sendo a escolha.

## Fluxo

1. Perguntar ao Marcelo: **"Qual bloco/tema e qual provider? (fal|openai)"** — default `fal`
2. Ler o branding relevante em `referencias/branding/` (ex: `branding-nanobanana-slides.md` pra slides YouTube, `branding-coda.md` pra CODA, `branding-youtube-apple.md` pra dashboards)
3. Ler o conteúdo do bloco correspondente
4. Ler referências visuais na pasta do bloco se houver
5. Montar o prompt combinando branding + conteúdo + referências
6. Chamar API (fal por default, openai quando liberar)
7. Salvar o resultado na pasta do bloco correspondente

## Providers

### Provider `fal` (default — disponível agora)

**Endpoint:** `https://fal.run/fal-ai/gpt-image-2`
**API Key:** variável de ambiente `FAL_KEY`
**Docs:** https://fal.ai/models/fal-ai/gpt-image-2

```bash
curl -s "https://fal.run/fal-ai/gpt-image-2" \
  -H "Authorization: Key ${FAL_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "PROMPT_AQUI",
    "image_size": "landscape_16_9",
    "num_images": 1,
    "quality": "high",
    "reasoning": true
  }' | python3 -c "
import sys, json, urllib.request
resp = json.load(sys.stdin)
url = resp['images'][0]['url']
urllib.request.urlretrieve(url, 'OUTPUT_PATH')
print('Imagem salva em OUTPUT_PATH')
"
```

**Parâmetros úteis:**
- `image_size`: `square_hd` (thumbs YouTube), `landscape_16_9` (slides), `portrait_9_16` (reels/stories), `landscape_4_3`
- `quality`: `low` | `medium` | `high` (default `medium`) — `high` ativa 2K
- `reasoning`: `true` pra ativar modo thinking (planeja antes de gerar, mais lento mas muito melhor pra texto/layout)
- `num_images`: 1-4

**Multi-turn edit (diferencial do GPT Image 2):**
Passar `image_url` (URL pública ou data URI) + novo prompt. O modelo mantém identidade entre edições sem drift.

```json
{
  "prompt": "mesmo personagem, mas agora segurando um laptop",
  "image_url": "https://.../primeira-imagem.png",
  "image_size": "landscape_16_9"
}
```

### Provider `openai` (oficial — abre ~maio/2026)

Quando liberar, trocar provider na chamada. Payload praticamente idêntico ao `gpt-image-1` atual:

```bash
curl -s "https://api.openai.com/v1/images/generations" \
  -H "Authorization: Bearer ${OPENAI_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-image-2",
    "prompt": "PROMPT_AQUI",
    "size": "1536x1024",
    "quality": "high",
    "n": 1
  }'
```

Response vem em `data[0].b64_json` (base64) ou `data[0].url` dependendo do param `response_format`.

## Montagem do prompt

Combinar branding + conteúdo + instruções específicas do GPT Image 2:

```
Crie um slide de apresentação 16:9.

ESTILO VISUAL:
[conteúdo de referencias/branding/*.md do contexto]

CONTEÚDO DO SLIDE:
- Título: "[TÍTULO DO SLIDE]"
- Subtítulo: "[se houver]"
- Elementos visuais: [descrição]

TEXTO NA IMAGEM:
Renderizar EXATAMENTE: "[texto que deve aparecer]"
Fonte: [serif/sans-serif, bold/regular]

Minimalista, muito espaço negativo, hierarquia clara.
```

**Diferenciais do GPT Image 2 no prompt:**
- Pode pedir texto multilíngue preciso (português acentuado, japonês, árabe — todos funcionam)
- Pode listar 100+ elementos numa cena complexa
- Modo reasoning (`reasoning: true`) faz layout + verificação do output automaticamente
- Edição multi-turn preserva identidade — ideal pra séries de slides com mesmo personagem/cena

## Padrões de uso por contexto

### Slides YouTube (branding CODA)
- Branding: `referencias/branding/branding-nanobanana-slides.md` + `branding-coda.md`
- Size: `landscape_16_9`, quality `high`, reasoning `true`
- Salvar em: `conteudo/YYYY-MM-DD-tema/slide-NN-nome.png`

### Thumbs YouTube
- Branding: `referencias/branding/branding-youtube-apple.md`
- Size: `square_hd` ou custom 1280x720, quality `high`
- Estilo: cinematográfico/Renascentista/3D premium (evitar "cara chocada + texto gigante")
- Salvar em: `assets/thumbnails/[video-id].png`

### Criativos CODA/Ads
- Branding: `referencias/branding/branding-coda.md` + `branding-criativos-live-gratuita.md`
- Size: `portrait_9_16` (stories/reels) ou `square_hd` (feed)
- Salvar em: `campanhas/[nome-campanha]/aprovados/` ou `descartados/`

### Dashboards/Landing Pages
- Branding: `referencias/branding/branding-youtube-apple.md` (Apple black)
- Size: `landscape_16_9`
- Salvar em: `assets/sites/[nome]/mockups/`

## Onde salvar

Sempre dentro da pasta do contexto correspondente — nunca no root.

Padrão de nome: `[tipo]-[tema-curto].png` (ex: `slide-fundamentos.png`, `thumb-segundo-cerebro.png`, `ad-coda-hook1.png`).

## Setup inicial (rodar uma vez)

Se `FAL_KEY` não estiver no env:

1. Criar conta em https://fal.ai/ (login com Google serve)
2. Dashboard → API Keys → Create Key
3. Adicionar ao `~/.zshrc`: `export FAL_KEY="fal_xxx..."`
4. `source ~/.zshrc`

Pra provider `openai` (quando abrir): usar a mesma `OPENAI_API_KEY` que você já tem pra outras skills.
