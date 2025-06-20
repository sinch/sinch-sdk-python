import pytest
from unittest.mock import Mock
from sinch.core.enums import HTTPAuthentication
from sinch.core.exceptions import ValidationException
from sinch.core.models.http_request import HttpRequest
from sinch.core.endpoint import HTTPEndpoint
from sinch.core.models.http_response import HTTPResponse
from sinch.core.ports.http_transport import HTTPTransport


# Mock classes and fixtures
class MockEndpoint(HTTPEndpoint):
    def __init__(self, auth_type):
        self.HTTP_AUTHENTICATION = auth_type
        self.HTTP_METHOD = "GET"

    def build_url(self, sinch):
        return "api.sinch.com/test"

    def get_url_without_origin(self, sinch):
        return "/test"

    def request_body(self):
        return {}

    def build_query_params(self):
        return {}

    def handle_response(self, response: HTTPResponse):
        return response


@pytest.fixture
def mock_sinch():
    sinch = Mock()
    sinch.configuration = Mock()
    sinch.configuration.key_id = "test_key_id"
    sinch.configuration.key_secret = "test_key_secret"
    sinch.configuration.project_id = "test_project_id"
    sinch.configuration.application_key = "test_app_key"
    sinch.configuration.application_secret = "dGVzdF9hcHBfc2VjcmV0X2Jhc2U2NA=="
    sinch.configuration.sms_api_token = "test_sms_token"
    sinch.configuration.service_plan_id = "test_service_plan"
    return sinch


@pytest.fixture
def base_request():
    return HttpRequest(
        headers={},
        protocol="https://",
        url="https://api.sinch.com/test",
        http_method="GET",
        request_body={},
        query_params={},
        auth=()
    )


class MockHTTPTransport(HTTPTransport):
    def request(self, endpoint: HTTPEndpoint) -> HTTPResponse:
        # Simple mock implementation that just returns a dummy response
        return HTTPResponse(status_code=200, body={}, headers={})


# Synchronous Transport Tests
class TestHTTPTransport:
    @pytest.mark.parametrize("auth_type", [
        HTTPAuthentication.BASIC.value,
        HTTPAuthentication.OAUTH.value,
        HTTPAuthentication.SIGNED.value,
        HTTPAuthentication.SMS_TOKEN.value
    ])
    def test_authenticate(self, mock_sinch, base_request, auth_type):
        transport = MockHTTPTransport(mock_sinch)
        endpoint = MockEndpoint(auth_type)

        if auth_type == HTTPAuthentication.BASIC.value:
            result = transport.authenticate(endpoint, base_request)
            assert result.auth == ("test_key_id", "test_key_secret")

        elif auth_type == HTTPAuthentication.OAUTH.value:
            mock_sinch.authentication.get_auth_token.return_value.access_token = "test_token"
            result = transport.authenticate(endpoint, base_request)
            assert result.headers["Authorization"] == "Bearer test_token"
            assert result.headers["Content-Type"] == "application/json"

        elif auth_type == HTTPAuthentication.SIGNED.value:
            result = transport.authenticate(endpoint, base_request)
            assert "x-timestamp" in result.headers
            assert "Authorization" in result.headers

        elif auth_type == HTTPAuthentication.SMS_TOKEN.value:
            result = transport.authenticate(endpoint, base_request)
            assert result.headers["Authorization"] == "Bearer test_sms_token"
            assert result.headers["Content-Type"] == "application/json"

    @pytest.mark.parametrize("auth_type,missing_creds", [
        (HTTPAuthentication.BASIC.value, {"key_id": None}),
        (HTTPAuthentication.OAUTH.value, {"key_secret": None}),
        (HTTPAuthentication.SIGNED.value, {"application_key": None}),
        (HTTPAuthentication.SMS_TOKEN.value, {"sms_api_token": None})
    ])
    def test_authenticate_missing_credentials(self, mock_sinch, base_request, auth_type, missing_creds):
        transport = MockHTTPTransport(mock_sinch)
        endpoint = MockEndpoint(auth_type)

        for cred, value in missing_creds.items():
            setattr(mock_sinch.configuration, cred, value)

        with pytest.raises(ValidationException):
            transport.authenticate(endpoint, base_request)
