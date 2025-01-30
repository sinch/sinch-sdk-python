import pytest
from sinch.domains.numbers.endpoints.available.activate_number import ActivateNumberEndpoint
from sinch.domains.numbers.models.available.activate_number_request import ActivateNumberRequest
from sinch.core.models.http_response import HTTPResponse


@pytest.fixture
def mock_sinch_client():
    class MockConfiguration:
        numbers_origin = "https://api.sinch.com"

    class MockSinchClient:
        configuration = MockConfiguration()

    return MockSinchClient()


@pytest.fixture
def mock_request_data():
    return ActivateNumberRequest(phone_number="+1234567890")


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


def test_build_url_expects_correct_url(mock_sinch_client, mock_request_data):
    """
    Check if endpoint URL is constructed correctly based on input data.
    """
    endpoint = ActivateNumberEndpoint(project_id="test_project", request_data=mock_request_data)
    expected_url = "https://api.sinch.com/v1/projects/test_project/availableNumbers/+1234567890:rent"
    assert endpoint.build_url(mock_sinch_client) == expected_url


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
