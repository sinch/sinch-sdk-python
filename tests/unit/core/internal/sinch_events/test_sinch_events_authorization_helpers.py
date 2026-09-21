"""Unit tests for sinch/core/internal/sinch_events/authorization_helpers.py"""
import base64
import hashlib
import hmac
import json

import pytest

from sinch.core.internal.sinch_events.authorization_helpers import (
    validate_authentication_header,
)
from tests.conftest import generate_service_authentication_header

SERVICE_SECRET = "vSMHuHj8tEoa0lfWfBKqEQ=="
SERVICE_ID = "serviceKey"


@pytest.fixture
def valid_request():
    method = "POST"
    path = "/webhooks/voice-v2/call/answered"
    body = json.dumps({"event": "call.answered"})
    headers = {
        "content-type": "application/json; charset=utf-8",
        "x-timestamp": "2026-06-10T21:27:04.1466768Z",
    }
    headers["authorization"] = generate_service_authentication_header(method, path, headers, body, SERVICE_SECRET, SERVICE_ID)
    return method, path, headers, body


def test_validate_authentication_header_expects_true_for_valid_signature(valid_request):
    """Test that a correctly signed request validates against the given secret and key."""
    method, path, headers, body = valid_request
    assert validate_authentication_header(
        SERVICE_ID, SERVICE_SECRET, headers, body, path, method
    )


def test_validate_authentication_header_expects_false_for_different_body(valid_request):
    """Test that a body modified after signing fails validation."""
    method, path, headers, _ = valid_request
    assert not validate_authentication_header(
        SERVICE_ID,
        SERVICE_SECRET,
        headers,
        json.dumps({"event": "call.hangup"}),
        path,
        method,
    )


def test_validate_authentication_header_expects_false_for_wrong_service_id(valid_request):
    """Test that a mismatched expected service_id fails validation."""
    method, path, headers, body = valid_request
    assert not validate_authentication_header(
        "other-service-key", SERVICE_SECRET, headers, body, path, method
    )

def test_validate_authentication_header_expects_false_for_missing_authorization_header(
    valid_request,
):
    """Test that a request without an Authorization header fails validation."""
    method, path, headers, body = valid_request
    del headers["authorization"]
    assert not validate_authentication_header(
        SERVICE_ID, SERVICE_SECRET, headers, body, path, method
    )


def test_validate_authentication_header_expects_false_for_unknown_scheme(valid_request):
    """Test that an Authorization header with an unsupported scheme fails validation."""
    method, path, headers, body = valid_request
    headers["authorization"] = "Bearer some-token"
    assert not validate_authentication_header(
        SERVICE_ID, SERVICE_SECRET, headers, body, path, method
    )


def test_validate_authentication_header_expects_false_for_missing_timestamp_header(
    valid_request,
):
    """Test that a request without the X-Timestamp header fails validation."""
    method, path, headers, body = valid_request
    del headers["x-timestamp"]
    assert not validate_authentication_header(
        SERVICE_ID, SERVICE_SECRET, headers, body, path, method
    )


def test_validate_authentication_header_expects_true_for_valid_signature_with_empty_body():
    """Test that a correctly signed request with an empty body validates against the given secret and key."""
    method = "GET"
    path = "/webhooks/voice-v2/call/answered"
    body = ""
    headers = {
        "content-type": "application/json; charset=utf-8",
        "x-timestamp": "2026-06-10T21:27:04.1466768Z",
    }
    headers["authorization"] = generate_service_authentication_header(
        method, path, headers, body, SERVICE_SECRET, SERVICE_ID
    )
    assert validate_authentication_header(
        SERVICE_ID, SERVICE_SECRET, headers, body, path, method
    )