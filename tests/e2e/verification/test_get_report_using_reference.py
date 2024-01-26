from sinch.domains.verification.models.responses import GetVerificationStatusByReferenceResponse


def test_get_report_verification_using_reference(
    sinch_client_sync
):
    verification_response = sinch_client_sync.verification.verification_status.get_by_reference(
        reference="random"
    )
    assert isinstance(verification_response, GetVerificationStatusByReferenceResponse)


async def test_get_report_verification_using_reference_async(
    sinch_client_async
):
    verification_response = await sinch_client_async.verification.verification_status.get_by_reference(
        reference="random"
    )
    assert isinstance(verification_response, GetVerificationStatusByReferenceResponse)
