import pytest
from sinch.domains.numbers.models.v1.internal import ListAvailableRegionsResponse


@pytest.fixture
def test_data():
    return {
        "availableRegions": [
            {
                "regionCode": "CA",
                "regionName": "Canada",
                "types": ["MOBILE", "LOCAL", "TOLL_FREE"]
            },
            {
                "regionCode": "SE",
                "regionName": "Sweden",
                "types": ["MOBILE", "LOCAL"]
            }
        ]
    }


def test_list_available_regions_response_expects_correct_mapping(test_data):
    """
    Check if response is handled and mapped to the appropriate fields correctly.
    """
    response = ListAvailableRegionsResponse(**test_data)
    assert hasattr(response, "content")
    assert response.content == response.available_regions

    region = response.available_regions[0]
    assert region.region_code == "CA"
    assert region.region_name == "Canada"
    assert len(region.types) == 3

    region = response.available_regions[1]
    assert region.region_code == "SE"
    assert region.region_name == "Sweden"
    assert len(region.types) == 2


def test_list_available_regions_response_expects_empty_list_handled():
    """
    Expects empty list to be handled correctly.
    """
    response = ListAvailableRegionsResponse(available_regions=[])
    assert response.available_regions == []
    assert response.content == []
