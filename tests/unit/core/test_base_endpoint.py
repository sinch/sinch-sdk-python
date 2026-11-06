"""Tests for BaseHTTPEndpoint, one block per template method.

Covers build_url, request_body (legacy exclude_none dump and opt-in
UNSET_SERIALIZATION exclude_unset dump, including how non-None defaults
behave under each mode), build_query_params, build_headers (identical in
both modes) and handle_response.
"""

from typing import List, Literal, Optional

from unittest.mock import Mock

import pytest
from pydantic import BaseModel, Field, StrictStr

from sinch.core.endpoint import BaseHTTPEndpoint, _StandardPaginatedLinkEndpoint
from sinch.core.exceptions import ValidationException
from sinch.core.models.http_response import HTTPResponse
from tests.conftest import json_http_response
from sinch.core.models.internal.base_model_config import BaseConfigModel


class _Request(BaseConfigModel):
    item_id: Optional[str] = None
    name: Optional[str] = None
    kind: Literal["fixed"] = "fixed"
    limit: Optional[int] = None
    channels: Optional[List[str]] = None
    token: Optional[str] = Field(default=None, alias="X-Token")
    tags: Optional[List[str]] = Field(default=None, alias="X-Tags")


class _Response(BaseModel):
    id: StrictStr
    name: Optional[StrictStr] = None


class _EndpointError(Exception):
    pass


class _LegacyEndpoint(BaseHTTPEndpoint):
    UNSET_SERIALIZATION = False
    ENDPOINT_URL = "{origin}/v1/{project_id}/items/{item_id}"
    HTTP_METHOD = "POST"
    HTTP_AUTHENTICATION = "OAUTH"

    QUERY_PARAM_FIELDS = {"limit"}
    QUERY_PARAM_FIELDS_EXPLODE_FALSE = {"channels"}

    def _get_origin(self, sinch) -> str:
        return "https://example.com"

    def _raise_for_error(self, response: HTTPResponse) -> None:
        if response.status_code >= 400:
            raise _EndpointError(response.status_code)


class _UnsetEndpoint(_LegacyEndpoint):
    UNSET_SERIALIZATION = True


class _HeaderEndpoint(_UnsetEndpoint):
    HEADER_PARAM_FIELDS = {"token", "tags"}


def _body(endpoint) -> dict:
    return endpoint.build_body().data


class TestBuildUrl:
    def test_fills_origin_project_id_and_path_params(self):
        endpoint = _LegacyEndpoint("test_project_id", _Request(item_id="123"))

        assert (
            endpoint.build_url(sinch=None)
            == "https://example.com/v1/test_project_id/items/123"
        )


class TestBuildUrlProjectId:
    def test_url_with_project_id_and_no_project_id_expects_validation_exception(self):
        endpoint = _UnsetEndpoint(None, _Request(item_id="123"))

        with pytest.raises(ValidationException, match="project_id is required by this API"):
            endpoint.build_url(Mock())

    def test_url_without_project_id_expects_no_exception(self):
        endpoint = _UnsetEndpoint(None, _Request(item_id="123"))
        endpoint.ENDPOINT_URL = "https://example.com/v1/items/{item_id}"

        assert endpoint.build_url(Mock()) == "https://example.com/v1/items/123"


class TestRequestBody:
    def test_unset_serialization_defaults_to_true(self):
        assert BaseHTTPEndpoint.UNSET_SERIALIZATION is True

    def test_returns_none_when_body_is_empty(self):
        class PathOnlyRequest(BaseConfigModel):
            item_id: Optional[str] = None

        endpoint = _UnsetEndpoint("project", PathOnlyRequest(item_id="123"))

        assert endpoint.build_body() is None

    def test_path_and_query_fields_are_excluded_from_body(self):
        endpoint = _UnsetEndpoint(
            "project",
            _Request(item_id="123", name="My Item", limit=10, channels=["SMS"]),
        )
        body = _body(endpoint)

        assert "item_id" not in body
        assert "limit" not in body
        assert "channels" not in body

    def test_header_fields_are_excluded_from_body(self):
        endpoint = _HeaderEndpoint(
            "project", _Request(item_id="123", token="secret", tags=["a", "b"])
        )
        body = _body(endpoint)

        assert "token" not in body
        assert "X-Token" not in body
        assert "tags" not in body
        assert "X-Tags" not in body

    # Legacy mode (UNSET_SERIALIZATION = False)

    def test_legacy_explicit_none_is_excluded(self):
        endpoint = _LegacyEndpoint(
            "project", _Request(item_id="123", name=None)
        )

        assert "name" not in _body(endpoint)

    def test_legacy_provided_value_is_included(self):
        endpoint = _LegacyEndpoint(
            "project", _Request(item_id="123", name="My Item")
        )

        assert _body(endpoint)["name"] == "My Item"

    def test_legacy_non_none_default_is_included(self):
        endpoint = _LegacyEndpoint("project", _Request(item_id="123"))

        assert _body(endpoint)["kind"] == "fixed"

    # Unset mode (UNSET_SERIALIZATION = True)

    def test_unset_omitted_field_is_absent(self):
        endpoint = _UnsetEndpoint("project", _Request(item_id="123"))

        assert "name" not in _body(endpoint)

    def test_unset_explicit_none_is_sent_as_null(self):
        endpoint = _UnsetEndpoint(
            "project", _Request(item_id="123", name=None)
        )

        assert _body(endpoint)["name"] is None

    def test_unset_provided_value_is_included(self):
        endpoint = _UnsetEndpoint(
            "project", _Request(item_id="123", name="My Item")
        )

        assert _body(endpoint)["name"] == "My Item"

    def test_unset_non_none_default_survives_exclude_unset(self):
        """BaseConfigModel marks applied non-None defaults as set, so flipping
        an endpoint to UNSET_SERIALIZATION never drops a defaulted field."""
        endpoint = _UnsetEndpoint("project", _Request(item_id="123"))

        assert _body(endpoint)["kind"] == "fixed"

    def test_unset_non_none_default_is_dropped_without_base_config_model(self):
        """Documents why request models must inherit BaseConfigModel: on a
        plain BaseModel an applied default is unset and exclude_unset drops it."""

        class PlainRequest(BaseModel):
            item_id: Optional[str] = None
            kind: Literal["fixed"] = "fixed"

        endpoint = _UnsetEndpoint("project", PlainRequest(item_id="123"))

        assert endpoint.build_body() is None


class TestBuildQueryParams:
    def test_none_query_param_is_omitted_in_both_modes(self):
        """Query strings cannot express null: None never travels, with or
        without UNSET_SERIALIZATION."""
        request = _Request(item_id="123", limit=None)

        assert _LegacyEndpoint("project", request).build_query_params() == {}
        assert _UnsetEndpoint("project", request).build_query_params() == {}

    def test_provided_query_param_is_included(self):
        endpoint = _UnsetEndpoint("project", _Request(item_id="123", limit=10))

        assert endpoint.build_query_params() == {"limit": 10}

    def test_explode_false_list_is_comma_joined(self):
        endpoint = _UnsetEndpoint(
            "project", _Request(item_id="123", channels=["SMS", "RCS"])
        )

        assert endpoint.build_query_params() == {"channels": "SMS,RCS"}


class TestBuildHeaders:
    def test_no_header_fields_declared_returns_empty_dict(self):
        endpoint = _UnsetEndpoint("project", _Request(item_id="123"))

        assert endpoint.build_headers() == {}

    def test_none_header_field_is_omitted(self):
        endpoint = _HeaderEndpoint("project", _Request(item_id="123"))

        assert endpoint.build_headers() == {}

    def test_provided_header_field_uses_alias_as_header_name(self):
        endpoint = _HeaderEndpoint(
            "project", _Request(item_id="123", token="secret")
        )

        assert endpoint.build_headers() == {"X-Token": "secret"}

    def test_list_header_field_is_comma_joined(self):
        endpoint = _HeaderEndpoint(
            "project", _Request(item_id="123", tags=["a", "b"])
        )

        assert endpoint.build_headers() == {"X-Tags": "a,b"}


class TestHandleResponse:
    def test_returns_parsed_response_model(self):
        endpoint = _LegacyEndpoint(
            "project", _Request(item_id="123"), response_model=_Response
        )
        response = json_http_response(
            status=200, body={"id": "123", "name": "My Item"}, headers={}
        )

        parsed = endpoint.handle_response(response)

        assert isinstance(parsed, _Response)
        assert parsed.id == "123"
        assert parsed.name == "My Item"

    def test_returns_none_when_no_response_model_declared(self):
        endpoint = _LegacyEndpoint("project", _Request(item_id="123"))
        response = json_http_response(status=200, body={}, headers={})

        assert endpoint.handle_response(response) is None

    def test_raises_domain_error_on_error_response(self):
        endpoint = _LegacyEndpoint(
            "project", _Request(item_id="123"), response_model=_Response
        )
        response = json_http_response(
            status=400, body={"error": "Invalid argument"}, headers={}
        )

        with pytest.raises(_EndpointError):
            endpoint.handle_response(response)

    def test_raises_value_error_on_invalid_response_structure(self):
        endpoint = _LegacyEndpoint(
            "project", _Request(item_id="123"), response_model=_Response
        )
        response = json_http_response(
            status=200, body={"name": "missing required id"}, headers={}
        )

        with pytest.raises(ValueError, match="Invalid response structure"):
            endpoint.handle_response(response)


class TestBuildRequest:
    def test_expects_request_assembled_from_the_endpoint(self):
        endpoint = _HeaderEndpoint(
            "test_project_id",
            _Request(item_id="123", name="n", limit=5, token="secret"),
        )

        request_data = endpoint.build_request(sinch=None)

        assert request_data.method == "POST"
        assert request_data.url == "https://example.com/v1/test_project_id/items/123"
        assert request_data.query_parameters == "?limit=5"
        assert request_data.headers["X-Token"] == "secret"
        assert request_data.headers["Content-Type"] == "application/json"
        assert request_data.content.as_json() == {"name": "n", "kind": "fixed"}

    def test_without_body_expects_no_content_and_no_content_type(self):
        endpoint = _UnsetEndpoint("test_project_id", _Request(item_id="123"))
        endpoint.build_body = lambda: None

        request_data = endpoint.build_request(sinch=None)

        assert request_data.content is None
        assert "Content-Type" not in request_data.headers

    def test_expects_no_transport_concerns(self):
        endpoint = _UnsetEndpoint("test_project_id", _Request(item_id="123"))

        request_data = endpoint.build_request(sinch=None)

        assert "User-Agent" not in request_data.headers
        assert "Authorization" not in request_data.headers
        assert request_data.timeout_seconds is None


def test_request_options_expects_none_by_default():
    endpoint = _UnsetEndpoint("test_project_id", _Request(item_id="123"))

    assert endpoint.request_options is None


def test_paginated_link_endpoint_expects_request_with_link_url():
    endpoint = _UnsetEndpoint("test_project_id", _Request(item_id="123", limit=5))
    wrapper = _StandardPaginatedLinkEndpoint(
        endpoint, "https://api.sinch.com/next?page_token=abc"
    )

    request_data = wrapper.build_request(sinch=None)

    assert request_data.url == "https://api.sinch.com/next?page_token=abc"
    assert request_data.query_parameters == ""
    assert request_data.method == "POST"
