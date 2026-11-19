"""Tests for sinch.core.models.http_response.HTTPResponse and HttpContent."""

import json

import pytest

from sinch.core.models.http_headers import HttpHeaders
from sinch.core.models.http_content import HttpContent
from sinch.core.models.http_response import HTTPResponse


class TestHttpContent:
    def test_as_bytes_returns_the_raw_body(self):
        assert HttpContent(b"\x00\x01").as_bytes() == b"\x00\x01"

    def test_none_raw_is_an_empty_body(self):
        assert HttpContent(None).as_bytes() == b""

    def test_as_string_decodes_utf8(self):
        assert HttpContent("héllo".encode("utf-8")).as_string() == "héllo"

    def test_as_json_parses_the_body(self):
        assert HttpContent(b'{"id": "123", "items": [1, 2]}').as_json() == {"id": "123", "items": [1, 2]}

    def test_as_json_of_an_empty_body_is_none(self):
        assert HttpContent(b"").as_json() is None
        assert HttpContent().as_json() is None

    def test_as_json_of_an_empty_object_is_an_empty_dict(self):
        assert HttpContent(b"{}").as_json() == {}

    def test_as_json_is_cached(self):
        content = HttpContent(b'{"id": "123"}')

        assert content.as_json() is content.as_json()

    def test_as_json_raises_on_invalid_json(self):
        with pytest.raises(json.JSONDecodeError):
            HttpContent(b"<html>Bad Gateway</html>").as_json()

    def test_invalid_json_is_still_readable_as_string(self):
        content = HttpContent(b"<html>Bad Gateway</html>")

        assert content.as_string() == "<html>Bad Gateway</html>"


class TestHttpResponse:
    def test_wraps_a_mapping_into_http_headers(self):
        response = HTTPResponse(status=200, headers={"Retry-After": "7"})

        assert isinstance(response.headers, HttpHeaders)
        assert response.headers["retry-after"] == "7"

    def test_defaults_to_no_headers_and_empty_content(self):
        response = HTTPResponse(status=204)

        assert len(response.headers) == 0
        assert response.content.as_bytes() == b""

    def test_wraps_bytes_into_http_content(self):
        response = HTTPResponse(status=200, content=b'{"id": "123"}')

        assert isinstance(response.content, HttpContent)
        assert response.content.as_json() == {"id": "123"}

    def test_keeps_the_given_http_content(self):
        content = HttpContent(b"raw")

        assert HTTPResponse(200, {}, content).content is content

    def test_accepts_bytes_as_third_positional_argument(self):
        response = HTTPResponse(200, {}, b"raw")

        assert response.content.as_bytes() == b"raw"
