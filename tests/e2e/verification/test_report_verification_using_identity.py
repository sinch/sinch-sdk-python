from sinch.domains.verification.models.responses import ReportVerificationByIdentityResponse

def test_report_verification_using_identity_and_sms(
    sinch_client_sync,
    phone_number
):
    verification_response = sinch_client_sync.verification.verifications.report_sms_by_identity(
        endpoint=phone_number,
        code="2302"
    )
    assert isinstance(verification_response, ReportVerificationByIdentityResponse)


def test_report_verification_using_identity_and_flash_call(
    sinch_client_sync,
    phone_number
):
    verification_response = sinch_client_sync.verification.verifications.report_flash_call_by_identity(
        endpoint=phone_number
    )
    assert isinstance(verification_response, ReportVerificationByIdentityResponse)


def test_report_verification_using_identity_and_phone_call(
    sinch_client_sync,
    verification_id,
    phone_number
):
    verification_response = sinch_client_sync.verification.verifications.report_phone_call_by_identity(
        endpoint=phone_number,
        code="2302"
    )
    assert isinstance(verification_response, ReportVerificationByIdentityResponse)


async def test_report_verification_using_identity_and_sms_async(
    sinch_client_async,
    verification_id,
    phone_number
):
    verification_response = await sinch_client_async.verification.verifications.report_sms_by_identity(
        endpoint=phone_number,
        code="2302"
    )
    assert isinstance(verification_response, ReportVerificationByIdentityResponse)


async def test_report_verification_using_identity_and_flash_call_async(
    sinch_client_async,
    phone_number
):
    verification_response = await sinch_client_async.verification.verifications.report_flash_call_by_identity(
        endpoint=phone_number
    )
    assert isinstance(verification_response, ReportVerificationByIdentityResponse)


async def test_report_verification_using_identity_and_phone_call_async(
    sinch_client_async,
    verification_id,
    phone_number
):
    verification_response = await sinch_client_async.verification.verifications.report_phone_call_by_identity(
        endpoint=phone_number,
        code="2302"
    )
    assert isinstance(verification_response, ReportVerificationByIdentityResponse)
