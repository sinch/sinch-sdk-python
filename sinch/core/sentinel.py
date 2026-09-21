"""Sentinel for distinguishing omitted parameters from ``None``."""

from typing import TypeVar, Union

__all__ = ["Unset", "UNSET", "UnsetOr"]


class Unset:
    """Sentinel type: the parameter was not provided by the caller."""

    _instance = None

    def __new__(cls) -> "Unset":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance


UNSET = Unset()

_T = TypeVar("_T")

#: Alias for annotating an omittable parameter: ``UnsetOr[str]``.
UnsetOr = Union[_T, Unset]
