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
            }
        ]
    }


def test_list_available_numbers_response_expects_correct_mapping(test_data):
    """
    Check if response is handled and mapped to the appropriate fields correctly.
    """
    response = ListAvailableNumbersResponse(**test_data)
    assert response.available_numbers[0].phone_number == "+12025550134"
    assert response.available_numbers[0].region_code == "US"
    assert response.available_numbers[0].type == "MOBILE"
    assert response.available_numbers[0].capability == ["SMS", "VOICE"]
    assert response.available_numbers[0].setup_price.currency_code == "USD"
    assert response.available_numbers[0].setup_price.amount == 2.00
    assert response.available_numbers[0].monthly_price.currency_code == "USD"
    assert response.available_numbers[0].monthly_price.amount == 2.00
    assert response.available_numbers[0].payment_interval_months == 0
    assert response.available_numbers[0].supporting_documentation_required is True
