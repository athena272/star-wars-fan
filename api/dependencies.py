"""FastAPI dependencies: SWAPI client, optional API key validation."""

from typing import Annotated

from fastapi import Header, HTTPException, status

from api.services.swapi_client import (
    SWAPIClientError,
    SWAPINotFoundError,
    get_list,
    get_resource,
    get_by_url,
)


def optional_api_key(
    x_api_key: Annotated[str | None, Header(alias="X-API-Key")] = None,
) -> str | None:
    """Extract optional API Key from header (validation done at API Gateway)."""
    return x_api_key


def get_swapi_people(
    page: int | None = None,
    search: str | None = None,
) -> dict:
    """Dependency: fetch people list from SWAPI."""
    return get_list("people", page=page, search=search)


def get_swapi_person(resource_id: int) -> dict:
    """Dependency: fetch single person by id."""
    try:
        return get_resource("people", resource_id)
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


def get_swapi_films(
    page: int | None = None,
    search: str | None = None,
) -> dict:
    """Dependency: fetch films list from SWAPI."""
    return get_list("films", page=page, search=search)


def get_swapi_film(resource_id: int) -> dict:
    """Dependency: fetch single film by id."""
    try:
        return get_resource("films", resource_id)
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


def get_swapi_planets(
    page: int | None = None,
    search: str | None = None,
) -> dict:
    """Dependency: fetch planets list from SWAPI."""
    return get_list("planets", page=page, search=search)


def get_swapi_planet(resource_id: int) -> dict:
    """Dependency: fetch single planet by id."""
    try:
        return get_resource("planets", resource_id)
    except SWAPINotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Planet not found",
        ) from None
    except SWAPIClientError as e:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=str(e),
        ) from e


def get_swapi_starships(
    page: int | None = None,
    search: str | None = None,
) -> dict:
    """Dependency: fetch starships list from SWAPI."""
    return get_list("starships", page=page, search=search)


def get_swapi_starship(resource_id: int) -> dict:
    """Dependency: fetch single starship by id."""
    try:
        return get_resource("starships", resource_id)
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


def resolve_url(url: str) -> dict:
    """Resolve a SWAPI URL to full resource (for correlated queries)."""
    try:
        return get_by_url(url)
    except SWAPINotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Related resource not found",
        ) from None
    except SWAPIClientError as e:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=str(e),
        ) from e
