from sinch.domains.numbers.models.v1.internal import RentAnyNumberRequest
from sinch.domains.numbers.models.v1.internal.sms_configuration_request import SmsConfigurationRequest
from sinch.domains.numbers.models.v1.internal.voice_configuration_request import VoiceConfigurationRTC


def test_rent_any_number_request_expects_valid_data():
    """
    Test that RentAnyNumberRequest correctly parses valid data.
    """
    data = {
        "numberPattern": {
            "pattern": "string",
            "searchPattern": "START"
        },
        "regionCode": "string",
        "type": "MOBILE",
        "capabilities": ["SMS"],
        "smsConfiguration": {
            "servicePlanId": "string",
            "campaignId": "string"
        },
        "voiceConfiguration": {
            "type": "RTC",
            "appId": "string"
        },
        "callbackUrl": "https://www.your-callback-server.com/callback"
    }

    request = RentAnyNumberRequest(**data)

    assert request.number_pattern.pattern == "string"
    assert request.number_pattern.search_pattern == "START"
    assert request.region_code == "string"
    assert request.number_type == "MOBILE"
    assert request.capabilities == ["SMS"]
    assert request.sms_configuration == SmsConfigurationRequest(campaign_id="string", service_plan_id="string")  
    assert request.voice_configuration == VoiceConfigurationRTC(app_id="string", type="RTC")


    assert request.event_destination_target == "https://www.your-callback-server.com/callback"


def test_rent_any_number_request_expects_missing_optional_fields():
    """
    Test that RentAnyNumberRequest handles missing optional fields correctly.
    """
    data = {
        "regionCode": "string",
        "type": "MOBILE"
    }

    request = RentAnyNumberRequest(**data)

    assert request.region_code == "string"
    assert request.number_type == "MOBILE"

    assert request.number_pattern is None
    assert request.capabilities is None
    assert request.sms_configuration is None
    assert request.voice_configuration is None
    assert request.event_destination_target is None
