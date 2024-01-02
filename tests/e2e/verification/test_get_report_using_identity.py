from sinch.domains.verification.models.responses import GetVerificationByIdentityResponse


def test_get_report_verification_using_identity(
    sinch_client_sync,
    phone_number
):
    verification_response = sinch_client_sync.verification.get_by_identity(
        endpoint=phone_number,
        method="sms"
    )
    assert isinstance(verification_response, GetVerificationByIdentityResponse)


async def test_get_report_verification_using_identity_async(
    sinch_client_async,
    phone_number
):
    verification_response = await sinch_client_async.verification.get_by_identity(
        endpoint=phone_number,
        method="sms"
    )
    assert isinstance(verification_response, GetVerificationByIdentityResponse)
