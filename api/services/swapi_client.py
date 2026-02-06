"""HTTP client for SWAPI with retry, timeout, and in-memory cache."""

import time
from typing import Any

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from api.config import get_settings


class SWAPIClientError(Exception):
    """Raised when SWAPI request fails after retries."""

    pass


class SWAPINotFoundError(SWAPIClientError):
    """Raised when resource is not found (404)."""

    pass


def _make_session() -> requests.Session:
    settings = get_settings()
    session = requests.Session()
    retry = Retry(
        total=settings.request_retries,
        backoff_factor=0.5,
        status_forcelist=(502, 503, 504),
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    return session


_session: requests.Session | None = None


def _get_session() -> requests.Session:
    global _session
    if _session is None:
        _session = _make_session()
    return _session


class _CacheEntry:
    def __init__(self, data: Any, ttl_seconds: int) -> None:
        self.data = data
        self.expires_at = time.monotonic() + ttl_seconds

    def is_valid(self) -> bool:
        return time.monotonic() < self.expires_at


_cache: dict[str, _CacheEntry] = {}


def clear_cache() -> None:
    """Clear in-memory cache (e.g. for tests)."""
    _cache.clear()


def _cache_get(key: str) -> Any | None:
    entry = _cache.get(key)
    if entry is None or not entry.is_valid():
        if key in _cache:
            del _cache[key]
        return None
    return entry.data


def _cache_set(key: str, value: Any, ttl_seconds: int) -> None:
    _cache[key] = _CacheEntry(value, ttl_seconds)


def _get(url: str) -> dict[str, Any]:
    settings = get_settings()
    cached = _cache_get(url)
    if cached is not None:
        return cached
    session = _get_session()
    try:
        resp = session.get(url, timeout=settings.request_timeout_seconds)
        resp.raise_for_status()
    except requests.HTTPError as e:
        if e.response is not None and e.response.status_code == 404:
            raise SWAPINotFoundError(f"Resource not found: {url}") from e
        raise SWAPIClientError(f"SWAPI error: {e}") from e
    except requests.RequestException as e:
        raise SWAPIClientError(f"SWAPI request failed: {e}") from e
    data = resp.json()
    _cache_set(url, data, settings.cache_ttl_seconds)
    return data


def get_resource(resource: str, resource_id: int | None = None) -> dict[str, Any]:
    """Fetch a single resource or list (with optional page)."""
    settings = get_settings()
    base = f"{settings.swapi_base_url}/{resource.rstrip('/')}"
    if resource_id is not None:
        url = f"{base}/{resource_id}/"
    else:
        url = f"{base}/"
    return _get(url)


def get_list(
    resource: str,
    page: int | None = None,
    search: str | None = None,
) -> dict[str, Any]:
    """Fetch paginated list with optional search."""
    settings = get_settings()
    url = f"{settings.swapi_base_url}/{resource.rstrip('/')}/"
    params: list[tuple[str, str]] = []
    if page is not None:
        params.append(("page", str(page)))
    if search:
        params.append(("search", search))
    if params:
        url += "?" + "&".join(f"{k}={v}" for k, v in params)
    return _get(url)


def get_by_url(url: str) -> dict[str, Any]:
    """Fetch any SWAPI URL (for resolving related resources)."""
    if not url.startswith(("http://", "https://")):
        settings = get_settings()
        url = f"{settings.swapi_base_url}/{url.lstrip('/')}"
    return _get(url)
