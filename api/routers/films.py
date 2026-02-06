"""Films router: list, get by id, correlated characters."""

from typing import Any

from fastapi import APIRouter, Query

from api.services.swapi_client import get_list, get_resource, get_by_url
from api.services.swapi_client import SWAPINotFoundError, SWAPIClientError
from api.services.formatters import sort_results, filter_by_film_id, expand_urls
from api.schemas.common import SortOrder
from fastapi import HTTPException, status

router = APIRouter(prefix="/films", tags=["films"])


@router.get("")
def list_films(
    page: int | None = None,
    search: str | None = None,
    sort: str | None = Query(None, description="Sort by: title, episode_id, release_date"),
    order: SortOrder = SortOrder.ASC,
    character_id: int | None = Query(None, description="Filter films where this character appears"),
) -> dict[str, Any]:
    """List films with optional search, pagination, sort, and filter by character."""
    if character_id is not None:
        try:
            person = get_resource("people", character_id)
            film_urls = person.get("films") or []
            results = [get_by_url(u) for u in film_urls]
        except (SWAPINotFoundError, SWAPIClientError):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Character not found",
            ) from None
        if sort:
            results = sort_results(results, sort, order.value)
        return {"count": len(results), "results": results, "next": None, "previous": None}
    raw = get_list("films", page=page, search=search)
    results = raw.get("results", [])
    if sort:
        results = sort_results(results, sort, order.value)
    return {
        "count": len(results),
        "results": results,
        "next": raw.get("next"),
        "previous": raw.get("previous"),
    }


@router.get("/{film_id}")
def get_film(
    film_id: int,
    expand: str | None = Query(None, description="Expand related: characters,planets,species,starships,vehicles"),
) -> dict[str, Any]:
    """Get film by id with optional expand of related resources."""
    try:
        film = get_resource("films", film_id)
    except SWAPINotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Film not found",
        ) from None
    except SWAPIClientError as e:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=str(e),
        ) from e
    if expand:
        keys = {k.strip() for k in expand.split(",") if k.strip()}
        film = expand_urls(film, keys)
    return film


@router.get("/{film_id}/characters")
def get_film_characters(
    film_id: int,
    sort: str | None = Query(None, description="Sort by: name, height, mass, birth_year"),
    order: SortOrder = SortOrder.ASC,
) -> dict[str, Any]:
    """Get characters that appear in this film (correlated query)."""
    try:
        film = get_resource("films", film_id)
    except SWAPINotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Film not found",
        ) from None
    except SWAPIClientError as e:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=str(e),
        ) from e
    urls = film.get("characters") or []
    characters = []
    for u in urls:
        try:
            characters.append(get_by_url(u))
        except (SWAPINotFoundError, SWAPIClientError):
            continue
    if sort:
        characters = sort_results(characters, sort, order.value)
    return {"count": len(characters), "results": characters}
