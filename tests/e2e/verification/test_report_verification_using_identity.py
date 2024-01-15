from sinch.domains.verification.models.responses import ReportVerificationUsingIdentityResponse


def test_report_verification_using_identity_and_sms(
    sinch_client_sync,
    phone_number
):
    verification_response = sinch_client_sync.verification.verifications.report_by_identity(
        endpoint=phone_number,
        verification_report_request={
              "method": "sms",
              "sms": {
                "code": "2302"
              }
        }
    )
    assert isinstance(verification_response, ReportVerificationUsingIdentityResponse)


async def test_report_verification_using_identity_and_sms_async(
    sinch_client_async,
    phone_number
):
    verification_response = await sinch_client_async.verification.verifications.report_by_identity(
        endpoint=phone_number,
        verification_report_request={
              "method": "sms",
              "sms": {
                "code": "2302"
              }
        }
    )
    assert isinstance(verification_response, ReportVerificationUsingIdentityResponse)
