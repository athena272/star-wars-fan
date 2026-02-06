"""Tests for films router."""

import responses


@responses.activate
def test_list_films(client):
    responses.add(
        responses.GET,
        "https://swapi.dev/api/films/",
        json={
            "count": 1,
            "results": [{"title": "A New Hope", "episode_id": 4, "url": "https://swapi.dev/api/films/1/"}],
            "next": None,
            "previous": None,
        },
        status=200,
    )
    r = client.get("/films")
    assert r.status_code == 200
    data = r.json()
    assert "results" in data
    assert len(data["results"]) == 1
    assert data["results"][0]["title"] == "A New Hope"


@responses.activate
def test_get_film_by_id(client):
    responses.add(
        responses.GET,
        "https://swapi.dev/api/films/1/",
        json={"title": "A New Hope", "episode_id": 4, "url": "https://swapi.dev/api/films/1/"},
        status=200,
    )
    r = client.get("/films/1")
    assert r.status_code == 200
    assert r.json()["title"] == "A New Hope"


@responses.activate
def test_get_film_404(client):
    responses.add(responses.GET, "https://swapi.dev/api/films/999/", status=404)
    r = client.get("/films/999")
    assert r.status_code == 404


@responses.activate
def test_get_film_characters_correlated(client):
    responses.add(
        responses.GET,
        "https://swapi.dev/api/films/1/",
        json={
            "title": "A New Hope",
            "characters": [
                "https://swapi.dev/api/people/1/",
                "https://swapi.dev/api/people/2/",
            ],
        },
        status=200,
    )
    responses.add(
        responses.GET,
        "https://swapi.dev/api/people/1/",
        json={"name": "Luke Skywalker", "url": "https://swapi.dev/api/people/1/"},
        status=200,
    )
    responses.add(
        responses.GET,
        "https://swapi.dev/api/people/2/",
        json={"name": "C-3PO", "url": "https://swapi.dev/api/people/2/"},
        status=200,
    )
    r = client.get("/films/1/characters")
    assert r.status_code == 200
    data = r.json()
    assert data["count"] == 2
    names = [c["name"] for c in data["results"]]
    assert "Luke Skywalker" in names
    assert "C-3PO" in names


@responses.activate
def test_list_films_filter_by_character_id(client):
    responses.add(
        responses.GET,
        "https://swapi.dev/api/people/1/",
        json={
            "name": "Luke Skywalker",
            "films": ["https://swapi.dev/api/films/1/", "https://swapi.dev/api/films/2/"],
        },
        status=200,
    )
    responses.add(
        responses.GET,
        "https://swapi.dev/api/films/1/",
        json={"title": "A New Hope", "url": "https://swapi.dev/api/films/1/"},
        status=200,
    )
    responses.add(
        responses.GET,
        "https://swapi.dev/api/films/2/",
        json={"title": "The Empire Strikes Back", "url": "https://swapi.dev/api/films/2/"},
        status=200,
    )
    r = client.get("/films?character_id=1")
    assert r.status_code == 200
    data = r.json()
    assert data["count"] == 2
    titles = [f["title"] for f in data["results"]]
    assert "A New Hope" in titles
    assert "The Empire Strikes Back" in titles
