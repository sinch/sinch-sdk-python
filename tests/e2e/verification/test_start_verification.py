from sinch.domains.verification.models.responses import StartVerificationResponse


def test_start_verification(
    sinch_client_sync,
    phone_number,
    verification_key,
    verification_secret
):
    sinch_client_sync.configuration.verification_key = verification_key
    sinch_client_sync.configuration.verification_secret = verification_secret

    verification_response = sinch_client_sync.verification.start(
        method="sms",
        identity={
            "type": "number",
            "endpoint": phone_number
        }
    )

    assert isinstance(verification_response, StartVerificationResponse)
