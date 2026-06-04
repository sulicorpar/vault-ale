---
name: lint
description: Auditoria periódica do vault no padrão LLM Wiki (Karpathy). Verifica contradições, páginas órfãs, info desatualizada, cross-references faltantes e gaps de conhecimento.
user-invocable: true
---

# /lint — Auditoria do Vault

Executa uma auditoria completa do vault Obsidian seguindo o padrão LLM Wiki do Karpathy.

## O que verificar

### 1. Páginas Órfãs
- Arquivos em `pessoas/` que não são mencionados em nenhum deal, reunião ou empresa
- Arquivos em `deals/` sem reuniões associadas
- Arquivos em `empresas/` sem deals ou pessoas linkadas

### 2. Informações Desatualizadas
- Deals com status desatualizado (verificar última atualização vs data atual)
- Pessoas com informações que podem ter mudado
- `CLAUDE.md` seção "Contexto Atual" — verificar se a semana/data está atualizada
- Referências a arquivos ou paths que não existem mais

### 3. Contradições
- Informações conflitantes entre `pessoas/` e `deals/` (ex: valores diferentes)
- Status de deal diferente entre `deals/` e `CLAUDE.md`
- Datas inconsistentes entre reuniões e deals

### 4. Cross-References Faltantes
- Reuniões que mencionam pessoas sem link para `pessoas/`
- Deals que mencionam empresas sem link para `empresas/`
- Conteúdo que referencia deals sem link

### 5. Gaps de Conhecimento
- Pessoas mencionadas em reuniões que não têm página em `pessoas/`
- Empresas mencionadas sem página em `empresas/`
- Deals mencionados em reuniões sem página em `deals/`

### 6. Saúde do Index
- Verificar se `index.md` lista todas as páginas existentes
- Identificar páginas novas não catalogadas
- Verificar se páginas deletadas ainda aparecem no index

## Fluxo de Execução

1. Ler `index.md` e comparar com arquivos reais no vault (Glob)
2. Ler `CLAUDE.md` e verificar seção "Contexto Atual"
3. Escanear `deals/` verificando status e datas
4. Escanear `pessoas/` verificando cross-references
5. Escanear `reunioes/` recentes verificando se geraram updates em pessoas/deals
6. Gerar relatório com:
   - Score de saúde (0-100)
   - Issues encontradas por categoria (crítico, médio, baixo)
   - Sugestões de ação
   - Perguntas para investigar (novos sources a adicionar)
7. Appendar entrada `[LINT]` no `log.md`
8. Se o Marcelo autorizar, executar as correções automaticamente

## Output

Relatório no formato:

```
# Lint Report — YYYY-MM-DD

**Score de Saúde:** XX/100

## Crítico (resolver agora)
- ...

## Médio (resolver essa semana)
- ...

## Baixo (quando puder)
- ...

## Sugestões
- Fontes para adicionar: ...
- Perguntas para investigar: ...
```
