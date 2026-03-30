import pytest
from unittest.mock import Mock, call
from sinch.core.enums import HTTPAuthentication
from sinch.core.exceptions import ValidationException
from sinch.core.models.http_request import HttpRequest
from sinch.core.endpoint import HTTPEndpoint
from sinch.core.models.http_response import HTTPResponse
from sinch.core.ports.http_transport import HTTPTransport
from sinch.core.token_manager import TokenState


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


class MockHTTPTransport(HTTPTransport):
    """Transport whose send() returns from a pre-configured list of responses."""

    def __init__(self, sinch, responses=None):
        super().__init__(sinch)
        self._responses = list(responses or [])
        self._call_count = 0

    def send(self, endpoint: HTTPEndpoint) -> HTTPResponse:
        if self._call_count < len(self._responses):
            resp = self._responses[self._call_count]
        else:
            resp = HTTPResponse(status_code=200, body={}, headers={})
        self._call_count += 1
        return resp

    @property
    def call_count(self):
        return self._call_count


# Synchronous Transport Tests
class TestHTTPTransport:
    @pytest.mark.parametrize("auth_type", [
        HTTPAuthentication.BASIC.value,
        HTTPAuthentication.OAUTH.value,
        HTTPAuthentication.SMS_TOKEN.value
    ])
    def test_authenticate(self, mock_sinch, base_request, auth_type):
        transport = MockHTTPTransport(mock_sinch)
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
        transport = MockHTTPTransport(mock_sinch)
        endpoint = _make_mock_endpoint(auth_type)

        for cred, value in missing_creds.items():
            setattr(mock_sinch.configuration, cred, value)

        with pytest.raises(ValidationException):
            transport.authenticate(endpoint, base_request)


class TestTokenRefreshRetry:
    """Tests for the automatic token refresh on 401 expired responses."""

    @staticmethod
    def _expired_401():
        return HTTPResponse(
            status_code=401,
            body={"error": "token expired"},
            headers={"www-authenticate": "Bearer error=\"expired\""},
        )

    @staticmethod
    def _non_expired_401():
        return HTTPResponse(
            status_code=401,
            body={"error": "unauthorized"},
            headers={"www-authenticate": "Bearer error=\"invalid_token\""},
        )

    @staticmethod
    def _ok_200():
        return HTTPResponse(status_code=200, body={"ok": True}, headers={})

    def test_retry_succeeds_after_expired_token(self, mock_sinch):
        """A single 401-expired followed by a 200 should retry once and succeed."""
        from sinch.core.token_manager import TokenManager

        token_manager = Mock(spec=TokenManager)
        token_manager.token_state = TokenState.VALID

        def mark_expired(http_response):
            token_manager.token_state = TokenState.EXPIRED

        token_manager.handle_invalid_token.side_effect = mark_expired
        mock_sinch.configuration.token_manager = token_manager

        transport = MockHTTPTransport(
            mock_sinch,
            responses=[self._expired_401(), self._ok_200()],
        )
        endpoint = _make_mock_endpoint(HTTPAuthentication.OAUTH.value)

        result = transport.request(endpoint)

        assert result.status_code == 200
        assert transport.call_count == 2
        token_manager.handle_invalid_token.assert_called_once()

    def test_no_infinite_loop_on_persistent_401(self, mock_sinch):
        """Two consecutive 401-expired must NOT cause infinite retries.

        The second 401 should be handed to the endpoint's error handler
        and send() should be called at most twice.
        """
        from sinch.core.token_manager import TokenManager

        token_manager = Mock(spec=TokenManager)
        token_manager.token_state = TokenState.VALID

        def mark_expired(http_response):
            token_manager.token_state = TokenState.EXPIRED

        token_manager.handle_invalid_token.side_effect = mark_expired
        mock_sinch.configuration.token_manager = token_manager

        transport = MockHTTPTransport(
            mock_sinch,
            responses=[self._expired_401(), self._expired_401()],
        )
        endpoint = _make_mock_endpoint(HTTPAuthentication.OAUTH.value, error_on_4xx=True)

        with pytest.raises(ValidationException, match="401"):
            transport.request(endpoint)

        # send() must have been called exactly twice: initial + one retry
        assert transport.call_count == 2

    def test_no_retry_when_401_is_not_expired(self, mock_sinch):
        """A 401 without 'expired' in WWW-Authenticate should NOT trigger a retry."""
        from sinch.core.token_manager import TokenManager

        token_manager = Mock(spec=TokenManager)
        token_manager.token_state = TokenState.VALID

        # handle_invalid_token inspects the header but does NOT set EXPIRED
        # because the header says "invalid_token", not "expired"
        token_manager.handle_invalid_token.side_effect = lambda r: None
        mock_sinch.configuration.token_manager = token_manager

        transport = MockHTTPTransport(
            mock_sinch,
            responses=[self._non_expired_401()],
        )
        endpoint = _make_mock_endpoint(HTTPAuthentication.OAUTH.value, error_on_4xx=True)

        with pytest.raises(ValidationException, match="401"):
            transport.request(endpoint)

        # send() called only once — no retry
        assert transport.call_count == 1

    def test_no_retry_for_non_oauth_endpoint(self, mock_sinch):
        """A 401 on a BASIC-auth endpoint should NOT trigger token refresh."""
        from sinch.core.token_manager import TokenManager

        token_manager = Mock(spec=TokenManager)
        mock_sinch.configuration.token_manager = token_manager

        transport = MockHTTPTransport(
            mock_sinch,
            responses=[self._expired_401()],
        )
        endpoint = _make_mock_endpoint(HTTPAuthentication.BASIC.value, error_on_4xx=True)

        with pytest.raises(ValidationException, match="401"):
            transport.request(endpoint)

        assert transport.call_count == 1
        token_manager.handle_invalid_token.assert_not_called()
