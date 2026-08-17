import json
import re
from abc import ABC, abstractmethod
from typing import Any, Iterable, Optional, Type, Union

from pydantic import BaseModel, TypeAdapter

from sinch.core.models.http_response import HTTPResponse
from sinch.core.models.internal.utils import query_params_to_comma_joined_lists
from sinch.core.types import BM


class HTTPEndpoint(ABC):
    """Minimal contract the transport layer needs to send any request."""

    IS_RETRYABLE: bool = False

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

    def __init__(self, project_id: Optional[str], request_data: Any) -> None:
        self.project_id = project_id
        self.request_data = request_data

    def build_query_params(self) -> Optional[dict]:
        """Builds the query string parameters sent with the request."""
        return None

    def request_body(self) -> Optional[Union[str, dict]]:
        """
        Builds the request body sent with the request.

        Mirrors what `requests`' `data=` accepts: a `str` is sent as-is, a `dict` is form-urlencoded.
        """
        return None

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
        return self.ENDPOINT_URL.format(
            origin=self._get_origin(sinch),
            project_id=self.project_id,
            **vars(self.request_data),
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
    
    def _build_body_data(self) -> dict[str, Any]:
        """Builds the request body fields as a dict, excluding path params, QUERY_PARAM_FIELDS and QUERY_PARAM_FIELDS_EXPLODE_FALSE."""
        exclude = (
            self._get_path_params_from_url()
            | self.QUERY_PARAM_FIELDS
            | self.QUERY_PARAM_FIELDS_EXPLODE_FALSE
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

    def request_body(self) -> Optional[str]:
        """Builds the request body, serialized as a JSON string."""
        body = self._build_body_data()
        return json.dumps(body) if body else None

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
        return self._process_response_model(response.body, self.response_model)
