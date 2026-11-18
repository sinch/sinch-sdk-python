import base64
import codecs
from email.message import Message
from typing import Any, Iterable, Mapping, Optional
from urllib.parse import urlencode

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


def encode_query_parameters(query_params: Optional[Mapping[str, Any]]) -> str:
    """Serializes query params into a URL-encoded query string, as ``requests`` does with ``params=``.

    A list value is sent as a repeated parameter and ``None`` values are omitted.

    :param query_params: Query-param dict, keyed by parameter name.
    :type query_params: Optional[Mapping[str, Any]]
    :returns: The query string including the leading ``?``, or ``""`` when there are no params.
    :rtype: str
    """
    pairs = []
    for key, value in (query_params or {}).items():
        values = value if isinstance(value, (list, tuple)) else [value]
        pairs.extend((key, item) for item in values if item is not None)
    return f"?{urlencode(pairs)}" if pairs else ""


def basic_auth_header(username: str, password: str) -> str:
    """Builds the ``Authorization`` header value for HTTP Basic credentials, as ``requests`` does with ``auth=``.

    :param username: The username.
    :type username: str
    :param password: The password.
    :type password: str
    :returns: The header value, ``"Basic <base64(username:password)>"``.
    :rtype: str
    """
    credentials = base64.b64encode(f"{username}:{password}".encode("latin1")).decode("ascii")
    return f"Basic {credentials}"


DEFAULT_CHARSET = "utf-8"


def parse_charset(content_type: Optional[str], default: str = DEFAULT_CHARSET) -> str:
    """Extracts the ``charset`` parameter of a ``Content-Type`` header value.

    :param content_type: The ``Content-Type`` header value, e.g. ``"text/plain; charset=iso-8859-1"``.
    :type content_type: Optional[str]
    :param default: The charset returned when none is declared or it is not a known Python codec.
    :type default: str
    :returns: The canonical name of the charset.
    :rtype: str
    """
    if not content_type:
        return default
    message = Message()
    message["Content-Type"] = content_type
    try:
        return codecs.lookup(message.get_content_charset() or default).name
    except LookupError:
        return default
