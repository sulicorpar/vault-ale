---
name: vidiq
description: Pesquisa de vídeos de maior performance no vidIQ. Abre app.vidiq.com com o login do Marcelo via Playwright MCP, busca o tema solicitado e retorna os vídeos com mais views/VPH/outlier score sobre o assunto. Use quando o Marcelo pedir "pesquisa no vidiq", "o que tá bombando sobre X", "top videos sobre X", "outliers de X" ou similar.
---

# vidIQ — Pesquisa de Videos que Bombaram

Abre o vidIQ logado via Playwright MCP, procura um tema e retorna os vídeos que mais performaram sobre o assunto (views, VPH, outlier score).

## Invocacao

- `/vidiq <tema>` — pesquisa o tema e traz top videos
- `/vidiq claude code obsidian` — exemplo

## Pre-requisitos

- **Cookies do vidIQ importados no Playwright** (dominio `.vidiq.com`)
  - Se nao existem: rodar `/setup-browser-cookies` e selecionar `vidiq.com` / `app.vidiq.com`
- Conta vidIQ Boost ou superior (pra acessar Outliers/Keyword Inspector)

## Workflow

### Passo 1 — Abrir e verificar login

Navegar pra `https://app.vidiq.com/` via `mcp__playwright__browser_navigate`.

Depois `mcp__playwright__browser_snapshot` pra ver a pagina.

**Se aparecer tela de login (Sign in / Email / Password):**
- Parar e pedir pro Marcelo: "Os cookies do vidIQ expiraram. Roda `/setup-browser-cookies` e seleciona `vidiq.com` no picker."

**Se aparecer o dashboard:** continuar.

### Passo 2 — Navegar pra pesquisa de keywords/outliers

O vidIQ tem algumas ferramentas que servem pra esse caso:

1. **Keyword Inspector** — `https://app.vidiq.com/keywords` (ou `/research/keywords`) — busca por keyword + mostra videos relacionados com score
2. **Outliers** — videos que explodiram acima da media do canal (pesquisa por tema tambem)
3. **Search** na barra superior — busca geral

**Estrategia:** na primeira execucao, usar `browser_snapshot` pra mapear o menu lateral e descobrir as URLs/botoes exatos. Salvar os seletores no fim desse arquivo (secao "Seletores Mapeados") pra proximas execucoes.

Tentar primeiro **Keyword Inspector** (traz videos top sobre a keyword). Se nao tiver essa feature no plano atual, cair pra **Search** ou **Outliers**.

### Passo 3 — Executar a busca

Com o tema que o Marcelo passou:
1. Localizar o input de busca (via snapshot)
2. `mcp__playwright__browser_type` com o tema
3. Submeter (Enter ou clique no botao)
4. `mcp__playwright__browser_wait_for` ate os resultados carregarem

### Passo 4 — Extrair top videos

Usar `mcp__playwright__browser_evaluate` pra pegar os dados da tabela de resultados. Estrutura alvo:

```js
// Exemplo de extracao (ajustar seletores conforme mapeamento)
const rows = document.querySelectorAll('[data-testid="video-row"], tr[role="row"], .video-result');
const videos = [];
rows.forEach(row => {
  const title = row.querySelector('a[href*="youtube.com/watch"], .video-title')?.textContent?.trim();
  const channel = row.querySelector('.channel-name, [data-testid="channel"]')?.textContent?.trim();
  const views = row.querySelector('.views, [data-testid="views"]')?.textContent?.trim();
  const vph = row.querySelector('.vph, [data-testid="vph"]')?.textContent?.trim();
  const outlier = row.querySelector('.outlier, [data-testid="outlier"]')?.textContent?.trim();
  const url = row.querySelector('a[href*="youtube.com/watch"]')?.href;
  if (title) videos.push({title, channel, views, vph, outlier, url});
});
return JSON.stringify(videos.slice(0, 15));
```

Se os seletores nao baterem na primeira rodada:
- Tirar screenshot com `mcp__playwright__browser_take_screenshot` pra debugar
- Usar `browser_snapshot` pra mapear estrutura real
- Atualizar os seletores na secao "Seletores Mapeados" abaixo

### Passo 5 — Reportar pro Marcelo

Apresentar em markdown:

```markdown
## vidIQ — Top Videos: "{tema}"
_Pesquisa: {data}_

| # | Titulo | Canal | Views | VPH | Outlier |
|---|--------|-------|-------|-----|---------|
| 1 | ... | ... | ... | ... | ... |
...

### Insights
- Canal recorrente: ...
- Formula de titulo dominante: ...
- Outliers extremos: ...
```

### Passo 6 — Salvar historico

Salvar em `conteudo/vidiq-pesquisas/YYYY-MM-DD-<tema-slug>.md` com:
- Tema pesquisado
- Data
- Tabela completa
- URL do vidIQ da busca (pra reabrir)
- Insights

Criar a pasta `conteudo/vidiq-pesquisas/` se nao existir.

Se ja existe pesquisa recente do mesmo tema (< 7 dias), avisar o Marcelo e perguntar se quer refazer ou reaproveitar.

## Seletores Mapeados (vidIQ — mapear na 1a execucao)

| Elemento | URL / Seletor |
|----------|---------------|
| Dashboard logado | `https://app.vidiq.com/` — verificar presenca de `[data-testid="user-menu"]` ou similar |
| Keyword Inspector | TBD |
| Input de busca | TBD |
| Botao de submit | TBD |
| Linha de resultado | TBD |
| Titulo do video | TBD |
| Canal | TBD |
| Views | TBD |
| VPH | TBD |
| Outlier score | TBD |
| URL do YouTube | TBD |
| Tela de login | presenca de input `[type="email"]` + `[type="password"]` |

**Primeira execucao:** rodar `browser_snapshot` no dashboard e no resultado de busca, colar os seletores reais aqui, commitar.

## Notas

- Rate limit: vidIQ pode limitar buscas excessivas — nao rodar em loop sem intervalo
- Cookies podem expirar — se der tela de login, `/setup-browser-cookies` pra reimportar dominio `vidiq.com`
- Se o tema nao retornar resultados no Keyword Inspector, tentar pelo Outliers (filtrar por keyword)
- Sempre extrair no minimo 10 videos, idealmente 15 pra ter amostragem boa
- Incluir URL do YouTube de cada video no relatorio pra o Marcelo poder abrir direto
- Se o Marcelo estiver planejando conteudo novo (ver `conteudo/`), cruzar com os videos encontrados pra sugerir formulas de titulo que estao bombando
