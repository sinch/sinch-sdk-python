from sinch.domains.verification.models.responses import (
    StartSMSInitiateVerificationResponse,
    StartFlashCallInitiateVerificationResponse
)
from sinch.domains.verification.enums import VerificationMethod


def test_start_verification_sms(
    sinch_client_sync,
    phone_number
):
    verification_response = sinch_client_sync.verification.verifications.start(
        method="sms",
        identity={
            "type": "number",
            "endpoint": phone_number
        },
        reference="random"
    )

    assert isinstance(verification_response, StartSMSInitiateVerificationResponse)


def test_start_verification_flash_call(
    sinch_client_sync,
    phone_number
):
    verification_response = sinch_client_sync.verification.verifications.start(
        method=VerificationMethod.FLASHCALL.value,
        identity={
            "type": "number",
            "endpoint": phone_number
        },
        reference="random5"
    )

    assert isinstance(verification_response, StartFlashCallInitiateVerificationResponse)


async def test_start_verification_async(
    sinch_client_async,
    phone_number
):
    verification_response = await sinch_client_async.verification.verifications.start(
        method="sms",
        identity={
            "type": "number",
            "endpoint": phone_number
        },
        reference="random"
    )

    assert isinstance(verification_response, StartSMSInitiateVerificationResponse)
