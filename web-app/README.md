# Projeto CTDOYA

Sistema de chat com IA usando o modelo Gemma 3 via Ollama.

## Requisitos

- Python 3.7+
- Ollama instalado e rodando
- Modelo Gemma 3 instalado no Ollama

## Instalação

1. Instale as dependências:
```bash
pip install -r requirements.txt
```

2. Instale o Ollama e o modelo Gemma 3:
```bash
ollama pull gemma3
```

## Executar a Aplicação

```bash
python app.py
```

A aplicação estará disponível em `http://localhost:5000`

## Funcionalidades

### Interface Web

- **Principal**: Página inicial com boas-vindas
- **Chat de Texto**: Chat interativo com streaming de respostas
- **Visão**: Análise de imagens com IA
- **Suporte**: Informações de ajuda
- **Contato**: Informações de contato

### API REST

#### POST /api/prompt

Envia um prompt para o modelo Gemma 3 e retorna a resposta em JSON.

**Request:**
```json
{
  "prompt": "Sua pergunta aqui"
}
```

**Response:**
```json
{
  "resposta": "Resposta da IA",
  "datahora": "2026-02-28T08:52:00.000000",
  "id": "hash_sha256"
}
```

**Exemplo:**
```bash
curl -X POST http://localhost:5000/api/prompt \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Olá, como você está?"}'
```

Ou use o script de teste:
```bash
./scripts/test_api.sh
```

## Estrutura do Projeto

```
web-app/
├── app.py                 # Aplicação Flask principal
├── requirements.txt       # Dependências Python
├── templates/            # Templates HTML
│   ├── base.html         # Template base com navegação
│   ├── principal.html    # Página principal
│   ├── chat.html         # Chat de texto
│   ├── vision_page.html  # Análise de imagem
│   ├── support.html      # Suporte
│   └── contact.html      # Contato
└── scripts/              # Scripts utilitários
    └── test_api.sh       # Teste da API
```

## Endpoints

- `GET /` - Página principal
- `GET /chat` - Chat de texto
- `GET /vision-page` - Análise de imagem
- `GET /support` - Suporte
- `GET /contact` - Contato
- `POST /ask` - Endpoint de chat com streaming (SSE)
- `POST /vision` - Endpoint de análise de imagem
- `POST /api/prompt` - API REST para prompts
