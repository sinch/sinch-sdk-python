from sinch.domains.verification.models.responses import StartVerificationResponse


def test_start_verification(
    sinch_client_sync,
    phone_number
):
    verification_response = sinch_client_sync.verification.verifications.start(
        method="sms",
        identity={
            "type": "number",
            "endpoint": phone_number
        },
        reference="random"
    )

    assert isinstance(verification_response, StartVerificationResponse)


async def test_start_verification_async(
    sinch_client_async,
    phone_number
):
    verification_response = await sinch_client_async.verification.verifications.start(
        method="sms",
        identity={
            "type": "number",
            "endpoint": phone_number
        },
        reference="random"
    )

    assert isinstance(verification_response, StartVerificationResponse)
