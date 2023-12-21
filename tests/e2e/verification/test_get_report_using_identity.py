from sinch.domains.verification.models.responses import GetVerificationByIdentityResponse


def test_get_report_verification_using_identity(
    sinch_client_sync,
    phone_number,
    verification_key,
    verification_secret
):
    sinch_client_sync.configuration.verification_key = verification_key
    sinch_client_sync.configuration.verification_secret = verification_secret

    verification_response = sinch_client_sync.verification.get_by_identity(
        endpoint=phone_number,
        method="sms"
    )

    assert isinstance(verification_response, GetVerificationByIdentityResponse)
