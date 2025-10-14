import pytest
from sinch.domains.numbers.models.v1.internal import ListAvailableNumbersResponse


@pytest.fixture
def test_data():
    return {
        "availableNumbers": [
            {
                "phoneNumber": "+12025550134",
                "regionCode": "US",
                "type": "MOBILE",
                "capability": ["SMS", "VOICE"],
                "setupPrice": {"currencyCode": "USD", "amount": "2.00"},
                "monthlyPrice": {"currencyCode": "USD", "amount": "2.00"},
                "paymentIntervalMonths": 0,
                "supportingDocumentationRequired": True,
            }
        ]
    }


def test_list_available_numbers_response_expects_correct_mapping(test_data):
    """
    Check if response is handled and mapped to the appropriate fields correctly.
    """
    response = ListAvailableNumbersResponse(**test_data)
    # Verify content property for pagination compatibility
    assert hasattr(response, "content")
    assert response.content == response.available_numbers

    number = response.content[0]
    assert number.phone_number == "+12025550134"
    assert number.region_code == "US"
    assert number.type == "MOBILE"
    assert number.capability == ["SMS", "VOICE"]
    assert number.setup_price.currency_code == "USD"
    assert number.setup_price.amount == 2.00
    assert number.monthly_price.currency_code == "USD"
    assert number.monthly_price.amount == 2.00
    assert number.payment_interval_months == 0
    assert number.supporting_documentation_required is True
