import json
from sinch.core.signature import Signature


def test_verification_signature(
    sinch_client_sync,
    verification_key,
    verification_secret
):
    sinch_client_sync.configuration.verification_key = verification_key
    sinch_client_sync.configuration.verification_secret = verification_secret

    signature = Signature(
        sinch_client_sync,
        http_method="POST",
        request_data=json.dumps({"test": "test"}),
        request_uri="/verification/v1/verifications"
    )
    signature.calculate()
    assert signature.authorization_signature
