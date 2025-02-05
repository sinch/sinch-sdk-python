import pytest
from sinch.domains.numbers.endpoints.available.search_for_number_endpoint import SearchForNumberEndpoint
from sinch.domains.numbers.models.available.check_number_availability_response import CheckNumberAvailabilityResponse
from sinch.domains.numbers.models.available.check_number_availability_request import CheckNumberAvailabilityRequest
from sinch.core.models.http_response import HTTPResponse


@pytest.fixture
def mock_sinch_client():
    """
    Mock the Sinch client with configuration.
    """
    class MockConfiguration:
        numbers_origin = "https://api.sinch.com"

    class MockSinchClient:
        configuration = MockConfiguration()

    return MockSinchClient()


@pytest.fixture
def mock_request_data():
    """
    Mock the request data for the endpoint.
    """
    return CheckNumberAvailabilityRequest(phone_number="+1234567890")


@pytest.fixture
def mock_response():
    """
    Mock the HTTP response object returned by the API.
    """
    return HTTPResponse(
        status_code=200,
        body={
              "phoneNumber": "+1234567890",
              "regionCode": "US",
              "type": "MOBILE",
              "capability": [
                "SMS",
                "VOICE"
              ],
              "setupPrice": {
                "currencyCode": "USD",
                "amount": "2.00"
              },
              "monthlyPrice": {
                "currencyCode": "USD",
                "amount": "2.00"
              },
              "paymentIntervalMonths": 0,
              "supportingDocumentationRequired": True
            },
        headers={"Content-Type": "application/json"}
    )


def test_build_url_expects_correct_url(mock_sinch_client, mock_request_data):
    """
    Check if endpoint URL is constructed correctly based on input data.
    """
    endpoint = SearchForNumberEndpoint(project_id="test_project", request_data=mock_request_data)
    expected_url = "https://api.sinch.com/v1/projects/test_project/availableNumbers/+1234567890"
    assert endpoint.build_url(mock_sinch_client) == expected_url


def test_handle_response_expects_correct_mapping(mock_request_data, mock_response):
    """
    Check if response is handled and mapped to the appropriate fields correctly.
    """
    endpoint = SearchForNumberEndpoint(project_id="test_project", request_data=mock_request_data)
    response = endpoint.handle_response(mock_response)

    assert isinstance(response, CheckNumberAvailabilityResponse)
    assert response.phone_number == "+1234567890"
    assert response.region_code == "US"
    assert response.type == "MOBILE"
    assert response.capability == ["SMS", "VOICE"]
    assert response.setup_price.currency_code == "USD"
    assert response.setup_price.amount == 2.00
    assert response.monthly_price.currency_code == "USD"
    assert response.monthly_price.amount == 2.00
    assert response.payment_interval_months == 0
    assert response.supporting_documentation_required is True


def test_handle_response_expects_missing_fields(mock_response):
    """
    Check if response handles missing fields by excluding them without failure.
    """
    mock_response.body.pop("paymentIntervalMonths")
    endpoint = SearchForNumberEndpoint(project_id="test_project", request_data=None)
    response = endpoint.handle_response(mock_response)

    assert response.phone_number == "+1234567890"
    assert response.region_code == "US"
    assert response.type == "MOBILE"
    assert response.capability == ["SMS", "VOICE"]
    assert response.monthly_price.currency_code == "USD"
    assert response.monthly_price.amount == 2.00
    assert response.supporting_documentation_required is True
    assert response.payment_interval_months is None
