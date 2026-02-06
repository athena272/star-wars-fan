"""Starships router: list, get by id."""

from typing import Any

from fastapi import APIRouter, Query

from api.services.swapi_client import get_list, get_resource
from api.services.swapi_client import SWAPINotFoundError, SWAPIClientError
from api.services.formatters import sort_results, expand_urls
from api.schemas.common import SortOrder
from fastapi import HTTPException, status

router = APIRouter(prefix="/starships", tags=["starships"])


@router.get("")
def list_starships(
    page: int | None = None,
    search: str | None = None,
    sort: str | None = Query(None, description="Sort by: name, model, length, crew"),
    order: SortOrder = SortOrder.ASC,
) -> dict[str, Any]:
    """List starships with optional search, pagination, and sort."""
    raw = get_list("starships", page=page, search=search)
    results: list[dict] = raw.get("results", [])
    if sort:
        results = sort_results(results, sort, order.value)
    return {
        "count": len(results),
        "results": results,
        "next": raw.get("next"),
        "previous": raw.get("previous"),
    }


@router.get("/{starship_id}")
def get_starship(
    starship_id: int,
    expand: str | None = Query(None, description="Expand related: films,pilots"),
) -> dict[str, Any]:
    """Get starship by id with optional expand of related resources."""
    try:
        starship = get_resource("starships", starship_id)
    except SWAPINotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Starship not found",
        ) from None
    except SWAPIClientError as e:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=str(e),
        ) from e
    if expand:
        keys = {k.strip() for k in expand.split(",") if k.strip()}
        starship = expand_urls(starship, keys)
    return starship
