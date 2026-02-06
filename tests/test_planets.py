"""Tests for planets router."""

import responses


@responses.activate
def test_list_planets(client):
    responses.add(
        responses.GET,
        "https://swapi.dev/api/planets/",
        json={
            "count": 1,
            "results": [{"name": "Tatooine", "population": "200000"}],
            "next": None,
            "previous": None,
        },
        status=200,
    )
    r = client.get("/planets")
    assert r.status_code == 200
    assert r.json()["results"][0]["name"] == "Tatooine"


@responses.activate
def test_get_planet_by_id(client):
    responses.add(
        responses.GET,
        "https://swapi.dev/api/planets/1/",
        json={"name": "Tatooine", "climate": "Arid"},
        status=200,
    )
    r = client.get("/planets/1")
    assert r.status_code == 200
    assert r.json()["name"] == "Tatooine"
