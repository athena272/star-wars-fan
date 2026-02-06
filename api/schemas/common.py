"""Common request/response schemas."""

from enum import Enum


class SortOrder(str, Enum):
    """Sort direction for list endpoints."""

    ASC = "asc"
    DESC = "desc"
