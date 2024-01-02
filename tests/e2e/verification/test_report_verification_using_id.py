from sinch.domains.verification.models.responses import ReportVerificationUsingIdResponse


def test_report_verification_using_id_and_sms(
    sinch_client_sync,
    phone_number,
    verification_id
):
    verification_response = sinch_client_sync.verification.report_using_id(
        id=verification_id,
        verification_report_request={
            "method": "sms",
            "sms": {
                "code": "2302"
            }
        }
    )
    assert isinstance(verification_response, ReportVerificationUsingIdResponse)
