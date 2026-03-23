# 🤖 AGENTS.md — Morça Bot

Este documento orienta agentes de IA a trabalhar corretamente neste repositório.

Leia atentamente antes de modificar qualquer código.

---

# 🧠 PRINCÍPIO FUNDAMENTAL

Este é um sistema SaaS com arquitetura baseada em separação de responsabilidades.

Antes de qualquer alteração:

* Analise o código existente profundamente
* Entenda o fluxo atual
* Prefira refatorar ao invés de recriar

Se houver dúvida ou perda de contexto:
→ Pare
→ Reanalise o projeto
→ Continue apenas com entendimento consistente

---

# 🧱 ARQUITETURA

Fluxo principal:

views → services → parser → utils → models

Responsabilidades:

* views:

  * recebem requisições HTTP
  * NÃO possuem regra de negócio

* services:

  * concentram regras de negócio
  * coordenam fluxo da aplicação

* parser:

  * interpreta mensagens do usuário
  * NÃO acessa banco de dados

* selectors:

  * consultas e buscas no banco
  * lógica de leitura de dados

* utils:

  * funções puras e reutilizáveis
  * sem regra de negócio

* models:

  * definição de dados e relações

---

# 📁 ORGANIZAÇÃO POR DOMÍNIO

## accounts/

* gestão de usuários
* billing (plan_expires_at)
* cupons e referral
* services:

  * user_service
  * coupon_service
  * referral_service

## expenses/

* registro de gastos
* parser de mensagens
* services:

  * message_service
* selectors:

  * category_selector
* relatório mensal (management command)

## utils/

* money: normalização e formatação de valores
* text: fuzzy match e helpers
* dates: manipulação de datas

---

# ⚠️ REGRAS CRÍTICAS

## 💰 Dinheiro

* NUNCA usar float
* SEMPRE usar Decimal
* Normalização via utils.money.normalize_brl_amount

---

## 🏷️ Categoria

* SEMPRE usar ForeignKey
* NUNCA usar string para categoria

---

## 🧠 Regra de negócio

* NÃO implementar regras em:

  * views
  * utils
  * parser

* SEMPRE usar services

---

## ⚙️ Configuração

* NÃO hardcodar valores
* Usar sempre settings.py

Exemplo:

* TRIAL_DURATION_DAYS

---

## 🔁 Migrations

* NÃO quebrar migrations existentes
* NÃO apagar migrations já aplicadas

---

# 💬 FLUXO PRINCIPAL (WHATSAPP)

1. Webhook recebe mensagem
2. View delega para service
