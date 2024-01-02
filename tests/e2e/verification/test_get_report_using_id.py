from sinch.domains.verification.models.responses import GetVerificationByIdResponse


def test_get_report_verification_using_id(
    sinch_client_sync,
    phone_number,
    verification_id
):
    verification_response = sinch_client_sync.verification.get_by_id(
        id=verification_id
    )
    assert isinstance(verification_response, GetVerificationByIdResponse)


async def test_get_report_verification_using_id_async(
    sinch_client_async,
    phone_number,
    verification_id
):
    verification_response = await sinch_client_async.verification.get_by_id(
        id=verification_id
    )
    assert isinstance(verification_response, GetVerificationByIdResponse)
