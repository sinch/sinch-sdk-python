from typing import Any, Mapping, Optional, Tuple, Union, overload
from urllib.parse import parse_qs

from typing_extensions import deprecated

from sinch.core.models.http_body import UrlEncodedBody
from sinch.core.models.http_headers import HeadersInput, HttpHeaders
from sinch.core.models.http_content import HttpContent
from sinch.core.models.internal.utils import (
    basic_auth_header,
    encode_query_parameters,
)


class HttpRequest:
    """
    Prepared HTTP request handed to a transport.

    The 2.x constructor is still accepted until 3.0, by keyword (``http_method``, ``request_body``,
    ``query_params``, ``auth``) or positionally in its order: ``headers, url, http_method,
    request_body, query_params, auth``. The ``Authorization`` header is masked in ``repr()``.

    :param method: The HTTP method, one of :class:`~sinch.core.enums.HTTPMethods` values.
    :type method: str
    :param url: The absolute URL, without query parameters.
    :type url: str
    :param query_parameters: The URL-encoded query string, including the leading ``?``, or ``""``.
    :type query_parameters: str
    :param headers: The request headers, as a mapping or as ``(name, value)`` pairs.
    :type headers: Optional[Union[Mapping[str, str], Iterable[Tuple[str, str]]]]
    :param content: The body sent on the wire, UTF-8 encoded when built by the SDK. It is exposed as an
        :class:`~sinch.core.models.http_content.HttpContent` that decodes it with the charset of ``headers``.
    :type content: Optional[bytes]
    :param timeout_seconds: The timeout in seconds for this request, overriding the one of the client configuration.
        ``0`` disables it. ``None`` leaves the client configuration in effect.
    :type timeout_seconds: Optional[float]
    """

    @overload
    def __init__(
        self,
        *,
        url: str,
        method: str,
        query_parameters: str = "",
        headers: Optional[HeadersInput] = None,
        content: Optional[bytes] = None,
        timeout_seconds: Optional[float] = None,
    ) -> None:
        pass

    @overload
    @deprecated("Use HttpRequest(method=..., url=..., query_parameters=..., headers=..., content=...) instead; removed in 3.0.")
    def __init__(
        self,
        *,
        url: str,
        http_method: str,
        headers: Optional[Mapping[str, str]] = None,
        request_body: Optional[Union[str, bytes, Mapping[str, Any]]] = None,
        query_params: Optional[Mapping[str, Any]] = None,
        auth: Optional[Tuple[str, str]] = None,
    ) -> None:
        pass

    @overload
    @deprecated("Use HttpRequest(method=..., url=..., query_parameters=..., headers=..., content=...) instead; removed in 3.0.")
    def __init__(
        self,
        headers: Optional[Mapping[str, str]],
        url: str,
        http_method: str,
        request_body: Optional[Union[str, bytes, Mapping[str, Any]]],
        query_params: Optional[Mapping[str, Any]],
        auth: Optional[Tuple[str, str]],
        /,
    ) -> None:
        pass

    def __init__(
        self,
        headers: Optional[HeadersInput] = None,
        url: Optional[str] = None,
        http_method: Optional[str] = None,
        request_body: Optional[Union[str, bytes, Mapping[str, Any]]] = None,
        query_params: Optional[Mapping[str, Any]] = None,
        auth: Optional[Tuple[str, str]] = None,
        *,
        method: Optional[str] = None,
        query_parameters: str = "",
        content: Optional[bytes] = None,
        timeout_seconds: Optional[float] = None,
    ) -> None:
        self.url = url
        self.timeout_seconds = timeout_seconds
        self.method = method if method is not None else http_method
        self.query_parameters = query_parameters
        self.headers = headers if isinstance(headers, HttpHeaders) else HttpHeaders(headers)
        self.content = HttpContent(content, self.headers) if content is not None else None
        if request_body is not None:
            self.request_body = request_body
        if query_params is not None:
            self.query_params = query_params
        if auth:
            self.auth = auth

    @property
    def http_method(self) -> Optional[str]:
        """
        The HTTP method.

        .. deprecated:: 2.5
            Use :attr:`method` instead; this alias will be removed in 3.0.
        """
        return self.method

    @http_method.setter
    def http_method(self, value: str) -> None:
        self.method = value

    @property
    def request_body(self) -> Optional[str]:
        """
        The body sent on the wire, decoded as UTF-8 text. Setting a dict form-urlencodes it.

        .. deprecated:: 2.5
            Use :attr:`content` instead; this alias will be removed in 3.0.
        """
        return self.content.as_string() if self.content is not None else None

    @request_body.setter
    def request_body(self, value: Optional[Union[str, bytes, Mapping[str, Any]]]) -> None:
        if not value:
            self.content = None
        elif isinstance(value, Mapping):
            body = UrlEncodedBody(value)
            self.headers.setdefault("Content-Type", body.content_type)
            self.content = HttpContent(body.encode(), self.headers)
        else:
            self.content = HttpContent(value.encode("utf-8") if isinstance(value, str) else value, self.headers)

    @property
    def query_params(self) -> dict:
        """
        The query parameters as a dict; a repeated parameter maps to a list of values.

        .. deprecated:: 2.5
            Use :attr:`query_parameters` instead; this alias will be removed in 3.0.
        """
        parsed = parse_qs(self.query_parameters.lstrip("?"), keep_blank_values=True)
        return {key: values[0] if len(values) == 1 else values for key, values in parsed.items()}

    @query_params.setter
    def query_params(self, value: Optional[Mapping[str, Any]]) -> None:
        self.query_parameters = encode_query_parameters(value)

    @property
    def auth(self) -> None:
        """
        Always ``None``: Basic credentials are sent in the ``Authorization`` header.
        Setting a ``(username, password)`` tuple stamps that header.

        .. deprecated:: 2.5
            Read and set the ``Authorization`` header instead; this alias will be removed in 3.0.
        """
        return None

    @auth.setter
    def auth(self, value: Optional[Tuple[str, str]]) -> None:
        if value:
            self.headers["Authorization"] = basic_auth_header(*value)

    def __repr__(self) -> str:
        headers = HttpHeaders(
            (name, "***" if name.lower() == "authorization" else value)
            for name, value in self.headers.multi_items()
        )
        return (
            f"HttpRequest(method={self.method!r}, url={self.url!r}, "
            f"query_parameters={self.query_parameters!r}, headers={headers!r})"
        )
