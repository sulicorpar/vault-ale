#!/bin/bash
# ============================================
# SYNC CLIENTES — MORTIMER → VAULT
# Busca clientes da API e cria a pasta padrão
# (00-BRIEFING a 09-MATERIAIS) para quem não tem.
# Roda automático via launchd a cada 5 minutos.
# ============================================

API="https://mortimer.adsconsultor.com.br/api/clients"
BASE="$HOME/Documents/VAULT-ALE/P-PROJETOS"

curl -s --max-time 20 "$API" | python3 -c "
import sys, json
try:
    d = json.load(sys.stdin)
    for c in d.get('clients', []):
        nome = (c.get('name') or '').strip()
        if nome:
            print(nome)
except Exception:
    pass
" | while IFS= read -r NOME; do
  [ -z "$NOME" ] && continue
  DESTINO="$BASE/$NOME"
  if [ ! -d "$DESTINO" ]; then
    for sub in 00-BRIEFING 01-DIAGNOSTICO 02-PROPOSTA 03-SEO 04-CONTEUDO-BLOG 05-GOOGLE-BUSINESS 06-RELATORIOS 07-ACESSOS 08-ENTREGAS 09-MATERIAIS; do
      mkdir -p "$DESTINO/$sub"
    done
    printf '# %s\n\nCliente criado automaticamente via MORTIMER em %s.\n\n- [[00-BRIEFING]]\n- Status: ver CRM no MORTIMER\n' "$NOME" "$(date '+%d/%m/%Y %H:%M')" > "$DESTINO/$NOME.md"
    echo "✅ Pasta criada no VAULT: $NOME"
  fi
done
