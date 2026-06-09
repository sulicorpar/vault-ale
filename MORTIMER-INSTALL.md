# 🚀 MORTIMER — GUIA DE INSTALAÇÃO (5 MINUTOS)

---

## 📋 PRÉ-REQUISITOS

✅ Node.js instalado (`node --version`)  
✅ CLAUDE_API_KEY (você tem)  
✅ Antigravity IDE ou terminal Mac  

---

## 🔧 PASSO 1: COPIAR ARQUIVOS PARA SEU VAULT

```bash
# 1. Ir para seu VAULT
cd ~/Documents/VAULT-ALE

# 2. Baixar os 3 arquivos em /mnt/user-data/outputs:
# - mortimer.js
# - mortimer-cli.js
# - package.json

# OU copiar manualmente:
# mortimer.js → ~/Documents/VAULT-ALE/mortimer.js
# mortimer-cli.js → ~/Documents/VAULT-ALE/mortimer-cli.js
# package.json → ~/Documents/VAULT-ALE/package.json
```

---

## 📦 PASSO 2: INSTALAR DEPENDÊNCIAS

```bash
cd ~/Documents/VAULT-ALE

npm install
```

**Deve aparecer:**
```
added 50 packages in 2.5s
```

---

## 🔑 PASSO 3: CONFIGURAR CLAUDE API KEY

```bash
# Adicionar sua chave ao ambiente
export CLAUDE_API_KEY=sk-sua-chave-aqui

# Ou adicionar ao ~/.zshrc para ser permanente:
echo 'export CLAUDE_API_KEY=sk-sua-chave-aqui' >> ~/.zshrc
source ~/.zshrc

# Verificar:
echo $CLAUDE_API_KEY
```

---

## ✅ PASSO 4: TESTAR MORTIMER

### **Opção 1: Modo Interativo (RECOMENDADO)**

```bash
cd ~/Documents/VAULT-ALE
node mortimer-cli.js
```

**Você verá:**
```
╔════════════════════════════════════════╗
║  🤖 MORTIMER 2.0 — Super Assistente  ║
║     Seu Assistente Pessoal IA          ║
╚════════════════════════════════════════╝

mortimer> _
```

**Digite seu primeiro comando:**
```
mortimer> teste rápido criar post instagram
```

**Mortimer responde em 5 segundos!** ✅

### **Opção 2: Comando Direto**

```bash
node mortimer.js "criar campanha Raio X R$500/dia SP"
```

---

## 🎯 SEU PRIMEIRO COMANDO

```bash
mortimer> criar campanha Raio X do Google, budget R$500/dia, 
público donos de negócio em SP, agendar reunião quinta 14h
```

**Mortimer retorna:**
```json
{
  "tipo": "multiplo",
  "campanha": { estrutura completa },
  "reuniao": { data, link meet, participantes },
  "proximos_passos": [...]
}
```

---

## 🛑 TROUBLESHOOTING

### ❌ Erro: "command not found: node"
```bash
# Instalar Node.js
brew install node

# Ou download em: https://nodejs.org
```

### ❌ Erro: "CLAUDE_API_KEY não encontrada"
```bash
# Configurar novamente:
export CLAUDE_API_KEY=sk-sua-chave

# Verificar:
echo $CLAUDE_API_KEY
```

### ❌ Erro: "Cannot find module @anthropic-ai/sdk"
```bash
# Instalar dependências novamente:
npm install

# Se não funcionar, limpar cache:
rm -rf node_modules package-lock.json
npm install
```

### ❌ Lento ou timeout
```bash
# Aumentar timeout:
NODE_OPTIONS="--max-old-space-size=4096" node mortimer-cli.js
```

---

## 🎮 ATALHO NO SHELL (OPCIONAL)

Adicionar comando ao seu `.zshrc`:

```bash
# Adicionar ao final de ~/.zshrc:
echo 'alias mortimer="cd ~/Documents/VAULT-ALE && node mortimer-cli.js"' >> ~/.zshrc

source ~/.zshrc

# Agora você pode usar em qualquer lugar:
mortimer
```

---

## 🚀 PRÓXIMOS PASSOS

### Imediato (Hoje):
1. ✅ Instalar Mortimer
2. ✅ Testar primeiro comando
3. ✅ Criar campanha Raio X

### Semana que vem:
1. Integrar com Google Calendar (agendar reuniões)
2. Integrar com Kommo (tasks automáticas)
3. Integrar com Obsidian (lembretes)
4. Integrar com N8N (executar campanhas automáticas)

### Próximas semanas:
1. Mortimer com RAG (acesso VAULT)
2. Multi-agent orchestrator
3. Skill creator dinâmico

---

## 📚 EXEMPLOS DE USO

```bash
# CAMPANHAS
mortimer> criar campanha para Raio X do Google

# CONTEÚDO
mortimer> post instagram sobre seo local para dentistas

# PROPOSTAS
mortimer> estruturar proposta para novo cliente e-commerce

# AUTOMAÇÕES
mortimer> criar automação whatsapp para qualificar leads

# ANÁLISES
mortimer> diagnosticar problema com meta ads cpa alto

# TUDO JUNTO
mortimer> campanha completa raio x: estrutura, posts, 
          proposta, automação, reunião quinta 14h
```

---

## 💡 DICAS

1. **Seja específico:** "criar campanha" → "criar campanha Raio X, budget R$500/dia, público donos negócio SP"

2. **Combine comandos:** Mortimer entende múltiplas tarefas em um comando

3. **Use contexto:** Mortimer lembra do que você pediu antes

4. **Peça sugestões:** "o que falta aqui?", "como posso melhorar isso?"

5. **Chame especialistas:** "quero opinião de especialista em copywriting"

---

## ✨ PRONTO!

Você agora tem **MORTIMER instalado e funcionando**!

Próximo passo: `node mortimer-cli.js` e comece a delegar!

---

**Status:** ✅ INSTALAÇÃO COMPLETA  
**Tempo:** 5 minutos  
**Próximo:** Use Mortimer para tudo!  

