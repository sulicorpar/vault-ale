# YouTube Thumbnail Generator

Gera thumbnails para YouTube no estilo Nate Herk + branding CODA, otimizadas para CTR.

## Invocacao

`/thumb-yt <tema ou titulo do video>` — o tema e passado como argumento.

Se nao houver argumento, perguntar: "Qual o tema do video?"

## Padroes de Thumb que Funcionam (baseado em analise do @nateherk)

### Regras de Ouro

1. **MAX 3-5 PALAVRAS** — texto enorme, legivel em tamanho pequeno (mobile)
2. **MAX 3 ELEMENTOS** — texto + visual principal + 1 elemento secundario. Nunca mais que isso
3. **CONTRASTE EXTREMO** — fundo escuro + elementos vibrantes. Nada sutil
4. **1 EMOCAO POR THUMB** — escolher UMA: choque, curiosidade, medo, poder, urgencia
5. **PONTUACAO DRAMATICA** — ponto final = autoridade ("It's here."), interrogacao = curiosidade gap
6. **SEMPRE USAR O CLONE DO MARCELO** — rosto em todas as thumbs (padrao Nate Herk). Fotos em `assets/imagens/clone-marcelo/`. Enviar a imagem como `inlineData` no prompt da API Gemini. Alternar entre as 3 fotos pra variar angulo

### Clone do Marcelo (fotos de referencia)

Sempre incluir o rosto do Marcelo nas thumbnails, usando as fotos de clone:

| Foto | Arquivo | Melhor uso |
|------|---------|------------|
| Frontal closeup | `freepik__retrato-closeup-frontal-enquadramento-do-peito-par__50553.png` | Expressao chocada, olhando pra camera |
| 3/4 virado direita | `freepik__retrato-trsquartos-virado-levemente-direita-cabea-__50552.png` | Olhando pro texto, preocupado |
| Cinematic | `freepik__ultraphotorealistic-professional-cinematic-portrai__50551.png` | Serio, confiante, autoritario |

**Path:** `assets/imagens/clone-marcelo/`

**Como enviar pra API:** usar `inlineData` com base64 da imagem no payload JSON. Como a imagem e grande demais pro argumento do curl, salvar o payload como arquivo JSON com Python e usar `curl -d @/tmp/payload.json`

### Formulas que Convertem (escolher 1 por thumb)

| Formula | Exemplo | Emocao |
|---------|---------|--------|
| **Numero Chocante** | "27 ANOS" / "$10,000" / "93.9%" | Choque |
| **Afirmacao Curta** | "PODEROSO DEMAIS." / "Game Over." / "God mode." | Autoridade |
| **Curiosity Gap** | "NAO LIBERARAM. POR QUE?" / "The truth" | Curiosidade |
| **Antes → Depois** | "Old → New" com seta | Transformacao |
| **Provocacao** | "PARE DE USAR ISSO." / "It feels unfair." | Urgencia/FOMO |
| **Nome do Produto** | "MYTHOS" / "/computer" grande | Novidade |

### Estilo Visual (branding CODA adaptado pra thumb)

- **Fundo:** preto puro (#000000)
- **Texto principal:** branco bold condensado uppercase, ENORME (ocupa 40-60% da thumb)
- **Destaque:** palavra-chave em laranja (#E8541E) ou verde (#00FF00) ou vermelho (#FF0000)
- **Robots:** pixel art laranja (#E8541E) isometricos — mascotes CODA
- **Asterisco:** laranja 6 pontas no canto (identidade CODA)
- **Logos/icones:** grandes, reconheciveis, com glow sutil
- **Setas:** brancas ou laranja quando usar formula antes/depois

### Mix de Fontes (recurso visual)

- Titulo principal: sans-serif bold condensada, uppercase
- Palavra destaque: mesma fonte mas em COR DIFERENTE (laranja, verde ou vermelho)
- Subtexto (se houver): sans-serif italic, cinza (#888888), menor

### Composicoes Padrao

**Layout A — Texto Dominante:**
```
┌─────────────────────────┐
│ *                       │
│                         │
│   TEXTO                 │
│   GIGANTE.    [visual]  │
│                         │
└─────────────────────────┘
```

**Layout B — Split (Antes/Depois):**
```
┌─────────────────────────┐
│ *                       │
│  [OLD]    →    [NEW]    │
│  visual        visual   │
│                         │
└─────────────────────────┘
```

**Layout C — Visual Dominante:**
```
┌─────────────────────────┐
│ *        TEXTO          │
│          CURTO.         │
│                         │
│    [visual grande       │
│     centralizado]       │
└─────────────────────────┘
```

## Workflow

1. Receber o tema/titulo do video
2. Gerar 6 variacoes usando formulas diferentes:
   - 1x Numero Chocante
   - 1x Afirmacao Curta
   - 1x Curiosity Gap
   - 1x Provocacao
   - 1x Nome do Produto / Visual Dominante
   - 1x Antes/Depois (se aplicavel) ou variacao livre
3. Para cada thumb, montar o prompt NanoBanana combinando:
   - Estilo visual CODA (preto, pixel art laranja, asterisco)
   - Formula escolhida
   - Texto curto (max 5 palavras)
   - Visual correspondente
4. Gerar via API Gemini (mesmo fluxo do /nanobanana)
5. Salvar em `conteudo/<pasta-do-video>/thumb-XX-nome.png`
6. Mostrar todas pro Marcelo escolher

## Prompt Base para NanoBanana

```
Create a 16:9 YouTube thumbnail. Style: pure black background (#000000). 
Bold condensed sans-serif font, uppercase, tight tracking. 
Orange pixel art robots (#E8541E) as visual elements. 
Isometric pixel art style. Must be extremely eye-catching and clickable. 
High contrast. Text must be HUGE and readable at small sizes. 
Maximum 3-5 words of text. Orange 6-pointed asterisk top-left as brand identity.
[FORMULA]: [CONTEUDO ESPECIFICO]
```

## API

**Modelo:** `gemini-3.1-flash-image-preview`
**Endpoint:** `https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-flash-image-preview:generateContent`
**API Key:** variavel de ambiente `GEMINI_API_KEY`

### Chamada via curl

```bash
curl -s "https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-flash-image-preview:generateContent" \
  -H "Content-Type: application/json" \
  -H "x-goog-api-key: ${GEMINI_API_KEY}" \
  -d '{
    "contents": [{"role":"user","parts":[{"text":"PROMPT_AQUI"}]}],
    "generationConfig": {
      "responseModalities": ["TEXT", "IMAGE"],
      "candidateCount": 1,
      "temperature": 0.7
    }
  }' | python3 -c "
import sys, json, base64
resp = json.load(sys.stdin)
for part in resp['candidates'][0]['content']['parts']:
    if 'inlineData' in part:
        img_data = base64.b64decode(part['inlineData']['data'])
        with open('OUTPUT_PATH', 'wb') as f:
            f.write(img_data)
        print('Imagem salva em OUTPUT_PATH')
    elif 'text' in part:
        print(part['text'])
"
```

## Notas

- Sempre gerar 6 variacoes — quantidade ideal pra A/B test
- Thumbs sao 16:9 (padrao YouTube)
- Priorizar legibilidade em mobile (texto GRANDE)
- Nunca usar mais de 5 palavras no texto principal
- Cores de destaque: laranja (#E8541E), verde (#00FF00), vermelho (#FF0000)
- Gerar em lotes de 3 paralelos pra velocidade
