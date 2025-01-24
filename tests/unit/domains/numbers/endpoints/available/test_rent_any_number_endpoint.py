import pytest
import json
from sinch.core.models.http_response import HTTPResponse
from sinch.domains.numbers.available_numbers import RentAnyNumberEndpoint
from sinch.domains.numbers.models.available.requests import RentAnyNumberRequest
from sinch.domains.numbers.models.available.responses import RentAnyNumberResponse


@pytest.fixture
def mock_sinch_client():
    class MockConfiguration:
        numbers_origin = "https://api.sinch.com"

    class MockSinchClient:
        configuration = MockConfiguration()

    return MockSinchClient()


@pytest.fixture
def valid_request_data():
    """
    Provides valid mock request data for RentAnyNumberRequest.
    """
    return RentAnyNumberRequest(
        region_code="US",
        type_="MOBILE",
        number_pattern={"pattern": "string", "searchPattern": "START"},
        capabilities=["SMS"],
        sms_configuration={"servicePlanId": "string", "campaignId": "string"},
        voice_configuration={"appId": "string"},
        callback_url="https://www.your-callback-server.com/callback",
    )


@pytest.fixture
def valid_response_data():
    """
    Provides valid mock response data for RentAnyNumberResponse.
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


def test_build_url_expects_correct_format(mock_sinch_client, valid_request_data):
    """
    Test that the build_url method constructs the URL correctly.
    """
    endpoint = RentAnyNumberEndpoint(project_id="test_project", request_data=valid_request_data)
    expected_url = "https://api.sinch.com/v1/projects/test_project/availableNumbers:rentAny"
    assert endpoint.build_url(mock_sinch_client) == expected_url


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
    mock_response = HTTPResponse(status_code=200, body=valid_response_data,
                                 headers="Content-Type:application/json")

    endpoint = RentAnyNumberEndpoint(project_id="test_project", request_data=None)
    response = endpoint.handle_response(mock_response)

    # Validate response fields
    assert isinstance(response, RentAnyNumberResponse)
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
        "app_id": "string"
    }
    assert response.callback_url == "https://www.your-callback-server.com/callback"
