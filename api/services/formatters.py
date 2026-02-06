"""Response formatting: sort, filter, expand related URLs."""

from typing import Any

from api.services.swapi_client import get_by_url


def _safe_number(value: Any) -> float | None:
    """Parse numeric value from SWAPI (often string or 'unknown')."""
    if value is None:
        return None
    if isinstance(value, (int, float)):
        return float(value)
    s = str(value).strip().lower()
    if s in ("unknown", "n/a", ""):
        return None
    try:
        return float(s.replace(",", ""))
    except ValueError:
        return None


def sort_results(
    items: list[dict[str, Any]],
    sort_by: str | None,
    order: str,
) -> list[dict[str, Any]]:
    """Sort list of SWAPI results in place; returns same list."""
    if not sort_by or not items:
        return items
    reverse = (order or "asc").lower() == "desc"

    def key(item: dict[str, Any]) -> Any:
        val = item.get(sort_by)
        num = _safe_number(val)
        if num is not None:
            return (0, num)
        return (1, str(val).lower() if val else "")

    items.sort(key=key, reverse=reverse)
    return items


def filter_people_by_gender(
    items: list[dict[str, Any]],
    gender: str | None,
) -> list[dict[str, Any]]:
    """Filter people by gender (case-insensitive)."""
    if not gender or not items:
        return items
    g = gender.strip().lower()
    return [p for p in items if (p.get("gender") or "").strip().lower() == g]


def filter_by_film_id(
    items: list[dict[str, Any]],
    film_id: int,
    film_url_path: str = "films",
) -> list[dict[str, Any]]:
    """Filter items that appear in the given film (by id)."""
    if not items:
        return items
    target_suffix = f"/films/{film_id}/"
    return [
        item
        for item in items
        if any(
            target_suffix in (u or "")
            for u in (item.get(film_url_path) or item.get("films") or [])
        )
    ]


def expand_urls(
    data: dict[str, Any],
    expand_keys: set[str],
) -> dict[str, Any]:
    """Replace URL fields with full objects (fetch from SWAPI)."""
    if not expand_keys:
        return data
    result = dict(data)
    for key in expand_keys:
        if key not in result:
            continue
        val = result[key]
        if isinstance(val, list):
            result[key] = [_fetch_one(u) for u in val if isinstance(u, str)]
        elif isinstance(val, str):
            result[key] = _fetch_one(val)
    return result


def _fetch_one(url: str) -> dict[str, Any] | str:
    """Fetch one URL; return minimal dict or original on error."""
    try:
        return get_by_url(url)
    except Exception:
        return url
