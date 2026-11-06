"""Tests for sinch.core.models.http_body."""

import io
import json
from unittest.mock import Mock

import pytest
import requests
from urllib3.fields import RequestField
from urllib3.filepost import encode_multipart_formdata

from sinch.core.models.http_body import FilePart, JsonBody, MultipartBody, UrlEncodedBody


class TestJsonBody:
    def test_encodes_the_data_as_json(self):
        assert json.loads(JsonBody({"a": 1, "b": [1, 2]}).encode()) == {"a": 1, "b": [1, 2]}

    def test_encodes_as_utf8_bytes(self):
        assert JsonBody({"text": "héllo"}).encode() == json.dumps({"text": "héllo"}).encode("utf-8")

    def test_content_type_is_json(self):
        assert JsonBody({}).content_type == "application/json"


class TestUrlEncodedBody:
    def test_encodes_the_fields_form_urlencoded(self):
        body = UrlEncodedBody({"grant_type": "client_credentials", "scope": "a b"})

        assert body.encode() == b"grant_type=client_credentials&scope=a+b"

    def test_list_value_is_a_repeated_field(self):
        assert UrlEncodedBody({"a": ["1", "2"]}).encode() == b"a=1&a=2"

    def test_omits_a_none_value(self):
        assert UrlEncodedBody({"a": "1", "b": None}).encode() == b"a=1"

    def test_matches_requests_data(self):
        fields = {"grant_type": "client_credentials", "scope": "a b"}
        expected = requests.Request("POST", "https://auth.sinch.com", data=fields).prepare()
        body = UrlEncodedBody(fields)

        assert body.encode().decode() == expected.body
        assert body.content_type == expected.headers["Content-Type"]


@pytest.fixture
def fixed_boundary(monkeypatch):
    monkeypatch.setattr("sinch.core.models.http_body.uuid4", lambda: Mock(hex="B1"))


class TestFilePart:
    def test_reads_bytes(self):
        assert FilePart(b"data", "a.bin").read() == b"data"

    def test_encodes_as_the_file_content(self):
        assert FilePart(b"data").encode() == b"data"

    def test_defaults_filename_to_the_name_of_a_path(self, tmp_path):
        part = FilePart(tmp_path / "photo.jpg")

        assert part.filename == "photo.jpg"
        assert part.content_type == "image/jpeg"

    def test_content_type_without_filename_defaults_to_octet_stream(self):
        part = FilePart(b"data")

        assert part.filename is None
        assert part.content_type == "application/octet-stream"

    def test_rejects_a_str_content(self):
        with pytest.raises(ValueError, match="content must be bytes"):
            FilePart("/tmp/a.bin", "a.bin")

    def test_reads_a_path(self, tmp_path):
        path = tmp_path / "a.txt"
        path.write_bytes(b"from disk")

        assert FilePart(path, "a.txt").read() == b"from disk"

    def test_reads_a_file_object(self):
        assert FilePart(io.BytesIO(b"from stream"), "a.txt").read() == b"from stream"

    def test_guesses_content_type_from_filename(self):
        assert FilePart(b"", "doc.pdf").content_type == "application/pdf"

    def test_content_type_defaults_to_octet_stream(self):
        assert FilePart(b"", "data.unknownext").content_type == "application/octet-stream"

    def test_explicit_content_type_wins(self):
        assert FilePart(b"", "doc.pdf", "text/plain").content_type == "text/plain"

    @pytest.mark.parametrize("content_type", ["text/plain\r\nX-Evil: 1", "text/plain\nX-Evil: 1", "text/plain\r"])
    def test_rejects_a_content_type_with_line_breaks(self, content_type):
        with pytest.raises(ValueError, match="content_type"):
            FilePart(b"", "doc.pdf", content_type)


class TestMultipartBodyBoundary:
    def test_generates_a_different_boundary_per_body(self):
        assert MultipartBody().boundary != MultipartBody().boundary

    def test_generated_boundary_is_in_content_type_and_body(self):
        body = MultipartBody(fields={"a": "1"})

        assert body.content_type == f"multipart/form-data; boundary={body.boundary}"
        assert f"--{body.boundary}--".encode() in body.encode()


@pytest.mark.usefixtures("fixed_boundary")
class TestMultipartBody:
    def test_encodes_text_fields(self):
        body = MultipartBody(fields={"to": "someone@adomain.com", "text": "Hello"})

        assert body.encode() == (
            b"--B1\r\n"
            b'Content-Disposition: form-data; name="to"\r\n\r\n'
            b"someone@adomain.com\r\n"
            b"--B1\r\n"
            b'Content-Disposition: form-data; name="text"\r\n\r\n'
            b"Hello\r\n"
            b"--B1--\r\n"
        )

    def test_encodes_a_file(self):
        body = MultipartBody(fields={"attachment": FilePart(b"%PDF", "doc.pdf")})

        assert body.encode() == (
            b"--B1\r\n"
            b'Content-Disposition: form-data; name="attachment"; filename="doc.pdf"\r\n'
            b"Content-Type: application/pdf\r\n\r\n"
            b"%PDF\r\n"
            b"--B1--\r\n"
        )

    def test_sends_parts_in_the_given_order(self):
        body = MultipartBody(
            fields={"file": FilePart(b"data", "a.txt"), "caption": "x"}
        ).encode()

        assert body.index(b'name="file"') < body.index(b'name="caption"')

    def test_list_can_mix_files_and_text(self):
        body = MultipartBody(
            fields={"item": ["hello", FilePart(b"data", "a.txt")]}
        ).encode()

        assert body.count(b'name="item"') == 2
        assert body.index(b"\r\n\r\nhello\r\n") < body.index(b'filename="a.txt"')
        assert b"\r\n\r\ndata\r\n" in body

    def test_files_under_the_same_name_are_all_sent(self):
        body = MultipartBody(
            fields={"file": [FilePart(b"one", "a.txt"), FilePart(b"two", "b.txt")]}
        ).encode()

        assert body.count(b'name="file"') == 2
        assert b'filename="a.txt"' in body and b'filename="b.txt"' in body

    def test_sends_binary_content_untouched(self):
        raw = bytes(range(256))

        body = MultipartBody(fields={"file": FilePart(raw, "a.bin")}).encode()

        assert b"\r\n\r\n" + raw + b"\r\n--B1--" in body

    def test_sends_a_non_text_field_value_as_its_string(self):
        body = MultipartBody(fields={"count": 3}).encode()

        assert b"\r\n\r\n3\r\n" in body

    def test_file_without_filename_sends_the_field_name(self):
        body = MultipartBody(fields={"doc": FilePart(b"data")}).encode()

        assert b'name="doc"; filename="doc"' in body

    def test_list_value_is_a_repeated_field(self):
        body = MultipartBody(fields={"tag": ["a", "b"]}).encode()

        assert body.count(b'name="tag"') == 2
        assert b"\r\n\r\na\r\n" in body and b"\r\n\r\nb\r\n" in body

    def test_omits_a_none_field(self):
        body = MultipartBody(fields={"kept": "1", "dropped": None}).encode()

        assert b'name="kept"' in body
        assert b"dropped" not in body and b"None" not in body

    def test_sends_bytes_field_value_untouched(self):
        body = MultipartBody(fields={"raw": b"\xff\xfe"}).encode()

        assert b"\r\n\r\n\xff\xfe\r\n" in body

    def test_encodes_non_ascii_text_and_filename_as_utf8(self):
        body = MultipartBody(
            fields={"text": "ñandú", "file": FilePart(b"x", "año.txt")}
        ).encode()

        assert "ñandú".encode("utf-8") in body
        assert 'filename="año.txt"'.encode("utf-8") in body

    @pytest.mark.parametrize(
        "name, escaped",
        [('a"b', "a%22b"), ("a\rb", "a%0Db"), ("a\nb", "a%0Ab")],
    )
    def test_escapes_quotes_and_line_breaks_in_names(self, name, escaped):
        body = MultipartBody(
            fields={name: "v", "file": FilePart(b"x", name)}
        ).encode()

        assert f'name="{escaped}"'.encode() in body
        assert f'filename="{escaped}"'.encode() in body

    def test_encode_is_repeatable_with_a_file_object(self):
        body = MultipartBody(fields={"file": FilePart(io.BytesIO(b"once"), "a.txt")})

        assert body.encode() == body.encode()
        assert b"once" in body.encode()

    def test_reads_a_path_when_encoding(self, tmp_path):
        path = tmp_path / "a.txt"
        path.write_bytes(b"late")
        body = MultipartBody(fields={"file": FilePart(path, "a.txt")})
        path.write_bytes(b"updated")

        assert b"updated" in body.encode()

    def test_matches_urllib3_encoding(self):
        field = RequestField(name="to", data="someone@adomain.com")
        field.make_multipart()
        file_field = RequestField(name="attachment", data=b"%PDF", filename="doc.pdf")
        file_field.make_multipart(content_type="application/pdf")
        expected, content_type = encode_multipart_formdata([field, file_field], boundary="B1")
        body = MultipartBody(
            fields={
                "to": "someone@adomain.com",
                "attachment": FilePart(b"%PDF", "doc.pdf"),
            },
        )

        assert body.encode() == expected
        assert body.content_type == content_type

    def test_repr_lists_names_without_content(self):
        body = MultipartBody(fields={"to": "x", "file": FilePart(b"secret", "a.txt")})

        assert "secret" not in repr(body)
        assert "'to'" in repr(body) and "'file'" in repr(body)
