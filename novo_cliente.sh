#!/bin/bash
NOME="$1"
BASE="$HOME/Documents/VAULT-ALE"
DESTINO="$BASE/P-PROJETOS/$NOME"
TEMPLATE="$BASE/R-RECURSOS/templates/TEMPLATE-CLIENTE.md"

mkdir -p "$DESTINO/00-BRIEFING"
mkdir -p "$DESTINO/01-DIAGNOSTICO"
mkdir -p "$DESTINO/02-PROPOSTA"
mkdir -p "$DESTINO/03-SEO"
mkdir -p "$DESTINO/04-CONTEUDO-BLOG"
mkdir -p "$DESTINO/05-GOOGLE-BUSINESS"
mkdir -p "$DESTINO/06-RELATORIOS"
mkdir -p "$DESTINO/07-ACESSOS"
mkdir -p "$DESTINO/08-ENTREGAS"

# Cria nota principal com links
sed "s/NOME DO CLIENTE/$NOME/g" "$TEMPLATE" > "$DESTINO/$NOME.md"

echo "✅ Cliente '$NOME' criado em P-PROJETOS com template e links!"
echo "📍 $DESTINO"
