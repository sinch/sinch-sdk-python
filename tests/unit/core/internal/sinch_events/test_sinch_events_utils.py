"""Unit tests for sinch/core/internal/sinch_events/utils.py"""
import pytest

from sinch.core.internal.sinch_events.utils import (
    build_string_to_sign,
    check_authorization_header_format,
    compute_content_md5,
    compute_signature,
    decode_payload,
    get_header,
    normalize_headers,
    parse_json,
)


def test_normalize_headers_expects_lowercase_keys_and_dropped_none_values():
    """Test that normalize_headers lower-cases keys and drops None values."""
    headers = {"Content-Type": "application/json", "X-Timestamp": None}
    assert normalize_headers(headers) == {"content-type": "application/json"}


def test_get_header_expects_first_item_for_list_value():
    """Test that get_header unwraps a list header value."""
    assert get_header(["a", "b"]) == "a"


def test_get_header_expects_none_for_empty_list():
    """Test that get_header returns None for an empty list."""
    assert get_header([]) is None


def test_decode_payload_expects_bytes_decoded_with_charset_from_headers():
    """Test that decode_payload decodes bytes using the Content-Type charset."""
    payload = "café".encode("latin-1")
    headers = {"content-type": "text/plain; charset=latin-1"}
    assert decode_payload(payload, headers) == "café"


def test_parse_json_expects_invalid_json_raises_value_error():
    """Test that parse_json raises ValueError for invalid JSON."""
    with pytest.raises(ValueError, match="Failed to decode JSON"):
        parse_json("not json")


def test_check_authorization_header_format_expects_scheme_and_value():
    """Test that check_authorization_header_format splits scheme from value."""
    assert check_authorization_header_format("service key:signature") == (
        "service",
        "key:signature",
    )


def test_check_authorization_header_format_expects_none_without_scheme():
    """Test that check_authorization_header_format returns None with no space."""
    assert check_authorization_header_format("malformed") is None


def test_compute_content_md5_expects_base64_encoded_digest():
    """Test that compute_content_md5 returns the expected Base64 MD5 digest."""
    assert compute_content_md5("") == "1B2M2Y8AsgTpgAmY7PhCfg=="


def test_build_string_to_sign_expects_newline_joined_canonical_string():
    """Test that build_string_to_sign joins its parts with newlines in order."""
    result = build_string_to_sign(
        "POST", "md5==", "application/json", "2026-01-01T00:00:00Z", "/path"
    )
    assert result == "POST\nmd5==\napplication/json\nx-timestamp:2026-01-01T00:00:00Z\n/path"


def test_compute_signature_expects_known_vector():
    """Test compute_signature against the documented Voice API v2 example vector."""
    string_to_sign = (
        "POST\n"
        "1B2M2Y8AsgTpgAmY7PhCfg==\n"
        "application/json; charset=utf-8\n"
        "x-timestamp:2026-06-10T21:27:04.1466768Z\n"
        "/webhooks/voice-v2/call/answered"
    )
    signature = compute_signature(string_to_sign, "BeIukql3pTKJ8RGL5zo0DA==")
    assert signature == "yb+8Wt8y1rn6/qIxq6oCrkX1t3ewmhitljHpWm91imI="
