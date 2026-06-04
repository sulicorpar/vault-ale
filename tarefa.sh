#!/bin/zsh

TAREFA="$*"

if [ -z "$TAREFA" ]; then
  echo "Erro: escreva a tarefa."
  echo 'Exemplo: ./tarefa.sh "Enviar orçamento para Juliana - Brazilicious"'
  exit 1
fi

ARQUIVO="ADS Consultor/99-TAREFAS/TODO-GERAL.md"

if [ ! -f "$ARQUIVO" ]; then
  mkdir -p "ADS Consultor/99-TAREFAS"
  cat > "$ARQUIVO" <<EOT
# To Do Geral - ADS Consultor

## Pendentes

## Em andamento

## Concluídas
EOT
fi

awk -v tarefa="- [ ] $TAREFA" '
/## Pendentes/ {
  print;
  print "";
  print tarefa;
  next
}
{ print }
' "$ARQUIVO" > "$ARQUIVO.tmp" && mv "$ARQUIVO.tmp" "$ARQUIVO"

git add "$ARQUIVO"
git commit -m "task: adicionar tarefa - $TAREFA"
git push origin main

echo "Tarefa adicionada com sucesso:"
echo "- [ ] $TAREFA"
