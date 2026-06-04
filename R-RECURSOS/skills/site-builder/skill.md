# Skill: site-builder — Landing Page de Infoproduto em 1 HTML

Cria landing page completa pra infoproduto/SaaS em **HTML único**, no padrão CODA Editorial Halftone, mobile-first, com captura Supabase + Meta Pixel + checkout Cakto pré-fiado.

## Quando invocar

`/site-builder <tema do produto>` — ou pedindo "use a skill site-builder pra criar a landing do produto X".

Marcelo usa pra: lançamento de live, info-produto, app SaaS, captura de lead, manifesto.

## Inputs esperados

Antes de gerar, perguntar/confirmar:

1. **Brief do produto:** público, dor, promessa, mecanismo (como entrega), ticket
2. **Branding:** CODA Dark (default), CODA Light, ou DESIGN.md customizado
3. **Domínio Vercel:** `<nome>.vercel.app` (ou custom)
4. **Integrações:** Supabase (tabela leads), Cakto (URL checkout), Meta Pixel (ID)

Se não tiver, usar defaults:
- Supabase: `kzarkxwdvbridhsvgatn`, tabela `leads_<slug>`, source `<slug>-<data>`
- Meta Pixel: `<YOUR_META_PIXEL_ID>`
- Cakto: pedir URL ao usuário

## Estrutura do HTML único

```
<!DOCTYPE html>
<html>
<head>
  - meta tags + og + twitter cards
  - Google Fonts: Space Grotesk + Inter (CODA Dark) ou JetBrains Mono (Halftone)
  - <style> inline (NÃO criar arquivos separados)
  - Meta Pixel snippet
</head>
<body>
  - HEADER fixo top (asterisco + nome + data badge)
  - HERO (manchete editorial + sub + visual + CTA)
  - MANIFESTO / POSICIONAMENTO (3-5 parágrafos punchy)
  - SEÇÃO COMO VAI SER (3 cards numerados ou jornada conectada)
  - PRA QUEM É (checklist 4 itens)
  - FORM CTA (nome, whatsapp mascarado, email)
    → POST Supabase REST
    → fbq('track', 'Lead')
    → redirect/CTA pro link Cakto OU YouTube live
  - FOOTER mínimo
</body>
</html>
```

## Padrões CODA Dark Editorial Halftone (default)

- BG `#000000` puro (jamais dark gray)
- Accent `#FF5000` (laranja CODA — NÃO `#E8541E` antigo)
- Texto `#FFFFFF` puro · muted `#B0B0B0` · dim `#666`
- Display: Space Grotesk Bold uppercase + letter-spacing -0.035em
- Mono: JetBrains Mono italic pra labels/lede
- Headlines editorial: quebrar em 4 linhas dramáticas, palavra-chave em laranja
- Hero pode ter imagem halftone (objeto concreto print + asterisco brushy)
- Pills com border laranja, mono uppercase white inside
- CTA: solid orange `#FF5000` text preto, radius 4px (NÃO pill 100px)
- Fundo grid sutil `#1a1a1a` opcional (graph paper)

## Padrões mobile-first

- `clamp()` em font-sizes
- `padding 80px 0` desktop · `60px 0` mobile
- Hero h1: `clamp(44px, 8.5vw, 118px)`
- Container: `max-width: 1100px; padding: 0 24px`
- `@media (prefers-reduced-motion: reduce){.fade-up{opacity:1;animation:none}}` SEMPRE

## Integrações canônicas (copy-paste)

### Supabase form submit

```js
const SUPABASE_URL = 'https://kzarkxwdvbridhsvgatn.supabase.co';
const SUPABASE_KEY = '<anon_key>';
async function submitLead(name, whatsapp, email) {
  await fetch(`${SUPABASE_URL}/rest/v1/leads_<slug>`, {
    method: 'POST',
    headers: {'Content-Type':'application/json','apikey':SUPABASE_KEY,'Authorization':`Bearer ${SUPABASE_KEY}`},
    body: JSON.stringify({name, whatsapp, email, source:'<slug>-<data>', ..._utm, created_at: new Date().toISOString()})
  });
  if (typeof fbq !== 'undefined') fbq('track','Lead',{content_name:'<nome>'});
}
```

### Meta Pixel

```html
<script>
!function(f,b,e,v,n,t,s){if(f.fbq)return;n=f.fbq=function(){n.callMethod?n.callMethod.apply(n,arguments):n.queue.push(arguments)};if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';n.queue=[];t=b.createElement(e);t.async=!0;t.src=v;s=b.getElementsByTagName(e)[0];s.parentNode.insertBefore(t,s)}(window,document,'script','https://connect.facebook.net/en_US/fbevents.js');
fbq('init','<YOUR_META_PIXEL_ID>');
fbq('track','PageView');
</script>
```

### UTM capture

```js
const _utm = Object.fromEntries(['utm_source','utm_medium','utm_campaign','utm_content','utm_term'].map(k => [k, new URLSearchParams(location.search).get(k) || null]));
```

## Fluxo de execução

1. **Confirmar brief** — fazer 3 perguntas se faltar input
2. **Criar pasta:** `assets/sites/backlog/<slug>/` com `about.md` + `index.html`
3. **Gerar HTML único** — todas as integrações inline, NÃO criar arquivos separados (CSS, JS)
4. **Otimizar imagens** — se tiver vídeos, comprimir com ffmpeg (libx264 CRF 28, 1280px)
5. **Lazy-load** com IntersectionObserver pra mídia abaixo do fold
6. **Testar localmente** — abrir `file://...index.html` no Chrome se possível
7. **Sugerir invocar `/deploy-auto`** pra subir pro Vercel

## Referência canônica

Site gold standard: `assets/sites/prod/info-10k-claude/index.html` (https://info-10k-claude.vercel.app)

Use como template estrutural — copiar a arquitetura HTML/CSS, adaptar copy + brand.

## Convenções de pasta

- `assets/sites/backlog/<slug>/index.html` — site novo (não deployado)
- `assets/sites/prod/<slug>/index.html` — site no ar (mover ao deployar)
- Cada pasta tem `about.md` (status, url, repo, plataforma)

## Regras

1. **HTML único** — sempre 1 arquivo só, JS/CSS inline. Sem build step.
2. **Mobile-first** — desenhar pro mobile, escalar pra desktop.
3. **Captura sempre presente** — landing sem form é landing sem propósito.
4. **CODA Dark é default** — só desviar se brief explicitar outro branding.
5. **Sem bibliotecas externas pesadas** — só Google Fonts + Pixel + Supabase REST.
6. **`prefers-reduced-motion`** — safety net obrigatório.
7. **Após gerar:** sugerir `/deploy-auto` pra subir.
