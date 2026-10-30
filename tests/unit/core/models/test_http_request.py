"""Tests for sinch.core.models.http_request.HttpRequest."""

from sinch.core.models.http_headers import HttpHeaders
from sinch.core.models.http_request import HttpRequest


class TestHttpRequest:
    def test_defaults(self):
        request = HttpRequest(method="GET", url="https://api.sinch.com/test")

        assert request.query_parameters == ""
        assert request.content is None
        assert len(request.headers) == 0

    def test_wraps_a_mapping_into_http_headers(self):
        request = HttpRequest(method="GET", url="https://api.sinch.com", headers={"Accept": "application/json"})

        assert isinstance(request.headers, HttpHeaders)
        assert request.headers["accept"] == "application/json"

    def test_keeps_given_http_headers_instance(self):
        headers = HttpHeaders({"Accept": "application/json"})

        request = HttpRequest(method="GET", url="https://api.sinch.com", headers=headers)

        assert request.headers is headers

    def test_repr_masks_the_authorization_header(self):
        request = HttpRequest(
            method="GET", url="https://api.sinch.com", headers={"Authorization": "Bearer secret", "Accept": "*/*"}
        )

        assert "secret" not in repr(request)
        assert "'Authorization', '***'" in repr(request)
        assert "'Accept', '*/*'" in repr(request)
