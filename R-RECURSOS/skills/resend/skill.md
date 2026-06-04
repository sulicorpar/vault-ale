# Skill: Resend — Email com Branding CODA

Envia emails transacionais e de marketing via Resend API com template HTML no branding da CODA.

## Configuracao

- **API Key:** variavel de ambiente `RESEND_API_KEY` (secrets.env)
- **Endpoint:** `https://api.resend.com/emails`
- **From padrao:** `CODA <noreply@comunidadecoda.com>` (dominio verificado: comunidadecoda.com, regiao sa-east-1)
- **Reply-to:** `<YOUR_EMAIL>`

## Fluxo

1. Ler `secrets.env` para pegar `RESEND_API_KEY`
2. Verificar dominios disponiveis: `GET https://api.resend.com/domains` com `Authorization: Bearer KEY`
3. Montar HTML com o template CODA abaixo
4. Enviar via Python (nunca curl — encoding UTF-8)
5. Confirmar envio com message ID retornado

## Template HTML CODA (branding padrao)

```html
<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{{ASSUNTO}}</title>
</head>
<body style="margin:0;padding:0;background-color:#000000;font-family:'Helvetica Neue',Helvetica,Arial,sans-serif;">
  <table width="100%" cellpadding="0" cellspacing="0" style="background:#000;min-height:100vh;">
    <tr>
      <td align="center" style="padding:40px 20px;">
        <table width="600" cellpadding="0" cellspacing="0" style="max-width:600px;width:100%;">

          <!-- Header -->
          <tr>
            <td style="padding-bottom:32px;border-bottom:1px solid #1a1a1a;">
              <span style="color:#E8541E;font-size:22px;font-weight:900;letter-spacing:-1px;">✳</span>
              <span style="color:#ffffff;font-size:14px;font-weight:600;letter-spacing:2px;text-transform:uppercase;margin-left:8px;">OPERACAO CLAUDE CODE</span>
            </td>
          </tr>

          <!-- Headline -->
          <tr>
            <td style="padding:40px 0 16px;">
              <h1 style="margin:0;color:#ffffff;font-size:36px;font-weight:900;line-height:1.1;text-transform:uppercase;letter-spacing:-1px;">
                {{HEADLINE}}
              </h1>
            </td>
          </tr>

          <!-- Corpo -->
          <tr>
            <td style="padding-bottom:32px;">
              <p style="margin:0;color:#B0B0B0;font-size:16px;line-height:1.6;">
                {{CORPO}}
              </p>
            </td>
          </tr>

          <!-- CTA (opcional) -->
          {{CTA_BLOCK}}

          <!-- Separador -->
          <tr>
            <td style="padding:32px 0;border-top:1px solid #1a1a1a;">
              <p style="margin:0;color:#555555;font-size:12px;line-height:1.5;">
                Voce esta recebendo este email da <strong style="color:#E8541E;">Comunidade CODA</strong>.<br>
                Contato: <a href="mailto:<YOUR_EMAIL>" style="color:#E8541E;text-decoration:none;"><YOUR_EMAIL></a>
              </p>
            </td>
          </tr>

          <!-- Footer logo -->
          <tr>
            <td style="padding-top:8px;" align="right">
              <span style="color:#ffffff;font-size:20px;font-weight:900;letter-spacing:-1px;">Coda</span>
            </td>
          </tr>

        </table>
      </td>
    </tr>
  </table>
</body>
</html>
```

## Bloco CTA (substituir {{CTA_BLOCK}} quando houver botao)

```html
<tr>
  <td style="padding-bottom:32px;">
    <a href="{{CTA_URL}}" style="display:inline-block;background:#E8541E;color:#ffffff;font-size:14px;font-weight:900;text-transform:uppercase;letter-spacing:2px;padding:14px 32px;border-radius:100px;text-decoration:none;">
      {{CTA_TEXTO}}
    </a>
  </td>
</tr>
```

## Envio via Python (obrigatorio — nunca curl)

```python
import urllib.request, json, base64
import os

RESEND_API_KEY = "<YOUR_API_KEY>"  # pegar do secrets.env

def send_email(to_emails, subject, html, attachments=None):
    """
    to_emails: list de strings ["email@exemplo.com"] ou [{"email": "...", "name": "..."}]
    attachments: list de {"filename": "arquivo.png", "content": base64_string}
    """
    payload = {
        "from": "CODA <noreply@comunidadecoda.com>",
        "to": to_emails,
        "reply_to": "<YOUR_EMAIL>",
        "subject": subject,
        "html": html,
    }
    if attachments:
        payload["attachments"] = attachments

    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(
        "https://api.resend.com/emails",
        data=data,
        headers={
            "Authorization": f"Bearer {RESEND_API_KEY}",
            "Content-Type": "application/json; charset=utf-8"
        },
        method="POST"
    )
    try:
        resp = urllib.request.urlopen(req, timeout=30)
        result = json.loads(resp.read().decode("utf-8"))
        print("Enviado! ID:", result.get("id"))
        return result
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8")
        print("Erro HTTP:", e.code, body)
        return None

# Exemplo com imagem anexa
with open("slide.png", "rb") as f:
    img_b64 = base64.b64encode(f.read()).decode("utf-8")

send_email(
    to_emails=["destinatario@email.com"],
    subject="Assunto aqui",
    html="<html>...</html>",
    attachments=[{"filename": "slide.png", "content": img_b64}]
)
```

## Verificar dominios disponiveis

```python
import urllib.request, json

req = urllib.request.Request(
    "https://api.resend.com/domains",
    headers={"Authorization": "Bearer RESEND_API_KEY"},
    method="GET"
)
resp = urllib.request.urlopen(req)
dominios = json.loads(resp.read().decode("utf-8"))
print(json.dumps(dominios, indent=2))
```

## Regras

1. **Sempre Python** — nunca curl para evitar problema de encoding
2. **Verificar dominio** antes do primeiro envio de uma sessao
3. **Sem confirmacao** — montar e enviar direto quando o usuario pedir
4. **Anexos grandes:** usar `attachments` no payload, nao base64 inline no HTML
5. **Tom dos emails:** direto, imperativo, branding CODA — sem enrolacao
