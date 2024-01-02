import json
from sinch.core.signature import Signature


def test_request_signature(
    sinch_client_sync
):
    signature = Signature(
        sinch_client_sync,
        http_method="POST",
        request_data=json.dumps({"test": "test"}),
        request_uri="/verification/v1/verifications"
    )
    signature.calculate()
    assert signature.authorization_signature


def test_request_signature_using_empty_body(
    sinch_client_sync
):
    signature = Signature(
        sinch_client_sync,
        http_method="POST",
        request_data=None,
        request_uri="/verification/v1/verifications"
    )
    signature.calculate()
    assert signature.authorization_signature
