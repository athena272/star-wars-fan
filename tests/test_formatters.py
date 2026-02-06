"""Tests for formatters: sort, filter, expand."""

import responses

from api.services.formatters import sort_results, filter_people_by_gender, expand_urls


def test_sort_results_by_name_asc():
    items = [{"name": "Leia"}, {"name": "Luke"}]
    sort_results(items, "name", "asc")
    assert items[0]["name"] == "Leia"
    assert items[1]["name"] == "Luke"


def test_sort_results_by_name_desc():
    items = [{"name": "Leia"}, {"name": "Luke"}]
    sort_results(items, "name", "desc")
    assert items[0]["name"] == "Luke"
    assert items[1]["name"] == "Leia"


def test_sort_results_by_height_numeric():
    items = [
        {"name": "A", "height": "200"},
        {"name": "B", "height": "100"},
    ]
    sort_results(items, "height", "asc")
    assert items[0]["height"] == "100"
    assert items[1]["height"] == "200"


def test_filter_people_by_gender():
    items = [
        {"name": "Luke", "gender": "male"},
        {"name": "Leia", "gender": "female"},
    ]
    out = filter_people_by_gender(items, "female")
    assert len(out) == 1
    assert out[0]["name"] == "Leia"


def test_filter_people_by_gender_empty_returns_all():
    items = [{"name": "Luke", "gender": "male"}]
    out = filter_people_by_gender(items, None)
    assert out == items


@responses.activate
def test_expand_urls_resolves_related():
    responses.add(
        responses.GET,
        "https://swapi.dev/api/planets/1/",
        json={"name": "Tatooine"},
        status=200,
    )
    data = {"homeworld": "https://swapi.dev/api/planets/1/"}
    out = expand_urls(data, {"homeworld"})
    assert out["homeworld"]["name"] == "Tatooine"
