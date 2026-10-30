import json
import pytest
from unittest.mock import Mock
from urllib3 import HTTPHeaderDict
from sinch.core.clients.retry_configuration import RetryConfiguration
from sinch.core.clients.retry_manager import RetryManager
from sinch.core.clients.transport_settings import TransportSettings
from sinch.core.enums import HTTPAuthentication, RetryPolicy
from sinch.core.exceptions import SinchException, ValidationException
from sinch.core.models.http_body import FilePart, JsonBody, MultipartBody, UrlEncodedBody
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

        def build_query_params(self):
            return {}

        def build_headers(self):
            return build_headers() if build_headers else None

        def handle_response(self, response: HTTPResponse):
            if error_on_4xx and response.status >= 400:
                raise ValidationException(
                    message=f"HTTP {response.status}",
                    is_from_server=True,
                    response=response,
                )
            return response

    return _Endpoint()


def _requests_response(status_code, body=None, headers=None):
    """Fake of a requests.Response, just enough for HTTPTransportRequests.send_request."""
    resp = Mock()
    resp.status_code = status_code
    resp.content = json.dumps(body or {}).encode()
    resp.text = resp.content.decode()
    resp.headers = headers or {}
    resp.raw.headers = HTTPHeaderDict(headers or {})
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
    sinch.configuration.transport_settings = TransportSettings()
    return sinch


@pytest.fixture
def sinch_auth_disabled(mock_sinch):
    mock_sinch.configuration.transport_settings = TransportSettings(use_sinch_auth=False)
    return mock_sinch


@pytest.fixture
def no_sleep(mocker):
    return mocker.patch("sinch.core.clients.retry_manager.time.sleep")

@pytest.fixture
def no_jitter(mocker):
    return mocker.patch("sinch.core.clients.retry_manager.random.uniform", return_value=0.0)

@pytest.fixture
def base_request():
    return HttpRequest(method="GET", url="https://api.sinch.com/test")


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
            # base64("test_key_id:test_key_secret")
            assert result.headers["Authorization"] == "Basic dGVzdF9rZXlfaWQ6dGVzdF9rZXlfc2VjcmV0"

        elif auth_type == HTTPAuthentication.OAUTH.value:
            mock_sinch.authentication.get_auth_token.return_value.access_token = "test_token"
            result = transport.authenticate(endpoint, base_request)
            assert result.headers["Authorization"] == "Bearer test_token"

        elif auth_type == HTTPAuthentication.SMS_TOKEN.value:
            result = transport.authenticate(endpoint, base_request)
            assert result.headers["Authorization"] == "Bearer test_sms_token"

    @pytest.mark.parametrize("auth_type", [HTTPAuthentication.OAUTH.value, HTTPAuthentication.SMS_TOKEN.value])
    def test_bearer_auth_does_not_set_content_type(self, mock_sinch, base_request, auth_type):
        mock_sinch.authentication.get_auth_token.return_value.access_token = "test_token"
        transport = HTTPTransportRequests(mock_sinch)

        result = transport.authenticate(_make_mock_endpoint(auth_type), base_request)

        assert "Content-Type" not in result.headers

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


class TestAuthenticateWithSinchAuthDisabled:
    def test_oauth_does_not_add_authorization_header(self, sinch_auth_disabled, base_request):
        transport = HTTPTransportRequests(sinch_auth_disabled)
        endpoint = _make_mock_endpoint(HTTPAuthentication.OAUTH.value)

        result = transport.authenticate(endpoint, base_request)

        assert "Authorization" not in result.headers

    def test_oauth_does_not_fetch_a_token(self, sinch_auth_disabled, base_request):
        transport = HTTPTransportRequests(sinch_auth_disabled)
        endpoint = _make_mock_endpoint(HTTPAuthentication.OAUTH.value)

        transport.authenticate(endpoint, base_request)

        sinch_auth_disabled.authentication.get_auth_token.assert_not_called()

    def test_oauth_does_not_require_key_id_and_key_secret(self, sinch_auth_disabled, base_request):
        sinch_auth_disabled.configuration.key_id = None
        sinch_auth_disabled.configuration.key_secret = None
        transport = HTTPTransportRequests(sinch_auth_disabled)
        endpoint = _make_mock_endpoint(HTTPAuthentication.OAUTH.value)

        transport.authenticate(endpoint, base_request)

    def test_oauth_requires_project_id(self, sinch_auth_disabled, base_request):
        sinch_auth_disabled.configuration.project_id = None
        transport = HTTPTransportRequests(sinch_auth_disabled)
        endpoint = _make_mock_endpoint(HTTPAuthentication.OAUTH.value)

        with pytest.raises(ValidationException, match="project_id is required by this API"):
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

    def test_serializes_query_params(self, mock_sinch):
        transport = HTTPTransportRequests(mock_sinch)
        endpoint = _make_mock_endpoint(HTTPAuthentication.BASIC.value)
        endpoint.build_query_params = lambda: {"pageSize": 5, "types": ["MOBILE", "LOCAL"]}

        request_data = transport.prepare_request(endpoint)

        assert request_data.url == "api.sinch.com/test"
        assert request_data.query_parameters == "?pageSize=5&types=MOBILE&types=LOCAL"

    def test_without_query_params_query_parameters_is_empty(self, mock_sinch):
        transport = HTTPTransportRequests(mock_sinch)
        endpoint = _make_mock_endpoint(HTTPAuthentication.BASIC.value)

        request_data = transport.prepare_request(endpoint)

        assert request_data.query_parameters == ""

    def test_json_body_is_encoded_with_its_content_type(self, mock_sinch):
        transport = HTTPTransportRequests(mock_sinch)
        endpoint = _make_mock_endpoint(HTTPAuthentication.BASIC.value)
        endpoint.build_body = lambda: JsonBody({"a": 1})

        request_data = transport.prepare_request(endpoint)

        assert request_data.content.as_bytes() == b'{"a": 1}'
        assert request_data.headers["content-type"] == "application/json"

    def test_dict_body_is_form_urlencoded(self, mock_sinch):
        transport = HTTPTransportRequests(mock_sinch)
        endpoint = _make_mock_endpoint(HTTPAuthentication.BASIC.value)
        endpoint.build_body = lambda: UrlEncodedBody({"grant_type": "client_credentials"})

        request_data = transport.prepare_request(endpoint)

        assert request_data.content.as_bytes() == b"grant_type=client_credentials"
        assert request_data.headers["content-type"] == "application/x-www-form-urlencoded"

    def test_multipart_body_is_encoded_with_its_boundary_in_the_content_type(self, mock_sinch):
        transport = HTTPTransportRequests(mock_sinch)
        endpoint = _make_mock_endpoint(HTTPAuthentication.BASIC.value)
        body = MultipartBody(fields={"a": "1"}, files={"file": FilePart(b"data", "a.txt")})
        endpoint.build_body = lambda: body

        request_data = transport.prepare_request(endpoint)

        assert request_data.content.as_bytes() == body.encode()
        assert request_data.headers["content-type"] == f"multipart/form-data; boundary={body.boundary}"

    def test_empty_body_has_no_content(self, mock_sinch):
        transport = HTTPTransportRequests(mock_sinch)
        endpoint = _make_mock_endpoint(HTTPAuthentication.BASIC.value)

        request_data = transport.prepare_request(endpoint)

        assert request_data.content is None
        assert "Content-Type" not in request_data.headers


class TestSend:
    def test_send_maps_requests_response(self, mock_sinch, base_request):
        transport = HTTPTransportRequests(mock_sinch)
        transport.http_session.request = Mock(
            return_value=_requests_response(200, body={"x": 1}, headers={"X-Trace": "abc"})
        )

        result = transport.send_request(base_request)

        assert isinstance(result, HTTPResponse)
        assert result.status == 200
        assert result.headers["x-trace"] == "abc"
        assert result.content.as_json() == {"x": 1}

    def test_send_keeps_repeated_response_headers(self, mock_sinch, base_request):
        transport = HTTPTransportRequests(mock_sinch)
        raw_headers = HTTPHeaderDict()
        raw_headers.add("Set-Cookie", "a=1")
        raw_headers.add("Set-Cookie", "b=2")
        response = _requests_response(200, headers={"Set-Cookie": "a=1, b=2"})
        response.raw.headers = raw_headers
        transport.http_session.request = Mock(return_value=response)

        result = transport.send_request(base_request)

        assert result.headers.get_all("set-cookie") == ["a=1", "b=2"]

    def test_send_keeps_the_raw_body(self, mock_sinch, base_request):
        transport = HTTPTransportRequests(mock_sinch)
        transport.http_session.request = Mock(
            return_value=Mock(
                status_code=200, content=b"not json", text="not json", headers={}, raw=Mock(headers=HTTPHeaderDict())
            )
        )

        result = transport.send_request(base_request)

        assert result.content.as_bytes() == b"not json"

    def test_send_appends_query_parameters_to_url(self, mock_sinch):
        transport = HTTPTransportRequests(mock_sinch)
        transport.http_session.request = Mock(return_value=_requests_response(200))
        request = HttpRequest(method="GET", url="https://api.sinch.com/test", query_parameters="?a=1&b=2")

        transport.send_request(request)

        kwargs = transport.http_session.request.call_args.kwargs
        assert kwargs["url"] == "https://api.sinch.com/test?a=1&b=2"
        assert "params" not in kwargs

    def test_send_passes_content_as_data(self, mock_sinch):
        transport = HTTPTransportRequests(mock_sinch)
        transport.http_session.request = Mock(return_value=_requests_response(200))
        request = HttpRequest(method="POST", url="https://api.sinch.com/test", content=b'{"a": 1}')

        transport.send_request(request)

        assert transport.http_session.request.call_args.kwargs["data"] == b'{"a": 1}'

    def test_send_does_not_pass_auth(self, mock_sinch, base_request):
        transport = HTTPTransportRequests(mock_sinch)
        transport.http_session.request = Mock(return_value=_requests_response(200))

        transport.send_request(base_request)

        assert "auth" not in transport.http_session.request.call_args.kwargs

    def test_send_passes_timeout_seconds(self, mock_sinch, base_request):
        mock_sinch.configuration.transport_settings = TransportSettings(timeout_seconds=30)
        transport = HTTPTransportRequests(mock_sinch)
        transport.http_session.request = Mock(return_value=_requests_response(200))

        transport.send_request(base_request)

        assert transport.http_session.request.call_args.kwargs["timeout"] == 30

    def test_send_disables_timeout_when_timeout_seconds_is_zero(self, mock_sinch, base_request):
        mock_sinch.configuration.transport_settings = TransportSettings(timeout_seconds=0)
        transport = HTTPTransportRequests(mock_sinch)
        transport.http_session.request = Mock(return_value=_requests_response(200))

        transport.send_request(base_request)

        assert transport.http_session.request.call_args.kwargs["timeout"] is None


class TestHandleResponse:
    def test_unparsable_body_raises_sinch_exception_with_the_response(self, mock_sinch, mocker):
        transport = HTTPTransportRequests(mock_sinch)
        endpoint = _make_mock_endpoint(HTTPAuthentication.BASIC.value)
        endpoint.handle_response = lambda response: response.content.as_json()
        mocker.patch.object(transport, "send_request", return_value=HTTPResponse(502, {}, b"<html>Bad Gateway</html>"))

        with pytest.raises(SinchException, match="Error while parsing json response") as exc_info:
            transport.request(endpoint)

        assert exc_info.value.response_status_code == 502
        assert exc_info.value.http_response.content.as_string() == "<html>Bad Gateway</html>"
        assert isinstance(exc_info.value.__cause__, json.JSONDecodeError)


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

        assert result.status == 200
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

        assert result.status == 200
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

    def test_no_refresh_when_sinch_auth_disabled(self, sinch_auth_disabled):
        token_manager = _token_manager(sinch_auth_disabled)
        transport = HTTPTransportRequests(sinch_auth_disabled)
        transport.http_session.request = Mock(side_effect=[self._expired_401()])
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

        assert result.status == 200
        assert transport.http_session.request.call_count == 3
        assert no_sleep.call_count == 2

    def test_gives_up_and_returns_last_response_after_max_retries(self, mock_sinch, no_sleep, no_jitter):
        transport = HTTPTransportRequests(mock_sinch)
        transport.http_session.request = Mock(return_value=self._rate_limited())
        endpoint = _make_mock_endpoint(HTTPAuthentication.BASIC.value)
        max_retries = mock_sinch.configuration.retry_manager.configuration.max_retries

        result = transport.request(endpoint)

        assert result.status == 429
        assert transport.http_session.request.call_count == max_retries + 1
        assert no_sleep.call_count == max_retries

    def test_no_retry_on_success(self, mock_sinch, no_sleep, no_jitter):
        transport = HTTPTransportRequests(mock_sinch)
        transport.http_session.request = Mock(return_value=_requests_response(200, body={"ok": True}))
        endpoint = _make_mock_endpoint(HTTPAuthentication.BASIC.value)

        result = transport.request(endpoint)

        assert result.status == 200
        assert transport.http_session.request.call_count == 1
        no_sleep.assert_not_called()

    def test_no_retry_on_non_retryable_status(self, mock_sinch, no_sleep, no_jitter):
        transport = HTTPTransportRequests(mock_sinch)
        transport.http_session.request = Mock(return_value=_requests_response(400, body={"error": "bad"}))
        endpoint = _make_mock_endpoint(HTTPAuthentication.BASIC.value)

        result = transport.request(endpoint)

        assert result.status == 400
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

        assert result.status == 429
        assert transport.http_session.request.call_count == 1
        no_sleep.assert_not_called()
