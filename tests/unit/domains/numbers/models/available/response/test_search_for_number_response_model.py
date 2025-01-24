import pytest
from pydantic import ValidationError
from sinch.domains.numbers.models.available.responses import CheckNumberAvailabilityResponse

def test_check_number_availability_response_expects_valid_data():
    """
    Excpects CheckNumberAvailabilityResponse to be created with valid data.
    """
    data = {
        "phoneNumber": "+1234567890",
        "regionCode": "US",
        "type": "MOBILE",
        "capability": ["SMS", "VOICE"],
        "setupPrice": {"amount": "10.00", "currency": "USD"},
        "monthlyPrice": {"amount": "5.00", "currency": "USD"},
        "paymentIntervalMonths": 1,
        "supportingDocumentationRequired": True
    }

    response = CheckNumberAvailabilityResponse(**data)

    assert response.phone_number == "+1234567890"
    assert response.region_code == "US"
    assert response.type == "MOBILE"
    assert response.capability == ["SMS", "VOICE"]
    assert response.setup_price == {"amount": "10.00", "currency": "USD"}
    assert response.monthly_price == {"amount": "5.00", "currency": "USD"}
    assert response.payment_interval_months == 1
    assert response.supporting_documentation_required is True

def test_check_number_availability_response_missing_optional_fields_expects_valid_data():
    """
    Verifies CheckNumberAvailabilityResponse can be created with missing optional fields,
    and doesn't include them in the response.
    """
    data = {
        "phoneNumber": "+1234567890",
        "regionCode": "US",
        "type": "MOBILE",
        "capability": ["SMS", "VOICE"],
        "setupPrice": {"amount": "10.00", "currency": "USD"},
        "monthlyPrice": {"amount": "5.00", "currency": "USD"}
    }

    response = CheckNumberAvailabilityResponse(**data)

    assert response.phone_number == "+1234567890"
    assert response.region_code == "US"
    assert response.type == "MOBILE"
    assert response.capability == ["SMS", "VOICE"]
    assert response.setup_price == {"amount": "10.00", "currency": "USD"}
    assert response.monthly_price == {"amount": "5.00", "currency": "USD"}
    assert response.payment_interval_months is None
    assert response.supporting_documentation_required is None

def test_check_number_availability_response_expects_validation_error_for_invalid_data():
    """
    Test CheckNumberAvailabilityResponse with invalid data.
    """
    data = {
        "phoneNumber": "+1234567890",
        "regionCode": "US",
        "type": "INVALID_TYPE",
        "capability": ["SMS", "VOICE"],
        "setupPrice": {"amount": "10.00", "currency": "USD"},
        "monthlyPrice": {"amount": "5.00", "currency": "USD"}
    }

    with pytest.raises(ValidationError):
        CheckNumberAvailabilityResponse(**data)

def test_check_number_availability_response_expects_validation_error_for_missing_required_fields():
    data = {
        "phoneNumber": "+1234567890",
        "regionCode": "US",
        "capability": ["SMS", "VOICE"],
        "setupPrice": {"amount": "10.00", "currency": "USD"},
        "monthlyPrice": {"amount": "5.00", "currency": "USD"}
    }

    with pytest.raises(ValidationError):
        CheckNumberAvailabilityResponse(**data)