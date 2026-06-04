#!/bin/zsh

CLIENTE="$1"

if [ -z "$CLIENTE" ]; then
  echo "Erro: informe o nome do cliente."
  echo 'Exemplo: ./novo_cliente.sh "MARILIA TAUBE"'
  exit 1
fi

BASE="ADS Consultor/CLIENTES/$CLIENTE"

mkdir -p "$BASE"/{00-BRIEFING,01-DIAGNOSTICO,02-PROPOSTA,03-SEO,04-CONTEUDO-BLOG,05-GOOGLE-BUSINESS,06-RELATORIOS,07-ACESSOS,08-ENTREGAS}

find "$BASE" -type d -exec touch "{}/.gitkeep" \;

cat > "$BASE/00-BRIEFING/BRIEFING-$CLIENTE.md" <<EOT
# Briefing - $CLIENTE

## Cliente
$CLIENTE

## Status
Pasta criada no Vault.

## Próximos passos
- Preencher briefing
- Adicionar diagnóstico
- Criar proposta
- Organizar entregas
EOT

git add "$BASE"
git commit -m "feat: cliente $CLIENTE - estrutura padrão completa"
git push origin main

open "$BASE"

echo "Cliente $CLIENTE criado, commitado, enviado para o GitHub e aberto no Finder."
