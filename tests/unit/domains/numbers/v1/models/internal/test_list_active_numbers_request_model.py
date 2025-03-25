import pytest
from pydantic import ValidationError
from sinch.domains.numbers.models.v1.internal import ListActiveNumbersRequest


@pytest.mark.parametrize(
    "order_by_input, expected_order_by",
    [
        ("phone_number", "phoneNumber"),
        ("PHONE_NUMBER", "phoneNumber"),
        ("display_name", "displayName"),
        ("DISPLAY_NAME", "displayName"),
        ("new_field", "newField"),
        ("newField", "newField"),
        (None, None)
    ]
)
def test_list_active_numbers_orderby_field_request_expects_camel_case_input(order_by_input, expected_order_by):
    """
    Test that the model correctly parses order_by field.
    """
    data = {
        "region_code": "US",
        "number_type": "MOBILE",
        "order_by": order_by_input
    }

    request = ListActiveNumbersRequest(**data)

    assert request.region_code == "US"
    assert request.number_type == "MOBILE"
    assert request.order_by == expected_order_by


def test_list_active_numbers_request_expects_parsed_input():
    """
    Test that the model correctly parses input.
    """
    data = {
        "region_code": "GB",
        "number_type": "LOCAL",
        "page_size": 5,
        "capabilities": ["SMS", "VOICE"],
        "number_search_pattern": "START",
        "number_pattern": "5678",
        "page_token": "abc123",
        "order_by": "PHONE_NUMBER"
    }

    request = ListActiveNumbersRequest(**data)

    assert request.region_code == "GB"
    assert request.number_type == "LOCAL"
    assert request.page_size == 5
    assert request.capabilities == ["SMS", "VOICE"]
    assert request.number_search_pattern == "START"
    assert request.number_pattern == "5678"
    assert request.page_token == "abc123"
    assert request.order_by == "phoneNumber"


def test_list_available_numbers_request_expects_camel_case_input():
    """
    Test that the model correctly handles camelCase input.
    """
    data = {
        "regionCode": "US",
        "number_type": "MOBILE",
    }
    request = ListActiveNumbersRequest(**data)
    assert request.region_code == "US"
    assert request.number_type == "MOBILE"


def test_list_active_numbers_request_expects_validation_error_for_missing_field():
    """
    Test that missing required fields raise a ValidationError.
    """
    data = {}
    with pytest.raises(ValidationError):
        ListActiveNumbersRequest(**data)
