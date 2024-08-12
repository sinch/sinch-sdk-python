import pytest
from sinch.domains.verification.models.responses import (
    StartSMSInitiateVerificationResponse,
    StartFlashCallInitiateVerificationResponse,
    StartCalloutInitiateVerificationResponse,
    StartDataInitiateVerificationResponse
)
from sinch.domains.verification.exceptions import VerificationException


def test_start_verification_sms(
    sinch_client_sync,
    phone_number
):
    verification_response = sinch_client_sync.verification.verifications.start_sms(
        identity={
            "type": "number",
            "endpoint": phone_number
        },
        reference="random",
        expiry="23:21:21"
    )

    assert isinstance(verification_response, StartSMSInitiateVerificationResponse)


def test_start_verification_sms_malformed_phone_number(
    sinch_client_sync,
    phone_number
):
    with pytest.raises(VerificationException) as err:
        sinch_client_sync.verification.verifications.start_sms(
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
        reference="random5"
    )

    assert isinstance(verification_response, StartFlashCallInitiateVerificationResponse)


def test_start_verification_phone_call(
    sinch_client_sync,
    phone_number
):
    verification_response = sinch_client_sync.verification.verifications.start_phone_call(
        identity={
            "type": "number",
            "endpoint": phone_number
        },
        reference="random32"
    )

    assert isinstance(verification_response, StartCalloutInitiateVerificationResponse)


@pytest.mark.skip(reason="Data verification. Mobile carrier support required.")
def test_start_verification_seamless(
    sinch_client_sync,
    phone_number
):
    verification_response = sinch_client_sync.verification.verifications.start_data(
        identity={
            "type": "number",
            "endpoint": phone_number
        },
        reference="random99"
    )

    assert isinstance(verification_response, StartDataInitiateVerificationResponse)


async def test_start_verification_sms_async(
    sinch_client_async,
    phone_number
):
    verification_response = await sinch_client_async.verification.verifications.start_sms(
        identity={
            "type": "number",
            "endpoint": phone_number
        },
        reference="random",
        expiry="23:21:21"
    )

    assert isinstance(verification_response, StartSMSInitiateVerificationResponse)
