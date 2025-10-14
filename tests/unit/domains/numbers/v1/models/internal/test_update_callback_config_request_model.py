import pytest
from pydantic import ValidationError
from sinch.domains.numbers.models.v1.internal import UpdateCallbackConfigurationRequest


def test_update_numbers_callback_config_request_expects_parsed_input():
    """
    Test that the model correctly handles valid input.
    """
    data = {"hmacSecret": "test-secret-key"}
    request = UpdateCallbackConfigurationRequest(**data)
    assert request.hmac_secret == "test-secret-key"


def test_update_numbers_callback_request_expects_validation_for_extra_type():
    """
    Test that validation errors are raised for invalid number types.
    """
    data = {"extra": "Extra Value"}
    request = UpdateCallbackConfigurationRequest(**data)
    assert request.extra == "Extra Value"


def test_update_numbers_callback_config_request_expects_optional_field_handled():
    """
    Test that hmac_secret is optional and can be None.
    """
    data = {}
    request = UpdateCallbackConfigurationRequest(**data)
    assert request.hmac_secret is None


def test_update_numbers_callback_config_request_expects_validation_error():
    """
    Test that the model raises a validation error for invalid hmac_secret type.
    """
    data = {"hmacSecret": 12345}
    with pytest.raises(ValidationError):
        UpdateCallbackConfigurationRequest(**data)
