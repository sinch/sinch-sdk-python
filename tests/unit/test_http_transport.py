import json
import pytest
from unittest.mock import Mock
from sinch.core.clients.retry_configuration import RetryConfiguration
from sinch.core.clients.retry_manager import RetryManager
from sinch.core.enums import HTTPAuthentication, RetryPolicy
from sinch.core.exceptions import ValidationException, SinchException
from sinch.core.models.http_request import HttpRequest
from sinch.core.endpoint import HTTPEndpoint
from sinch.core.models.http_response import HTTPResponse
from sinch.core.adapters.requests_http_transport import HTTPTransportRequests
from sinch.core.ports.http_transport import HTTPTransport
from sinch.core.token_manager import TokenManager
from sinch.domains.authentication.models.v1.authentication import OAuthToken


# Mock classes and fixtures
def _make_mock_endpoint(auth_type, error_on_4xx=False, build_headers=None):
    """Create a MockEndpoint that satisfies the abstract property contract."""

    class _Endpoint(HTTPEndpoint):
        ENDPOINT_URL = "{origin}/test"
        HTTP_AUTHENTICATION = auth_type
        HTTP_METHOD = "GET"

        def __init__(self):
            # Skip super().__init__ — we don't need project_id / request_data
            pass

        def build_url(self, sinch):
            return "api.sinch.com/test"

        def request_body(self):
            return {}

        def build_query_params(self):
            return {}

        def build_headers(self):
            return build_headers() if build_headers else None

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
    sinch.configuration.retry_manager = RetryManager(RetryConfiguration())
    return sinch


@pytest.fixture
def no_sleep(mocker):
    return mocker.patch("sinch.core.clients.retry_manager.time.sleep")

@pytest.fixture
def no_jitter(mocker):
    return mocker.patch("sinch.core.clients.retry_manager.random.uniform", return_value=0.0)

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


class TestPrepareRequest:

    def test_merges_endpoint_headers(self, mock_sinch):
        transport = HTTPTransportRequests(mock_sinch)
        endpoint = _make_mock_endpoint(
            HTTPAuthentication.BASIC.value,
            build_headers=lambda: {"Idempotency-Key": "abc123"},
        )

        request_data = transport.prepare_request(endpoint)

        assert request_data.headers["Idempotency-Key"] == "abc123"
        assert "User-Agent" in request_data.headers

    def test_endpoint_without_headers_only_sends_user_agent(self, mock_sinch):
        transport = HTTPTransportRequests(mock_sinch)
        endpoint = _make_mock_endpoint(HTTPAuthentication.BASIC.value)

        request_data = transport.prepare_request(endpoint)

        assert list(request_data.headers) == ["User-Agent"]


class TestSend:
    def test_send_maps_requests_response(self, mock_sinch, base_request):
        transport = HTTPTransportRequests(mock_sinch)
        transport.http_session.request = Mock(
            return_value=_requests_response(200, body={"x": 1})
        )

        result = transport.send_request(base_request)

        assert isinstance(result, HTTPResponse)
        assert result.status_code == 200
        assert result.body == {"x": 1}

    def test_send_empty_body_returns_empty_dict(self, mock_sinch, base_request):
        transport = HTTPTransportRequests(mock_sinch)
        transport.http_session.request = Mock(
            return_value=Mock(status_code=204, content=b"", headers={})
        )

        result = transport.send_request(base_request)

        assert result.status_code == 204
        assert result.body == {}

    def test_send_raises_on_invalid_json(self, mock_sinch, base_request):
        transport = HTTPTransportRequests(mock_sinch)
        bad_response = Mock(status_code=200, content=b"not json", headers={})
        bad_response.json.side_effect = ValueError("bad json")
        transport.http_session.request = Mock(return_value=bad_response)

        with pytest.raises(SinchException):
            transport.send_request(base_request)


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


class TestRetryWithBackoff:
    """Tests for the automatic retry-with-backoff on rate-limited (429) responses.

    The retry policy itself (which status codes, which delay) is exercised in
    tests/unit/core/clients/test_retry_manager.py; these just confirm
    HTTPTransport wires every endpoint through it.
    """

    @staticmethod
    def _rate_limited(headers=None):
        return _requests_response(429, body={"error": "rate limited"}, headers=headers)

    def test_retries_on_429_then_succeeds(self, mock_sinch, no_sleep, no_jitter):
        transport = HTTPTransportRequests(mock_sinch)
        transport.http_session.request = Mock(side_effect=[
            self._rate_limited(),
            self._rate_limited(),
            _requests_response(200, body={"ok": True}),
        ])
        endpoint = _make_mock_endpoint(HTTPAuthentication.BASIC.value)

        result = transport.request(endpoint)

        assert result.status_code == 200
        assert transport.http_session.request.call_count == 3
        assert no_sleep.call_count == 2

    def test_gives_up_and_returns_last_response_after_max_retries(self, mock_sinch, no_sleep, no_jitter):
        transport = HTTPTransportRequests(mock_sinch)
        transport.http_session.request = Mock(return_value=self._rate_limited())
        endpoint = _make_mock_endpoint(HTTPAuthentication.BASIC.value)
        max_retries = mock_sinch.configuration.retry_manager.configuration.max_retries

        result = transport.request(endpoint)

        assert result.status_code == 429
        assert transport.http_session.request.call_count == max_retries + 1
        assert no_sleep.call_count == max_retries

    def test_no_retry_on_success(self, mock_sinch, no_sleep, no_jitter):
        transport = HTTPTransportRequests(mock_sinch)
        transport.http_session.request = Mock(return_value=_requests_response(200, body={"ok": True}))
        endpoint = _make_mock_endpoint(HTTPAuthentication.BASIC.value)

        result = transport.request(endpoint)

        assert result.status_code == 200
        assert transport.http_session.request.call_count == 1
        no_sleep.assert_not_called()

    def test_no_retry_on_non_retryable_status(self, mock_sinch, no_sleep, no_jitter):
        transport = HTTPTransportRequests(mock_sinch)
        transport.http_session.request = Mock(return_value=_requests_response(400, body={"error": "bad"}))
        endpoint = _make_mock_endpoint(HTTPAuthentication.BASIC.value)

        result = transport.request(endpoint)

        assert result.status_code == 400
        assert transport.http_session.request.call_count == 1
        no_sleep.assert_not_called()

    def test_honors_retry_after_header(self, mock_sinch, no_sleep, no_jitter):
        transport = HTTPTransportRequests(mock_sinch)
        transport.http_session.request = Mock(side_effect=[
            self._rate_limited(headers={"Retry-After": "7"}),
            _requests_response(200, body={"ok": True}),
        ])
        endpoint = _make_mock_endpoint(HTTPAuthentication.BASIC.value)

        transport.request(endpoint)

        no_sleep.assert_called_once_with(7.0)

    def test_headers_built_once_are_reused_across_retries(self, mock_sinch, no_sleep, no_jitter):
        """endpoint.build_headers() is only consulted once per request() call, so a
        header like Idempotency-Key stays identical across every automatic retry."""
        transport = HTTPTransportRequests(mock_sinch)
        transport.http_session.request = Mock(side_effect=[
            self._rate_limited(),
            self._rate_limited(),
            _requests_response(200, body={"ok": True}),
        ])
        build_headers = Mock(side_effect=lambda: {"Idempotency-Key": "fixed-key"})
        endpoint = _make_mock_endpoint(
            HTTPAuthentication.BASIC.value, build_headers=build_headers
        )

        transport.request(endpoint)

        build_headers.assert_called_once()
        sent_headers = [
            call.kwargs["headers"]["Idempotency-Key"]
            for call in transport.http_session.request.call_args_list
        ]
        assert sent_headers == ["fixed-key", "fixed-key", "fixed-key"]

    def test_no_retry_when_policy_is_none(self, mock_sinch, no_sleep, no_jitter):
        mock_sinch.configuration.retry_manager = RetryManager(RetryConfiguration(retry_policy=RetryPolicy.NONE))
        transport = HTTPTransportRequests(mock_sinch)
        transport.http_session.request = Mock(return_value=self._rate_limited())
        endpoint = _make_mock_endpoint(HTTPAuthentication.BASIC.value)

        result = transport.request(endpoint)

        assert result.status_code == 429
        assert transport.http_session.request.call_count == 1
        no_sleep.assert_not_called()


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

        assert result.status_code == 200

        assert transport.send_calls == 2
        token_manager.refresh_auth_token.assert_called_once_with("old")

    def test_request_raises_when_send_request_not_implemented(self, mock_sinch):
        transport = _NoHookTransport(mock_sinch)
        endpoint = _make_mock_endpoint(HTTPAuthentication.BASIC.value)

        with pytest.raises(NotImplementedError, match="send_request"):
            transport.request(endpoint)
