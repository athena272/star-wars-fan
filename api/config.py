"""Configuration from environment variables."""

import os
from functools import lru_cache


def _get_int(key: str, default: int) -> int:
    raw = os.environ.get(key)
    if raw is None:
        return default
    try:
        return int(raw)
    except ValueError:
        return default


@lru_cache(maxsize=1)
def get_settings() -> "Settings":
    return Settings()


class Settings:
    """Application settings from environment."""

    swapi_base_url: str
    cache_ttl_seconds: int
    request_timeout_seconds: int
    request_retries: int

    def __init__(self) -> None:
        self.swapi_base_url = os.environ.get(
            "SWAPI_BASE_URL", "https://swapi.dev/api"
        ).rstrip("/")
        self.cache_ttl_seconds = _get_int("CACHE_TTL_SECONDS", 300)
        self.request_timeout_seconds = _get_int("REQUEST_TIMEOUT_SECONDS", 10)
        self.request_retries = _get_int("REQUEST_RETRIES", 3)
