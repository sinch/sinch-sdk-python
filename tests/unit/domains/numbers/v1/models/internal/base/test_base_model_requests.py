from sinch.domains.numbers.models.v1.internal.base import BaseModelConfigurationRequest


def test_model_handles_camel_case_input_and_output_expects_camelCase():
    """
    Test that the model correctly maps snake_case input to camelCase output.
    """
    data = {
        "sms_configuration": {"service_plan_id": "YOUR_SMS_servicePlanId"},
        "voice_configuration": {"app_id": "YOUR_voice_appID", "type": "RTC"},
    }
    request = BaseModelConfigurationRequest(**data)
    response = request.model_dump(by_alias=True)

    assert response == {
        "smsConfiguration": {"servicePlanId": "YOUR_SMS_servicePlanId"},
        "voiceConfiguration": {"appId": "YOUR_voice_appID", "type": "RTC"},
    }


def test_model_handles_camel_case_extra_input_and_output_expects_camelCase():
    """
    Test that the model correctly maps snake_case input to camelCase output.
    """
    data = {
        "phone_number": "+1234567890",
        "appId": "app_id",
        "sms_configuration": {"service_plan_id": "YOUR_SMS_servicePlanId"},
        "voice_configuration": {"appId": "YOUR_voice_appID", "type": "RTC"},
    }
    request = BaseModelConfigurationRequest(**data)
    response = request.model_dump(by_alias=True)

    assert response == {
        "phoneNumber": "+1234567890",
        "appId": "app_id",
        "smsConfiguration": {"servicePlanId": "YOUR_SMS_servicePlanId"},
        "voiceConfiguration": {"appId": "YOUR_voice_appID", "type": "RTC"},
    }
