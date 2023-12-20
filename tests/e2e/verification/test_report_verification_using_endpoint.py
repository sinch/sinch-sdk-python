from sinch.domains.verification.models.responses import GetVerificationByIdentityResponse


def test_get_report_verification_using_endpoint(
    sinch_client_sync,
    phone_number,
    verification_key,
    verification_secret
):
    sinch_client_sync.configuration.verification_key = verification_key
    sinch_client_sync.configuration.verification_secret = verification_secret

    verification_response = sinch_client_sync.verification.get_by_identity(
        method="sms",
        identity={
            "type": "number",
            "endpoint": phone_number
        }
    )

    assert isinstance(verification_response, GetVerificationByIdentityResponse)
