import pytest
from pydantic import ValidationError
from sinch.domains.numbers.models.v1.internal import UpdateNumberConfigurationRequest


def test_update_number_configuration_request_valid_expects_parsed_response():
    """ Test that the model correctly handles request. """
    data = {
        "phoneNumber": "+1234567890",
        "displayName": "Test Number",
        "smsConfiguration": {
            "servicePlanId": "string",
            "campaignId": "YOUR_campaignId_from_TCR"
          },
          "voiceConfiguration": {
            "type": "RTC",
            "appId": "YOUR_Voice_appId"
          },
          "callbackUrl": "https://www.your-callback-server.com/callback"
    }
    request = UpdateNumberConfigurationRequest(**data)
    assert request.phone_number == "+1234567890"
    assert request.display_name == "Test Number"
    assert request.sms_configuration == {
            "servicePlanId": "string",
            "campaignId": "YOUR_campaignId_from_TCR"
    }
    assert request.voice_configuration == {
            "type": "RTC",
            "appId": "YOUR_Voice_appId"
    }
    assert request.callback_url == "https://www.your-callback-server.com/callback"

def test_update_number_configuration_request_missing_phone_number_expects_error():
    """Test that the model raises a validation error for missing required fields. """
    data = {
        "displayName": "Test Number",
        "callbackUrl": "https://www.your-callback-server.com/callback"
    }
    with pytest.raises(ValidationError):
        UpdateNumberConfigurationRequest(**data)

def test_update_number_configuration_request_invalid_phone_number():
    """Test that the model raises a validation error for invalid phone number type. """
    data = {
        "phoneNumber": 1234567890,
        "displayName": "Test Number",
        "callbackUrl": "https://www.your-callback-server.com/callback"
    }
    with pytest.raises(ValidationError):
        UpdateNumberConfigurationRequest(**data)

def test_update_number_configuration_request_optional_fields():
    data = {
        "phoneNumber": "+1234567890"
    }
    request = UpdateNumberConfigurationRequest(**data)
    assert request.phone_number == "+1234567890"
    assert request.display_name is None
    assert request.sms_configuration is None
    assert request.voice_configuration is None
    assert request.callback_url is None