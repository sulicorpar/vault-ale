#!/bin/bash
VAULT="$HOME/Documents/VAULT-ALE"
echo "👁️ Monitorando vault..."

fswatch -0 "$VAULT" | while IFS= read -r -d "" ARQUIVO; do
    [[ "$ARQUIVO" == *.md ]] && continue
    [[ "$ARQUIVO" == */.git/* ]] && continue
    [[ "$ARQUIVO" == *~* ]] && continue
    [[ ! -f "$ARQUIVO" ]] && continue

    NOME=$(basename "$ARQUIVO")
    PASTA=$(dirname "$ARQUIVO")
    NOME_SEM_EXT="${NOME%.*}"
    EXT="${NOME##*.}"
    MD="$PASTA/$NOME_SEM_EXT.md"

    if [ ! -f "$MD" ]; then
        echo "# $NOME_SEM_EXT" > "$MD"
        echo "" >> "$MD"
        echo "## Arquivo original" >> "$MD"
        echo "- Nome: $NOME" >> "$MD"
        echo "- Tipo: .$EXT" >> "$MD"
        echo "" >> "$MD"
        echo "## Sobre" >> "$MD"
        echo "(Descreva o conteúdo)" >> "$MD"
        echo "" >> "$MD"
        echo "## Links" >> "$MD"
        echo "- [[HUB]]" >> "$MD"
        echo "- [[PRODUTOS]]" >> "$MD"
        echo "" >> "$MD"
        echo "## Tags" >> "$MD"
        echo "#documento #$EXT" >> "$MD"
        echo "✅ .md criado: $NOME_SEM_EXT.md"
    fi
done
