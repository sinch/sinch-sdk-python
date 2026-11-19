from typing import Iterable, Mapping, Optional, Tuple, Union

from sinch.core.clients.request_options import RequestOptions
from sinch.core.enums import HTTPMethods
from sinch.core.exceptions import ValidationException
from sinch.core.models.http_body import (
    HttpBody,
    MultipartBody,
    MultipartValue,
)
from sinch.core.models.http_headers import HttpHeaders
from sinch.core.models.http_request import HttpRequest
from sinch.core.models.http_response import HTTPResponse
from sinch.core.models.internal.utils import parse_charset
from sinch.domains.http.api.v1.base import BaseHttp
from sinch.domains.http.api.v1.internal import HttpCallEndpoint


class Http(BaseHttp):
    """
    Low-level HTTP primitives to call any Sinch API, with the facilities of the SDK: authentication,
    token cache, retries and request level options.

    The URL and the query parameters are sent as given, without any encoding or processing, and so is a
    ``str`` or ``bytes`` body. A :class:`~sinch.core.models.http_body.HttpBody` is encoded by the SDK.
    A response with a status of 400 or above raises :class:`~sinch.domains.http.api.v1.exceptions.HttpException`.
    """

    def get(
        self,
        url: str,
        query_params: str = "",
        headers: Optional[Union[Mapping[str, str], Iterable[Tuple[str, str]]]] = None,
        options: Optional[RequestOptions] = None,
    ) -> HTTPResponse:
        """
        Sends a GET request.

        :param url: The absolute URL, without query parameters.
        :type url: str
        :param query_params: The URL-encoded query string. The leading ``?`` is added if missing.
        :type query_params: str
        :param headers: The headers to send, as a mapping or as ``(name, value)`` pairs. The values of a repeated
            header are kept in order, and the default transport sends them joined with ``", "``.
        :type headers: Optional[Union[Mapping[str, str], Iterable[Tuple[str, str]]]]
        :param options: The options for this request, overriding the client configuration.
        :type options: Optional[RequestOptions]

        :returns: The HTTP response.
        :rtype: HTTPResponse
        """
        return self._send(
            method=HTTPMethods.GET,
            url=url,
            query_params=query_params,
            headers=headers,
            body=None,
            options=options,
        )

    def delete(
        self,
        url: str,
        query_params: str = "",
        headers: Optional[Union[Mapping[str, str], Iterable[Tuple[str, str]]]] = None,
        options: Optional[RequestOptions] = None,
    ) -> HTTPResponse:
        """
        Sends a DELETE request.

        :param url: The absolute URL, without query parameters.
        :type url: str
        :param query_params: The URL-encoded query string. The leading ``?`` is added if missing.
        :type query_params: str
        :param headers: The headers to send, as a mapping or as ``(name, value)`` pairs. The values of a repeated
            header are kept in order, and the default transport sends them joined with ``", "``.
        :type headers: Optional[Union[Mapping[str, str], Iterable[Tuple[str, str]]]]
        :param options: The options for this request, overriding the client configuration.
        :type options: Optional[RequestOptions]

        :returns: The HTTP response.
        :rtype: HTTPResponse
        """
        return self._send(
            method=HTTPMethods.DELETE,
            url=url,
            query_params=query_params,
            headers=headers,
            body=None,
            options=options,
        )

    def post(
        self,
        url: str,
        body: Optional[Union[str, bytes, HttpBody]] = None,
        query_params: str = "",
        headers: Optional[Union[Mapping[str, str], Iterable[Tuple[str, str]]]] = None,
        options: Optional[RequestOptions] = None,
    ) -> HTTPResponse:
        """
        Sends a POST request.

        :param url: The absolute URL, without query parameters.
        :type url: str
        :param body: The body. A :class:`~sinch.core.models.http_body.HttpBody` sets the ``Content-Type`` header,
            replacing any given. Any other body requires that header: ``bytes`` are sent untouched and a ``str``
            is encoded with the charset it declares, UTF-8 if it declares none.
        :type body: Optional[Union[str, bytes, HttpBody]]
        :param query_params: The URL-encoded query string. The leading ``?`` is added if missing.
        :type query_params: str
        :param headers: The headers to send, as a mapping or as ``(name, value)`` pairs. The values of a repeated
            header are kept in order, and the default transport sends them joined with ``", "``.
        :type headers: Optional[Union[Mapping[str, str], Iterable[Tuple[str, str]]]]
        :param options: The options for this request, overriding the client configuration.
        :type options: Optional[RequestOptions]

        :returns: The HTTP response.
        :rtype: HTTPResponse
        :raises ValidationException: If the body type is not supported,
            or a ``str`` or ``bytes`` body has no ``Content-Type`` header.
        """
        return self._send(
            method=HTTPMethods.POST,
            url=url,
            query_params=query_params,
            headers=headers,
            body=body,
            options=options,
        )

    def put(
        self,
        url: str,
        body: Optional[Union[str, bytes, HttpBody]] = None,
        query_params: str = "",
        headers: Optional[Union[Mapping[str, str], Iterable[Tuple[str, str]]]] = None,
        options: Optional[RequestOptions] = None,
    ) -> HTTPResponse:
        """
        Sends a PUT request.

        :param url: The absolute URL, without query parameters.
        :type url: str
        :param body: The body. A :class:`~sinch.core.models.http_body.HttpBody` sets the ``Content-Type`` header,
            replacing any given. Any other body requires that header: ``bytes`` are sent untouched and a ``str``
            is encoded with the charset it declares, UTF-8 if it declares none.
        :type body: Optional[Union[str, bytes, HttpBody]]
        :param query_params: The URL-encoded query string. The leading ``?`` is added if missing.
        :type query_params: str
        :param headers: The headers to send, as a mapping or as ``(name, value)`` pairs. The values of a repeated
            header are kept in order, and the default transport sends them joined with ``", "``.
        :type headers: Optional[Union[Mapping[str, str], Iterable[Tuple[str, str]]]]
        :param options: The options for this request, overriding the client configuration.
        :type options: Optional[RequestOptions]

        :returns: The HTTP response.
        :rtype: HTTPResponse
        :raises ValidationException: If the body type is not supported,
            or a ``str`` or ``bytes`` body has no ``Content-Type`` header.
        """
        return self._send(
            method=HTTPMethods.PUT,
            url=url,
            query_params=query_params,
            headers=headers,
            body=body,
            options=options,
        )

    def patch(
        self,
        url: str,
        body: Optional[Union[str, bytes, HttpBody]] = None,
        query_params: str = "",
        headers: Optional[Union[Mapping[str, str], Iterable[Tuple[str, str]]]] = None,
        options: Optional[RequestOptions] = None,
    ) -> HTTPResponse:
        """
        Sends a PATCH request.

        :param url: The absolute URL, without query parameters.
        :type url: str
        :param body: The body. A :class:`~sinch.core.models.http_body.HttpBody` sets the ``Content-Type`` header,
            replacing any given. Any other body requires that header: ``bytes`` are sent untouched and a ``str``
            is encoded with the charset it declares, UTF-8 if it declares none.
        :type body: Optional[Union[str, bytes, HttpBody]]
        :param query_params: The URL-encoded query string. The leading ``?`` is added if missing.
        :type query_params: str
        :param headers: The headers to send, as a mapping or as ``(name, value)`` pairs. The values of a repeated
            header are kept in order, and the default transport sends them joined with ``", "``.
        :type headers: Optional[Union[Mapping[str, str], Iterable[Tuple[str, str]]]]
        :param options: The options for this request, overriding the client configuration.
        :type options: Optional[RequestOptions]

        :returns: The HTTP response.
        :rtype: HTTPResponse
        :raises ValidationException: If the body type is not supported,
            or a ``str`` or ``bytes`` body has no ``Content-Type`` header.
        """
        return self._send(
            method=HTTPMethods.PATCH,
            url=url,
            query_params=query_params,
            headers=headers,
            body=body,
            options=options,
        )

    def post_form_data(
        self,
        url: str,
        form_params: Mapping[str, MultipartValue],
        query_params: str = "",
        headers: Optional[Union[Mapping[str, str], Iterable[Tuple[str, str]]]] = None,
        options: Optional[RequestOptions] = None,
    ) -> HTTPResponse:
        """
        Sends a POST request with a ``multipart/form-data`` body. The ``Content-Type`` header is set by the SDK.

        :param url: The absolute URL, without query parameters.
        :type url: str
        :param form_params: The form fields, sent in the given order. A
            :class:`~sinch.core.models.http_body.FilePart` is sent as a file and any other value as a text field.
            A list value repeats the field, and it can mix files and other values. A ``None`` value is omitted.
        :type form_params: Mapping[str, Optional[Union[str, bytes, int, float, bool, FilePart, Sequence[Union[str, bytes, int, float, bool, FilePart]]]]]
        :param query_params: The URL-encoded query string. The leading ``?`` is added if missing.
        :type query_params: str
        :param headers: The headers to send, as a mapping or as ``(name, value)`` pairs. The values of a repeated
            header are kept in order, and the default transport sends them joined with ``", "``.
        :type headers: Optional[Union[Mapping[str, str], Iterable[Tuple[str, str]]]]
        :param options: The options for this request, overriding the client configuration.
        :type options: Optional[RequestOptions]

        :returns: The HTTP response.
        :rtype: HTTPResponse
        """
        return self._send(
            method=HTTPMethods.POST,
            url=url,
            query_params=query_params,
            headers=headers,
            body=MultipartBody(fields=form_params),
            options=options,
        )

    def _send(
        self,
        method: HTTPMethods,
        url: str,
        query_params: str,
        headers: Optional[Union[Mapping[str, str], Iterable[Tuple[str, str]]]],
        body: Optional[Union[str, bytes, HttpBody]],
        options: Optional[RequestOptions],
    ) -> HTTPResponse:
        if query_params and not query_params.startswith("?"):
            query_params = f"?{query_params}"
        request_headers = HttpHeaders(headers)
        request_data = HttpRequest(
            method=method.value,
            url=url,
            query_parameters=query_params or "",
            headers=request_headers,
            content=_encode_body(body, request_headers) if body is not None else None,
        )
        return self._request(
            endpoint_class=HttpCallEndpoint,
            request_data=request_data,
            request_options=options,
        )


def _encode_body(body: Union[str, bytes, HttpBody], headers: HttpHeaders) -> bytes:
    if isinstance(body, HttpBody):
        headers["Content-Type"] = body.content_type
        return body.encode()
    if not isinstance(body, (str, bytes)):
        raise ValidationException(
            message=f"Unsupported body type: {type(body).__name__}.",
            is_from_server=False,
            response=None,
        )
    content_type = headers.get("Content-Type")
    if not content_type:
        raise ValidationException(
            message="Content-Type header is required when sending a body.",
            is_from_server=False,
            response=None,
        )
    if isinstance(body, str):
        return body.encode(parse_charset(content_type))
    return body
