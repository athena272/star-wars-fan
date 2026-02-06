"""Unit tests for SWAPI client."""

import pytest
import responses

from api.services.swapi_client import (
    get_resource,
    get_list,
    get_by_url,
    SWAPINotFoundError,
    SWAPIClientError,
)


@responses.activate
def test_get_resource_returns_data():
    responses.add(
        responses.GET,
        "https://swapi.dev/api/people/1/",
        json={"name": "Luke Skywalker", "url": "https://swapi.dev/api/people/1/"},
        status=200,
    )
    data = get_resource("people", 1)
    assert data["name"] == "Luke Skywalker"


@responses.activate
def test_get_resource_404_raises_not_found():
    responses.add(
        responses.GET,
        "https://swapi.dev/api/people/999/",
        status=404,
    )
    with pytest.raises(SWAPINotFoundError):
        get_resource("people", 999)


@responses.activate
def test_get_list_returns_results():
    responses.add(
        responses.GET,
        "https://swapi.dev/api/people/",
        json={
            "count": 1,
            "results": [{"name": "Luke"}],
            "next": None,
            "previous": None,
        },
        status=200,
    )
    data = get_list("people")
    assert data["count"] == 1
    assert len(data["results"]) == 1
    assert data["results"][0]["name"] == "Luke"


@responses.activate
def test_get_list_with_search():
    responses.add(
        responses.GET,
        "https://swapi.dev/api/people/?search=luke",
        json={"count": 1, "results": [{"name": "Luke Skywalker"}], "next": None, "previous": None},
        status=200,
    )
    data = get_list("people", search="luke")
    assert data["results"][0]["name"] == "Luke Skywalker"


@responses.activate
def test_get_by_url_resolves_full_url():
    responses.add(
        responses.GET,
        "https://swapi.dev/api/films/1/",
        json={"title": "A New Hope"},
        status=200,
    )
    data = get_by_url("https://swapi.dev/api/films/1/")
    assert data["title"] == "A New Hope"


@responses.activate
def test_get_resource_502_raises_client_error():
    responses.add(
        responses.GET,
        "https://swapi.dev/api/people/1/",
        status=502,
    )
    with pytest.raises(SWAPIClientError):
        get_resource("people", 1)
