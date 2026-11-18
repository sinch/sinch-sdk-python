import pytest

from sinch.core.clients.request_options import RequestOptions
from sinch.core.enums import HTTPAuthentication
from sinch.core.models.http_content import HttpContent
from sinch.core.models.http_request import HttpRequest
from sinch.core.models.http_response import HTTPResponse
from sinch.domains.http.api.v1.exceptions import HttpException
from sinch.domains.http.api.v1.internal.http_endpoints import HttpCallEndpoint


@pytest.fixture
def options():
    return RequestOptions(timeout_seconds=3)


@pytest.fixture
def request_data():
    return HttpRequest(
        method="POST",
        url="https://calling.api.sinch.com/calling/v1/callouts",
        query_parameters="?pageSize=5&name=John%20Doe&tag=a&tag=b",
        headers={"Content-Type": "application/json", "Accept": "*/*"},
        content=b'{"a":  1}',
    )


@pytest.fixture
def endpoint(request_data, options):
    return HttpCallEndpoint(None, request_data, options)


def test_build_request_expects_request_as_given(
    endpoint, request_data, mock_sinch_client_http
):
    assert endpoint.build_request(mock_sinch_client_http) is request_data


def test_build_url_expects_url_as_given(endpoint, mock_sinch_client_http):
    assert (
        endpoint.build_url(mock_sinch_client_http)
        == "https://calling.api.sinch.com/calling/v1/callouts"
    )


def test_http_method_expects_request_method(endpoint):
    assert endpoint.HTTP_METHOD == "POST"


def test_request_options_expects_options_given(endpoint, options):
    assert endpoint.request_options is options


def test_request_options_expects_none_by_default(request_data):
    assert HttpCallEndpoint(None, request_data).request_options is None


def test_http_authentication_expects_oauth_by_default(endpoint):
    assert endpoint.HTTP_AUTHENTICATION == HTTPAuthentication.OAUTH.value


def test_set_authentication_method_with_access_key_expects_oauth(
    endpoint, mock_sinch_client_http
):
    mock_sinch_client_http.configuration.service_plan_id = "service_plan_id"
    mock_sinch_client_http.configuration.sms_api_token = "sms_api_token"

    endpoint.set_authentication_method(mock_sinch_client_http)

    assert endpoint.HTTP_AUTHENTICATION == HTTPAuthentication.OAUTH.value


def test_set_authentication_method_with_sms_token_only_expects_sms_token(
    endpoint, mock_sinch_client_http
):
    mock_sinch_client_http.configuration.key_id = None
    mock_sinch_client_http.configuration.key_secret = None
    mock_sinch_client_http.configuration.service_plan_id = "service_plan_id"
    mock_sinch_client_http.configuration.sms_api_token = "sms_api_token"

    endpoint.set_authentication_method(mock_sinch_client_http)

    assert endpoint.HTTP_AUTHENTICATION == HTTPAuthentication.SMS_TOKEN.value


def test_set_authentication_method_without_credentials_expects_oauth(
    endpoint, mock_sinch_client_http
):
    mock_sinch_client_http.configuration.key_id = None
    mock_sinch_client_http.configuration.key_secret = None

    endpoint.set_authentication_method(mock_sinch_client_http)

    assert endpoint.HTTP_AUTHENTICATION == HTTPAuthentication.OAUTH.value


def test_handle_response_expects_response_returned_as_is(endpoint):
    response = HTTPResponse(status=200, content=HttpContent(b"not json"))

    assert endpoint.handle_response(response) is response


def test_handle_response_expects_exception_on_error_status(endpoint):
    response = HTTPResponse(
        status=404, content=HttpContent(b'{"error": "not found"}')
    )

    with pytest.raises(HttpException) as error:
        endpoint.handle_response(response)

    assert error.value.is_from_server is True
    assert error.value.response_status_code == 404
    assert error.value.http_response is response
    assert "404" in str(error.value)
