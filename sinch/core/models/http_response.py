import json
from typing import Any, Mapping, Optional, Union, overload

from typing_extensions import deprecated

from sinch.core.models.http_content import HttpContent
from sinch.core.models.http_headers import HttpHeaders


def _to_http_content(content: Any, body: Any, headers: HttpHeaders) -> HttpContent:
    if isinstance(content, HttpContent):
        return content
    if isinstance(content, bytes):
        return HttpContent(content, headers)
    # 2.x: an already-parsed JSON body, passed as ``body=`` or as the third positional argument
    legacy_body = content if content is not None else body
    if legacy_body is None:
        return HttpContent()
    return HttpContent(json.dumps(legacy_body).encode("utf-8"))


class HTTPResponse:
    """
    HTTP response returned by a transport.

    :param status: The HTTP status code.
    :type status: int
    :param headers: The response headers.
    :type headers: Optional[Union[HttpHeaders, Mapping[str, str]]]
    :param content: The response body, as received.
    :type content: Optional[Union[HttpContent, bytes]]
    :param status_code: The HTTP status code.

        .. deprecated:: 2.5
            Use ``status`` instead; this parameter will be removed in 3.0.
    :type status_code: Optional[int]
    :param body: The already-parsed JSON body, also accepted as the third positional argument.

        .. deprecated:: 2.5
            Use ``content`` instead; this parameter will be removed in 3.0.
    :type body: Any
    """

    @overload
    def __init__(
        self,
        status: int,
        headers: Optional[Union[HttpHeaders, Mapping[str, str]]] = None,
        content: Optional[Union[HttpContent, bytes]] = None,
    ) -> None:
        pass

    @overload
    @deprecated("Use HTTPResponse(status=..., headers=..., content=...) instead; removed in 3.0.")
    def __init__(self, *, status_code: int, headers: Mapping[str, str], body: Any = None) -> None:
        pass

    @overload
    @deprecated("Pass the raw body bytes as content instead of a parsed JSON body; removed in 3.0.")
    def __init__(self, status: int, headers: Mapping[str, str], body: Any, /) -> None:
        pass

    def __init__(
        self,
        status: Optional[int] = None,
        headers: Optional[Union[HttpHeaders, Mapping[str, str]]] = None,
        content: Any = None,
        *,
        status_code: Optional[int] = None,
        body: Any = None,
    ) -> None:
        self.status = status if status is not None else status_code
        self.headers = headers if isinstance(headers, HttpHeaders) else HttpHeaders(headers)
        self.content = _to_http_content(content, body, self.headers)

    @property
    def status_code(self) -> int:
        """
        The HTTP status code.

        .. deprecated:: 2.5
            Use :attr:`status` instead; this alias will be removed in 3.0.
        """
        return self.status

    @property
    def body(self) -> Any:
        """
        The body parsed as JSON, or an empty dict if the body is empty.

        .. deprecated:: 2.5
            Use ``content.as_json()`` instead; this alias will be removed in 3.0.
        """
        body = self.content.as_json()
        return body if body is not None else {}

    def __repr__(self) -> str:
        return f"HTTPResponse(status={self.status!r}, headers={self.headers!r})"
