#!/bin/bash
BASE="/Users/alejandrosulichin/Documents/VAULT-ALE"
python3 "$BASE/atualizar_crm.py"
git add "$BASE/CRM.md" "$BASE/crm.html" "$BASE/atualizar_crm.py" "$BASE/atualizar_crm.sh" 2>/dev/null || true
git commit -m "crm: atualizar painel de clientes" 2>/dev/null || true
git push origin main 2>/dev/null || true
