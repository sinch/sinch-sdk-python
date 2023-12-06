from sinch.core.signature import Signature


def test_verification_signature(sinch_client_sync):
    signature = Signature(
        sinch_client_sync,
        http_method="POST",
        request_data={},
        request_uri="/verification/v1/verifications"
    )
    signature.calculate()
    assert signature.authorization_signature
