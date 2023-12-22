from sinch.domains.verification.models.responses import GetVerificationByIdResponse


def test_report_verification_using_id_and_sms(
    sinch_client_sync,
    phone_number,
    verification_key,
    verification_secret,
    verification_id
):
    sinch_client_sync.configuration.verification_key = verification_key
    sinch_client_sync.configuration.verification_secret = verification_secret

    verification_response = sinch_client_sync.verification.report_using_id(
        id=verification_id,
        verification_report_request={
            "method": "sms",
            "sms": {
                "code": "1481"
            }
        }
    )

    assert isinstance(verification_response, GetVerificationByIdResponse)
