import re
from abc import ABC, abstractmethod
from typing import Any, Mapping, Optional, Type, Union

from pydantic import BaseModel, TypeAdapter

from sinch.core.clients.request_options import RequestOptions
from sinch.core.exceptions import ValidationException
from sinch.core.models.http_body import HttpBody, JsonBody, UrlEncodedBody
from sinch.core.models.http_headers import HttpHeaders
from sinch.core.models.http_request import HttpRequest
from sinch.core.models.http_response import HTTPResponse
from sinch.core.models.internal.unions import parses_response
from sinch.core.models.internal.utils import (
    encode_query_parameters,
    query_params_to_comma_joined_lists,
)
from sinch.core.types import BM


class HTTPEndpoint(ABC):
    """Minimal contract the transport layer needs to send any request."""

    @property
    @abstractmethod
    def ENDPOINT_URL(self) -> str:
        """URL template for the request"""

    @property
    @abstractmethod
    def HTTP_METHOD(self) -> str:
        """HTTP verb the request is sent with."""

    @property
    @abstractmethod
    def HTTP_AUTHENTICATION(self) -> str:
        """Authentication scheme the request is sent with."""

    #: Options overriding, for this request only, the client level transport configuration.
    request_options: Optional[RequestOptions] = None

    #: Marker appended to the ``User-Agent`` header to tell this kind of request apart.
    USER_AGENT_TAG: Optional[str] = None

    def __init__(self, project_id: Optional[str], request_data: Any) -> None:
        self.project_id = project_id
        self.request_data = request_data

    def build_request(self, sinch) -> HttpRequest:
        """
        Builds the request sent to the API, without the transport level concerns: ``User-Agent``, timeout
        and authentication.

        By default it is assembled from :meth:`build_url`, :meth:`build_query_string`, :meth:`build_headers`
        and :meth:`build_body`, whose ``content_type`` sets the ``Content-Type`` header.
        """
        headers = HttpHeaders(self.build_headers())
        body = self.build_body()
        if body is not None:
            headers["Content-Type"] = body.content_type
        return HttpRequest(
            method=self.HTTP_METHOD,
            url=self.build_url(sinch),
            query_parameters=self.build_query_string(),
            headers=headers,
            content=body.encode() if body is not None else None,
        )

    def build_query_params(self) -> Optional[dict]:
        """Builds the query string parameters sent with the request."""
        return None

    def build_query_string(self) -> str:
        """
        Builds the query string sent with the request, including the leading ``?``, or ``""`` if there is none.

        By default it URL-encodes :meth:`build_query_params`.
        """
        return encode_query_parameters(self.build_query_params())

    def build_headers(self) -> Optional[Mapping[str, str]]:
        """Builds the request-specific headers sent with the request."""
        return None

    def build_body(self) -> Optional[HttpBody]:
        """Builds the request body sent with the request, or None if the request has no body."""
        return None

    def request_body(self) -> Optional[Union[str, dict]]:
        """
        The request body as returned in 2.x: a JSON string, or a dict for a form body.

        .. deprecated:: 2.5
            Use :meth:`build_body` instead; this method will be removed in 3.0.
        """
        body = self.build_body()
        if body is None:
            return None
        if isinstance(body, UrlEncodedBody):
            return dict(body.fields)
        return body.encode().decode("utf-8")

    @abstractmethod
    def build_url(self, sinch) -> str:
        """Builds the absolute URL the request is sent to."""

    @abstractmethod
    def handle_response(self, response: HTTPResponse) -> Any:
        """Raises on an error response, otherwise returns the parsed result."""


class BaseHTTPEndpoint(HTTPEndpoint, ABC):
    """
    Shared implementation for domain endpoint base classes.

    Centralizes the request-building and response-handling logic used per domain.
    A domain base class only needs to implement `_get_origin` and `_raise_for_error`.
    Concrete endpoints then only declare the `ENDPOINT_URL`, `HTTP_METHOD`, `HTTP_AUTHENTICATION` 
    and optionally `response_model` and `QUERY_PARAM_FIELDS`.
    """
    #: Opt-in unset semantics for the body: fields the caller didn't set are omitted
    #: and an explicit ``None`` is sent as ``null``. Endpoints already deployed keep
    #: the legacy behavior by overriding this field to False, until the next major version, where
    #: this defaults to ``True`` and ``_build_body_data_legacy`` is removed.
    UNSET_SERIALIZATION: bool = True

    # Always pass the field name for QUERY_PARAM_FIELDS and QUERY_PARAM_FIELDS_EXPLODE_FALSE, not the alias
    #: request_data fields sent as query params.
    QUERY_PARAM_FIELDS: set = set()
    #: request_data fields sent as query params with explode=false (comma-separated values).
    QUERY_PARAM_FIELDS_EXPLODE_FALSE: set = set()

    # Always pass the field name for HEADER_PARAM_FIELDS, not the alias
    #: request_data fields sent as request headers. The field's alias is used as the header name.
    HEADER_PARAM_FIELDS: set = set()

    def __init__(
        self,
        project_id: Optional[str],
        request_data: BaseModel,
        response_model: Optional[Type[BaseModel]] = None,
    ) -> None:
        super().__init__(project_id, request_data)
        self.request_data: BaseModel = request_data
        self.response_model: Optional[Type[BaseModel]] = response_model

    @abstractmethod
    def _get_origin(self, sinch) -> str:
        """Resolves the domain's base URL (scheme + host) from the sinch client config."""

    def build_url(self, sinch) -> str:
        """Fills ENDPOINT_URL with the domain origin, project_id and request_data fields."""
        self._validate_project_id()
        return self.ENDPOINT_URL.format(
            origin=self._get_origin(sinch),
            project_id=self.project_id,
            **vars(self.request_data),
        )

    def _validate_project_id(self) -> None:
        """Raises if ENDPOINT_URL needs the project_id and there is none."""
        if "{project_id}" in self.ENDPOINT_URL and not self.project_id:
            raise ValidationException(
                message=(
                    "project_id is required by this API. "
                    "It can be obtained from Sinch portal."
                ),
                is_from_server=False,
                response=None,
            )

    def _get_path_params_from_url(self) -> set:
        """Returns the ENDPOINT_URL placeholder names, excluding 'origin' and 'project_id'."""
        path_params = set(re.findall(r"\{(\w+)\}", self.ENDPOINT_URL))
        path_params.discard("origin")
        path_params.discard("project_id")

        return path_params

    def build_query_params(self) -> dict[str, Any]:
        """Builds the query string parameters sent with the request, from QUERY_PARAM_FIELDS and QUERY_PARAM_FIELDS_EXPLODE_FALSE."""
        query_params: dict[str, Any] = {}
        if self.QUERY_PARAM_FIELDS:
            query_params.update(self.request_data.model_dump(
                mode="json", by_alias=True, exclude_none=True,
                include=self.QUERY_PARAM_FIELDS,
            ))
        if self.QUERY_PARAM_FIELDS_EXPLODE_FALSE:
            exploded = self.request_data.model_dump(
                mode="json", by_alias=True, exclude_none=True,
                include=self.QUERY_PARAM_FIELDS_EXPLODE_FALSE,
            )
            query_params.update(query_params_to_comma_joined_lists(exploded, exploded.keys()))
        return query_params

    def build_headers(self) -> dict[str, str]:
        """Builds the request headers sent with the request, from HEADER_PARAM_FIELDS. The field's alias is used as the header name.

        A list value is comma-joined into a single header.
        """
        headers: dict[str, str] = {}
        if self.HEADER_PARAM_FIELDS:
            values = self.request_data.model_dump(
                mode="json", by_alias=True, exclude_none=True,
                include=self.HEADER_PARAM_FIELDS,
            )
            values = query_params_to_comma_joined_lists(values, values.keys())
            headers.update({name: str(value) for name, value in values.items()})
        return headers

    def _build_body_data(self) -> dict[str, Any]:
        """Builds the request body fields as a dict, excluding path params, QUERY_PARAM_FIELDS, QUERY_PARAM_FIELDS_EXPLODE_FALSE and HEADER_PARAM_FIELDS."""
        exclude = (
            self._get_path_params_from_url()
            | self.QUERY_PARAM_FIELDS
            | self.QUERY_PARAM_FIELDS_EXPLODE_FALSE
            | self.HEADER_PARAM_FIELDS
        )
        if self.UNSET_SERIALIZATION:
            return self.request_data.model_dump(
                by_alias=True, exclude_unset=True, exclude=exclude, mode="json"
            )
        return self._build_body_data_legacy(exclude)

    def _build_body_data_legacy(self, exclude: set) -> dict[str, Any]:
        """Builds the request body dict with the legacy semantics: ``None`` fields are omitted.

        .. deprecated:: Migrate the endpoint to ``UNSET_SERIALIZATION``; this method
            is removed in the next major version, where the flag defaults to ``True``.
        """
        return self.request_data.model_dump(
            by_alias=True, exclude_none=True, exclude=exclude, mode="json"
        )

    def build_body(self) -> Optional[JsonBody]:
        """Builds the JSON request body, or None if there are no body fields."""
        data = self._build_body_data()
        return JsonBody(data) if data else None

    @parses_response
    def _process_response_model(
        self, response_body: dict, response_model: Type[BM]
    ) -> BM:
        """Maps a raw response body dict onto response_model."""
        try:
            return TypeAdapter(response_model).validate_python(response_body)
        except Exception as e:
            raise ValueError(f"Invalid response structure: {e}") from e

    @abstractmethod
    def _raise_for_error(self, response: HTTPResponse) -> None:
        """Raises the domain-specific exception when the response indicates an error."""

    def handle_response(self, response: HTTPResponse) -> Optional[BaseModel]:
        """Raises a domain exception on error, otherwise returns the parsed response model (or None if the endpoint declares none)."""
        self._raise_for_error(response)
        if self.response_model is None:
            return None
        body = response.content.as_json()
        return self._process_response_model(body if body is not None else {}, self.response_model)


class _StandardPaginatedLinkEndpoint:
    """Delegates to a paginated endpoint but targets an absolute URL served by the API.

    The URL already carries the pagination information along with every other query parameter,
    so it is used as-is instead of being rebuilt from the request data.

    :meta private:
    """

    def __init__(self, endpoint, url):
        self._endpoint = endpoint
        self._url = url

    def __getattr__(self, name):
        # everything but the URL is handled by the endpoint being paginated
        return getattr(self._endpoint, name)

    def build_url(self, sinch):
        return self._url

    def build_query_params(self):
        return {}

    def build_query_string(self):
        return ""

    def build_request(self, sinch):
        return HTTPEndpoint.build_request(self, sinch)
