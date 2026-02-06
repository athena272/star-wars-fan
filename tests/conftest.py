"""Pytest fixtures: mock SWAPI, FastAPI test client."""

import pytest
import responses

from fastapi.testclient import TestClient

from api.main import app
from api.services.swapi_client import clear_cache


@pytest.fixture(autouse=True)
def clear_swapi_cache():
    """Clear SWAPI cache before each test so mocks are used."""
    clear_cache()
    yield


@pytest.fixture
def client() -> TestClient:
    """FastAPI test client."""
    return TestClient(app)


@pytest.fixture
def mock_swapi():
    """Context manager that mocks SWAPI base URL for responses library."""
    with responses.RequestsMock() as rsps:
        yield rsps


def add_swapi_list(rsps: responses.RequestsMock, resource: str, results: list[dict], next_url: str | None = None) -> None:
    """Register mock for SWAPI list endpoint."""
    url = f"https://swapi.dev/api/{resource}/"
    body = {"count": len(results), "results": results, "next": next_url, "previous": None}
    rsps.add(responses.GET, url, json=body, status=200)


def add_swapi_resource(rsps: responses.RequestsMock, resource: str, resource_id: int, data: dict) -> None:
    """Register mock for SWAPI single resource."""
    url = f"https://swapi.dev/api/{resource}/{resource_id}/"
    rsps.add(responses.GET, url, json=data, status=200)


def add_swapi_url(rsps: responses.RequestsMock, url: str, data: dict) -> None:
    """Register mock for any SWAPI URL."""
    rsps.add(responses.GET, url, json=data, status=200)
