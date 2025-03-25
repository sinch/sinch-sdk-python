import pytest
from pydantic import ValidationError
from sinch.domains.numbers.models.v1.internal import ListAvailableNumbersRequest


def test_list_available_numbers_request_expects_snake_case_input():
    """
    Test that the model correctly handles snake_case input.
    """
    data = {
        "region_code": "US",
        "number_type": "MOBILE",
        "page_size": 10,
        "capabilities": ["SMS", "VOICE"],
        "number_search_pattern": "prefix",
        "number_pattern": "12345"
    }

    # Instantiate the model
    request = ListAvailableNumbersRequest(**data)

    # Assert the field values
    assert request.region_code == "US"
    assert request.number_type == "MOBILE"
    assert request.page_size == 10
    assert request.capabilities == ["SMS", "VOICE"]
    assert request.number_search_pattern == "prefix"
    assert request.number_pattern == "12345"


def test_list_available_numbers_request_expects_camel_case_input():
    """
    Test that the model correctly handles camelCase input.
    """
    data = {
        "regionCode": "US",
        "type": "MOBILE",
        "size": 10,
        "capabilities": ["SMS", "VOICE"],
        "numberPattern.searchPattern": "prefix",
        "numberPattern.pattern": "12345"
    }

    # Instantiate the model
    request = ListAvailableNumbersRequest(**data)

    # Assert the field values
    assert request.region_code == "US"
    assert request.number_type == "MOBILE"
    assert request.page_size == 10
    assert request.capabilities == ["SMS", "VOICE"]
    assert request.number_search_pattern == "prefix"
    assert request.number_pattern == "12345"


def test_list_available_numbers_request_expects_mixed_case_input():
    """
    Test that the model correctly handles mixed camelCase and snake_case input.
    """
    data = {
        "region_code": "US",
        "type": "MOBILE",
        "size": 10,
        "capabilities": ["SMS", "VOICE"],
        "number_search_pattern": "prefix",
        "numberPattern.pattern": "12345"
    }

    # Instantiate the model
    request = ListAvailableNumbersRequest(**data)

    # Assert the field values
    assert request.region_code == "US"
    assert request.number_type == "MOBILE"
    assert request.page_size == 10
    assert request.capabilities == ["SMS", "VOICE"]
    assert request.number_search_pattern == "prefix"
    assert request.number_pattern == "12345"


def test_list_available_numbers_request_expects_validation_error_for_missing_required_field():
    """
    Test that the model raises a validation error for missing required fields.
    """
    data = {
        "number_type": "MOBILE",
        "size": 10,
        "capabilities": ["SMS", "VOICE"]
    }

    with pytest.raises(ValidationError) as exc_info:
        ListAvailableNumbersRequest(**data)

    # Assert the error mentions the missing region_code field
    assert "region_code" in str(exc_info.value) or "regionCode" in str(exc_info.value)


def test_list_available_numbers_expects_parsed_extra_field_snake_case():
    """
    Expects unrecognized fields to be dynamically added as snake_case attributes.
    """
    data = {
        "number_type": "MOBILE",
        "size": 10,
        "region_code": "US",
        "capabilities": ["SMS", "VOICE"],
        "extraField": "Extra Value"
    }
    response = ListAvailableNumbersRequest(**data)

    # Assert known fields
    assert response.extraField == "Extra Value"


def test_list_available_numbers_expects_snake_case_to_parsed_extra_field_snake_case():
    """
    Expects unrecognized fields to be dynamically added as snake_case attributes.
    """
    data = {
        "number_type": "MOBILE",
        "size": 10,
        "region_code": "US",
        "capabilities": ["SMS", "VOICE"],
        "extra_field": "Extra Value"
    }
    response = ListAvailableNumbersRequest(**data)

    # Assert known fields
    assert response.extra_field == "Extra Value"


def test_list_available_numbers_expects_extra_capability():
    """
    Expects unrecognized fields to be dynamically added as snake_case attributes.
    """
    data = {
        "number_type": "MOBILE",
        "size": 10,
        "region_code": "US",
        "capabilities": ["SMS", "VOICE", "EXTRA"],
        "extra_field": "Extra Value"
    }
    response = ListAvailableNumbersRequest(**data)

    # Assert known fields
    assert response.capabilities == ["SMS", "VOICE", "EXTRA"]
