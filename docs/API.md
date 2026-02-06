# Especificação da API - Star Wars Fan API

## Autenticação

Na implantação atual (Cloud Function direta), **nenhuma API Key é necessária**: todos os endpoints são públicos e podem ser chamados sem header de autenticação.

Se no futuro a API for exposta através do **GCP API Gateway** com proteção por API Key, será preciso enviar o header:

```
X-API-Key: <sua-api-key>
```

A criação e gestão da API Key é feita no console do GCP (API Gateway / API Keys). Sem a chave (ou com chave inválida), o gateway retornaria 403.

## Base URL

- **Local**: `http://localhost:8080` (ou a porta configurada no uvicorn).
- **Produção**: `https://us-central1-smooth-helper-486601-t3.cloudfunctions.net/star-wars-fan`

## Testando com Insomnia ou Postman

A API é REST: use a Base URL acima e adicione o path do endpoint (ex.: `/people/1`, `/films`, `/health`). Método **GET** para todos os endpoints atuais. Não é necessário configurar autenticação na requisição. Exemplo: `GET https://us-central1-smooth-helper-486601-t3.cloudfunctions.net/star-wars-fan/people/1`

**Template para Insomnia:** o arquivo [insomnia/star-wars-fan-api.yaml](../insomnia/star-wars-fan-api.yaml) é uma especificação OpenAPI que pode ser importada no Insomnia (Application → Import/Export → Import Data → From File). Serão criadas requisições para todos os endpoints com a URL de produção já configurada.

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
