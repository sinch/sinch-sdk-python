from decimal import Decimal
import pytest
from sinch.core.models.http_response import HTTPResponse
from sinch.domains.numbers.api.v1.internal import AvailableNumbersEndpoint
from sinch.domains.numbers.models.v1.internal import ListAvailableNumbersRequest, ListAvailableNumbersResponse


@pytest.fixture
def request_data():
    return ListAvailableNumbersRequest(
        region_code="US",
        number_type="MOBILE",
        page_size=10,
        capabilities=["SMS"],
        number_pattern="123",
        number_search_pattern="STARTS_WITH",
        extra_field="extra value",
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
                    "capability": ["SMS", "VOICE"],
                    "setupPrice": {"currencyCode": "EUR", "amount": "0.80"},
                    "monthlyPrice": {"currencyCode": "EUR", "amount": "0.85"},
                    "paymentIntervalMonths": 1,
                    "supportingDocumentationRequired": True,
                },
                {
                    "phoneNumber": "+13456789012",
                    "regionCode": "US",
                    "type": "LOCAL",
                    "capability": ["SMS", "VOICE"],
                    "setupPrice": {"currencyCode": "EUR", "amount": "0.80"},
                    "monthlyPrice": {"currencyCode": "EUR", "amount": "1.00"},
                    "paymentIntervalMonths": 2,
                    "supportingDocumentationRequired": True,
                },
            ],
        },
        headers={"Content-Type": "application/json"},
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
        "extraField": "extra value",
    }
    assert endpoint.build_query_params() == expected_params


def test_handle_response_expects_correct_mapping(endpoint, mock_response):
    """
    Check if response is handled and mapped to the appropriate fields correctly.
    """
    parsed_response = endpoint.handle_response(mock_response)
    assert isinstance(parsed_response, ListAvailableNumbersResponse)
    assert hasattr(parsed_response, "content")
    assert parsed_response.content == parsed_response.available_numbers
    assert len(parsed_response.available_numbers) == 2

    first_number = parsed_response.available_numbers[0]
    assert first_number.phone_number == "+1234567890"
    assert first_number.region_code == "US"
    assert first_number.type == "LOCAL"
    assert first_number.capability == ["SMS", "VOICE"]
    assert first_number.setup_price.currency_code == "EUR"
    assert first_number.setup_price.amount == Decimal("0.80")
    assert first_number.monthly_price.currency_code == "EUR"
    assert first_number.monthly_price.amount == Decimal("0.85")
    assert first_number.payment_interval_months == 1
    assert first_number.supporting_documentation_required is True

    second_number = parsed_response.available_numbers[1]
    assert second_number.phone_number == "+13456789012"
    assert second_number.region_code == "US"
    assert second_number.type == "LOCAL"
    assert second_number.capability == ["SMS", "VOICE"]
    assert second_number.setup_price.currency_code == "EUR"
    assert second_number.setup_price.amount == Decimal("0.80")
    assert second_number.monthly_price.currency_code == "EUR"
    assert second_number.monthly_price.amount == 1.00
    assert second_number.payment_interval_months == 2
    assert second_number.supporting_documentation_required is True
