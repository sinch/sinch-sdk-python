import pytest
from sinch.domains.numbers.endpoints.active.list_active_numbers_endpoint import ListActiveNumbersEndpoint
from sinch.domains.numbers.models.active.list_active_numbers_request import ListActiveNumbersRequest
from sinch.domains.numbers.models.active.list_active_numbers_response import ListActiveNumbersResponse
from sinch.core.models.http_response import HTTPResponse

@pytest.fixture
def request_data():
    return ListActiveNumbersRequest(
        region_code="AR",
        number_type="LOCAL",
        page_size=15,
        capabilities=["SMS"],
        number_pattern="123",
        number_search_pattern="STARTS_WITH"
    )

@pytest.fixture
def mock_response():
    return HTTPResponse(
        status_code=200,
        body={
            "activeNumbers": [
               {
                   "phoneNumber": "+1234567890",
                   "projectId": "37b62a7b-0177-429a-bb0b-e10f848de0b8",
                   "displayName": "",
                   "regionCode": "US",
                   "type": "LOCAL",
                   "capability": ["SMS", "VOICE"],
                   "money": {
                       "currencyCode": "EUR",
                       "amount": "0.80"
                   },
                   "paymentIntervalMonths": 1,
                   "nextChargeDate": "2025-02-28T14:04:26.190127Z",
                   "expireAt": "2025-02-28T14:04:26.190127Z",
                "callbackUrl": "https://yourcallback/numbers"}],
            "nextPageToken": "CgtwaG9uoLnNDQzajQSDCsxMzE1OTA0MzM1OQ==",
            "totalSize": 10
        },
        headers={"Content-Type": "application/json"}
    )

@pytest.fixture
def endpoint(request_data):
    return ListActiveNumbersEndpoint("test_project_id", request_data)

def test_build_url(endpoint, mock_sinch_client):
    assert endpoint.build_url(mock_sinch_client) == "https://api.sinch.com/v1/projects/test_project_id/activeNumbers"

def test_build_query_params_expects_correct_mapping(endpoint):
    """
    Check if Query params is handled and mapped to the appropriate fields correctly.
    """
    expected_params = {
        "regionCode": "AR",
        "type": "LOCAL",
        "pageSize": 15,
        "capabilities": ["SMS"],
        "numberPattern.pattern": "123",
        "numberPattern.searchPattern": "STARTS_WITH"
    }
    assert endpoint.build_query_params() == expected_params

def test_handle_response_expects_correct_mapping(endpoint, mock_response):
    """
    Check if response is handled and mapped to the appropriate fields correctly.
    """
    parsed_response = endpoint.handle_response(mock_response)
    assert isinstance(parsed_response, ListActiveNumbersResponse)
    assert parsed_response.active_numbers[0].phone_number == "+1234567890"
    assert parsed_response.active_numbers[0].project_id == "37b62a7b-0177-429a-bb0b-e10f848de0b8"
    assert parsed_response.active_numbers[0].display_name == ""
