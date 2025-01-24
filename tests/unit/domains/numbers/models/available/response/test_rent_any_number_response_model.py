import pytest
from pydantic import ValidationError
from sinch.domains.numbers.models.available.responses import RentAnyNumberResponse

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
        "expireAt": "2025-01-24T09:32:27.437Z",
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
            "lastUpdatedTime": "2025-01-24T09:32:27.437Z",
            "scheduledVoiceProvisioning": {
                "type": "RTC",
                "lastUpdatedTime": "2025-01-24T09:32:27.437Z",
                "status": "PROVISIONING_STATUS_UNSPECIFIED",
                "trunkId": "string",
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
    assert response.money == {"currency_code": "USD", "amount": "2.00"}
    assert response.payment_interval_months == 0
    assert response.next_charge_date == "2025-01-24T09:32:27.437Z"
    assert response.expire_at == "2025-01-24T09:32:27.437Z"
    assert response.sms_configuration == {
        "service_plan_id": "string",
        "campaign_id": "string",
        "scheduled_provisioning": {
            "service_plan_id": "string",
            "campaign_id": "string",
            "status": "PROVISIONING_STATUS_UNSPECIFIED",
            "last_updated_time": "2025-01-24T09:32:27.437Z",
            "error_codes": ["ERROR_CODE_UNSPECIFIED"],
        },
    }
    assert response.voice_configuration == {
        "last_updated_time": "2025-01-24T09:32:27.437Z",
        "scheduled_voice_provisioning": {
            "type": "RTC",
            "last_updated_time": "2025-01-24T09:32:27.437Z",
            "status": "PROVISIONING_STATUS_UNSPECIFIED",
            "trunk_id": "string",
        },
        "app_id": "string",
    }
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

    assert response.phone_number == "+12025550134"
    assert response.project_id == "51bc3f40-f266-4ca8-8938-a1ed0ff32b9a"
    assert response.region_code == "US"
    assert response.type == "MOBILE"
    assert response.capability == ["SMS"]
    assert response.money == {"currency_code": "USD", "amount": "2.00"}
    assert response.payment_interval_months == 0

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
    }

    with pytest.raises(ValidationError) as exc_info:
        RentAnyNumberResponse(**data)

    # Assert the validation error mentions missing fields
    assert "phoneNumber" in str(exc_info.value)
    assert "capability" in str(exc_info.value)


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

    # Assert extra fields are ignored
    assert not hasattr(response, "extraField")
