# Star Wars Fan API

API REST em Python que consome a [SWAPI](https://swapi.dev/) (Star Wars API), com filtros, ordenação, consultas correlacionadas, autenticação via API Key e deploy no GCP (Cloud Functions + API Gateway).

Desafio técnico — **Desenvolvedor Back End Python** — PowerOfData.

## Funcionalidades

- **Recursos**: Filmes, personagens, planetas e naves (dados da SWAPI).
- **Filtros**: `search`, `page`, `gender` (people), `character_id` (films).
- **Ordenação**: `sort` e `order` (asc/desc) em listagens.
- **Consultas correlacionadas**: Ex.: `GET /films/{id}/characters` (personagens de um filme) e `GET /films?character_id=1` (filmes de um personagem).
- **Expand**: Parâmetro `expand` para resolver URLs relacionadas (ex.: `?expand=characters`).
- **Autenticação**: API Key no header `X-API-Key` (configurada no API Gateway).
- **Cache**: Cache em memória para reduzir chamadas à SWAPI (TTL configurável).

## Pré-requisitos

- Python 3.11+ (ou 3.10)
- [Google Cloud SDK](https://cloud.google.com/sdk/docs/install) (para deploy)

## Ambiente virtual (recomendado)

Para projetos Python é boa prática usar um **ambiente virtual**: ele isola as dependências do projeto do Python do sistema e de outros projetos, evita conflitos de versão e facilita reproduzir o mesmo ambiente em outra máquina.

O repositório já ignora a pasta do ambiente (`.venv` no `.gitignore`), então você pode criá-la localmente sem risco de commitá-la.

### Como criar e ativar

Na raiz do projeto (`star-wars-fan`):

**Windows (PowerShell ou CMD):**
```bash
python -m venv .venv
.venv\Scripts\activate
```

**Windows (Git Bash):**
```bash
python -m venv .venv
source .venv/Scripts/activate
```

**Linux e macOS:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

Quando o ambiente estiver ativo, o prompt deve mostrar algo como `(.venv)` no início. Para desativar depois: `deactivate`.

## Instalação e execução local

Com o ambiente virtual **criado e ativado** (veja acima):

```bash
# Clone o repositório (se ainda não tiver)
git clone <repo-url>
cd star-wars-fan

# Criar e ativar o ambiente virtual (se ainda não fez)
# python -m venv .venv  e  activate conforme seu OS

# Instalar dependências (dentro do venv)
pip install -r requirements.txt

# Variáveis de ambiente (opcional)
cp .env.example .env
# Edite .env se quiser (SWAPI_BASE_URL, CACHE_TTL_SECONDS)

# Executar a API
uvicorn api.main:app --reload --host 0.0.0.0 --port 8080
```

A API estará em `http://localhost:8080`. Documentação interativa: `http://localhost:8080/docs`.

## Testes

Com o ambiente virtual ativado:

```bash
pytest tests/ -v
```

## Deploy no GCP

1. Configure o projeto e a região:

   ```bash
   gcloud config set project SEU_PROJECT_ID
   export REGION=us-central1
   ```

2. Ative as APIs necessárias:

   ```bash
   gcloud services enable cloudfunctions.googleapis.com run.googleapis.com apigateway.googleapis.com
   ```

3. Faça o deploy da Cloud Function e do API Gateway usando o script em `scripts/deploy.sh` (ou siga os passos em [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) e na documentação do GCP).

Detalhes do script de deploy: [scripts/deploy.sh](scripts/deploy.sh).

## Documentação técnica

- [Arquitetura](docs/ARCHITECTURE.md): Diagrama, componentes, fluxo, cache e decisões.
- [API](docs/API.md): Endpoints, parâmetros e exemplos.

## Estrutura do projeto

```
star-wars-fan/
├── api/
│   ├── main.py              # FastAPI app + entrypoint Cloud Function
│   ├── config.py            # Configuração (env)
│   ├── dependencies.py      # Dependências (opcional API Key)
│   ├── routers/             # films, people, planets, starships
│   ├── services/            # swapi_client, formatters
│   └── schemas/             # Pydantic (SortOrder, etc.)
├── openapi/
│   └── api_config.yaml      # OpenAPI para API Gateway
├── tests/                   # Testes unitários (pytest)
├── docs/
│   ├── ARCHITECTURE.md
│   └── API.md
├── scripts/
│   └── deploy.sh            # Deploy Cloud Function + API Gateway
├── requirements.txt
├── .env.example
└── .gcloudignore
```

## Licença

Ver [LICENSE](LICENSE).
