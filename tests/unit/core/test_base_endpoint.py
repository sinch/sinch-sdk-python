"""Tests for BaseHTTPEndpoint, one block per template method.

Covers build_url, request_body (legacy exclude_none dump and opt-in
UNSET_SERIALIZATION exclude_unset dump, including how non-None defaults
behave under each mode), build_query_params (identical in both modes) and
handle_response.
"""

import json
from typing import List, Literal, Optional

import pytest
from pydantic import BaseModel, StrictStr

from sinch.core.endpoint import BaseHTTPEndpoint
from sinch.core.models.http_response import HTTPResponse
from sinch.core.models.internal.base_model_config import BaseConfigModel


class _Request(BaseConfigModel):
    item_id: Optional[str] = None
    name: Optional[str] = None
    kind: Literal["fixed"] = "fixed"
    limit: Optional[int] = None
    channels: Optional[List[str]] = None


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


def _body(endpoint) -> dict:
    return json.loads(endpoint.request_body())


class TestBuildUrl:
    def test_fills_origin_project_id_and_path_params(self):
        endpoint = _LegacyEndpoint("test_project_id", _Request(item_id="123"))

        assert (
            endpoint.build_url(sinch=None)
            == "https://example.com/v1/test_project_id/items/123"
        )


class TestRequestBody:
    def test_unset_serialization_defaults_to_true(self):
        assert BaseHTTPEndpoint.UNSET_SERIALIZATION is True

    def test_returns_none_when_body_is_empty(self):
        class PathOnlyRequest(BaseConfigModel):
            item_id: Optional[str] = None

        endpoint = _UnsetEndpoint("project", PathOnlyRequest(item_id="123"))

        assert endpoint.request_body() is None

    def test_path_and_query_fields_are_excluded_from_body(self):
        endpoint = _UnsetEndpoint(
            "project",
            _Request(item_id="123", name="My Item", limit=10, channels=["SMS"]),
        )
        body = _body(endpoint)

        assert "item_id" not in body
        assert "limit" not in body
        assert "channels" not in body

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

        assert endpoint.request_body() is None


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


class TestHandleResponse:
    def test_returns_parsed_response_model(self):
        endpoint = _LegacyEndpoint(
            "project", _Request(item_id="123"), response_model=_Response
        )
        response = HTTPResponse(
            status_code=200, body={"id": "123", "name": "My Item"}, headers={}
        )

        parsed = endpoint.handle_response(response)

        assert isinstance(parsed, _Response)
        assert parsed.id == "123"
        assert parsed.name == "My Item"

    def test_returns_none_when_no_response_model_declared(self):
        endpoint = _LegacyEndpoint("project", _Request(item_id="123"))
        response = HTTPResponse(status_code=200, body={}, headers={})

        assert endpoint.handle_response(response) is None

    def test_raises_domain_error_on_error_response(self):
        endpoint = _LegacyEndpoint(
            "project", _Request(item_id="123"), response_model=_Response
        )
        response = HTTPResponse(
            status_code=400, body={"error": "Invalid argument"}, headers={}
        )

        with pytest.raises(_EndpointError):
            endpoint.handle_response(response)

    def test_raises_value_error_on_invalid_response_structure(self):
        endpoint = _LegacyEndpoint(
            "project", _Request(item_id="123"), response_model=_Response
        )
        response = HTTPResponse(
            status_code=200, body={"name": "missing required id"}, headers={}
        )

        with pytest.raises(ValueError, match="Invalid response structure"):
            endpoint.handle_response(response)
