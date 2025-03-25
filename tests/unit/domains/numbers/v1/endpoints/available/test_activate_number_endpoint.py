import pytest
import json
from sinch.domains.numbers.api.v1.internal import ActivateNumberEndpoint
from sinch.domains.numbers.models.v1.internal import ActivateNumberRequest
from sinch.core.models.http_response import HTTPResponse


@pytest.fixture
def mock_request_data():
    return ActivateNumberRequest(
        phone_number="+1234567890",
        sms_configuration={"servicePlanId": "YOUR_SMS_servicePlanId"},
        voice_configuration={"type": "RTC", "appId": "YOUR_Voice_appId"}
    )


@pytest.fixture
def mock_request_data_snake_case():
    return ActivateNumberRequest(
        phone_number="+1234567890",
        sms_configuration={"service_plan_id": "YOUR_SMS_servicePlanId"},
        voice_configuration={"type": "RTC", "appId": "YOUR_Voice_appId"}
    )


@pytest.fixture
def mock_response():
    return HTTPResponse(
        status_code=200,
        body={
            "phoneNumber": "+1234567890",
            "regionCode": "US",
            "type": "mobile",
            "capability": ["SMS", "Voice"]
        },
        headers={"Content-Type": "application/json"}
    )


@pytest.fixture
def mock_response_body():
    expected_body = {
        "phoneNumber": "+1234567890",
        "smsConfiguration": {
            "servicePlanId": "YOUR_SMS_servicePlanId"
        },
        "voiceConfiguration": {
            "type": "RTC",
            "appId": "YOUR_Voice_appId"
        }
    }
    return json.dumps(expected_body)


def test_build_url_expects_correct_url(mock_sinch_client_numbers, mock_request_data):
    """
    Check if endpoint URL is constructed correctly based on input data.
    """
    endpoint = ActivateNumberEndpoint(project_id="test_project", request_data=mock_request_data)
    expected_url = "https://mock-numbers-api.sinch.com/v1/projects/test_project/availableNumbers/+1234567890:rent"
    assert endpoint.build_url(mock_sinch_client_numbers) == expected_url


def test_request_body_expects_correct_json(mock_request_data, mock_response_body):
    """
    Check if request body is constructed correctly based on input data.
    """
    endpoint = ActivateNumberEndpoint(project_id="test_project", request_data=mock_request_data)
    request_body = endpoint.request_body()
    assert request_body == mock_response_body


def test_request_body_snake_case_dict_expects_correct_json(mock_request_data_snake_case, mock_response_body):
    """
    Check if request body is constructed correctly based on input data.
    """
    endpoint = ActivateNumberEndpoint(project_id="test_project", request_data=mock_request_data_snake_case)
    request_body = endpoint.request_body()

    assert request_body == mock_response_body


def test_handle_response_expects_correct_mapping(mock_request_data, mock_response):
    """
    Check if response is handled and mapped to the appropriate fields correctly.
    """
    endpoint = ActivateNumberEndpoint(project_id="test_project", request_data=mock_request_data)
    response = endpoint.handle_response(mock_response)

    # Verify each field is mapped as expected
    assert response.phone_number == "+1234567890"
    assert response.region_code == "US"
    assert response.type == "mobile"
    assert response.capability == ["SMS", "Voice"]
