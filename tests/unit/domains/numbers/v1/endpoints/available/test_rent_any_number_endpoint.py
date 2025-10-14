import pytest
import json
from datetime import datetime, timezone
from sinch.core.models.http_response import HTTPResponse
from sinch.domains.numbers.api.v1.internal import RentAnyNumberEndpoint
from sinch.domains.numbers.models.v1.internal import RentAnyNumberRequest
from sinch.domains.numbers.models.v1.response import ActiveNumber


@pytest.fixture
def valid_request_data():
    """
    Provides valid mock request data for RentAnyNumberRequest.
    """
    return RentAnyNumberRequest(
        region_code="US",
        number_type="MOBILE",
        number_pattern={"pattern": "string", "searchPattern": "START"},
        capabilities=["SMS"],
        sms_configuration={"servicePlanId": "string", "campaignId": "string"},
        voice_configuration={"appId": "string"},
        callback_url="https://www.your-callback-server.com/callback",
    )


@pytest.fixture
def valid_response_data():
    """
    Provides valid mock response data for ActiveNumer.
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
                "trunkId": "string",
            },
            "appId": "string",
        },
        "callbackUrl": "https://www.your-callback-server.com/callback",
    }


def test_build_url_expects_correct_format(mock_sinch_client_numbers, valid_request_data):
    """
    Test that the build_url method constructs the URL correctly.
    """
    endpoint = RentAnyNumberEndpoint(project_id="test_project", request_data=valid_request_data)
    expected_url = "https://mock-numbers-api.sinch.com/v1/projects/test_project/availableNumbers:rentAny"
    assert endpoint.build_url(mock_sinch_client_numbers) == expected_url


def test_request_body_expects_correct_json(valid_request_data):
    """
    Test that the request_body method returns the correct JSON structure.
    """
    endpoint = RentAnyNumberEndpoint(project_id="test_project", request_data=valid_request_data)
    request_body = endpoint.request_body()

    expected_body = {
        "numberPattern": {"pattern": "string", "searchPattern": "START"},
        "regionCode": "US",
        "type": "MOBILE",
        "capabilities": ["SMS"],
        "smsConfiguration": {"servicePlanId": "string", "campaignId": "string"},
        "voiceConfiguration": {"appId": "string"},
        "callbackUrl": "https://www.your-callback-server.com/callback",
    }

    assert json.loads(request_body) == expected_body


def test_handle_response_expects_valid_mapping(valid_response_data):
    """
    Test that the handle_response method correctly maps the response data.
    """
    mock_response = HTTPResponse(status_code=200, body=valid_response_data, headers="Content-Type:application/json")

    endpoint = RentAnyNumberEndpoint(project_id="test_project", request_data=None)
    response = endpoint.handle_response(mock_response)

    # Validate response fields
    assert isinstance(response, ActiveNumber)
    assert response.phone_number == "+12025550134"
    assert response.project_id == "51bc3f40-f266-4ca8-8938-a1ed0ff32b9a"
    assert response.region_code == "US"
    assert response.type == "MOBILE"
    assert response.capability == ["SMS"]
    assert response.money.currency_code == "USD"
    assert response.money.amount == 2.00
    assert response.payment_interval_months == 0
    expected_next_charge_date = datetime(2025, 1, 24, 9, 32, 27, 437000, tzinfo=timezone.utc)
    assert response.next_charge_date == expected_next_charge_date
    expected_expire_at = datetime(2025, 1, 25, 9, 32, 27, 437000, tzinfo=timezone.utc)
    assert response.expire_at == expected_expire_at

    sms_config = response.sms_configuration
    assert sms_config.service_plan_id == "string"
    assert sms_config.campaign_id == "string"
    assert sms_config.scheduled_provisioning.service_plan_id == "string"
    assert sms_config.scheduled_provisioning.campaign_id == "string"
    assert sms_config.scheduled_provisioning.status == "PROVISIONING_STATUS_UNSPECIFIED"
    expected_last_updated_time = datetime(2025, 1, 24, 9, 32, 27, 437000, tzinfo=timezone.utc)
    assert sms_config.scheduled_provisioning.last_updated_time == expected_last_updated_time
    assert sms_config.scheduled_provisioning.error_codes == ["ERROR_CODE_UNSPECIFIED"]

    voice_config = response.voice_configuration
    assert voice_config.type == "RTC"
    assert voice_config.last_updated_time == expected_last_updated_time
    assert voice_config.scheduled_voice_provisioning.type == "RTC"
    assert voice_config.scheduled_voice_provisioning.last_updated_time == expected_last_updated_time
    assert voice_config.scheduled_voice_provisioning.status == "PROVISIONING_STATUS_UNSPECIFIED"
    assert voice_config.scheduled_voice_provisioning.trunk_id == "string"
    assert voice_config.app_id == "string"
    assert response.callback_url == "https://www.your-callback-server.com/callback"
