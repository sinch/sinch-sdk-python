import pytest
from datetime import datetime, timezone
from decimal import Decimal
from sinch.core.models.http_response import HTTPResponse
from sinch.domains.numbers.api.v1.internal import GetNumberConfigurationEndpoint
from sinch.domains.numbers.models.v1.internal import NumberRequest
from sinch.domains.numbers.models.v1.response import ActiveNumber


@pytest.fixture
def request_data():
    return NumberRequest(phone_number="+1234567890")


@pytest.fixture
def mock_response():
    return HTTPResponse(
        status_code=200,
        body={
            "phoneNumber": "+1234567890",
            "projectId": "51bc3f40-f266-4ca8-8938-a1ed0ff32b9a",
            "displayName": "",
            "regionCode": "US",
            "type": "LOCAL",
            "capability": ["SMS", "VOICE"],
            "money": {"currencyCode": "EUR", "amount": "0.80"},
            "paymentIntervalMonths": 1,
            "nextChargeDate": "2025-02-28T14:04:26.190127Z",
            "expireAt": "2025-02-28T14:04:26.190127Z",
            "callbackUrl": "https://yourcallback/numbers",
        },
        headers={"Content-Type": "application/json"},
    )


@pytest.fixture
def endpoint(request_data):
    return GetNumberConfigurationEndpoint("test_project_id", request_data)


def test_build_url(endpoint, mock_sinch_client_numbers):
    assert (
        endpoint.build_url(mock_sinch_client_numbers)
        == "https://mock-numbers-api.sinch.com/v1/projects/test_project_id/activeNumbers/+1234567890"
    )


def test_handle_response_expects_correct_mapping(endpoint, mock_response):
    """
    Check if response is handled and mapped to the appropriate fields correctly.
    """
    parsed_response = endpoint.handle_response(mock_response)
    assert isinstance(parsed_response, ActiveNumber)
    assert parsed_response.phone_number == "+1234567890"
    assert parsed_response.project_id == "51bc3f40-f266-4ca8-8938-a1ed0ff32b9a"
    assert parsed_response.display_name == ""
    assert parsed_response.region_code == "US"
    assert parsed_response.type == "LOCAL"
    assert parsed_response.capability == ["SMS", "VOICE"]
    assert parsed_response.money.currency_code == "EUR"
    assert parsed_response.money.amount == Decimal("0.80")
    assert parsed_response.payment_interval_months == 1
    expected_next_charge_date = datetime(2025, 2, 28, 14, 4, 26, 190127, tzinfo=timezone.utc)
    assert parsed_response.next_charge_date == expected_next_charge_date
    expected_expire_at = datetime(2025, 2, 28, 14, 4, 26, 190127, tzinfo=timezone.utc)
    assert parsed_response.expire_at == expected_expire_at
    assert parsed_response.callback_url == "https://yourcallback/numbers"
