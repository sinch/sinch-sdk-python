"""
Backward compatibility of the 2.x transport API, kept until 3.0.

Covers transports written against the deprecated surface: the ``send(endpoint)`` hook,
the ``HttpRequest`` aliases (``http_method``, ``request_body``, ``query_params``, ``auth``),
the ``HTTPEndpoint.request_body()`` hook,
``HTTPResponse(status_code, headers, body)`` and the ``status_code`` / ``body`` aliases.
Delete this file together with that surface in 3.0.
"""
import json
from unittest.mock import Mock

import pytest
import requests

from sinch.core.adapters.requests_http_transport import HTTPTransportRequests
from sinch.core.endpoint import HTTPEndpoint
from sinch.core.enums import HTTPAuthentication
from sinch.core.exceptions import SinchException
from sinch.core.models.http_body import JsonBody, UrlEncodedBody
from sinch.core.models.http_request import HttpRequest
from sinch.core.models.http_response import HTTPResponse
from sinch.core.ports.http_transport import HTTPTransport
from sinch.domains.authentication.models.v1.authentication import OAuthToken
from tests.unit.test_http_transport import (  # noqa: F401
    _make_mock_endpoint,
    _requests_response,
    mock_sinch,
)


class _LegacyTransport(HTTPTransport):
    """A pre-2.1 transport that overrides the deprecated ``send(endpoint)`` hook."""

    def __init__(self, sinch, responses):
        super().__init__(sinch)
        self._responses = list(responses)
        self.send_calls = 0

    def send(self, endpoint: HTTPEndpoint) -> HTTPResponse:
        self.send_calls += 1
        return self._responses.pop(0)


class _NoHookTransport(HTTPTransport):
    """A transport that implements neither ``send`` nor ``send_request``."""
    pass


class TestLegacySend:
    """Tests for the deprecated ``send(endpoint)`` override path (_legacy_request)."""

    @staticmethod
    def _expired_401():
        return HTTPResponse(
            status_code=401,
            headers={"www-authenticate": 'Bearer error="expired"'},
            body={"error": "token expired"},
        )

    @staticmethod
    def _ok_200():
        return HTTPResponse(status_code=200, headers={}, body={"ok": True})

    def test_legacy_send_emits_deprecation_warning(self, mock_sinch):
        with pytest.warns(DeprecationWarning, match="send"):
            _LegacyTransport(mock_sinch, [self._ok_200()])

    def test_legacy_request_retries_on_expired_token(self, mock_sinch):
        token_manager = Mock()
        token_manager.token = OAuthToken(
            access_token="old", expires_in=3599, scope="", token_type="bearer"
        )
        token_manager.refresh_auth_token.return_value = OAuthToken(
            access_token="new", expires_in=3599, scope="", token_type="bearer"
        )
        mock_sinch.configuration.token_manager = token_manager

        with pytest.warns(DeprecationWarning):
            transport = _LegacyTransport(mock_sinch, [self._expired_401(), self._ok_200()])
        endpoint = _make_mock_endpoint(HTTPAuthentication.OAUTH.value)

        result = transport.request(endpoint)

        assert result.status == 200

        assert transport.send_calls == 2
        token_manager.refresh_auth_token.assert_called_once_with("old")

    def test_request_raises_when_send_request_not_implemented(self, mock_sinch):
        transport = _NoHookTransport(mock_sinch)
        endpoint = _make_mock_endpoint(HTTPAuthentication.BASIC.value)

        with pytest.raises(NotImplementedError, match="send_request"):
            transport.request(endpoint)


class _LegacySendRequestTransport(HTTPTransport):
    """A 2.1-2.4 transport, as in the README, reading the 2.x request model and returning ``HTTPResponse``."""

    def __init__(self, sinch, responses):
        super().__init__(sinch)
        self._responses = list(responses)
        self.prepared = []

    def send_request(self, request_data: HttpRequest) -> HTTPResponse:
        self.prepared.append(requests.Request(
            method=request_data.http_method,
            url=request_data.url,
            data=request_data.request_body,
            auth=request_data.auth,
            headers=request_data.headers,
            params=request_data.query_params,
        ).prepare())
        return self._responses.pop(0)


def _sent_by_requests_transport(sinch, endpoint):
    """The request HTTPTransportRequests puts on the wire for the endpoint."""
    transport = HTTPTransportRequests(sinch)
    transport.http_session.request = Mock(return_value=_requests_response(200))
    transport.request(endpoint)
    kwargs = transport.http_session.request.call_args.kwargs
    return requests.Request(
        method=kwargs["method"], url=kwargs["url"], data=kwargs["data"], headers=kwargs["headers"]
    ).prepare()


def _as_bytes(body):
    return body.encode("utf-8") if isinstance(body, str) else body


def _endpoint(auth_type):
    endpoint = _make_mock_endpoint(auth_type)
    endpoint.build_url = lambda sinch: "https://api.sinch.com/test"
    return endpoint


def _oauth_get_endpoint():
    endpoint = _make_mock_endpoint(HTTPAuthentication.OAUTH.value)
    endpoint.build_url = lambda sinch: "https://numbers.api.sinch.com/v1/projects/p/activeNumbers"
    endpoint.build_query_params = lambda: {"pageSize": 5, "types": ["MOBILE", "LOCAL"], "skip": None}
    endpoint.build_body = lambda: None
    return endpoint


def _basic_form_endpoint():
    endpoint = _make_mock_endpoint(HTTPAuthentication.BASIC.value)
    endpoint.HTTP_METHOD = "POST"
    endpoint.build_url = lambda sinch: "https://auth.sinch.com/oauth2/token"
    endpoint.build_body = lambda: UrlEncodedBody({"grant_type": "client_credentials"})
    return endpoint


class TestLegacySendRequestTransport:
    @pytest.mark.parametrize("make_endpoint", [_oauth_get_endpoint, _basic_form_endpoint])
    def test_sends_the_same_request_as_the_requests_transport(self, mock_sinch, make_endpoint):
        mock_sinch.authentication.get_auth_token.return_value.access_token = "token"
        legacy = _LegacySendRequestTransport(mock_sinch, [HTTPResponse(status_code=200, headers={})])

        legacy.request(make_endpoint())
        expected = _sent_by_requests_transport(mock_sinch, make_endpoint())

        sent = legacy.prepared[0]
        assert sent.method == expected.method
        assert sent.url == expected.url
        assert _as_bytes(sent.body) == _as_bytes(expected.body)
        assert sent.headers["Authorization"] == expected.headers["Authorization"]
        assert sent.headers.get("Content-Type") == expected.headers.get("Content-Type")

    def test_returned_http_response_reaches_the_endpoint(self, mock_sinch):
        legacy = _LegacySendRequestTransport(
            mock_sinch, [HTTPResponse(status_code=200, headers={}, body={"ok": True})]
        )

        result = legacy.request(_endpoint(HTTPAuthentication.BASIC.value))

        assert result.status == 200
        assert result.content.as_json() == {"ok": True}

    def test_refreshes_the_token_on_expired_401(self, mock_sinch):
        token_manager = Mock()
        token_manager.refresh_auth_token.return_value = OAuthToken(
            access_token="new", expires_in=3599, scope="", token_type="bearer"
        )
        mock_sinch.configuration.token_manager = token_manager
        mock_sinch.authentication.get_auth_token.return_value.access_token = "old"
        legacy = _LegacySendRequestTransport(mock_sinch, [
            HTTPResponse(status_code=401, headers={"WWW-Authenticate": 'Bearer error="expired"'}),
            HTTPResponse(status_code=200, headers={}, body={"ok": True}),
        ])

        result = legacy.request(_endpoint(HTTPAuthentication.OAUTH.value))

        assert result.status == 200
        assert legacy.prepared[1].headers["Authorization"] == "Bearer new"


class TestHttpRequestAliases:
    def test_constructor_accepts_the_2x_keyword_arguments(self):
        request = HttpRequest(
            headers={},
            url="https://auth.sinch.com/oauth2/token",
            http_method="POST",
            request_body={"grant_type": "client_credentials"},
            query_params={"a": "1"},
            auth=("key_id", "key_secret"),
        )

        assert request.method == "POST"
        assert request.content.as_bytes() == b"grant_type=client_credentials"
        assert request.headers["Content-Type"] == "application/x-www-form-urlencoded"
        assert request.query_parameters == "?a=1"
        assert request.headers["Authorization"].startswith("Basic ")

    def test_constructor_accepts_the_2x_positional_arguments(self):
        request = HttpRequest(
            {}, "https://api.sinch.com", "POST", {"a": "1"}, {"b": "2"}, ("key_id", "key_secret")
        )

        assert request.url == "https://api.sinch.com"
        assert request.method == "POST"
        assert request.content.as_bytes() == b"a=1"
        assert request.query_parameters == "?b=2"
        assert request.headers["Authorization"].startswith("Basic ")

    def test_http_method_reads_and_writes_method(self):
        request = HttpRequest(method="GET", url="https://api.sinch.com")

        request.http_method = "DELETE"

        assert request.http_method == "DELETE"
        assert request.method == "DELETE"

    def test_request_body_reads_and_writes_content(self):
        request = HttpRequest(method="POST", url="https://api.sinch.com")

        request.request_body = '{"a": 1}'

        assert request.request_body == '{"a": 1}'
        assert request.content.as_bytes() == b'{"a": 1}'

    def test_query_params_reads_query_parameters_as_a_dict(self):
        request = HttpRequest(
            method="GET", url="https://api.sinch.com", query_parameters="?pageSize=5&types=MOBILE&types=LOCAL"
        )

        assert request.query_params == {"pageSize": "5", "types": ["MOBILE", "LOCAL"]}

    def test_query_params_writes_query_parameters(self):
        request = HttpRequest(method="GET", url="https://api.sinch.com")

        request.query_params = {"to": "+46701234567"}

        assert request.query_parameters == "?to=%2B46701234567"

    def test_auth_is_always_none(self):
        request = HttpRequest(method="GET", url="https://api.sinch.com", auth=("key_id", "key_secret"))

        assert request.auth is None

    def test_setting_auth_stamps_the_basic_authorization_header(self):
        request = HttpRequest(method="GET", url="https://api.sinch.com")

        request.auth = ("key_id", "key_secret")

        expected = requests.Request("GET", "https://api.sinch.com", auth=("key_id", "key_secret")).prepare()
        assert request.headers["Authorization"] == expected.headers["Authorization"]


class TestHttpResponseAliases:
    def test_status_code_is_status(self):
        assert HTTPResponse(status=404).status_code == 404

    def test_body_is_the_parsed_json_content(self):
        response = HTTPResponse(status_code=200, headers={}, body={"id": "123"})

        assert response.body == {"id": "123"}

    def test_legacy_keywords_build_status_headers_and_content(self):
        response = HTTPResponse(status_code=200, headers={"X-Trace": "abc"}, body={"id": "123"})

        assert response.status == 200
        assert response.headers["x-trace"] == "abc"
        assert response.content.as_json() == {"id": "123"}

    def test_http_response_without_body_has_empty_content(self):
        response = HTTPResponse(status_code=204, headers={})

        assert response.content.as_bytes() == b""
        assert response.body == {}

    def test_http_response_accepts_positional_arguments(self):
        response = HTTPResponse(200, {}, {"id": "123"})

        assert response.status == 200
        assert response.body == {"id": "123"}

    def test_exception_exposes_the_status_code(self):
        response = HTTPResponse(status_code=400, headers={}, body={})

        error = SinchException(message="Bad request", response=response, is_from_server=True)

        assert error.response_status_code == 400
        assert error.http_response.status_code == 400


class TestEndpointRequestBody:
    def test_json_body_is_the_json_string(self):
        endpoint = _make_mock_endpoint(HTTPAuthentication.OAUTH.value)
        endpoint.build_body = lambda: JsonBody({"text": "héllo"})

        assert endpoint.request_body() == json.dumps({"text": "héllo"})

    def test_urlencoded_body_is_the_fields_dict(self):
        endpoint = _make_mock_endpoint(HTTPAuthentication.BASIC.value)
        endpoint.build_body = lambda: UrlEncodedBody({"grant_type": "client_credentials"})

        assert endpoint.request_body() == {"grant_type": "client_credentials"}

    def test_no_body_is_none(self):
        assert _make_mock_endpoint(HTTPAuthentication.OAUTH.value).request_body() is None


class TestDeserializeJsonResponse:
    def test_parses_the_json_body(self):
        response = Mock(content=b'{"id": "123"}')
        response.json.return_value = {"id": "123"}

        assert HTTPTransport.deserialize_json_response(response) == {"id": "123"}

    def test_empty_body_is_an_empty_dict(self):
        assert HTTPTransport.deserialize_json_response(Mock(content=b"")) == {}

    def test_raises_on_invalid_json(self):
        response = Mock(content=b"not json")
        response.json.side_effect = ValueError("bad json")

        with pytest.raises(SinchException):
            HTTPTransport.deserialize_json_response(response)
