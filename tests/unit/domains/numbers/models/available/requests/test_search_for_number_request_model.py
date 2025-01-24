import pytest
from pydantic import ValidationError

from sinch.domains.numbers.models.available.requests import CheckNumberAvailabilityRequest


def test_check_number_availability_request_expects_accepts_snake_case_input():
    """
    Test that the model accepts snake_case input when allow_population_by_field_name is True.
    """
    request = CheckNumberAvailabilityRequest(phone_number="+1234567890")

    assert request.phone_number == "+1234567890"


def test_check_number_availability_request_expects_accepts_camel_case_input():
    """
    Test that the model accepts snake_case input when allow_population_by_field_name is True.
    """
    request = CheckNumberAvailabilityRequest(phoneNumber="+1234567890")

    assert request.phone_number == "+1234567890"


def test_check_number_availability_request_expects_alias_mapping_correct():
    """
    Test that the model correctly handles alias mappings for phoneNumber.
    """
    request = CheckNumberAvailabilityRequest(phoneNumber="+1234567890")

    assert request.dict(by_alias=True)["phoneNumber"] == "+1234567890"
    assert request.dict(by_alias=False)["phone_number"] == "+1234567890"


def test_search_number_request_expects_validation_error_for_missing_field():
    """
    Test that the model raises a ValidationError when a required field is missing.
    """
    data = {}

    with pytest.raises(ValidationError) as excinfo:
        CheckNumberAvailabilityRequest(**data)

    # Verify the error contains information about the missing 'phoneNumber' field
    assert "field required" in str(excinfo.value)
    assert "phoneNumber" in str(excinfo.value)