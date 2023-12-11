# from sinch.domains.verification.models.responses import StartVerificationResponse


def test_report_verification_using_identity(
    sinch_client_sync,
    phone_number,
    verification_key,
    verification_secret
):
    sinch_client_sync.configuration.verification_key = verification_key
    sinch_client_sync.configuration.verification_secret = verification_secret

    verification_response = sinch_client_sync.verification.report_using_identity()
    # assert isinstance(verification_response, StartVerificationResponse)
