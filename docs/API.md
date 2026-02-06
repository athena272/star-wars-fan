# Especificação da API - Star Wars Fan API

## Autenticação

A API pode ser protegida por **API Key** no GCP API Gateway. Envie o header:

```
X-API-Key: <sua-api-key>
```

Sem a chave (ou com chave inválida), o gateway retorna 403. A criação e gestão da API Key é feita no console do GCP (API Gateway / API Keys).

## Base URL

- **Local**: `http://localhost:8080` (ou a porta configurada no uvicorn).
- **Produção**: URL do API Gateway após o deploy (ex.: `https://gateway-xxx.apigateway.PROJECT.cloud.goog`).

## Endpoints

### Raiz e saúde

| Método | Path    | Descrição        |
|--------|---------|------------------|
| GET    | `/`     | Informações da API e links para recursos |
| GET    | `/health` | Health check (status OK) |

### Films (filmes)

| Método | Path | Descrição |
|--------|------|-----------|
| GET | `/films` | Lista filmes com filtros e ordenação |
| GET | `/films/{film_id}` | Detalhe do filme por id |
| GET | `/films/{film_id}/characters` | Personagens do filme (consulta correlacionada) |

**Query params para `GET /films`:**

- `page` (int): Página da paginação SWAPI.
- `search` (string): Busca por título (repassado à SWAPI).
- `sort` (string): Ordenação — `title`, `episode_id`, `release_date`.
- `order` (string): `asc` ou `desc`.
- `character_id` (int): Filtra filmes em que o personagem com esse id aparece.

**Query params para `GET /films/{film_id}`:**

- `expand` (string): Lista de relacionamentos a expandir (objetos no lugar de URLs), separados por vírgula: `characters`, `planets`, `species`, `starships`, `vehicles`.

### People (personagens)

| Método | Path | Descrição |
|--------|------|-----------|
| GET | `/people` | Lista personagens com filtros e ordenação |
| GET | `/people/{person_id}` | Detalhe do personagem por id |

**Query params para `GET /people`:**

- `page` (int): Página.
- `search` (string): Busca por nome (repassado à SWAPI).
- `gender` (string): Filtro por gênero (ex.: `male`, `female`).
- `sort` (string): `name`, `height`, `mass`, `birth_year`.
- `order` (string): `asc` ou `desc`.

**Query params para `GET /people/{person_id}`:**

- `expand` (string): Relacionamentos a expandir: `films`, `species`, `starships`, `vehicles`, `homeworld`.

### Planets (planetas)

| Método | Path | Descrição |
|--------|------|-----------|
| GET | `/planets` | Lista planetas |
| GET | `/planets/{planet_id}` | Detalhe do planeta por id |

**Query params para `GET /planets`:** `page`, `search`, `sort`, `order`.

**Query params para `GET /planets/{planet_id}`:** `expand` (ex.: `residents`, `films`).

### Starships (naves)

| Método | Path | Descrição |
|--------|------|-----------|
| GET | `/starships` | Lista naves |
| GET | `/starships/{starship_id}` | Detalhe da nave por id |

**Query params para `GET /starships`:** `page`, `search`, `sort`, `order`.

**Query params para `GET /starships/{starship_id}`:** `expand` (ex.: `films`, `pilots`).

## Exemplos

### Listar personagens com filtro e ordenação

```http
GET /people?search=luke&gender=male&sort=name&order=asc
```

### Obter personagens de um filme (correlacionado)

```http
GET /films/1/characters?sort=name&order=asc
```

### Filmes em que um personagem aparece

```http
GET /films?character_id=1
```

### Detalhe de filme com personagens expandidos

```http
GET /films/1?expand=characters
```

## Códigos de resposta

- **200**: Sucesso.
- **404**: Recurso não encontrado (id inexistente na SWAPI).
- **502**: Erro ao comunicar com a SWAPI (timeout, 5xx).
- **403**: API Key inválida ou ausente (quando o gateway está configurado com API Key).
