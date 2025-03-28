import pytest
from sinch.domains.numbers.api.v1.internal.available_regions_endpoints import ListAvailableRegionsEndpoint
from sinch.domains.numbers.models.v1.internal import ListAvailableRegionsRequest, ListAvailableRegionsResponse
from sinch.core.models.http_response import HTTPResponse


@pytest.fixture
def request_data():
    return ListAvailableRegionsRequest(
        types=["LOCAL", "MOBILE"]
    )


@pytest.fixture
def mock_response():
    return HTTPResponse(
        status_code=200,
        body={
            "availableRegions": [
                {
                    "regionCode": "US",
                    "regionName": "United States",
                    "types": ["LOCAL", "MOBILE", "TOLL_FREE"]
                },
                {
                    "regionCode": "SE",
                    "regionName": "Sweden",
                    "types": ["LOCAL", "MOBILE"]
                }
            ]
        },
        headers={"Content-Type": "application/json"}
    )


@pytest.fixture
def endpoint(request_data):
    return ListAvailableRegionsEndpoint("test_project_id", request_data)


def test_build_url(endpoint, mock_sinch_client_numbers):
    assert (endpoint.build_url(mock_sinch_client_numbers) ==
            "https://mock-numbers-api.sinch.com/v1/projects/test_project_id/availableRegions")


def test_build_query_params_expects_correct_mapping(endpoint):
    """
    Check if Query params is handled and mapped to the appropriate fields correctly.
    """
    expected_params = {
        "types": ["LOCAL", "MOBILE"]
    }
    assert endpoint.build_query_params() == expected_params


def test_handle_response_expects_correct_mapping(endpoint, mock_response):
    """
    Check if response is handled and mapped to the appropriate fields correctly.
    """
    parsed_response = endpoint.handle_response(mock_response)
    assert isinstance(parsed_response, ListAvailableRegionsResponse)
    assert hasattr(parsed_response, "available_regions")
    assert len(parsed_response.available_regions) == 2

    region = parsed_response.available_regions[0]
    assert region.region_code == "US"
    assert region.region_name == "United States"
    assert len(region.types) == 3

    region = parsed_response.available_regions[1]
    assert region.region_code == "SE"
    assert region.region_name == "Sweden"
    assert len(region.types) == 2
