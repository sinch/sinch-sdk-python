from sinch.domains.verification.models.responses import GetVerificationByReferenceResponse


def test_get_report_verification_using_reference(
    sinch_client_sync
):
    verification_response = sinch_client_sync.verification.get_by_reference(
        reference="random"
    )
    assert isinstance(verification_response, GetVerificationByReferenceResponse)
