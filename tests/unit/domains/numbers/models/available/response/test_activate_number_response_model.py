import pytest
from sinch.domains.numbers.models.available.responses import ActivateNumberResponse

@pytest.fixture
def test_data():
    return {
        "phoneNumber": "+12025550134",
        "displayName": "string",
        "regionCode": "US",
        "type": "MOBILE",
        "capability": ["SMS"],
        "money": {"currencyCode": "USD", "amount": "2.00"},
        "paymentIntervalMonths": 0,
        "nextChargeDate": "2025-01-22T13:19:31.095Z",
        "expireAt": "2025-01-22T13:19:31.095Z",
        "smsConfiguration": {
            "servicePlanId": "string",
            "campaignId": "string",
            "scheduledProvisioning": {
                "servicePlanId": "string",
                "campaignId": "string",
                "status": "PROVISIONING_STATUS_UNSPECIFIED",
                "lastUpdatedTime": "2025-01-22T13:19:31.095Z",
                "errorCodes": ["ERROR_CODE_UNSPECIFIED"],
            },
        },
        "voiceConfiguration": {
            "lastUpdatedTime": "2025-01-22T13:19:31.095Z",
            "scheduledVoiceProvisioning": {
                "type": "RTC",
                "lastUpdatedTime": "2025-01-22T13:19:31.095Z",
                "status": "PROVISIONING_STATUS_UNSPECIFIED",
                "trunkId": "string",
            },
            "appId": "string",
        },
        "callbackUrl": "https://www.your-callback-server.com/callback",
    }

def assert_sms_configuration(sms_config):
    """
    Assert sms_configuration fields.
    """
    assert sms_config["service_plan_id"] == "string"
    assert sms_config["campaign_id"] == "string"
    scheduled_provisioning = sms_config["scheduled_provisioning"]
    assert scheduled_provisioning["service_plan_id"] == "string"
    assert scheduled_provisioning["campaign_id"] == "string"
    assert scheduled_provisioning["status"] == "PROVISIONING_STATUS_UNSPECIFIED"
    assert scheduled_provisioning["last_updated_time"] == "2025-01-22T13:19:31.095Z"
    assert scheduled_provisioning["error_codes"] == ["ERROR_CODE_UNSPECIFIED"]

def assert_voice_configuration(voice_config):
    """
    Assert voice_configuration fields.
    """
    assert voice_config["last_updated_time"] == "2025-01-22T13:19:31.095Z"
    assert voice_config["app_id"] == "string"
    scheduled_voice_provisioning = voice_config["scheduled_voice_provisioning"]
    assert scheduled_voice_provisioning["type"] == "RTC"
    assert scheduled_voice_provisioning["last_updated_time"] == "2025-01-22T13:19:31.095Z"
    assert scheduled_voice_provisioning["status"] == "PROVISIONING_STATUS_UNSPECIFIED"
    assert scheduled_voice_provisioning["trunk_id"] == "string"

def test_activate_number_response_expects_all_fields_mapped_correctly(test_data):
    """
    Expects all fields to map correctly from camelCase input,
    converts nested keys to snake_case, and handles dynamic fields
    """
    data = {
        "phoneNumber": "+12025550134",
        "displayName": "string",
        "regionCode": "US",
        "type": "MOBILE",
        "capability": ["SMS"],
        "money": {"currencyCode": "USD", "amount": "2.00"},
        "paymentIntervalMonths": 0,
        "nextChargeDate": "2025-01-22T13:19:31.095Z",
        "expireAt": "2025-01-22T13:19:31.095Z",
        "smsConfiguration": {
            "servicePlanId": "string",
            "campaignId": "string",
            "scheduledProvisioning": {
                "servicePlanId": "string",
                "campaignId": "string",
                "status": "PROVISIONING_STATUS_UNSPECIFIED",
                "lastUpdatedTime": "2025-01-22T13:19:31.095Z",
                "errorCodes": ["ERROR_CODE_UNSPECIFIED"],
            },
        },
        "voiceConfiguration": {
            "lastUpdatedTime": "2025-01-22T13:19:31.095Z",
            "scheduledVoiceProvisioning": {
                "type": "RTC",
                "lastUpdatedTime": "2025-01-22T13:19:31.095Z",
                "status": "PROVISIONING_STATUS_UNSPECIFIED",
                "trunkId": "string",
            },
            "appId": "string",
        },
        "callbackUrl": "https://www.your-callback-server.com/callback",
    }
    response = ActivateNumberResponse(**data)

    assert response.phone_number == "+12025550134"
    assert response.display_name == "string"
    assert response.region_code == "US"
    assert response.type == "MOBILE"
    assert response.capability == ["SMS"]
    assert response.money["currency_code"] == "USD"
    assert response.payment_interval_months == 0
    assert response.next_charge_date == "2025-01-22T13:19:31.095Z"
    assert response.expire_at == "2025-01-22T13:19:31.095Z"
    assert response.callback_url == "https://www.your-callback-server.com/callback"
    # Assert sms_configuration and voice_configuration using helper functions
    assert_sms_configuration(response.sms_configuration)
    assert_voice_configuration(response.voice_configuration)


def test_activate_number_response_expects_unrecognized_fields():
    """
    Expects unrecognized fields to be dynamically added as snake_case attributes.
    """
    data = {
        "phoneNumber": "+12025550134",
        "regionCode": "US",
        "type": "MOBILE",
        "capability": ["SMS"],
        "unexpectedField": "unexpectedValue",
        "anotherExtraField": 42,
    }
    response = ActivateNumberResponse(**data)

    # Assert known fields
    assert response.phone_number == "+12025550134"

    # Assert unrecognized fields are dynamically added
    assert response.unexpected_field == "unexpectedValue"
    assert response.another_extra_field == 42
