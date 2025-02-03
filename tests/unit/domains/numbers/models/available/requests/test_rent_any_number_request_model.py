from sinch.domains.numbers.models.available.rent_any_number_request import RentAnyNumberRequest


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
    assert request.number_pattern.search_pattern =="START"
    assert request.region_code == "string"
    assert request.type_ == "MOBILE"
    assert request.capabilities == ["SMS"]
    assert request.sms_configuration.service_plan_id ==  "string"
    assert request.sms_configuration.campaign_id == "string"
    assert request.voice_configuration.app_id == "string"
    assert request.callback_url == "https://www.your-callback-server.com/callback"


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
    assert request.type_ == "MOBILE"

    assert request.number_pattern is None
    assert request.capabilities is None
    assert request.sms_configuration is None
    assert request.voice_configuration is None
    assert request.callback_url is None


def test_rent_any_number_request_expects_extra_fields():
    """
    Test that RentAnyNumberRequest accepts extra fields.
    """
    data = {
        "regionCode": "string",
        "type": "MOBILE",
        "extraField": "Extra field"
    }

    request = RentAnyNumberRequest(**data)

    assert request.region_code == "string"
    assert request.type_ == "MOBILE"
    assert request.extraField == "Extra field"
