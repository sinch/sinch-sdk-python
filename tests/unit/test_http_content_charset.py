import json
from unittest.mock import Mock

import pytest
from urllib3 import HTTPHeaderDict

from sinch.core.adapters.requests_http_transport import HTTPTransportRequests
from sinch.core.models.http_headers import HttpHeaders
from sinch.core.models.http_request import HttpRequest
from sinch.core.models.http_content import HttpContent
from sinch.core.models.http_response import HTTPResponse
from sinch.core.models.internal.utils import parse_charset

TEXT = "Hólà ñandú"


@pytest.mark.parametrize(
    "content_type, expected",
    [
        ("text/plain; charset=iso-8859-1", "iso8859-1"),
        ('text/plain; charset="utf-16"', "utf-16"),
        ("text/plain; CHARSET=UTF-8", "utf-8"),
        ("text/plain; charset=utf8", "utf-8"),
        ("text/plain; charset=UTF_8", "utf-8"),
        ("application/json", "utf-8"),
        ("text/plain; charset=not-a-charset", "utf-8"),
        ("", "utf-8"),
        (None, "utf-8"),
    ],
)
def test_parse_charset_returns_canonical_declared_charset_or_utf8(content_type, expected):
    assert parse_charset(content_type) == expected


def test_as_string_uses_charset_from_headers():
    headers = HttpHeaders({"Content-Type": "text/plain; charset=iso-8859-1"})

    assert HttpContent(TEXT.encode("iso-8859-1"), headers).as_string() == TEXT


def test_as_string_defaults_to_utf8_without_charset():
    headers = HttpHeaders({"Content-Type": "application/json"})

    assert HttpContent(TEXT.encode("utf-8"), headers).as_string() == TEXT


def test_as_string_defaults_to_utf8_without_headers():
    assert HttpContent(TEXT.encode("utf-8")).as_string() == TEXT


def test_as_string_defaults_to_utf8_with_unknown_charset():
    headers = HttpHeaders({"Content-Type": "text/plain; charset=not-a-charset"})

    assert HttpContent(TEXT.encode("utf-8"), headers).as_string() == TEXT


def test_as_string_reads_charset_set_after_creation():
    headers = HttpHeaders()
    content = HttpContent(TEXT.encode("iso-8859-1"), headers)
    headers["Content-Type"] = "text/plain; charset=iso-8859-1"

    assert content.as_string() == TEXT


def test_as_string_raises_on_invalid_bytes_by_default():
    with pytest.raises(UnicodeDecodeError):
        HttpContent(b"\xff\xfe\xfa").as_string()


def test_as_string_replaces_invalid_bytes_when_requested():
    assert "�" in HttpContent(b"\xff\xfe\xfa").as_string(errors="replace")


def test_as_json_uses_charset_from_headers():
    headers = HttpHeaders({"Content-Type": "application/json; charset=iso-8859-1"})
    raw = json.dumps({"name": TEXT}, ensure_ascii=False).encode("iso-8859-1")

    assert HttpContent(raw, headers).as_json() == {"name": TEXT}


def test_as_json_skips_utf8_bom_with_utf8_charset_alias():
    headers = HttpHeaders({"Content-Type": "application/json; charset=utf8"})
    raw = b"\xef\xbb\xbf" + json.dumps({"name": TEXT}, ensure_ascii=False).encode("utf-8")

    assert HttpContent(raw, headers).as_json() == {"name": TEXT}


def test_as_json_detects_utf16_without_charset():
    raw = json.dumps({"name": TEXT}, ensure_ascii=False).encode("utf-16")

    assert HttpContent(raw).as_json() == {"name": TEXT}


def test_as_json_skips_utf8_bom_with_declared_utf8_charset():
    headers = HttpHeaders({"Content-Type": "application/json; charset=utf-8"})
    raw = b"\xef\xbb\xbf" + json.dumps({"name": TEXT}, ensure_ascii=False).encode("utf-8")

    assert HttpContent(raw, headers).as_json() == {"name": TEXT}


def test_response_binds_content_to_its_headers():
    response = HTTPResponse(
        status=200,
        headers={"content-type": "text/plain; charset=iso-8859-1"},
        content=TEXT.encode("iso-8859-1"),
    )

    assert response.content.as_string() == TEXT


def test_request_binds_content_to_its_headers():
    request = HttpRequest(
        method="POST",
        url="https://api.sinch.com/test",
        headers={"Content-Type": "text/plain; charset=iso-8859-1"},
        content=TEXT.encode("iso-8859-1"),
    )

    assert request.content.as_string() == TEXT


def _transport_with_response(raw, content_type):
    sinch = Mock()
    sinch.configuration.transport_settings.timeout_seconds = 5
    transport = HTTPTransportRequests(sinch)
    transport.http_session = Mock()
    transport.http_session.request.return_value = Mock(
        status_code=200,
        content=raw,
        raw=Mock(headers=HTTPHeaderDict({"Content-Type": content_type})),
    )
    return transport, sinch.configuration.logger


def _logged(logger):
    return [call.args[1:] for call in logger.debug.call_args_list]


def test_send_request_logs_request_body_with_request_charset():
    transport, logger = _transport_with_response(b"", "text/plain")
    request = HttpRequest(
        method="POST",
        url="https://api.sinch.com/test",
        headers={"Content-Type": "text/plain; charset=iso-8859-1"},
        content=TEXT.encode("iso-8859-1"),
    )

    transport.send_request(request)

    assert _logged(logger)[0][1] == TEXT


def test_send_request_logs_response_body_with_response_charset():
    transport, logger = _transport_with_response(TEXT.encode("iso-8859-1"), "text/plain; charset=iso-8859-1")
    request = HttpRequest(method="GET", url="https://api.sinch.com/test")

    transport.send_request(request)

    assert _logged(logger)[1][1] == TEXT


def test_send_request_sends_request_content_bytes():
    transport, _ = _transport_with_response(b"", "text/plain")
    raw = TEXT.encode("iso-8859-1")
    request = HttpRequest(
        method="POST",
        url="https://api.sinch.com/test",
        headers={"Content-Type": "text/plain; charset=iso-8859-1"},
        content=raw,
    )

    transport.send_request(request)

    assert transport.http_session.request.call_args.kwargs["data"] == raw


def test_send_request_does_not_fail_logging_undecodable_response_body():
    transport, logger = _transport_with_response(b"\xff\xfe\xfa", "text/plain")
    request = HttpRequest(method="GET", url="https://api.sinch.com/test")

    transport.send_request(request)

    assert "�" in _logged(logger)[1][1]
