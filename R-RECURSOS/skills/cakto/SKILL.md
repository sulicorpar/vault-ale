---
name: cakto
description: Puxa métricas de vendas da Cakto — faturamento, pedidos, compradores, produtos. Use quando quiser ver números de vendas, relatório do dia/semana/mês, ou consultar dados de clientes.
tags: [skill]
---

# Skill: Cakto — Métricas de Vendas

## Autenticação

Autenticar via OAuth2 antes de qualquer request:

```bash
curl -s -X POST https://api.cakto.com.br/public_api/token/ \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "client_id=<YOUR_CAKTO_CLIENT_ID>" \
  -d "client_secret=<YOUR_CAKTO_CLIENT_SECRET>"
```

Extrair `access_token` do response. Token expira em 10h.

## Base URL

`https://api.cakto.com.br/public_api/`

Header: `Authorization: Bearer {token}`

## Endpoints disponíveis

### Produtos
- `GET /products/` — lista produtos (filtros: status, type, search, price__gte/lte, createdAt__gte/lte)
- `GET /products/{id}/` — detalhe do produto

### Pedidos (vendas)
- `GET /orders/` — lista pedidos (filtros: status, customer, paidAt__gte/lte, amount__gte/lte, type, paymentMethod, ordering)
- `GET /orders/{id}/` — detalhe do pedido
- Campos úteis: amount, baseAmount, fees, status, paidAt, customer.name, customer.email, product.name, commissions

### Ofertas
- `GET /offers/` — lista ofertas (filtros: product, status, type)

## Como calcular métricas

### Faturamento bruto (período)
```
GET /orders/?status=paid&paidAt__gte=YYYY-MM-DD&paidAt__lte=YYYY-MM-DD&limit=100
```
Somar `amount` de todos os results. Paginar se `count > limit`.

### Faturamento líquido
Somar `commissions[].commissionValue` onde `userId=1772544` (Marcelo).

### Vendas por produto
Agrupar orders por `product.name` e somar.

### Compradores únicos
Agrupar por `customer.email` (deduplica).

### Ticket médio
Faturamento bruto / count de orders.

### Métodos de pagamento
Agrupar por `paymentMethod` (pix, credit_card, boleto, threeDs).

## Valores importantes

- Preços na API estão em BRL (reais), formato decimal (697.00 = R$697)
- `amount` inclui juros de parcelamento, `baseAmount` é o valor original
- `fees` são taxas da plataforma (já descontadas das comissões)
- Marcelo (producer): userId `1772544`, email `<YOUR_EMAIL>`
- Davi (coproducer em alguns produtos): userId `1128061`, email `davicastrowp@gmail.com`

## Comportamento da skill

Quando o usuário chamar `/cakto`:

1. Autenticar e obter token
2. Se não especificou período, usar **últimos 30 dias**
3. Puxar orders pagas do período (paginar se necessário, limit=100 por página)
4. Puxar lista de produtos ativos
5. Calcular e apresentar:

### Relatório padrão

```
📊 Métricas Cakto — {período}

Faturamento bruto:    R$ X.XXX,XX
Faturamento líquido:  R$ X.XXX,XX (comissão Marcelo)
Vendas:               XX pedidos
Ticket médio:         R$ XXX,XX
Compradores únicos:   XX

Top produtos:
1. Produto A — XX vendas — R$ X.XXX
2. Produto B — XX vendas — R$ X.XXX

Métodos de pagamento:
- Pix: XX% (XX vendas)
- Cartão: XX% (XX vendas)

Última venda: Produto X — R$XXX — Nome — DD/MM HH:MM
```

6. Se o usuário pedir algo específico (ex: "vendas da Comunidade Coda", "quem comprou hoje", "faturamento de março"), filtrar adequadamente.

## Variações aceitas

- `/cakto` → relatório dos últimos 30 dias
- `/cakto hoje` → vendas de hoje
- `/cakto semana` → últimos 7 dias
- `/cakto março` ou `/cakto 2026-03` → mês específico
- `/cakto produto Coda` → filtrado por produto
- `/cakto compradores` → lista de compradores recentes
