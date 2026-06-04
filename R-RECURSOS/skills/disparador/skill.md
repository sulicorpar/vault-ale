Skill para gerenciar disparos de mensagens WhatsApp via Baserow. O envio real é feito por uma automação n8n que roda a cada 1 minuto.

## Credenciais Baserow

- **API Token:** `<YOUR_BASEROW_TOKEN>`
- **Table ID:** `677567`
- **Base URL:** `https://api.baserow.io/api/database/rows/table/677567/`
- **Upload URL:** `https://api.baserow.io/api/user-files/upload-file/`

## Estrutura da Tabela "Disparador"

| Campo | Tipo | Observação |
|-------|------|------------|
| Mensagem | long_text | Texto da mensagem (serve como legenda quando tipo = Imagem/Vídeo) |
| Grupo de Envio | multiple_select | Grupos destino — usar IDs numéricos das options |
| Tipo da MSG | multiple_select | Texto (4153031), Imagem (4153029) ou Vídeo (4153030) |
| Dia de Disparo | date | Formato API: `YYYY-MM-DD` |
| Hora de Disparo | duration | Segundos desde meia-noite. Fórmula: `horas * 3600 + minutos * 60` |
| Arquivo a Enviar | file | Upload via endpoint separado, depois referenciar pelo `name` retornado |
| Mencionar Todos | boolean | true/false — menciona @todos no grupo |

## Grupos Disponíveis

| Nome no Baserow | ID | Grupo real no WhatsApp |
|-----------------|-----|----------------------|
| MGTInc #01 | 4153019 | Call Semanal MGTInc GP1 |
| MGTInc #02 | 4153020 | — |
| MGTInc #03 | 4153021 | — |
| Mentor{IA} 3ª Turma | 4153022 | — |
| Interno | 4153643 | — |
| AI Movement | 4158701 | — |
| Avisos CheckList | 4158702 | Checklist CONTROLE INTERNO |
| BootCamp Normal | 5296486 | — |
| BootCamp X | 5296487 | — |
| GRUPO CALL SEMANAL | 5303402 | ENCONTROS CODA 👾 |
| GRUPO CALL SEMANAL 2 | 5781988 | CODA ENCONTROS 👾 #2 |

## Tipos de Mensagem

| Tipo | ID |
|------|-----|
| Texto | 4153031 |
| Imagem | 4153029 |
| Vídeo | 4153030 |

## Conversão de Horário

Fórmula: `horas * 3600 + minutos * 60`

Exemplos rápidos: 08:00=28800, 09:00=32400, 10:00=36000, 12:00=43200, 14:00=50400, 18:00=64800, 20:00=72000

## Comandos

### Listar disparos

```bash
curl -s "https://api.baserow.io/api/database/rows/table/677567/?user_field_names=true" \
  -H "Authorization: Token <YOUR_BASEROW_TOKEN>"
```

### Criar disparo (texto)

```bash
curl -s -X POST "https://api.baserow.io/api/database/rows/table/677567/?user_field_names=true" \
  -H "Authorization: Token <YOUR_BASEROW_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "Mensagem": "TEXTO_AQUI",
    "Grupo de Envio": [5303402],
    "Tipo da MSG": [4153031],
    "Dia de Disparo": "2026-03-31",
    "Hora de Disparo": 44400,
    "Mencionar Todos": true
  }'
```

### Criar disparo (imagem) — 2 passos

**Passo 1: Upload do arquivo pro Baserow**

```bash
curl -s -X POST "https://api.baserow.io/api/user-files/upload-file/" \
  -H "Authorization: Token <YOUR_BASEROW_TOKEN>" \
  -F "file=@/caminho/para/imagem.png"
```

Retorna JSON com campo `name` — guardar esse valor.

**Passo 2: Criar o disparo referenciando o arquivo**

```bash
curl -s -X POST "https://api.baserow.io/api/database/rows/table/677567/?user_field_names=true" \
  -H "Authorization: Token <YOUR_BASEROW_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "Mensagem": "LEGENDA_DA_IMAGEM",
    "Grupo de Envio": [5303402, 5781988],
    "Tipo da MSG": [4153029],
    "Dia de Disparo": "2026-03-31",
    "Hora de Disparo": 44400,
    "Arquivo a Enviar": [{"name": "NOME_RETORNADO_DO_UPLOAD"}],
    "Mencionar Todos": true
  }'
```

### Atualizar disparo

```bash
curl -s -X PATCH "https://api.baserow.io/api/database/rows/table/677567/ROW_ID/?user_field_names=true" \
  -H "Authorization: Token <YOUR_BASEROW_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{ "Mensagem": "NOVO_TEXTO" }'
```

### Deletar disparo

```bash
curl -s -X DELETE "https://api.baserow.io/api/database/rows/table/677567/ROW_ID/" \
  -H "Authorization: Token <YOUR_BASEROW_TOKEN>"
```

### Listar com filtro (ex: disparos de hoje)

```bash
curl -s "https://api.baserow.io/api/database/rows/table/677567/?user_field_names=true&filter__Dia%20de%20Disparo__date_equal=2026-03-31" \
  -H "Authorization: Token <YOUR_BASEROW_TOKEN>"
```

## Fluxo de uso

1. Marcelo pede para agendar disparo (ex: "manda mensagem nos grupos CODA amanhã 10h")
2. Montar registro com mensagem, grupo(s), tipo, dia, hora e mencionar todos
3. Se tiver imagem/vídeo: fazer upload primeiro, depois criar o registro com o `name` do arquivo
4. Criar via POST no Baserow — **sem pedir confirmação**
5. O n8n pega automaticamente no horário e envia via Z-API

## Regras

1. **NÃO pedir confirmação** — criar o disparo direto. Marcelo corrige se precisar.
2. Sempre usar `user_field_names=true` nas requests.
3. Se Marcelo disser "grupos CODA" ou "encontros" → usar GRUPO CALL SEMANAL (5303402) + GRUPO CALL SEMANAL 2 (5781988).
4. Se disser "MGTInc" sem especificar → usar MGTInc #01 (4153019).
5. Se tiver imagem local → gerar via NanoBanana se necessário, fazer upload pro Baserow, depois criar o disparo.
6. Tom das mensagens: direto, informal mas profissional (estilo do Marcelo).
7. Quando Marcelo pedir "bolinha" nos grupos → é um lembrete curto e direto sobre a live/call semanal.
