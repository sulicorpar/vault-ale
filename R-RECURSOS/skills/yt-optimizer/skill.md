# YouTube Optimizer — Assistente de A/B Test Contínuo

Loop infinito de otimizacao de CTR: checa testes finalizados, mantem o campeao, gera novos challengers com `/thumb-yt`, sobe e inicia novo teste.

## Invocacao

`/yt-optimizer` — sem argumentos. Ele checa todos os videos publicos automaticamente.
`/yt-optimizer <video-id>` — checa um video especifico.

## Pre-requisitos

- Cookies do YouTube importados no Playwright (dominio `.youtube.com` via `/setup-browser-cookies`)
- Skill `/thumb-yt` disponivel pra gerar thumbnails challengers
- Fotos clone em `assets/imagens/clone-marcelo/`
- Branding CODA em `referencias/branding/branding-criativos-live-gratuita.md`

## Branding dos Challengers

TODAS as thumbnails challengers DEVEM seguir o branding CODA dos criativos:
- **Fundo:** preto puro (#000000)
- **Texto:** sans-serif bold condensada, uppercase, tracking apertado
- **Destaque:** palavra-chave em laranja (#E8541E), verde (#00FF00) ou vermelho (#FF0000)
- **Robos:** pixel art laranja (#E8541E) isometricos
- **Asterisco:** laranja 6 pontas no canto (identidade CODA)
- **Clone do Marcelo:** SEMPRE incluir rosto do clone (fotos em `assets/imagens/clone-marcelo/`)
- **Max 3-5 palavras** de texto, legivel em mobile

Referencia completa: `referencias/branding/branding-criativos-live-gratuita.md`

Gerar thumbs via API Gemini com prompt base:
```
Create a 16:9 YouTube thumbnail. Style: pure black background (#000000).
Bold condensed sans-serif font, uppercase, tight tracking.
Orange pixel art robots (#E8541E) as visual elements.
Isometric pixel art style. Must be extremely eye-catching and clickable.
High contrast. Text must be HUGE and readable at small sizes.
Maximum 3-5 words of text. Orange 6-pointed asterisk top-left as brand identity.
Use the provided person photo with [EXPRESSION]. Remove white background, place on black.
[FORMULA]: [CONTEUDO ESPECIFICO]
```

Enviar foto do clone como `inlineData` no payload. Salvar payload como JSON em `/tmp/` e usar `curl -d @file.json` (imagem e grande demais pro argumento do curl).

## Auth — Injetar Cookies no Playwright

Antes de navegar pro YouTube Studio, SEMPRE injetar os cookies. Usar o MCP Playwright `browser_evaluate` pra setar os cookies via `document.cookie`:

```js
// Pegar cookies do gstack browse
// Depois setar no Playwright via document.cookie
// Navegar pra youtube.com primeiro, depois setar cookies, depois ir pro Studio
```

**Fluxo de auth:**
1. Navegar pra `https://www.youtube.com`
2. Injetar cookies via `browser_evaluate` (os cookies sao os importados do Comet via gstack browse)
3. Navegar pra `https://studio.youtube.com`
4. Verificar que carregou o "Painel do canal" (nao a tela de login)

Se der tela de login: pedir pro Marcelo reimportar cookies com `/setup-browser-cookies`.

## Workflow Principal

### Passo 1 — Listar videos publicos

Navegar pra `https://studio.youtube.com/channel/UCXK2fOoYibsFE6mrFYDrnfA/videos`

Extrair lista de videos com JavaScript:
```js
const rows = document.querySelectorAll('ytcp-video-row');
const videos = [];
rows.forEach(row => {
  const title = row.querySelector('a.video-title-text, .video-title-wrapper a')?.textContent?.trim();
  const allText = row.textContent;
  const isPublic = allText.includes('Público') || allText.includes('Public');
  const videoLink = row.querySelector('a[href*="/video/"]');
  const videoId = videoLink?.href?.match(/video\/([^/?]+)/)?.[1];
  if (title && isPublic) videos.push({title, videoId});
});
return JSON.stringify(videos);
```

### Passo 2 — Checar testes de cada video

Para cada video publico, navegar pra: `https://studio.youtube.com/video/{VIDEO_ID}/edit`

Verificar se existe botao "Abrir relatório do teste":
```js
const btn = Array.from(document.querySelectorAll('button, [role="button"], ytcp-button'))
  .find(b => b.textContent.includes('Abrir relatório do teste'));
```

Se existe → clicar e ler o relatorio.
Se nao existe → video sem teste ativo, oferecer criar um.

### Passo 3 — Ler relatorio do teste

Apos clicar "Abrir relatório do teste", a modal abre com:
- **Status:** "Temos uma opção vencedora!" ou "O teste foi finalizado sem um resultado conclusivo" ou "Teste em andamento"
- **Variacoes:** titulo + thumbnail + % watch time para cada
- **Periodo:** datas de inicio e fim
- **Botoes:** "Novo teste" e "Pronto"

Extrair dados com JavaScript:
```js
// Ler todos os textos da modal de relatorio
const modal = document.querySelector('ytcp-test-and-compare-report-dialog, [role="dialog"]');
const text = modal?.textContent;
// Parsear: titulos, percentuais, status
```

**Regra de decisao:**
- Se "Temos uma opção vencedora!" → campeao definido, gerar 2 novos challengers
- Se "sem um resultado conclusivo" → manter o de maior % como campeao, gerar 2 novos challengers
- Se "Teste em andamento" → pular, reportar status

### Passo 4 — Gerar novos challengers

Usar a skill `/thumb-yt` pra gerar 2 novas thumbnails challengers baseadas no tema do video.

**Importante:** O campeao (A) fica. So gera B e C.

Para titulos challengers: gerar 2 variacoes do titulo usando formulas diferentes:
- Numero chocante
- Curiosity gap
- Afirmacao curta
- Provocacao

### Passo 5 — Iniciar novo teste

1. Clicar "Novo teste" no relatorio
2. Confirmar na modal "Realizar novo teste?" → clicar "Novo teste"
3. No formulario que abre:
   - Opcao "Titulo e miniatura" (testar titulo + thumb juntos)
   - Subir as variacoes B e C (titulo + thumbnail)
4. Confirmar e iniciar teste

### Passo 6 — Reportar

Apresentar pro Marcelo:
```
## YouTube Optimizer — Relatório

### Video: [titulo]
- **Status anterior:** [vencedor/inconclusivo]
- **Campeão (A):** [titulo] — [%] watch time
- **Novo challenger B:** [titulo] — [thumb gerada]
- **Novo challenger C:** [titulo] — [thumb gerada]
- **Teste iniciado:** [sim/nao]

### Video: [titulo 2]
...
```

### Passo 7 — Salvar historico

Salvar log em `conteudo/yt-optimizer-log.md`:
```markdown
## [DATA]

### [Video titulo] (VIDEO_ID)
- Teste anterior: [A] vs [B] → vencedor: [X] ([%])
- Novo teste: [A campeao] vs [B novo] vs [C novo]
- Thumbs geradas: [paths]
```

## Seletores Mapeados (YouTube Studio — Abril 2026)

| Elemento | Seletor/Metodo |
|----------|---------------|
| Lista de videos | `ytcp-video-row` |
| Titulo do video | `a.video-title-text, .video-title-wrapper a` |
| Video publico | `row.textContent.includes('Público')` |
| Video ID | `href.match(/video\/([^/?]+)/)` |
| Botao relatorio | `textContent.includes('Abrir relatório do teste')` |
| Botao novo teste | `textContent.includes('Novo teste')` |
| Botao confirmar | `textContent === 'Novo teste'` dentro de dialog |
| Botao pronto | `textContent.trim() === 'Pronto'` |
| Botao cancelar | `textContent.trim() === 'Cancelar'` |
| Botao editar titulo | `textContent.includes('Editar título')` |
| Modal relatorio | `ytcp-test-and-compare-report-dialog` ou `[role="dialog"]` |
| Status vencedor | `textContent.includes('Temos uma opção vencedora')` |
| Status inconclusivo | `textContent.includes('sem um resultado conclusivo')` |

## Canal

- **Channel ID:** `UCXK2fOoYibsFE6mrFYDrnfA`
- **Studio URL:** `https://studio.youtube.com/channel/UCXK2fOoYibsFE6mrFYDrnfA`
- **Videos URL:** `https://studio.youtube.com/channel/UCXK2fOoYibsFE6mrFYDrnfA/videos`
- **Video edit:** `https://studio.youtube.com/video/{VIDEO_ID}/edit`

## Videos com testes mapeados (referencia)

| Video | ID | Ultimo teste | Resultado |
|-------|-----|-------------|-----------|
| Criei Meus Proprios MULTI-AGENTS... | LzLH6F5LPFw | 23/mar-6/abr | Inconclusivo (28.6% vs 32.7%) |
| PARE de pagar pelo Claude Code... | ufsvhLN_N7Y | 19/mar-20/mar | Vencedor: "Como usar Claude Code DE GRACA..." (36.3% vs 26%) |

## Notas

- YouTube permite max 3 variacoes por teste (A, B, C)
- Testes rodam ~2 semanas
- Campeao e definido por % de watch time (nao CTR)
- Se teste inconclusivo, a primeira variacao fica como padrao
- Cookies podem expirar — se der tela de login, reimportar com `/setup-browser-cookies`
- Nunca excluir um teste sem reportar os resultados pro Marcelo primeiro
- Sempre salvar historico em `conteudo/yt-optimizer-log.md`
