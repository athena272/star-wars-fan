"""Tests for people router."""

import pytest
import responses


@responses.activate
def test_list_people(client):
    responses.add(
        responses.GET,
        "https://swapi.dev/api/people/",
        json={
            "count": 1,
            "results": [{"name": "Luke Skywalker", "gender": "male"}],
            "next": None,
            "previous": None,
        },
        status=200,
    )
    r = client.get("/people")
    assert r.status_code == 200
    data = r.json()
    assert len(data["results"]) == 1
    assert data["results"][0]["name"] == "Luke Skywalker"


@responses.activate
def test_list_people_with_gender_filter(client):
    responses.add(
        responses.GET,
        "https://swapi.dev/api/people/",
        json={
            "count": 2,
            "results": [
                {"name": "Luke Skywalker", "gender": "male"},
                {"name": "Leia Organa", "gender": "female"},
            ],
            "next": None,
            "previous": None,
        },
        status=200,
    )
    r = client.get("/people?gender=female")
    assert r.status_code == 200
    data = r.json()
    assert data["count"] == 1
    assert data["results"][0]["gender"] == "female"


@responses.activate
def test_get_person_by_id(client):
    responses.add(
        responses.GET,
        "https://swapi.dev/api/people/1/",
        json={"name": "Luke Skywalker", "height": "172", "url": "https://swapi.dev/api/people/1/"},
        status=200,
    )
    r = client.get("/people/1")
    assert r.status_code == 200
    assert r.json()["name"] == "Luke Skywalker"


@responses.activate
def test_get_person_404(client):
    responses.add(responses.GET, "https://swapi.dev/api/people/999/", status=404)
    r = client.get("/people/999")
    assert r.status_code == 404


@responses.activate
def test_list_people_with_sort(client):
    responses.add(
        responses.GET,
        "https://swapi.dev/api/people/",
        json={
            "count": 2,
            "results": [
                {"name": "Leia", "height": "150"},
                {"name": "Luke", "height": "172"},
            ],
            "next": None,
            "previous": None,
        },
        status=200,
    )
    r = client.get("/people?sort=name&order=asc")
    assert r.status_code == 200
    data = r.json()
    # Leia before Luke
    assert data["results"][0]["name"] == "Leia"
    assert data["results"][1]["name"] == "Luke"
