from sinch.domains.verification.models.responses import ReportVerificationUsingIdentityResponse


def test_report_verification_using_identity_and_sms(
    sinch_client_sync,
    phone_number
):
    verification_response = sinch_client_sync.verification.report_using_identity(
        endpoint=phone_number,
        verification_report_request={
              "method": "sms",
              "sms": {
                "code": "2302"
              }
        }
    )
    assert isinstance(verification_response, ReportVerificationUsingIdentityResponse)
