from unittest.mock import Mock

import pytest
from urllib3 import HTTPHeaderDict

from sinch import SinchClient
from sinch.core.clients.request_options import RequestOptions
from sinch.core.exceptions import ValidationException
from sinch.core.models.http_body import FilePart, JsonBody
from sinch.core.models.http_headers import HttpHeaders
from sinch.core.models.http_response import HTTPResponse
from sinch.domains.http import Http
from sinch.domains.http.api.v1.exceptions import HttpException
from sinch.domains.http.api.v1.internal import HttpCallEndpoint


@pytest.fixture
def http(mock_sinch_client_http):
    mock_sinch_client_http.configuration.transport.request.return_value = (
        HTTPResponse(status=200)
    )
    return Http(mock_sinch_client_http)


@pytest.fixture
def endpoint_spy(mocker):
    return mocker.spy(HttpCallEndpoint, "__init__")


@pytest.fixture
def client():
    client = SinchClient(key_id="k", key_secret="s", project_id="p")
    client.authentication.get_auth_token = Mock(
        return_value=Mock(access_token="token")
    )
    return client


def _captured_call(spy):
    spy.assert_called_once()
    _, kwargs = spy.call_args
    return kwargs


def _captured_request(spy):
    return _captured_call(spy)["request_data"]


@pytest.mark.parametrize(
    "verb, method", [("get", "GET"), ("delete", "DELETE")]
)
def test_verb_without_body_expects_valid_request(
    http, endpoint_spy, mock_sinch_client_http, verb, method
):
    options = RequestOptions(timeout_seconds=5)

    response = getattr(http, verb)(
        url="https://numbers.api.sinch.com/v1/projects/P1/activeNumbers",
        query_params="?pageSize=5&name=John%20Doe",
        headers={"accept": "application/json"},
        options=options,
    )

    request_data = _captured_request(endpoint_spy)
    assert request_data.method == method
    assert (
        request_data.url
        == "https://numbers.api.sinch.com/v1/projects/P1/activeNumbers"
    )
    assert request_data.query_parameters == "?pageSize=5&name=John%20Doe"
    assert request_data.headers.get("Accept") == "application/json"
    assert request_data.content is None
    assert _captured_call(endpoint_spy)["request_options"] is options
    assert isinstance(response, HTTPResponse)
    mock_sinch_client_http.configuration.transport.request.assert_called_once()


@pytest.mark.parametrize(
    "verb, method", [("post", "POST"), ("put", "PUT"), ("patch", "PATCH")]
)
def test_verb_with_body_expects_valid_request(
    http, endpoint_spy, mock_sinch_client_http, verb, method
):
    options = RequestOptions(use_sinch_auth=False)

    response = getattr(http, verb)(
        url="https://calling.api.sinch.com/calling/v1/callouts",
        body='{"method": "ttsCallout"}',
        query_params="?a=1",
        headers={"content-type": "application/json"},
        options=options,
    )

    request_data = _captured_request(endpoint_spy)
    assert request_data.method == method
    assert (
        request_data.url == "https://calling.api.sinch.com/calling/v1/callouts"
    )
    assert request_data.query_parameters == "?a=1"
    assert request_data.headers["Content-Type"] == "application/json"
    assert request_data.content.as_bytes() == b'{"method": "ttsCallout"}'
    assert _captured_call(endpoint_spy)["request_options"] is options
    assert isinstance(response, HTTPResponse)
    mock_sinch_client_http.configuration.transport.request.assert_called_once()


def test_post_without_body_expects_no_body_and_no_content_type_required(
    http, endpoint_spy
):
    http.post(url="https://example.com/ping")

    assert _captured_request(endpoint_spy).content is None


def test_request_without_options_expects_no_request_options(http, endpoint_spy):
    http.get(url="https://example.com")

    assert _captured_call(endpoint_spy)["request_options"] is None


def test_post_with_body_and_no_content_type_expects_validation_error(
    http, mock_sinch_client_http
):
    with pytest.raises(ValidationException, match="Content-Type"):
        http.post(url="https://example.com/upload", body=b"data")

    mock_sinch_client_http.configuration.transport.request.assert_not_called()


def test_get_with_repeated_headers_expects_them_preserved(http, endpoint_spy):
    headers = HttpHeaders([("X-Tag", "a"), ("x-tag", "b")])

    http.get(url="https://example.com", headers=headers)

    request_data = _captured_request(endpoint_spy)
    assert request_data.headers.get_all("X-Tag") == ["a", "b"]
    assert request_data.headers is not headers


def test_get_with_header_pairs_expects_repeated_header_kept(http, endpoint_spy):
    http.get(
        url="https://example.com",
        headers=[("X-Tag", "a"), ("X-Tag", "b")],
    )

    assert _captured_request(endpoint_spy).headers.get_all("X-Tag") == ["a", "b"]


def test_post_with_http_body_expects_encoded_body(http, endpoint_spy):
    http.post(url="https://example.com", body=JsonBody({"a": 1}))

    assert _captured_request(endpoint_spy).content.as_bytes() == b'{"a": 1}'


def test_post_with_http_body_expects_its_content_type_replacing_the_given_one(
    http, endpoint_spy
):
    http.post(
        url="https://example.com",
        body=JsonBody({"a": 1}),
        headers={"content-type": "text/plain"},
    )

    headers = _captured_request(endpoint_spy).headers
    assert headers.get_all("Content-Type") == ["application/json"]


def test_put_with_file_part_expects_file_sent_with_guessed_content_type(
    http, endpoint_spy, tmp_path
):
    path = tmp_path / "photo.jpg"
    path.write_bytes(b"\xff\xd8\xff")

    http.put(url="https://example.com/upload", body=FilePart(path))

    request_data = _captured_request(endpoint_spy)
    assert request_data.content.as_bytes() == b"\xff\xd8\xff"
    assert request_data.headers["Content-Type"] == "image/jpeg"


def test_post_with_unsupported_body_expects_validation_exception(http):
    with pytest.raises(ValidationException, match="Unsupported body type: dict"):
        http.post(url="https://example.com", body={"a": 1})


def test_post_with_str_body_expects_encoded_with_content_type_charset(
    http, endpoint_spy
):
    http.post(
        url="https://example.com/upload",
        body="olé",
        headers={"Content-Type": "text/plain; charset=iso-8859-1"},
    )

    assert _captured_request(endpoint_spy).content.as_bytes() == "olé".encode("iso-8859-1")


def test_post_with_str_body_and_no_charset_expects_utf8(http, endpoint_spy):
    http.post(
        url="https://example.com/upload",
        body="olé",
        headers={"Content-Type": "text/plain"},
    )

    assert _captured_request(endpoint_spy).content.as_bytes() == "olé".encode("utf-8")


def test_post_with_bytes_body_expects_sent_untouched(http, endpoint_spy):
    http.post(
        url="https://example.com/upload",
        body=b"\x00\x01",
        headers={"Content-Type": "application/octet-stream"},
    )

    assert _captured_request(endpoint_spy).content.as_bytes() == b"\x00\x01"


def test_get_with_none_query_params_expects_empty_query_string(http, endpoint_spy):
    http.get(url="https://example.com", query_params=None)

    assert _captured_request(endpoint_spy).query_parameters == ""


def test_get_with_query_params_without_question_mark_expects_it_added(
    http, endpoint_spy
):
    http.get(url="https://example.com", query_params="a=1&b=2")

    assert _captured_request(endpoint_spy).query_parameters == "?a=1&b=2"


def test_get_with_query_params_with_question_mark_expects_it_kept_once(
    http, endpoint_spy
):
    http.get(url="https://example.com", query_params="?a=1")

    assert _captured_request(endpoint_spy).query_parameters == "?a=1"


def test_request_expects_no_project_id(http, endpoint_spy):
    http.get(url="https://example.com")

    assert _captured_call(endpoint_spy)["project_id"] is None


def test_post_form_data_expects_multipart_body_with_fields_and_files(
    http, endpoint_spy
):
    file_part = FilePart(b"hello", filename="a.txt")
    attachments = [
        FilePart(b"1", filename="1.txt"),
        FilePart(b"2", filename="2.txt"),
    ]

    http.post_form_data(
        url="https://example.com",
        form_params={
            "to": "someone@adomain.com",
            "doc": file_part,
            "attachments": attachments,
        },
        query_params="?a=1",
        headers={"accept": "application/json"},
    )

    request_data = _captured_request(endpoint_spy)
    content = request_data.content.as_bytes()
    assert request_data.method == "POST"
    assert request_data.query_parameters == "?a=1"
    assert request_data.headers["Content-Type"].startswith(
        "multipart/form-data; boundary="
    )
    assert b'name="to"\r\n\r\nsomeone@adomain.com\r\n' in content
    assert b'name="doc"; filename="a.txt"' in content
    assert b'name="attachments"; filename="1.txt"' in content
    assert b'name="attachments"; filename="2.txt"' in content


def test_sinch_client_expects_http_domain():
    assert isinstance(
        SinchClient(key_id="k", key_secret="s", project_id="p").http, Http
    )


def test_post_through_transport_expects_untouched_request_on_the_wire(
    client, mocker
):
    raw = Mock(status_code=201, content=b'{"id": "1"}')
    raw.raw.headers = HTTPHeaderDict({"Content-Type": "application/json"})
    send = mocker.patch.object(
        client.configuration.transport.http_session,
        "request",
        return_value=raw,
    )

    response = client.http.post(
        url="https://calling.api.sinch.com/calling/v1/callouts",
        body='{"a":   1}',
        query_params="?name=John%20Doe&tag=a&tag=b",
        headers=HttpHeaders(
            [
                ("content-type", "application/json"),
                ("X-Tag", "a"),
                ("x-tag", "b"),
            ]
        ),
        options=RequestOptions(timeout_seconds=7),
    )

    kwargs = send.call_args.kwargs
    assert kwargs["method"] == "POST"
    assert (
        kwargs["url"]
        == "https://calling.api.sinch.com/calling/v1/callouts?name=John%20Doe&tag=a&tag=b"
    )
    assert kwargs["data"] == b'{"a":   1}'
    assert kwargs["timeout"] == 7
    assert kwargs["headers"]["Authorization"] == "Bearer token"
    assert kwargs["headers"].get_all("X-Tag") == ["a", "b"]
    assert kwargs["headers"]["User-Agent"].endswith(
        "HTTPTransportRequests; http)"
    )
    assert response.status == 201
    assert response.content.as_json() == {"id": "1"}


def test_get_without_project_id_expects_request_authenticated(mocker):
    client = SinchClient(key_id="k", key_secret="s")
    raw = Mock(
        status_code=200,
        content=b'{"access_token": "token", "expires_in": 3599, "scope": "", "token_type": "bearer"}',
    )
    raw.raw.headers = HTTPHeaderDict()
    send = mocker.patch.object(
        client.configuration.transport.http_session,
        "request",
        return_value=raw,
    )

    client.http.get(url="https://calling.api.sinch.com/calling/v1/callouts/1")

    assert send.call_args.kwargs["headers"]["Authorization"] == "Bearer token"


def test_get_through_transport_with_error_status_expects_http_exception(
    client, mocker
):
    raw = Mock(status_code=404, content=b"")
    raw.raw.headers = HTTPHeaderDict()
    mocker.patch.object(
        client.configuration.transport.http_session,
        "request",
        return_value=raw,
    )

    with pytest.raises(HttpException) as error:
        client.http.get(
            url="https://calling.api.sinch.com/calling/v1/callouts/1"
        )

    assert error.value.response_status_code == 404
