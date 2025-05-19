# 💳 FastAPI Mercado Pago Checkout

Este projeto é uma integração completa com os principais métodos de pagamento da API do [Mercado Pago](https://www.mercadopago.com.br/), desenvolvida com **FastAPI** e renderização via **Jinja2**. A interface utiliza **TailwindCSS** e proporciona uma experiência de checkout moderna e interativa.

## ✅ Funcionalidades

- 💰 Pagamento via Cartão de Crédito
- 🧾 Pagamento via Boleto Bancário
- ⚡ Pagamento via PIX com redirecionamento automático
- 🔒 Segurança com `X-Idempotency-Key` para evitar duplicidade
- 🧠 Estrutura clara e separação entre backend e frontend

---

## 📁 Estrutura do Projeto

```
.
├── app.py                      # Aplicação FastAPI principal
├── services/
│   ├── __init__.py
│   └── mercadopago.py         # Classe com integração à API do Mercado Pago
├── templates/
│   └── checkout.html          # Interface HTML com formulário dinâmico de pagamento
├── .env-example               # Exemplo para configuração local
├── requirements.txt           # Lista de dependências do projeto
```

---

## 🚀 Como Executar

### 1. Crie e ative o ambiente virtual

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

### 2. Instale as dependências

```bash
pip install -r requirements.txt
```

### 3. Configure o `.env`

Crie um arquivo `.env` com base no `.env-example`:

```env
MP_ACCESS_TOKEN=sua_chave_de_acesso
MP_BASE_API_URL=https://api.mercadopago.com
```

### 4. Execute o servidor

```bash
uvicorn app:app --reload
```

Acesse: [http://localhost:8000](http://localhost:8000)

---

## 💡 Exemplos de Uso

### 🔹 Pagamento com Cartão de Crédito

- Preencha os dados do cartão, CPF e parcelas.
- Clique em **Pagar**.
- O sistema valida e responde com status de sucesso ou erro.

### 🔹 Pagamento via PIX

- Insira seu CPF e e-mail.
- O sistema redireciona automaticamente para o QR Code do Mercado Pago.

### 🔹 Pagamento via Boleto

- Preencha seus dados completos (nome, endereço, CPF, etc.).
- O sistema gera e redireciona para o boleto.

---

## 📸 Interface (Checkout)

> Interface simples, responsiva e feita com TailwindCSS:

```
[ Cartão ] [ PIX ] [ Boleto ]
📄 Formulário dinâmico baseado no método de pagamento selecionado
✅ Mensagens de sucesso ou erro com animação
```


## 🧪 Testes com Sandbox

Para testar os métodos de pagamento em ambiente de desenvolvimento, utilize as [credenciais de teste do Mercado Pago](https://www.mercadopago.com.br/developers/panel).

---

> Projeto desenvolvido como base de estudo e aplicação real para integração com sistemas de pagamento.
