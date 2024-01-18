import json
from sinch.core.signature import Signature


def test_request_signature(
    sinch_client_sync,
    verification_request_signature,
    verification_request_signature_timestamp
):
    signature = Signature(
        sinch_client_sync,
        http_method="GET",
        request_data=json.dumps({"test": "test"}),
        request_uri="/verification/v1/verifications"
    )
    signature.signature_timestamp = verification_request_signature_timestamp
    signature.calculate()

    assert signature.authorization_signature
    assert isinstance(signature.authorization_signature, str)
    assert verification_request_signature == signature.authorization_signature


def test_request_signature_using_empty_body(
    sinch_client_sync,
    verification_request_with_empty_body_signature,
    verification_request_signature_timestamp
):
    signature = Signature(
        sinch_client_sync,
        http_method="POST",
        request_data=None,
        request_uri="/verification/v1/verifications"
    )
    signature.signature_timestamp = verification_request_signature_timestamp
    signature.calculate()

    assert signature.authorization_signature
    assert isinstance(signature.authorization_signature, str)
    assert verification_request_with_empty_body_signature == signature.authorization_signature


def test_get_headers_with_signature_and_async_client(
    sinch_client_async,
    verification_request_with_empty_body_signature,
    verification_request_signature_timestamp
):
    signature = Signature(
        sinch_client_async,
        http_method="POST",
        request_data=None,
        request_uri="/verification/v1/verifications"
    )
    signature.signature_timestamp = verification_request_signature_timestamp
    headers = signature.get_http_headers_with_signature()

    assert "x-timestamp" in headers
    assert "Authorization" in headers
    assert "Content-Type" in headers
    assert verification_request_with_empty_body_signature in headers["Authorization"]
