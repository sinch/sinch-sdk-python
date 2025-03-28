import pytest
from pydantic import ValidationError
from sinch.domains.numbers.models.v1.response import AvailableRegion


@pytest.fixture
def test_data():
    return {
        "regionCode": "US",
        "regionName": "United States",
        "types": ["MOBILE", "LOCAL", "TOLL_FREE"]
    }


def test_available_region_expects_all_fields_mapped_correctly(test_data):
    """
    Expects all fields to map correctly from camelCase input,
    and handles type conversions properly
    """
    response = AvailableRegion(**test_data)

    assert response.region_code == "US"
    assert response.region_name == "United States"
    assert len(response.types) == 3


def test_available_region_expects_validation_error_on_empty_types_list():
    """
    Expects validation error when types list is empty due to min_length=1 constraint
    """
    invalid_data = {
        "regionCode": "US",
        "regionName": "United States",
        "types": []
    }
    with pytest.raises(ValidationError):
        AvailableRegion(**invalid_data)


def test_available_region_expects_validation_error_on_non_string_fields():
    """
    Expects validation error when StrictStr fields receive non-string values
    """
    invalid_data = {
        "regionCode": 123,
        "regionName": "United States",
        "types": ["MOBILE"]
    }
    with pytest.raises(ValidationError):
        AvailableRegion(**invalid_data)
