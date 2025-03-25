import pytest
from datetime import datetime, timezone
from pydantic import ValidationError
from sinch.domains.numbers.models.v1.response import RentAnyNumberResponse


@pytest.fixture
def valid_data():
    """
    Provides valid test data for RentAnyNumberResponse.
    """
    return {
        "phoneNumber": "+12025550134",
        "projectId": "51bc3f40-f266-4ca8-8938-a1ed0ff32b9a",
        "displayName": "string",
        "regionCode": "US",
        "type": "MOBILE",
        "capability": ["SMS"],
        "money": {"currencyCode": "USD", "amount": "2.00"},
        "paymentIntervalMonths": 0,
        "nextChargeDate": "2025-01-24T09:32:27.437Z",
        "expireAt": "2025-01-25T09:32:27.437Z",
        "smsConfiguration": {
            "servicePlanId": "string",
            "campaignId": "string",
            "scheduledProvisioning": {
                "servicePlanId": "string",
                "campaignId": "string",
                "status": "PROVISIONING_STATUS_UNSPECIFIED",
                "lastUpdatedTime": "2025-01-24T09:32:27.437Z",
                "errorCodes": ["ERROR_CODE_UNSPECIFIED"],
            },
        },
        "voiceConfiguration": {
            "type": "RTC",
            "lastUpdatedTime": "2025-01-24T09:32:27.437Z",
            "scheduledVoiceProvisioning": {
                "type": "RTC",
                "lastUpdatedTime": "2025-01-24T09:32:27.437Z",
                "status": "PROVISIONING_STATUS_UNSPECIFIED",
                "appId": "string",
            },
            "appId": "string",
        },
        "callbackUrl": "https://www.your-callback-server.com/callback",
    }


def test_rent_any_number_response_expects_valid_data(valid_data):
    """
    Test that RentAnyNumberResponse correctly parses valid data.
    """
    response = RentAnyNumberResponse(**valid_data)

    assert response.phone_number == "+12025550134"
    assert response.project_id == "51bc3f40-f266-4ca8-8938-a1ed0ff32b9a"
    assert response.region_code == "US"
    assert response.type == "MOBILE"
    assert response.capability == ["SMS"]
    assert response.money.currency_code == "USD"
    assert response.money.amount == 2.00
    assert response.payment_interval_months == 0
    expected_next_charge_date = (
        datetime(2025, 1, 24, 9, 32, 27, 437000, tzinfo=timezone.utc)
    )
    assert response.next_charge_date == expected_next_charge_date
    expected_expire_at = (
        datetime(2025, 1, 25, 9, 32, 27, 437000, tzinfo=timezone.utc)
    )
    assert response.expire_at == expected_expire_at

    sms_config = response.sms_configuration
    assert sms_config.service_plan_id == "string"
    assert sms_config.campaign_id == "string"
    assert sms_config.scheduled_provisioning.service_plan_id == "string"
    assert sms_config.scheduled_provisioning.campaign_id == "string"
    assert sms_config.scheduled_provisioning.status == "PROVISIONING_STATUS_UNSPECIFIED"
    expected_last_updated_time = (
        datetime(2025, 1, 24, 9, 32, 27, 437000, tzinfo=timezone.utc))
    assert sms_config.scheduled_provisioning.last_updated_time == expected_last_updated_time
    assert sms_config.scheduled_provisioning.error_codes == ["ERROR_CODE_UNSPECIFIED"]

    voice_config = response.voice_configuration
    assert voice_config.type == "RTC"
    expected_last_updated_time = (
        datetime(2025, 1, 24, 9, 32, 27, 437000, tzinfo=timezone.utc))
    assert voice_config.last_updated_time == expected_last_updated_time
    scheduled_voice_provisioning = voice_config.scheduled_voice_provisioning
    assert scheduled_voice_provisioning.type == "RTC"
    assert scheduled_voice_provisioning.last_updated_time == expected_last_updated_time
    assert scheduled_voice_provisioning.status == "PROVISIONING_STATUS_UNSPECIFIED"
    assert scheduled_voice_provisioning.app_id == "string"
    assert voice_config.app_id == "string"
    assert response.callback_url == "https://www.your-callback-server.com/callback"


def test_rent_any_number_response_expects_missing_optional_fields():
    """
    Test that RentAnyNumberResponse handles missing optional fields correctly.
    """
    data = {
        "phoneNumber": "+12025550134",
        "projectId": "51bc3f40-f266-4ca8-8938-a1ed0ff32b9a",
        "regionCode": "US",
        "type": "MOBILE",
        "capability": ["SMS"],
        "money": {"currencyCode": "USD", "amount": "2.00"},
        "paymentIntervalMonths": 0,
    }

    response = RentAnyNumberResponse(**data)

    assert response.next_charge_date is None
    assert response.expire_at is None
    assert response.sms_configuration is None
    assert response.voice_configuration is None
    assert response.callback_url is None


def test_rent_any_number_response_expects_validation_error_for_missing_required_fields():
    """
    Test that RentAnyNumberResponse raises a validation error for missing required fields.
    """
    data = {
        "projectId": "51bc3f40-f266-4ca8-8938-a1ed0ff32b9a",
        "regionCode": "US",
        "smsConfiguration": {
            # Missing required field "service_plan_id"
            "campaignId": "string"
        }
    }

    with pytest.raises(ValidationError) as exc_info:
        RentAnyNumberResponse(**data)
    # Assert the validation error mentions missing fields
    assert "smsConfiguration.servicePlanId" in str(exc_info.value)


def test_rent_any_number_response_expects_ignore_extra_fields():
    """
    Test that RentAnyNumberResponse ignores extra fields.
    """
    data = {
        "phoneNumber": "+12025550134",
        "projectId": "51bc3f40-f266-4ca8-8938-a1ed0ff32b9a",
        "regionCode": "US",
        "type": "MOBILE",
        "capability": ["SMS"],
        "money": {"currency_code": "USD", "amount": "2.00"},
        "paymentIntervalMonths": 0,
        "extraField": "unexpected",
    }

    response = RentAnyNumberResponse(**data)

    # Assert valid fields are parsed correctly
    assert response.phone_number == "+12025550134"
    assert response.project_id == "51bc3f40-f266-4ca8-8938-a1ed0ff32b9a"
    assert response.region_code == "US"
    assert response.extra_field == "unexpected"
