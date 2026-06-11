import json
import pytest
from unittest.mock import Mock
from sinch.core.enums import HTTPAuthentication
from sinch.core.exceptions import ValidationException, SinchException
from sinch.core.models.http_request import HttpRequest
from sinch.core.endpoint import HTTPEndpoint
from sinch.core.models.http_response import HTTPResponse
from sinch.core.adapters.requests_http_transport import HTTPTransportRequests
from sinch.core.token_manager import TokenManager
from sinch.domains.authentication.models.v1.authentication import OAuthToken


# Mock classes and fixtures
def _make_mock_endpoint(auth_type, error_on_4xx=False):
    """Create a MockEndpoint that satisfies the abstract property contract."""

    class _Endpoint(HTTPEndpoint):
        HTTP_AUTHENTICATION = auth_type
        HTTP_METHOD = "GET"

        def __init__(self):
            # Skip super().__init__ — we don't need project_id / request_data
            pass

        def build_url(self, sinch):
            return "api.sinch.com/test"

        def get_url_without_origin(self, sinch):
            return "/test"

        def request_body(self):
            return {}

        def build_query_params(self):
            return {}

        def handle_response(self, response: HTTPResponse):
            if error_on_4xx and response.status_code >= 400:
                raise ValidationException(
                    message=f"HTTP {response.status_code}",
                    is_from_server=True,
                    response=response,
                )
            return response

    return _Endpoint()


def _requests_response(status_code, body=None, headers=None):
    """Fake of a requests.Response, just enough for deserialize_json_response."""
    resp = Mock()
    resp.status_code = status_code
    resp.content = json.dumps(body or {}).encode()
    resp.json.return_value = body or {}
    resp.headers = headers or {}
    return resp


def _server_rejecting_expired_token(accepted_token):
    """Fake http_session.request: 200 only when the request carries `accepted_token`,
    otherwise a 401-expired — like a server that rejects the stale token."""
    def respond(*args, **kwargs):
        if kwargs["headers"].get("Authorization") == accepted_token:
            return _requests_response(200, body={"ok": True})
        return _requests_response(401, headers={"www-authenticate": 'Bearer error="expired"'})
    return respond


def _token_manager(mock_sinch, *, old="old", new="new"):
    """Mock TokenManager that hands out `old` and renews to `new`."""
    token_manager = Mock(spec=TokenManager)
    token_manager.refresh_auth_token.return_value = OAuthToken(
        access_token=new, expires_in=3599, scope="", token_type="bearer"
    )
    mock_sinch.configuration.token_manager = token_manager
    # authenticate() reads the initial token via sinch.authentication.get_auth_token()
    mock_sinch.authentication.get_auth_token.return_value.access_token = old
    return token_manager


@pytest.fixture
def mock_sinch():
    sinch = Mock()
    sinch.configuration = Mock()
    sinch.configuration.key_id = "test_key_id"
    sinch.configuration.key_secret = "test_key_secret"
    sinch.configuration.project_id = "test_project_id"
    sinch.configuration.sms_api_token = "test_sms_token"
    sinch.configuration.service_plan_id = "test_service_plan"
    return sinch


@pytest.fixture
def base_request():
    return HttpRequest(
        headers={},
        url="https://api.sinch.com/test",
        http_method="GET",
        request_body={},
        query_params={},
        auth=()
    )


class TestHTTPTransport:
    @pytest.mark.parametrize("auth_type", [
        HTTPAuthentication.BASIC.value,
        HTTPAuthentication.OAUTH.value,
        HTTPAuthentication.SMS_TOKEN.value
    ])
    def test_authenticate(self, mock_sinch, base_request, auth_type):
        transport = HTTPTransportRequests(mock_sinch)
        endpoint = _make_mock_endpoint(auth_type)

        if auth_type == HTTPAuthentication.BASIC.value:
            result = transport.authenticate(endpoint, base_request)
            assert result.auth == ("test_key_id", "test_key_secret")

        elif auth_type == HTTPAuthentication.OAUTH.value:
            mock_sinch.authentication.get_auth_token.return_value.access_token = "test_token"
            result = transport.authenticate(endpoint, base_request)
            assert result.headers["Authorization"] == "Bearer test_token"
            assert result.headers["Content-Type"] == "application/json"

        elif auth_type == HTTPAuthentication.SMS_TOKEN.value:
            result = transport.authenticate(endpoint, base_request)
            assert result.headers["Authorization"] == "Bearer test_sms_token"
            assert result.headers["Content-Type"] == "application/json"

    @pytest.mark.parametrize("auth_type,missing_creds", [
        (HTTPAuthentication.BASIC.value, {"key_id": None}),
        (HTTPAuthentication.OAUTH.value, {"key_secret": None}),
        (HTTPAuthentication.SMS_TOKEN.value, {"sms_api_token": None})
    ])
    def test_authenticate_missing_credentials(self, mock_sinch, base_request, auth_type, missing_creds):
        transport = HTTPTransportRequests(mock_sinch)
        endpoint = _make_mock_endpoint(auth_type)

        for cred, value in missing_creds.items():
            setattr(mock_sinch.configuration, cred, value)

        with pytest.raises(ValidationException):
            transport.authenticate(endpoint, base_request)


class TestSend:
    def test_send_maps_requests_response(self, mock_sinch, base_request):
        transport = HTTPTransportRequests(mock_sinch)
        transport.http_session.request = Mock(
            return_value=_requests_response(200, body={"x": 1})
        )

        result = transport.send(base_request)

        assert isinstance(result, HTTPResponse)
        assert result.status_code == 200
        assert result.body == {"x": 1}

    def test_send_empty_body_returns_empty_dict(self, mock_sinch, base_request):
        transport = HTTPTransportRequests(mock_sinch)
        transport.http_session.request = Mock(
            return_value=Mock(status_code=204, content=b"", headers={})
        )

        result = transport.send(base_request)

        assert result.status_code == 204
        assert result.body == {}

    def test_send_raises_on_invalid_json(self, mock_sinch, base_request):
        transport = HTTPTransportRequests(mock_sinch)
        bad_response = Mock(status_code=200, content=b"not json", headers={})
        bad_response.json.side_effect = ValueError("bad json")
        transport.http_session.request = Mock(return_value=bad_response)

        with pytest.raises(SinchException):
            transport.send(base_request)


class TestTokenRefreshRetry:
    """Tests for the automatic token refresh on 401-expired responses."""

    @staticmethod
    def _expired_401():
        return _requests_response(
            401,
            body={"error": "token expired"},
            headers={"www-authenticate": 'Bearer error="expired"'},
        )

    @staticmethod
    def _non_expired_401():
        return _requests_response(
            401,
            body={"error": "unauthorized"},
            headers={"www-authenticate": 'Bearer error="invalid_token"'},
        )

    def test_retry_succeeds_after_expired_token(self, mock_sinch):
        token_manager = _token_manager(mock_sinch)
        transport = HTTPTransportRequests(mock_sinch)
        # The server accepts only the renewed token, so a 200 proves the retry re-stamped it.
        transport.http_session.request = Mock(side_effect=_server_rejecting_expired_token("Bearer new"))
        endpoint = _make_mock_endpoint(HTTPAuthentication.OAUTH.value)

        result = transport.request(endpoint)

        assert result.status_code == 200
        assert transport.http_session.request.call_count == 2
        token_manager.refresh_auth_token.assert_called_once_with("old")

    def test_no_retry_when_401_is_not_expired(self, mock_sinch):
        token_manager = _token_manager(mock_sinch)
        transport = HTTPTransportRequests(mock_sinch)
        transport.http_session.request = Mock(side_effect=[self._non_expired_401()])
        endpoint = _make_mock_endpoint(HTTPAuthentication.OAUTH.value, error_on_4xx=True)

        with pytest.raises(ValidationException, match="401"):
            transport.request(endpoint)

        assert transport.http_session.request.call_count == 1
        token_manager.refresh_auth_token.assert_not_called()

    def test_no_retry_for_non_oauth_endpoint(self, mock_sinch):
        token_manager = _token_manager(mock_sinch)
        transport = HTTPTransportRequests(mock_sinch)
        transport.http_session.request = Mock(side_effect=[self._expired_401()])
        endpoint = _make_mock_endpoint(HTTPAuthentication.BASIC.value, error_on_4xx=True)

        with pytest.raises(ValidationException, match="401"):
            transport.request(endpoint)

        assert transport.http_session.request.call_count == 1
        token_manager.refresh_auth_token.assert_not_called()

    def test_only_one_retry_on_persistent_401(self, mock_sinch):
        token_manager = _token_manager(mock_sinch)
        transport = HTTPTransportRequests(mock_sinch)
        transport.http_session.request = Mock(side_effect=[self._expired_401(), self._expired_401()])
        endpoint = _make_mock_endpoint(HTTPAuthentication.OAUTH.value, error_on_4xx=True)

        with pytest.raises(ValidationException, match="401"):
            transport.request(endpoint)

        assert transport.http_session.request.call_count == 2
        token_manager.refresh_auth_token.assert_called_once()

    def test_no_refresh_on_successful_request(self, mock_sinch):
        token_manager = _token_manager(mock_sinch)
        transport = HTTPTransportRequests(mock_sinch)
        transport.http_session.request = Mock(
            return_value=_requests_response(200, body={"ok": True})
        )
        endpoint = _make_mock_endpoint(HTTPAuthentication.OAUTH.value)

        result = transport.request(endpoint)

        assert result.status_code == 200
        assert transport.http_session.request.call_count == 1
        token_manager.refresh_auth_token.assert_not_called()

    def test_no_refresh_on_401_without_www_authenticate(self, mock_sinch):
        token_manager = _token_manager(mock_sinch)
        transport = HTTPTransportRequests(mock_sinch)
        transport.http_session.request = Mock(
            return_value=_requests_response(401, body={})
        )
        endpoint = _make_mock_endpoint(HTTPAuthentication.OAUTH.value, error_on_4xx=True)

        with pytest.raises(ValidationException, match="401"):
            transport.request(endpoint)

        assert transport.http_session.request.call_count == 1
        token_manager.refresh_auth_token.assert_not_called()
