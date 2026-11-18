import json
from typing import Any, Optional

from sinch.core.models.http_headers import HttpHeaders
from sinch.core.models.internal.utils import parse_charset

_NOT_PARSED = object()


class HttpContent:
    """
    Buffered body of an HTTP request or response, read on demand.

    The charset used to decode it is the one declared by the ``Content-Type`` header of ``headers``,
    read when decoding, or UTF-8 if there is none.

    :param raw: The raw body bytes, or ``None`` for an empty body.
    :type raw: Optional[bytes]
    :param headers: The headers of the message carrying the body, used to resolve the charset.
    :type headers: Optional[HttpHeaders]
    """

    def __init__(self, raw: Optional[bytes] = None, headers: Optional[HttpHeaders] = None) -> None:
        self._raw = raw if raw is not None else b""
        self._headers = headers
        self._json = _NOT_PARSED

    def _charset(self) -> str:
        return parse_charset(self._headers.get("Content-Type") if self._headers is not None else None)

    def as_bytes(self) -> bytes:
        """
        Returns the body as received.

        :returns: The raw body.
        :rtype: bytes
        """
        return self._raw

    def as_string(self, errors: str = "strict") -> str:
        """
        Returns the body decoded with the charset of the ``Content-Type`` header, or UTF-8 if it declares none.

        :param errors: The codec error handler, as in :meth:`bytes.decode`.
        :type errors: str
        :returns: The body text.
        :rtype: str
        :raises UnicodeDecodeError: If the body is not valid in its charset and ``errors`` is ``"strict"``.
        """
        return self._raw.decode(self._charset(), errors=errors)

    def as_json(self) -> Any:
        """
        Returns the body parsed as JSON. The result is cached, so repeated calls return the same object.

        :returns: The parsed body, or ``None`` if the body is empty.
        :rtype: Any
        :raises json.JSONDecodeError: If the body is present but not valid JSON.
        :raises UnicodeDecodeError: If the body is not valid in the charset declared by ``Content-Type``.
        """
        if self._json is _NOT_PARSED:
            if not self._raw:
                self._json = None
            elif self._charset() == "utf-8":
                # json.loads detects UTF-8/16/32 and skips the BOM on bytes
                self._json = json.loads(self._raw)
            else:
                self._json = json.loads(self.as_string())
        return self._json
