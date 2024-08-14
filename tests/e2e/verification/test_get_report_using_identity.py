from sinch.domains.verification.models.responses import GetVerificationStatusByIdentityResponse


def test_get_report_verification_using_identity(
    sinch_client_sync,
    phone_number
):
    verification_response = sinch_client_sync.verification.verification_status.get_by_identity(
        endpoint=phone_number,
        method="sms"
    )
    assert isinstance(verification_response, GetVerificationStatusByIdentityResponse)


def test_get_report_verification_using_identity(
    sinch_client_sync,
    phone_number
):
    verification_response = sinch_client_sync.verification.verification_status.get_by_identity(
        endpoint=phone_number,
        method="sms"
    )
    assert isinstance(verification_response, GetVerificationStatusByIdentityResponse)


def test_get_report_verification_using_identity(
    sinch_client_sync,
    phone_number
):
    verification_response = sinch_client_sync.verification.verification_status.get_by_identity(
        endpoint=phone_number,
        method="sms"
    )
    assert isinstance(verification_response, GetVerificationStatusByIdentityResponse)


async def test_get_report_verification_using_identity_async(
    sinch_client_async,
    phone_number
):
    verification_response = await sinch_client_async.verification.verification_status.get_by_identity(
        endpoint=phone_number,
        method="sms"
    )
    assert isinstance(verification_response, GetVerificationStatusByIdentityResponse)


async def test_get_report_verification_using_identity_async(
    sinch_client_async,
    phone_number
):
    verification_response = await sinch_client_async.verification.verification_status.get_by_identity(
        endpoint=phone_number,
        method="sms"
    )
    assert isinstance(verification_response, GetVerificationStatusByIdentityResponse)


async def test_get_report_verification_using_identity_async(
    sinch_client_async,
    phone_number
):
    verification_response = await sinch_client_async.verification.verification_status.get_by_identity(
        endpoint=phone_number,
        method="sms"
    )
    assert isinstance(verification_response, GetVerificationStatusByIdentityResponse)
