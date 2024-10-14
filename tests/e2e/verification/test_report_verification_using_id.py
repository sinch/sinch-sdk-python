from sinch.domains.verification.models.responses import ReportVerificationByIdResponse


def test_report_verification_using_id_and_sms_legacy_api(
    sinch_client_sync,
    phone_number,
    verification_id
):
    verification_response = sinch_client_sync.verification.verifications.report_by_id(
        id=verification_id,
        verification_report_request={
            "method": "sms",
            "sms": {
                "code": "2302"
            }
        }
    )
    assert isinstance(verification_response, ReportVerificationByIdResponse)


def test_report_verification_using_id_and_sms(
    sinch_client_sync,
    verification_id
):
    verification_response = sinch_client_sync.verification.verifications.report_sms_by_id(
        id=verification_id,
        code="2302"
    )
    assert isinstance(verification_response, ReportVerificationByIdResponse)


def test_report_verification_using_id_and_flash_call(
    sinch_client_sync,
    verification_id
):
    verification_response = sinch_client_sync.verification.verifications.report_flash_call_by_id(
        id=verification_id,
        cli="+19473452226"
    )
    assert isinstance(verification_response, ReportVerificationByIdResponse)


def test_report_verification_using_id_and_and_phone_call(
    sinch_client_sync,
    verification_id
):
    verification_response = sinch_client_sync.verification.verifications.report_phone_call_by_id(
        id=verification_id,
        code="8943"
    )
    assert isinstance(verification_response, ReportVerificationByIdResponse)


async def test_report_verification_using_id_and_sms_async(
    sinch_client_async,
    verification_id
):
    verification_response = await sinch_client_async.verification.verifications.report_sms_by_id(
        id=verification_id,
        code="2302"
    )
    assert isinstance(verification_response, ReportVerificationByIdResponse)


async def test_report_verification_using_id_and_flash_call_async(
    sinch_client_async,
    verification_id
):
    verification_response = await sinch_client_async.verification.verifications.report_flash_call_by_id(
        id=verification_id,
        cli="+19473452226"
    )
    assert isinstance(verification_response, ReportVerificationByIdResponse)


async def test_report_verification_using_id_and_and_phone_call_async(
    sinch_client_async,
    verification_id
):
    verification_response = await sinch_client_async.verification.verifications.report_phone_call_by_id(
        id=verification_id,
        code="8943"
    )
    assert isinstance(verification_response, ReportVerificationByIdResponse)
