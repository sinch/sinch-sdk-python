import pytest
from unittest.mock import MagicMock
from sinch.domains.numbers.available_numbers import AvailableNumbers
from sinch.domains.numbers.endpoints.available.list_available_numbers import AvailableNumbersEndpoint
from sinch.domains.numbers.endpoints.available.activate_number import ActivateNumberEndpoint
from sinch.domains.numbers.endpoints.available.rent_any_number import RentAnyNumberEndpoint
from sinch.domains.numbers.endpoints.available.search_for_number import SearchForNumberEndpoint

from sinch.domains.numbers.models.available.requests import (
    ListAvailableNumbersRequest,
    ActivateNumberRequest,
    RentAnyNumberRequest,
    CheckNumberAvailabilityRequest,
)
from sinch.domains.numbers.models.available.responses import (
    ListAvailableNumbersResponse,
    ActivateNumberResponse,
    RentAnyNumberResponse,
    CheckNumberAvailabilityResponse,
)
from sinch.domains.numbers.models.available.responses import (
    ListAvailableNumbersResponse,
    Number
)

@pytest.fixture
def mock_sinch():
    """Creates a mocked Sinch client."""
    mock_sinch = MagicMock()
    mock_sinch.configuration.project_id = "test_project_id"
    mock_sinch.configuration.transport.request = MagicMock()
    return mock_sinch


def test_list_available_numbers_expects_valid_request(mock_sinch, mocker):
    """
    Test that the AvailableNumbers.list method sends the correct request
    and handles the response properly.
    """
    # Use construct to create a mock response without Pydantic validation
    mock_response = ListAvailableNumbersResponse(availableNumbers=[])
    mock_sinch.configuration.transport.request.return_value = mock_response

    # Spy on the AvailableNumbersEndpoint to capture calls
    spy_endpoint = mocker.spy(AvailableNumbersEndpoint, "__init__")

    available_numbers = AvailableNumbers(mock_sinch)
    response = available_numbers.list(
        region_code="US",
        number_type="LOCAL",
        capabilities=["SMS", "VOICE"],
        page_size=10,
        number_search_pattern="START"
    )

    # Verify the endpoint's constructor was called with the correct arguments
    spy_endpoint.assert_called_once()
    _, kwargs = spy_endpoint.call_args

    # Validate the kwargs
    assert kwargs["project_id"] == "test_project_id"
    assert kwargs["request_data"] == ListAvailableNumbersRequest(
        region_code="US",
        number_type="LOCAL",
        page_size=10,
        capabilities=["SMS", "VOICE"],
        number_search_pattern="START",
    )

    assert response == mock_response
    mock_sinch.configuration.transport.request.assert_called_once()


def test_activate_number_expects_correct_request(mock_sinch, mocker):
    """
    Test that the AvailableNumbers.activate method sends the correct request
    and handles the response properly.
    """
    mock_response = ActivateNumberResponse.construct()
    mock_sinch.configuration.transport.request.return_value = mock_response

    spy_endpoint = mocker.spy(ActivateNumberEndpoint, "__init__")

    available_numbers = AvailableNumbers(mock_sinch)
    response = available_numbers.activate(phone_number="+1234567890")

    spy_endpoint.assert_called_once()
    _, kwargs = spy_endpoint.call_args
    assert kwargs["project_id"] == "test_project_id"
    assert kwargs["request_data"] == ActivateNumberRequest(phone_number="+1234567890")

    assert response == mock_response


def test_rent_any_number_expects_correct_request(mock_sinch, mocker):
    """
    Test that the AvailableNumbers.rent_any method sends the correct request
    and handles the response properly.
    """
    mock_response = RentAnyNumberResponse.construct()
    mock_sinch.configuration.transport.request.return_value = mock_response

    spy_endpoint = mocker.spy(RentAnyNumberEndpoint, "__init__")

    available_numbers = AvailableNumbers(mock_sinch)
    response = available_numbers.rent_any(
        region_code="US",
        type_="LOCAL",
        capabilities=["SMS", "VOICE"]
    )

    spy_endpoint.assert_called_once()
    _, kwargs = spy_endpoint.call_args
    assert kwargs["project_id"] == "test_project_id"
    assert kwargs["request_data"] == RentAnyNumberRequest(
        region_code="US",
        type_="LOCAL",
        capabilities=["SMS", "VOICE"]
    )

    assert response == mock_response


def test_check_availability_expects_correct_request(mock_sinch, mocker):
    """
    Test that the AvailableNumbers.check_availability method sends the correct request
    and handles the response properly.
    """
    mock_response = CheckNumberAvailabilityResponse.construct()
    mock_sinch.configuration.transport.request.return_value = mock_response

    spy_endpoint = mocker.spy(SearchForNumberEndpoint, "__init__")

    available_numbers = AvailableNumbers(mock_sinch)
    response = available_numbers.check_availability(phone_number="+1234567890")

    spy_endpoint.assert_called_once()
    _, kwargs = spy_endpoint.call_args
    assert kwargs["project_id"] == "test_project_id"
    assert kwargs["request_data"] == CheckNumberAvailabilityRequest(phone_number="+1234567890")

    assert response == mock_response