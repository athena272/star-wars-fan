"""People router: list, get by id, filters and sort."""

from typing import Any

from fastapi import APIRouter, Query

from api.services.swapi_client import get_list, get_resource
from api.services.swapi_client import SWAPINotFoundError, SWAPIClientError
from api.services.formatters import sort_results, filter_people_by_gender, expand_urls
from api.schemas.common import SortOrder
from fastapi import HTTPException, status

router = APIRouter(prefix="/people", tags=["people"])


@router.get("")
def list_people(
    page: int | None = None,
    search: str | None = None,
    gender: str | None = Query(None, description="Filter by gender (e.g. male, female)"),
    sort: str | None = Query(None, description="Sort by: name, height, mass, birth_year"),
    order: SortOrder = SortOrder.ASC,
) -> dict[str, Any]:
    """List people with optional search, pagination, gender filter, and sort."""
    raw = get_list("people", page=page, search=search)
    results: list[dict] = raw.get("results", [])
    if gender:
        results = filter_people_by_gender(results, gender)
    if sort:
        results = sort_results(results, sort, order.value)
    return {
        "count": len(results),
        "results": results,
        "next": raw.get("next"),
        "previous": raw.get("previous"),
    }


@router.get("/{person_id}")
def get_person(
    person_id: int,
    expand: str | None = Query(None, description="Expand related: films,species,starships,vehicles,homeworld"),
) -> dict[str, Any]:
    """Get person by id with optional expand of related resources."""
    try:
        person = get_resource("people", person_id)
    except SWAPINotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Person not found",
        ) from None
    except SWAPIClientError as e:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=str(e),
        ) from e
    if expand:
        keys = {k.strip() for k in expand.split(",") if k.strip()}
        person = expand_urls(person, keys)
    return person
