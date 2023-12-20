from sinch.domains.verification.models.responses import GetVerificationByIdResponse


def test_get_report_verification_using_id(
    sinch_client_sync,
    phone_number,
    verification_key,
    verification_secret
):
    sinch_client_sync.configuration.verification_key = verification_key
    sinch_client_sync.configuration.verification_secret = verification_secret

    verification_response = sinch_client_sync.verification.get_by_id(
        id="test"
    )

    assert isinstance(verification_response, GetVerificationByIdResponse)
