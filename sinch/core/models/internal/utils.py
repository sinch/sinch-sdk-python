from typing import Iterable
from typing import Any

from sinch.core.sentinel import Unset


def strip_unset(data: dict[str, Any]) -> dict[str, Any]:
    """Removes the keys whose value is ``UNSET``.

    ``None`` values are kept: they were explicitly provided by the caller.

    :param data: Keyword arguments collected at the public SDK boundary.
    :type data: dict[str, Any]
    :returns: A new dict without the unset keys.
    :rtype: dict[str, Any]
    """
    return {k: v for k, v in data.items() if not isinstance(v, Unset)}


def query_params_to_comma_joined_lists(query_params: dict[str, Any], keys: Iterable[str]) -> dict[str, Any]:
    """Transforms list values in a query-param dict into comma-joined strings, for the given keys.

    :param query_params: Query-param dict, keyed by field alias.
    :type query_params: dict[str, Any]
    :param keys: Keys of the fields to join.
    :type keys: Iterable[str]
    :returns: The same dict, with list values under the given aliases comma-joined.
    :rtype: dict[str, Any]
    """
    for key in keys:
        value = query_params.get(key)
        if isinstance(value, list):
            query_params[key] = ",".join(str(item) for item in value)
    return query_params
