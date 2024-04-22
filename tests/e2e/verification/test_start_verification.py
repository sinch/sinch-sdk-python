import pytest
from sinch.domains.verification.models.responses import (
    StartSMSInitiateVerificationResponse,
    StartFlashCallInitiateVerificationResponse
)
from sinch.domains.verification.enums import VerificationMethod
from sinch.domains.verification.exceptions import VerificationException


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


def test_start_verification_sms_malformed_phone_number(
    sinch_client_sync,
    phone_number
):
    with pytest.raises(VerificationException) as err:
        sinch_client_sync.verification.verifications.start(
            method="sms",
            identity={
                "type": "number",
                "endpoint": "abcd" + phone_number + "abcd"
            },
            reference="random"
        )
    assert "invalid" in err.value.http_response.body["message"]


def test_start_verification_flash_call(
    sinch_client_sync,
    phone_number
):
    verification_response = sinch_client_sync.verification.verifications.start_flash_call(
        identity={
            "type": "number",
            "endpoint": phone_number
        },
        reference="random5",
        dial_timeout=5
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
