from sinch.core.pagination import TokenBasedPaginator
from sinch.domains.numbers.api.v1 import ActiveNumbers
from sinch.domains.numbers.api.v1.internal import (
    ListActiveNumbersEndpoint,
    GetNumberConfigurationEndpoint,
    UpdateNumberConfigurationEndpoint,
    ReleaseNumberFromProjectEndpoint,
)
from sinch.domains.numbers.models.v1.internal import (
    ListActiveNumbersRequest,
    ListActiveNumbersResponse,
    NumberRequest,
    UpdateNumberConfigurationRequest,
)
from sinch.domains.numbers.models.v1.response import ActiveNumber


def test_list_active_numbers_expects_valid_request(mock_sinch_client_numbers, mocker):
    """
    Test that the ActiveNumbers.list() method sends the correct request
    and handles the response properly.
    """
    mock_response = ListActiveNumbersResponse(activeNumbers=[])
    mock_sinch_client_numbers.configuration.transport.request.return_value = mock_response

    # Spy on the ActiveNumbersEndpoint to capture calls
    spy_endpoint = mocker.spy(ListActiveNumbersEndpoint, "__init__")

    active_numbers = ActiveNumbers(mock_sinch_client_numbers)
    response = active_numbers.list(
        region_code="US",
        number_type="LOCAL",
        capabilities=["SMS", "VOICE"],
        page_size=10,
        number_search_pattern="START",
    )

    spy_endpoint.assert_called_once()
    _, kwargs = spy_endpoint.call_args

    assert kwargs["project_id"] == "test_project_id"
    assert kwargs["request_data"] == ListActiveNumbersRequest(
        region_code="US",
        number_type="LOCAL",
        page_size=10,
        capabilities=["SMS", "VOICE"],
        number_search_pattern="START",
    )

    assert isinstance(response, TokenBasedPaginator)
    assert hasattr(response, "has_next_page")
    assert response.result == mock_response
    mock_sinch_client_numbers.configuration.transport.request.assert_called_once()


def test_check_availability_expects_correct_request(mock_sinch_client_numbers, mocker):
    """
    Test that the ActiveNumbers.get() method sends the correct request
    and handles the response properly.
    """
    mock_response = ActiveNumber.model_construct()
    mock_sinch_client_numbers.configuration.transport.request.return_value = mock_response

    spy_endpoint = mocker.spy(GetNumberConfigurationEndpoint, "__init__")

    active_numbers = ActiveNumbers(mock_sinch_client_numbers)
    response = active_numbers.get(phone_number="+1234567890")

    spy_endpoint.assert_called_once()
    _, kwargs = spy_endpoint.call_args
    assert kwargs["project_id"] == "test_project_id"
    assert kwargs["request_data"] == NumberRequest(phone_number="+1234567890")

    assert response == mock_response


def test_release_active_numbers_expects_valid_request(mock_sinch_client_numbers, mocker):
    """
    Test that the ActiveNumbers.update() method sends the correct request
    and handles the response properly.
    """
    mock_response = ActiveNumber.model_construct()
    mock_sinch_client_numbers.configuration.transport.request.return_value = mock_response

    spy_endpoint = mocker.spy(ReleaseNumberFromProjectEndpoint, "__init__")

    active_numbers = ActiveNumbers(mock_sinch_client_numbers)
    response = active_numbers.release(
        phone_number="+1234567890",
    )

    spy_endpoint.assert_called_once()
    _, kwargs = spy_endpoint.call_args
    assert kwargs["project_id"] == "test_project_id"
    assert kwargs["request_data"] == NumberRequest(
        phone_number="+1234567890",
    )

    assert response == mock_response


def test_update_active_numbers_expects_valid_request(mock_sinch_client_numbers, mocker):
    """
    Test that the ActiveNumbers.update() method sends the correct request
    and handles the response properly.
    """
    mock_response = ActiveNumber.model_construct()
    mock_sinch_client_numbers.configuration.transport.request.return_value = mock_response

    spy_endpoint = mocker.spy(UpdateNumberConfigurationEndpoint, "__init__")

    active_numbers = ActiveNumbers(mock_sinch_client_numbers)
    response = active_numbers.update(phone_number="+1234567890", display_name="Test Display Name")

    spy_endpoint.assert_called_once()
    _, kwargs = spy_endpoint.call_args
    assert kwargs["project_id"] == "test_project_id"
    assert kwargs["request_data"] == UpdateNumberConfigurationRequest(
        phone_number="+1234567890", display_name="Test Display Name"
    )

    assert response == mock_response
