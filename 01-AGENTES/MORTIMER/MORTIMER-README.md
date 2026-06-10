# 🤖 MORTIMER 2.1 — Super Assistente Pessoal ADS Consultor

> Documentação oficial | Atualizado: 10/06/2026
> Status: **EM PRODUÇÃO 24/7**

---

## 📌 RESUMO EXECUTIVO

MORTIMER é o assistente de IA da ADS Consultor para produção de entregáveis de marketing (copy, quiz, VSL, propostas, SEO-GEO-LLM) com qualidade nível JARVIS+. Roda 24/7 no VPS Hostinger com memória de conversa, módulo de tarefas, upload de anexos e CRM integrado.

| Item | Valor |
|------|-------|
| **URL** | https://mortimer.adsconsultor.com.br |
| **API Health** | https://mortimer.adsconsultor.com.br/api/health |
| **Tarefas (JSON)** | https://mortimer.adsconsultor.com.br/api/tasks |
| **Modelo IA** | claude-opus-4-6 (Anthropic) |
| **VPS** | Hostinger KVM 1 — 217.196.60.183 (Ubuntu 24.04) |

---

## 🏗 ARQUITETURA

```
Safari/Chrome (qualquer dispositivo)
    ↓ HTTPS
Traefik (Docker Swarm — portas 80/443, SSL automático)
    ↓
├── mortimer_mortimer-frontend (nginx:alpine)
│     └── serve /opt/mortimer/frontend/dist
└── mortimer_mortimer-backend (node:20-alpine)
      └── roda /opt/mortimer/backend/server.js
            ↓
      ├── API Anthropic (claude-opus-4-6, max_tokens 8096)
      └── Supabase (histórico + tarefas)
```

### Localização dos códigos

| Onde | Caminho | Função |
|------|---------|--------|
| **Mac (fonte)** | `~/mortimer-webapp/frontend/src/` | Código React editável |
| **Mac (fonte)** | `~/mortimer-webapp/backend/server.js` | Cópia local do backend |
| **VPS (produção)** | `/opt/mortimer/backend/server.js` | Backend REAL em execução |
| **VPS (produção)** | `/opt/mortimer/frontend/dist/` | Frontend buildado servido |

⚠️ O backend em `/root/mortimer-webapp` no VPS é cópia antiga — IGNORAR. O PM2 foi removido; tudo roda via Docker Swarm.

---

## ⚙️ FUNCIONALIDADES (v2.1)

1. **10 Módulos de marketing** — Post Instagram SEO-GEO-LLM, Copy Ads, Página de Vendas, VSL, Email/WhatsApp, Scripts SDR, Quiz, Mídia Paga, SEO-GEO-LLM, Proposta Comercial. Padrão mínimo de qualidade: nível JARVIS (personagens nomeados, dados numéricos, scripts palavra por palavra).
2. **Memória de conversa por sessão** — busca as últimas 6 interações (janela de 2h) da MESMA sessão no Supabase.
3. **Módulo de tarefas** — "agenda para amanhã X" → bloco [TASKS] invisível → salvo em `mortimer_tasks` → exposto em GET /api/tasks. Concluir: POST /api/tasks/:id/done.
4. **Upload de anexos** — 📎 no chat aceita PDF, JPG, PNG, GIF, WEBP (máx 10MB, base64). CDR NÃO é suportado (converter antes em cloudconvert.com/cdr-to-png).
5. **CRM de clientes** — dados em `frontend/src/clientsData.js` (estático). Card + detalhe com timeline, arquivos, tarefas.
6. **Botão WhatsApp** — campo `whatsapp: '55DDDNUMERO'` no clientsData → botão verde no detalhe abre wa.me direto.
7. **"Conversar com Mortimer sobre este cliente"** — cria sessão NOVA (zera memória) e envia o contexto do cliente automaticamente.

---

## 🚀 FLUXO DE DEPLOY (FRONTEND)

Sempre que editar qualquer arquivo em `~/mortimer-webapp/frontend/src/`:

```bash
cd ~/mortimer-webapp/frontend && npm run build && scp -r dist root@217.196.60.183:/opt/mortimer/frontend/
```

Depois: **Cmd+Shift+R** no navegador.

## 🚀 FLUXO DE DEPLOY (BACKEND)

Editar `/opt/mortimer/backend/server.js` direto no VPS (nano ou patch Python), depois:

```bash
docker service update --force mortimer_mortimer-backend
```

---

## 🛠 COMANDOS ÚTEIS (VPS)

```bash
# Conectar
ssh root@217.196.60.183

# Logs do backend
docker service logs mortimer_mortimer-backend --tail 50

# Reiniciar backend
docker service update --force mortimer_mortimer-backend

# Ver serviços rodando
docker service ls

# Testar API
curl -s https://mortimer.adsconsultor.com.br/api/health
```

---

## 🗄 SUPABASE

Projeto: dqfgozlhxrawnvgnpryv.supabase.co

| Tabela | Função |
|--------|--------|
| `mortimer_conversations` | Histórico: command, response, modulo, session_id |
| `mortimer_tasks` | Tarefas: cliente, titulo, detalhe, prazo, prioridade, status |

## 🔑 CREDENCIAIS

Todas em `/opt/mortimer/backend/.env` no VPS (e cópia em `~/mortimer-webapp/.env` no Mac):
- CLAUDE_API_KEY (key MORTIMER-OPUS do console.anthropic.com)
- SUPABASE_URL / SUPABASE_KEY
- AUTH_TOKEN

⚠️ Nunca commitar .env no git.

---

## 📋 ROADMAP

- [ ] **Clientes no Supabase** — tabela mortimer_clients + CRUD na interface ("+ Novo Cliente" sem build)
- [ ] **Dashboard de tarefas** — consumir GET /api/tasks na tela Dashboard com botão Concluir
- [ ] **Números de WhatsApp** dos demais clientes no clientsData.js
- [ ] **Upload de arquivos por cliente** — Supabase Storage na aba Arquivos
- [ ] **WhatsApp bidirecional** — falar com o MORTIMER pelo WhatsApp (Evolution API já no VPS)
- [ ] Skills claudetemplates.com.br para o VAULT (R$47-67 vitalício)

## 📝 CHANGELOG

**10/06/2026 — v2.1**
- Deploy completo no VPS via Docker Swarm + Traefik + SSL
- Memória de conversa por sessão (fix: mistura entre clientes)
- Módulo de tarefas com Supabase + API
- Upload de anexos (PDF/imagens) no chat
- CRM: Aplike adicionada, cidades corrigidas, status MMC=Ativo / Nutrolife=Em proposta
- Botão WhatsApp direto no detalhe do cliente
- Auto-envio de contexto ao clicar "Conversar sobre este cliente"

**09/06/2026 — v2.0**
- 10 módulos com padrão JARVIS+ no system prompt
- Modelo claude-opus-4-6 + key MORTIMER-OPUS
- Histórico no Supabase
- Fix: input vazio no frontend (JSON error)

---

## 🧭 PAPÉIS DAS FERRAMENTAS

| Ferramenta | Uso |
|------------|-----|
| **MORTIMER** | Produção diária de entregáveis para clientes |
| **Claude (claude.ai)** | Estratégia, arquitetura, evolução do MORTIMER |
| **Antigravity IDE** | Edição de código e navegação do VAULT |

Novo cliente: briefing no MORTIMER + `./novo_cliente.sh "NOME"` no VAULT (já cria 00-BRIEFING a 09-MATERIAIS).
