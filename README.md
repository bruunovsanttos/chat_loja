# Chat Loja

Chatbot de atendimento para uma loja de tecnologia desenvolvido com Python e Flask.

O sistema permite consultar produtos, preços e quantidades em estoque. Os dados são armazenados em SQLite e a integração com IA é realizada através da API do OpenRouter.

## Tecnologias

- Python
- Flask
- Flask-SQLAlchemy
- SQLite
- OpenRouter API
- HTML, CSS e JavaScript

## Como executar

### 1. Clone o repositório

```bash
git clone https://github.com/bruunovsanttos/chat_loja.git
cd chat_loja
```

### 2. Crie o ambiente virtual

```bash
python -m venv venv
```

No Windows, ative com:

```bash
venv\Scripts\activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure a API

Crie um arquivo `.env` na raiz do projeto utilizando o `.env.example` como referência:

```env
OPENROUTER_API_KEY=sua_chave_openrouter_aqui
```

A chave da API não deve ser adicionada ao repositório.

### 5. Inicialize os produtos

```bash
python seed.py
```

### 6. Execute a aplicação

```bash
python run.py
```

Acesse no navegador:

```text
http://127.0.0.1:5000
```

## Funcionalidades

- Chat com linguagem natural
- Consulta de produtos
- Consulta de preços
- Consulta de estoque
- Integração com LLM via OpenRouter
- Persistência de dados com SQLite

As informações de produtos, preços e estoque são obtidas diretamente do banco de dados. A LLM atua como camada de interpretação da linguagem natural, evitando que informações comerciais sejam utilizadas sem validação dos dados da aplicação.