from sinch.domains.verification.models.responses import (
    StartFlashCallInitiateVerificationResponse,
    GetVerificationStatusByIdResponse
)

UNICODE_POTATO = '🥔'

def test_sending_unicode_potato_using_verification_api(
    sinch_client_sync,
    phone_number
):

    verification_response = sinch_client_sync.verification.verifications.start_flash_call(
        identity={
            "type": "number",
            "endpoint": phone_number
        },
        reference=UNICODE_POTATO,
        dial_timeout=5
    )

    assert isinstance(verification_response, StartFlashCallInitiateVerificationResponse)


async def test_receiving_unicode_potato_using_verification_api_async(
    sinch_client_async,
    verification_id
):
    verification_response = await sinch_client_async.verification.verification_status.get_by_id(
        id=verification_id
    )
    assert isinstance(verification_response, GetVerificationStatusByIdResponse)
    assert verification_response.reference == UNICODE_POTATO
