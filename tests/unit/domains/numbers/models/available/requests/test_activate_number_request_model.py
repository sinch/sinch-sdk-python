import pytest
from pydantic import ValidationError
from sinch.domains.numbers.models.available.activate_number_request import ActivateNumberRequest

def test_activate_number_request_expects_snake_case_input():
    """
    Test that the model correctly handles snake_case input.
    """
    data = {
        "phone_number": "+1234567890",
        "sms_configuration": {"service_plan_id": "YOUR_SMS_servicePlanId"},
        "voice_configuration": {
            "app_id": "YOUR_voice_appID",
            "type": "RTC"
        },
        "callback_url": "https://example.com/callback"
    }

    # Instantiate the model
    request = ActivateNumberRequest(**data)

    # Assert the field values
    assert request.phone_number == "+1234567890"
    assert request.sms_configuration == {"service_plan_id": "YOUR_SMS_servicePlanId"}
    assert request.voice_configuration == {
        "app_id": "YOUR_voice_appID",
        "type": "RTC"
    }
    assert request.callback_url == "https://example.com/callback"

def test_activate_number_request_expects_camel_case_input():
    """
    Test that the model correctly handles camelCase input.
    """
    data = {
        "phoneNumber": "+1234567890",
        "smsConfiguration": {"servicePlanId": "YOUR_SMS_servicePlanId"},
        "voice_configuration": {
            "appId": "YOUR_voice_appID",
            "type": "RTC"
        },
        "callback_url": "https://example.com/callback"
    }
    request = ActivateNumberRequest(**data)

    # Assert fields are populated correctly
    assert request.phone_number == "+1234567890"
    assert request.sms_configuration == {"servicePlanId": "YOUR_SMS_servicePlanId"}
    assert request.voice_configuration == {
         "appId": "YOUR_voice_appID",
         "type": "RTC"
        }
    assert request.callback_url == "https://example.com/callback"

def test_activate_number_request_expects_mixed_case_input():
    """
    Test that the model correctly handles mixed camelCase and snake_case input.
    """
    data = {
        "phone_number": "+1234567890",
        "smsConfiguration": {"servicePlanId": "YOUR_SMS_servicePlanId"},
        "voice_configuration": {
            "appId": "YOUR_voice_appID",
            "type": "RTC"
        },
        "callback_url": "https://example.com/callback"
    }
    request = ActivateNumberRequest(**data)

    # Assert fields are populated correctly
    assert request.phone_number == "+1234567890"
    assert request.sms_configuration == {"servicePlanId": "YOUR_SMS_servicePlanId"}
    assert request.voice_configuration == {
            "appId": "YOUR_voice_appID",
            "type": "RTC"
        }
    assert request.callback_url == "https://example.com/callback"

def test_activate_number_request_expects_validation_error_for_missing_field():
    """
    Test that the model raises a validation error for missing required fields.
    """
    data = {
        "sms_configuration": {"servicePlanId": "YOUR_SMS_servicePlanId"},
        "voice_configuration": {
            "appId": "YOUR_voice_appID",
            "type": "RTC"
         },
        "callback_url": "https://example.com/callback"
    }
    with pytest.raises(ValidationError) as exc_info:
        ActivateNumberRequest(**data)

    # Assert the error mentions the missing phone_number field
    assert "phone_number" in str(exc_info.value) or "phoneNumber" in str(exc_info.value)
