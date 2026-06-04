---
name: zap
description: Envia mensagens no WhatsApp via Z-API — texto, imagens, documentos. Use quando o Marcelo pedir para mandar mensagem, avisar alguém, enviar arquivo ou se comunicar com a equipe/clientes.
tags: [skill]
---

Skill para enviar mensagens no WhatsApp via Z-API.

## Credenciais

- **Instance ID:** `<YOUR_ZAPI_INSTANCE_ID>`
- **Token:** `<YOUR_ZAPI_TOKEN>`
- **Client-Token:** `<YOUR_ZAPI_CLIENT_TOKEN>`
- **Base URL:** `https://api.z-api.io/instances/<YOUR_ZAPI_INSTANCE_ID>/token/<YOUR_ZAPI_TOKEN>`

## Contatos conhecidos

Antes de enviar, sempre verificar `pessoas/` no vault para encontrar o número do contato. Se não tiver número salvo, perguntar ao Marcelo.

Formato do telefone: código do país + DDD + número, sem +, sem espaços, sem traços.
Exemplo: `5548999999999`

## Comandos disponíveis

### 1. Verificar status da conexão

```bash
curl -s "https://api.z-api.io/instances/<YOUR_ZAPI_INSTANCE_ID>/token/<YOUR_ZAPI_TOKEN>/status" \
  -H "Client-Token: <YOUR_ZAPI_CLIENT_TOKEN>"
```

### 2. Enviar mensagem de texto

```bash
curl -s -X POST \
  "https://api.z-api.io/instances/<YOUR_ZAPI_INSTANCE_ID>/token/<YOUR_ZAPI_TOKEN>/send-text" \
  -H "Content-Type: application/json" \
  -H "Client-Token: <YOUR_ZAPI_CLIENT_TOKEN>" \
  -d '{
    "phone": "NUMERO_AQUI",
    "message": "MENSAGEM_AQUI"
  }'
```

### 3. Enviar imagem (com legenda opcional)

```bash
curl -s -X POST \
  "https://api.z-api.io/instances/<YOUR_ZAPI_INSTANCE_ID>/token/<YOUR_ZAPI_TOKEN>/send-image" \
  -H "Content-Type: application/json" \
  -H "Client-Token: <YOUR_ZAPI_CLIENT_TOKEN>" \
  -d '{
    "phone": "NUMERO_AQUI",
    "image": "URL_DA_IMAGEM",
    "caption": "LEGENDA_OPCIONAL"
  }'
```

### 4. Enviar documento/arquivo

```bash
curl -s -X POST \
  "https://api.z-api.io/instances/<YOUR_ZAPI_INSTANCE_ID>/token/<YOUR_ZAPI_TOKEN>/send-document/pdf" \
  -H "Content-Type: application/json" \
  -H "Client-Token: <YOUR_ZAPI_CLIENT_TOKEN>" \
  -d '{
    "phone": "NUMERO_AQUI",
    "document": "URL_DO_DOCUMENTO",
    "fileName": "nome-do-arquivo.pdf"
  }'
```

### 5. Enviar link com preview

```bash
curl -s -X POST \
  "https://api.z-api.io/instances/<YOUR_ZAPI_INSTANCE_ID>/token/<YOUR_ZAPI_TOKEN>/send-link" \
  -H "Content-Type: application/json" \
  -H "Client-Token: <YOUR_ZAPI_CLIENT_TOKEN>" \
  -d '{
    "phone": "NUMERO_AQUI",
    "message": "MENSAGEM_AQUI",
    "image": "URL_IMAGEM_PREVIEW",
    "linkUrl": "URL_DO_LINK",
    "title": "TITULO_DO_LINK",
    "linkDescription": "DESCRICAO"
  }'
```

## Formato de telefone

- **Contato individual:** código do país + DDD + número, sem +, sem espaços, sem traços. Ex: `5548999999999`
- **Grupo:** usar o ID do grupo com sufixo `-group`. Ex: `<YOUR_GROUP_JID>`

## Grupos conhecidos

- **CODA TIME** — `<YOUR_GROUP_JID>`
- **Call Semanal MGTInc GP1** — `<YOUR_GROUP_JID>`
- **Call Semanal MGTInc GP2** — `<YOUR_GROUP_JID>`
- **Call Semanal MGTInc GP3** — `<YOUR_GROUP_JID>`
- **Checklist Controle Interno** — `<YOUR_GROUP_JID>`
- **Build In Public [Open]** — `<YOUR_GROUP_JID>`
- **Encontros Semanais 👾** — `<YOUR_GROUP_JID>` (NÃO é de compradores)
- **Bate Papo (alunos/compradores CODA)** — `<YOUR_GROUP_JID>`
- **MGT - ALDIR** — `<YOUR_GROUP_JID>`

## Regras de uso

1. **NÃO pedir confirmação** — montar a mensagem e enviar direto. Marcelo corrige se precisar.
2. Nunca enviar spam ou mensagens em massa sem autorização explícita
3. Manter intervalo de 1-2 segundos entre mensagens múltiplas
4. Tom das mensagens: direto, informal mas profissional (estilo do Marcelo)
5. Para arquivos locais, primeiro fazer upload para URL pública (ou usar base64 se suportado) antes de enviar
6. **🔗 LINKS SEMPRE COM `https://`** — WhatsApp só transforma em link clicável quando o link tem o protocolo explícito. Escrever `fistcare-lp.vercel.app` NÃO funciona, mas `https://fistcare-lp.vercel.app` SIM. Sempre usar o protocolo completo nos disparos. (Feedback do Marcelo, 30/04/2026)

## Exemplos de uso

**Marcelo:** "manda pro Theo que a call com o Aldir fechou"
**Fluxo:**
1. Buscar número do Theo em `pessoas/theo.md`
2. Montar mensagem: "Theo, fechou o deal do Aldir (SendMix)! R$30K, entrada de R$15K paga. Vou montar o squad de devs pra começar semana que vem."
3. Mostrar pro Marcelo e pedir OK
4. Enviar via `/send-text`

**Marcelo:** "envia a proposta pro Aldir"
**Fluxo:**
1. Buscar número em `pessoas/aldir-alyson.md`
2. Enviar link da proposta via `/send-link` com preview
3. Ou enviar PDF do contrato via `/send-document/pdf`
