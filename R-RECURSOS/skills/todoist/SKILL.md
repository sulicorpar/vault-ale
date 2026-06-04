---
name: todoist
description: Gerencia tarefas no Todoist — ver projetos, tasks, criar, editar, completar, deletar, mover entre seções, ver desempenho e gerar dashboards. Use quando quiser ver tarefas, organizar trabalho, ou acompanhar produtividade.
tags: [skill]
---

# Skill: Todoist — Gestão de Tarefas

## Autenticação

API Key fixa. Ler do arquivo `.env`:

```bash
TODOIST_API_KEY=$(grep TODOIST_API_KEY <YOUR_VAULT_PATH>/scripts/.env | cut -d= -f2)
```

Header em todos os requests: `Authorization: Bearer $TODOIST_API_KEY`

## Base URL

`https://api.todoist.com/api/v1/`

## Endpoints

### Projetos
- `GET /projects` → `results[]` com todos os projetos
- `GET /projects/{id}` → detalhe do projeto

### Seções
- `GET /sections?project_id={id}` → seções de um projeto
- `POST /sections` → criar seção `{ "project_id": "...", "name": "..." }`

### Tarefas
- `GET /tasks?project_id={id}` → tasks de um projeto (results[])
- `GET /tasks?project_id={id}&section_id={id}` → tasks de uma seção
- `GET /tasks/{id}` → detalhe da task
- `POST /tasks` → criar task
- `POST /tasks/{id}` → atualizar task
- `POST /tasks/{id}/close` → completar task
- `POST /tasks/{id}/reopen` → reabrir task
- `DELETE /tasks/{id}` → deletar task
- `POST /tasks/{id}/move` → mover task `{ "section_id": "..." }` ou `{ "project_id": "..." }`

### Criar task (POST /tasks)
```json
{
  "content": "Nome da tarefa",
  "description": "Descrição opcional",
  "project_id": "...",
  "section_id": "...",
  "priority": 1-4,
  "due_string": "today",
  "labels": ["label1"]
}
```
- priority: 1=normal, 2=medium, 3=high, 4=urgent

### Atualizar task (POST /tasks/{id})
```json
{
  "content": "Novo nome",
  "description": "Nova descrição",
  "priority": 3
}
```

### Completed tasks (histórico)
- `GET /tasks/completed?project_id={id}&since=2026-03-01T00:00:00&limit=200` → tasks completadas

## Projetos do Marcelo (cache)

| Projeto | ID | Tipo |
|---|---|---|
| Inbox | 6XQXwC85x9F4HXGq | pessoal |
| MGTInc | 6g829J43r352m5qH | empresa, compartilhado |
| Conteudos MGT | 6g82GvRJq4MrQ9jC | conteúdo, compartilhado |
| 19/03/2026 | 6gC9Fm96C7H23v8X | evento, compartilhado |
| LucidDream | 6gF2fhx9hgQWJCmQ | projeto Lucas, compartilhado |
| TAREFAS DE CADA 1 | 6gFMcCf6GW3HJ38V | delegação por pessoa |

## Seções importantes (cache)

### MGTInc
- Para Fazer: 6g82CVMQrCWgjm4q
- Semana 23/03/2026: 6gF76QVmwHGM7fcq
- Tasks passadas: 6g9xgF87XVmcpvxq
- A fazer - nao feito: 6gCFF74Jfrpq2PFH
- METAS: 6g9Rccwwq7gcpQvH
- Fazendo: 6g82CW4R6qhrwC8H
- Feito: 6g82CWHgQ75rx83q
- Tema LIVE: 6gFMVp5mFHRpFmRq
- Em espera: 6g82CWg4xc872Jjq
- Ideias de Agents: 6gFRpxP9Mf3j66pq

### Conteudos MGT
- Reels: 6g82Gw4WvRxHgp3j
- Youtube: 6g82GwQgjQX8FmqC
- Criativos: 6g82H2CmmXFPCJ9j
- Carrossel: 6g82GwmmjFg4mxhC
- Feitos: 6g82GxCvfVXR875j

### LucidDream
- A Fazer: 6gF2fp5RWxg5CxmQ
- Fazendo: 6gF2fpVWrPf5WpmQ
- Feito: 6gF2fpj4CX8gP4mx

### TAREFAS DE CADA 1
- THEO: 6gFMcFg54MHPMGVV
- MARCELO: 6gFMcG2jVJ4rm43V
- DAVI: 6gFMcGgwvWrc9JfV

## User IDs
- Marcelo: 53044541
- Davi: 39146014 (coproducer, colaborador)
- Theo: 57912349

## Comportamento da skill

### /todoist (sem argumentos) — Dashboard geral
1. Buscar tasks de TODOS os projetos
2. Apresentar resumo:

```
📋 Todoist — Dashboard

Projetos ativos: X
Tasks abertas: XX
Tasks por projeto:
  MGTInc: XX (Fazendo: X, Para Fazer: X, Em espera: X)
  Conteudos MGT: XX (Reels: X, Youtube: X, Criativos: X)
  LucidDream: XX
  TAREFAS DE CADA 1: Theo X, Marcelo X, Davi X

⚡ Urgentes (P4): lista...
🔴 Alta (P3): lista...

📅 Com deadline hoje: lista...
📅 Atrasadas: lista...
```

### /todoist {projeto} — Ver tasks do projeto
Ex: `/todoist mgtinc`, `/todoist conteudos`, `/todoist lucidream`
- Listar tasks agrupadas por seção
- Mostrar prioridade, responsável, deadline

### /todoist criar {texto} — Criar task
Ex: `/todoist criar Gravar reel sobre Claude Code no MGTInc`
- Parsear projeto do contexto ou perguntar
- Se não especificou seção, colocar em "Para Fazer" ou equivalente

### /todoist done {texto ou ID} — Completar task
Buscar task por nome parcial ou ID e marcar como completa.

### /todoist mover {task} para {seção} — Mover entre seções
Ex: `/todoist mover "Video Youtube" para Fazendo`

### /todoist deletar {task} — Deletar task
Confirmar antes de deletar.

### /todoist desempenho — Relatório de produtividade
1. Buscar tasks completadas dos últimos 7 dias
2. Calcular:
   - Tasks completadas por dia
   - Tasks completadas por projeto
   - Tasks completadas por pessoa (se compartilhado)
   - Taxa de conclusão (completadas vs criadas)
3. Apresentar com gráfico ASCII

### /todoist semana — Foco da semana
Listar tasks da seção "Semana" do MGTInc + tasks com deadline esta semana.

### /todoist {pessoa} — Tasks por pessoa
Ex: `/todoist theo`, `/todoist davi`, `/todoist marcelo`
- Buscar tasks assigned_to a pessoa
- Incluir projeto "TAREFAS DE CADA 1" da seção da pessoa

## Regras

1. Sempre usar API v1 (`/api/v1/`)
2. Resultados vêm em `results[]` com paginação via `next_cursor`
3. Ao criar task, sempre confirmar o projeto se ambíguo
4. Ao deletar, sempre pedir confirmação
5. Prioridades: 4=urgente (vermelho), 3=alta, 2=média, 1=normal
6. Datas: `due_string` aceita "today", "tomorrow", "next monday", "Mar 25"
7. Para mover task entre seções: `POST /tasks/{id}/move` com body `{"section_id": "..."}`
8. Para completed tasks: endpoint `/tasks/completed` retorna histórico

## Variações aceitas

- `/todoist` → dashboard geral
- `/todoist mgtinc` → tasks do MGTInc
- `/todoist conteudos` → tasks do Conteudos MGT
- `/todoist criar Fazer proposta do Kaká` → cria task
- `/todoist done Proposta do Kaká` → completa task
- `/todoist mover "Proposta" para Fazendo` → move task
- `/todoist deletar "Task antiga"` → deleta task
- `/todoist desempenho` → relatório semanal
- `/todoist semana` → foco da semana
- `/todoist theo` → tasks do Theo
- `/todoist davi` → tasks do Davi
- `/todoist urgentes` → lista P3 e P4
