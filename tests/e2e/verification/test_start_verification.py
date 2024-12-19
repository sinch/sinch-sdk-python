import pytest
from sinch.domains.verification.exceptions import VerificationException
from sinch.domains.verification.models.responses import (
    StartSMSVerificationResponse,
    StartFlashCallVerificationResponse,
    StartPhoneCallVerificationResponse,
    StartDataVerificationResponse,
    StartFlashCallInitiateVerificationResponse,
    StartCalloutInitiateVerificationResponse,
    StartDataInitiateVerificationResponse
)


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
    assert isinstance(verification_response, StartSMSVerificationResponse)


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
        reference="random7"
    )
    assert isinstance(verification_response, StartFlashCallVerificationResponse)


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
    assert isinstance(verification_response, StartPhoneCallVerificationResponse)


def test_start_verification_callout(
    sinch_client_sync,
    phone_number
):
    verification_response = sinch_client_sync.verification.verifications.start_callout(
        identity={
            "type": "number",
            "endpoint": phone_number
        },
        reference="random32",
        speech_locale="en-US"
    )

    assert isinstance(verification_response, StartPhoneCallVerificationResponse)


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
    assert isinstance(verification_response, StartDataVerificationResponse)


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
    assert isinstance(verification_response, StartSMSVerificationResponse)
