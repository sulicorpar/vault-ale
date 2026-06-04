---
name: fathom-sync
description: Sincroniza reuniões do Fathom com o vault Obsidian — puxa transcrições e resumos automaticamente para inbox/.
tags: [skill]
---

# Fathom Sync

Integra o Fathom (gravador de reuniões) com o vault Obsidian. Cada reunião nova vira uma nota em `inbox/` com transcrição, resumo e action items prontos para processar com `/reuniao`.

## Primeiro uso — setup

### 1. Instalar dependência
```bash
pip3 install requests
```

### 2. Gerar API Key no Fathom
Fathom → Settings → API → Generate Key

### 3. Salvar a chave
Criar o arquivo `scripts/.env` no vault:
```
FATHOM_API_KEY=sua_chave_aqui
```

### 4. Registrar reuniões existentes (para não duplicar)
Na primeira vez, rode isso para registrar todo o histórico sem baixar nada:
```bash
python3 -c "
import requests
api_key = open('scripts/.env').read().split('=')[1].strip()
headers = {'X-Api-Key': api_key}
all_ids = []
cursor = None
while True:
    params = {'limit': 20}
    if cursor: params['cursor'] = cursor
    data = requests.get('https://api.fathom.ai/external/v1/meetings', headers=headers, params=params).json()
    for m in data.get('items', []): all_ids.append(str(m['recording_id']))
    cursor = data.get('next_cursor')
    if not cursor: break
open('scripts/synced_ids.txt', 'w').write('\n'.join(all_ids) + '\n')
print(f'{len(all_ids)} reuniões registradas — histórico protegido')
"
```

---

## Uso no dia a dia

**Sincronizar reuniões novas:**
```bash
python3 scripts/fathom_sync.py
```

**Puxar de uma data específica:**
```bash
python3 scripts/fathom_sync.py --after 2026-03-10
```

**Puxar um dia específico:**
```bash
python3 scripts/fathom_sync.py --after 2026-03-02 --before 2026-03-02
```

Após rodar, use `/reuniao` para processar cada arquivo que aparecer em `inbox/`.

---

## O que cada reunião salva contém
- Frontmatter com `fathom_id`, `date`, `fathom_url`
- Resumo automático do Fathom
- Action items identificados
- Transcrição completa com speaker e timestamp

---

## Quando o usuário diz "sincroniza Fathom" ou "puxa reuniões"

1. Verificar se `scripts/fathom_sync.py` existe no vault
2. Se não existir → fazer setup completo (criar script, .env, registrar histórico)
3. Se existir → rodar `python3 scripts/fathom_sync.py`
4. Listar os arquivos que chegaram no `inbox/`
5. Perguntar: "Quer processar alguma agora?"
