from sinch.core.pagination import TokenBasedPaginator
from sinch.domains.numbers.api.v1 import AvailableRegions
from sinch.domains.numbers.api.v1.internal import ListAvailableRegionsEndpoint
from sinch.domains.numbers.models.v1.internal import (
    ListAvailableRegionsRequest, ListAvailableRegionsResponse,
)


def test_list_available_regions_expects_valid_request(mock_sinch_client_numbers, mocker):
    """
    Test that the AvailableRegions.list() method sends the correct request
    and handles the response properly.
    """
    mock_response = ListAvailableRegionsResponse(availableRegions=[])
    mock_sinch_client_numbers.configuration.transport.request.return_value = mock_response

    spy_endpoint = mocker.spy(ListAvailableRegionsEndpoint, "__init__")

    available_regions = AvailableRegions(mock_sinch_client_numbers)
    response = available_regions.list(
        types=["MOBILE", "LOCAL", "TOLL_FREE"]
    )

    spy_endpoint.assert_called_once()
    _, kwargs = spy_endpoint.call_args

    assert kwargs["project_id"] == "test_project_id"
    assert kwargs["request_data"] == ListAvailableRegionsRequest(
        types=["MOBILE", "LOCAL", "TOLL_FREE"]
    )

    assert isinstance(response, TokenBasedPaginator)
    assert hasattr(response, 'has_next_page')
    assert response.result == mock_response
    mock_sinch_client_numbers.configuration.transport.request.assert_called_once()
