import pytest
from sinch.domains.numbers.api.v1.internal import AvailableNumbersEndpoint
from sinch.domains.numbers.models.v1.internal import ListAvailableNumbersRequest
from sinch.core.models.http_response import HTTPResponse

@pytest.fixture
def request_data():
    return ListAvailableNumbersRequest(
        region_code="US",
        number_type="MOBILE",
        page_size=10,
        capabilities=["SMS"],
        number_pattern="123",
        number_search_pattern="STARTS_WITH",
        extra_field="extra value"
    )

@pytest.fixture
def mock_response():
    return HTTPResponse(
        status_code=200,
        body={
            "availableNumbers": [
                {
                    "phoneNumber": "+1234567890",
                    "regionCode": "US",
                    "type": "LOCAL",
                    "capability": [
                        "SMS",
                        "VOICE"
                    ],
                    "setupPrice": {
                        "currencyCode": "EUR",
                        "amount": "0.80"
                    },
                    "monthlyPrice": {
                        "currencyCode": "EUR",
                        "amount": "0.80"
                    },
                    "paymentIntervalMonths": 1,
                    "supportingDocumentationRequired": True
                },
                {
                    "phoneNumber": "+2345678901",
                    "regionCode": "US",
                    "type": "LOCAL",
                    "capability": [
                        "SMS",
                        "VOICE"
                    ],
                    "setupPrice": {
                        "currencyCode": "EUR",
                        "amount": "0.80"
                    },
                    "monthlyPrice": {
                        "currencyCode": "EUR",
                        "amount": "0.80"
                    },
                    "paymentIntervalMonths": 1,
                    "supportingDocumentationRequired": True
                }
            ],
        },
        headers={"Content-Type": "application/json"}
    )

@pytest.fixture
def endpoint(request_data):
    return AvailableNumbersEndpoint("test_project_id", request_data)

def test_build_url(endpoint, mock_sinch_client_numbers):
    """
    Check if endpoint URL is constructed correctly based on input data.
    """
    expected_url = "https://mock-numbers-api.sinch.com/v1/projects/test_project_id/availableNumbers"
    assert endpoint.build_url(mock_sinch_client_numbers) == expected_url

def test_build_query_params_expects_correct_mapping(endpoint):
    """
    Check if Query params is handled and mapped to the appropriate fields correctly.
    """
    expected_params = {
        "regionCode": "US",
        "type": "MOBILE",
        "size": 10,
        "capabilities": ["SMS"],
        "numberPattern.pattern": "123",
        "numberPattern.searchPattern": "STARTS_WITH",
        "extraField": "extra value"
    }
    assert endpoint.build_query_params() == expected_params

def test_handle_response_expects_correct_mapping(endpoint, mock_response):
    """
    Check if response is handled and mapped to the appropriate fields correctly.
    """
    parsed_response = endpoint.handle_response(mock_response)
    assert isinstance(parsed_response, list)
    assert len(parsed_response) == 2
    assert parsed_response[0].phone_number == "+1234567890"
    assert parsed_response[1].phone_number == "+2345678901"