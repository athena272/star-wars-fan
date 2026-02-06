"""Tests for starships router."""

import responses


@responses.activate
def test_list_starships(client):
    responses.add(
        responses.GET,
        "https://swapi.dev/api/starships/",
        json={
            "count": 1,
            "results": [{"name": "Death Star", "model": "DS-1"}],
            "next": None,
            "previous": None,
        },
        status=200,
    )
    r = client.get("/starships")
    assert r.status_code == 200
    assert r.json()["results"][0]["name"] == "Death Star"


@responses.activate
def test_get_starship_by_id(client):
    responses.add(
        responses.GET,
        "https://swapi.dev/api/starships/9/",
        json={"name": "Death Star", "model": "DS-1 Orbital Battle Station"},
        status=200,
    )
    r = client.get("/starships/9")
    assert r.status_code == 200
    assert r.json()["name"] == "Death Star"
