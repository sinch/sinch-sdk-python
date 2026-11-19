from collections.abc import MutableMapping
from typing import Iterable, Iterator, List, Mapping, Optional, Tuple, Union

HeadersInput = Union[Mapping[str, str], Iterable[Tuple[str, str]]]


class HttpHeaders(MutableMapping[str, str]):
    """
    Case-insensitive, multi-value and order-preserving collection of HTTP headers.

    Behaves as a ``Mapping[str, str]``: reading a header repeated several times returns
    its values joined with ``", "``. Use :meth:`add`, :meth:`get_all` and :meth:`multi_items`
    to work with the individual values.

    :param headers: Initial headers, as a mapping or as ``(name, value)`` pairs.
    :type headers: Optional[Union[Mapping[str, str], Iterable[Tuple[str, str]]]]
    """

    def __init__(
        self,
        headers: Optional[HeadersInput] = None,
    ) -> None:
        self._items: List[Tuple[str, str]] = []
        if headers is None:
            return
        if isinstance(headers, HttpHeaders):
            pairs = headers.multi_items()
        elif isinstance(headers, Mapping):
            pairs = headers.items()
        else:
            pairs = headers
        for name, value in pairs:
            self.add(name, value)

    def add(self, name: str, value: str) -> None:
        """
        Appends a value for a header, keeping the values already present.

        :param name: The header name.
        :type name: str
        :param value: The header value.
        :type value: str
        """
        self._items.append((name, value))

    def get_all(self, name: str) -> List[str]:
        """
        Returns every value of a header, in insertion order.

        :param name: The header name, case-insensitive.
        :type name: str
        :returns: The values, or an empty list if the header is absent.
        :rtype: List[str]
        """
        key = name.lower()
        return [value for item_name, value in self._items if item_name.lower() == key]

    def multi_items(self) -> List[Tuple[str, str]]:
        """
        Returns every ``(name, value)`` pair, in insertion order, without joining repeated headers.

        :returns: The header pairs.
        :rtype: List[Tuple[str, str]]
        """
        return list(self._items)

    def __getitem__(self, name: str) -> str:
        values = self.get_all(name)
        if not values:
            raise KeyError(name)
        return ", ".join(values)

    def __setitem__(self, name: str, value: str) -> None:
        key = name.lower()
        position = next(
            (index for index, (item_name, _) in enumerate(self._items) if item_name.lower() == key),
            len(self._items),
        )
        self._items = [item for item in self._items if item[0].lower() != key]
        self._items.insert(position, (name, value))

    def __delitem__(self, name: str) -> None:
        key = name.lower()
        remaining = [item for item in self._items if item[0].lower() != key]
        if len(remaining) == len(self._items):
            raise KeyError(name)
        self._items = remaining

    def __iter__(self) -> Iterator[str]:
        seen = set()
        for name, _ in self._items:
            key = name.lower()
            if key not in seen:
                seen.add(key)
                yield name

    def __len__(self) -> int:
        return len({name.lower() for name, _ in self._items})

    def __repr__(self) -> str:
        return f"HttpHeaders({self._items!r})"
