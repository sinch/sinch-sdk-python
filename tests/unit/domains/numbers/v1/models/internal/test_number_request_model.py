import pytest
from pydantic import ValidationError
from sinch.domains.numbers.models.v1.internal import NumberRequest


def test_check_number_availability_request_expects_accepts_snake_case_input():
    """
    Test that the model accepts snake_case input when allow_population_by_field_name is True.
    """
    request = NumberRequest(phone_number="+1234567890")

    assert request.phone_number == "+1234567890"


def test_check_number_availability_request_expects_accepts_camel_case_input():
    """
    Test that the model accepts snake_case input when allow_population_by_field_name is True.
    """
    request = NumberRequest(phoneNumber="+1234567890")

    assert request.phone_number == "+1234567890"


def test_check_number_availability_request_expects_alias_mapping_correct():
    """
    Test that the model correctly handles alias mappings for phoneNumber.
    """
    request = NumberRequest(phoneNumber="+1234567890")

    assert request.model_dump(by_alias=True)["phoneNumber"] == "+1234567890"
    assert request.model_dump(by_alias=False)["phone_number"] == "+1234567890"


def test_search_number_request_expects_validation_error_for_missing_field():
    """
    Test that the model raises a ValidationError when a required field is missing.
    """
    data = {}

    with pytest.raises(ValidationError) as excinfo:
        NumberRequest(**data)

    error_message = str(excinfo.value)

    assert "Field required" in error_message or "field required" in error_message
    assert "phoneNumber" in error_message