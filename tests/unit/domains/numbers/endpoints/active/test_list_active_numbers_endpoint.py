from datetime import datetime, timezone
from decimal import Decimal

import pytest
from sinch.domains.numbers.endpoints.active.list_active_numbers_endpoint import ListActiveNumbersEndpoint
from sinch.domains.numbers.models.active.list_active_numbers_request import ListActiveNumbersRequest
from sinch.domains.numbers.models.active.list_active_numbers_response import ListActiveNumbersResponse
from sinch.core.models.http_response import HTTPResponse

@pytest.fixture
def request_data():
    return ListActiveNumbersRequest(
        region_code="US",
        number_type="LOCAL",
        page_size=15,
        capabilities=["SMS", "VOICE"],
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
                   "callbackUrl": "https://yourcallback/numbers"
               }
            ],
            "nextPageToken": "CgtwaG9uoLnNDQzajQSDCsxMzE1OTA0MzM1OQ==",
            "totalSize": 10
        },
        headers={"Content-Type": "application/json"}
    )

@pytest.fixture
def endpoint(request_data):
    return ListActiveNumbersEndpoint("test_project_id", request_data)

def test_build_url(endpoint, mock_sinch_client_numbers):
    assert (endpoint.build_url(mock_sinch_client_numbers) ==
            "https://mock-numbers-api.sinch.com/v1/projects/test_project_id/activeNumbers")

def test_build_query_params_expects_correct_mapping(endpoint):
    """
    Check if Query params is handled and mapped to the appropriate fields correctly.
    """
    expected_params = {
        "regionCode": "US",
        "type": "LOCAL",
        "pageSize": 15,
        "capabilities": ["SMS", "VOICE"],
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
    assert parsed_response.active_numbers[0].region_code == "US"
    assert parsed_response.active_numbers[0].type == "LOCAL"
    assert parsed_response.active_numbers[0].capability == ["SMS", "VOICE"]
    assert parsed_response.active_numbers[0].money.currency_code == "EUR"
    assert parsed_response.active_numbers[0].money.amount == Decimal("0.80")
    assert parsed_response.active_numbers[0].payment_interval_months == 1
    expected_next_charge_date = (
        datetime(2025, 2, 28, 14, 4, 26, 190127, tzinfo=timezone.utc))
    assert parsed_response.active_numbers[0].next_charge_date == expected_next_charge_date
    expected_expire_at = (
        datetime(2025, 2, 28, 14, 4, 26, 190127, tzinfo=timezone.utc))
    assert parsed_response.active_numbers[0].expire_at == expected_expire_at
    assert parsed_response.active_numbers[0].callback_url == "https://yourcallback/numbers"
    assert parsed_response.next_page_token == "CgtwaG9uoLnNDQzajQSDCsxMzE1OTA0MzM1OQ=="
    assert parsed_response.total_size == 10
