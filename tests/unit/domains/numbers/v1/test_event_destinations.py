import pytest
from sinch.domains.numbers.api.v1 import EventDestinations
from sinch.domains.numbers.api.v1.internal import (
    GetEventDestinationEndpoint, UpdateEventDestinationEndpoint
)
from sinch.domains.numbers.models.v1.internal import UpdateEventDestinationRequest
from sinch.domains.numbers.models.v1.internal.base import BaseModelConfigurationRequest
from sinch.domains.numbers.models.v1.response import EventDestinationResponse


@pytest.mark.parametrize(
    "test_name, config_kwargs, expected_request_data",
    [
        (
            "without_extra_params", {}, None
        ),
        (
            "with_extra_params", {"kwargs": {"extra_param": "value"}},
            BaseModelConfigurationRequest(kwargs={"extra_param": "value"})
        ),
    ],
)
def test_get_numbers_callback_config_expects_valid_request(
        mock_sinch_client_numbers, mocker, test_name, config_kwargs, expected_request_data
):
    """
    Test that the get() method sends the correct request
    and handles the response properly with or without extra parameters.
    """
    mock_response = EventDestinationResponse(project_id="test_project_id", hmac_secret="test_secret")
    mock_sinch_client_numbers.configuration.transport.request.return_value = mock_response
    spy_endpoint = mocker.spy(GetEventDestinationEndpoint, "__init__")

    event_destination = EventDestinations(mock_sinch_client_numbers)
    response = event_destination.get(**config_kwargs)

    spy_endpoint.assert_called_once()
    _, kwargs = spy_endpoint.call_args

    assert kwargs["project_id"] == "test_project_id"
    if expected_request_data:
        assert kwargs["request_data"] == expected_request_data

    assert response == mock_response
    mock_sinch_client_numbers.configuration.transport.request.assert_called_once()


def test_update_numbers_callback_config_expects_valid_request(mock_sinch_client_numbers, mocker):
    """
    Test that the update() method sends the correct request
    and handles the response properly.
    """
    mock_response = EventDestinationResponse(project_id="test_project_id", hmac_secret="new_secret")
    mock_sinch_client_numbers.configuration.transport.request.return_value = mock_response

    spy_endpoint = mocker.spy(UpdateEventDestinationEndpoint, "__init__")

    event_destination = EventDestinations(mock_sinch_client_numbers)
    response = event_destination.update(hmac_secret="new_secret")

    spy_endpoint.assert_called_once()
    _, kwargs = spy_endpoint.call_args

    assert kwargs["project_id"] == "test_project_id"
    assert kwargs["request_data"] == UpdateEventDestinationRequest(hmac_secret="new_secret")

    assert response == mock_response
    mock_sinch_client_numbers.configuration.transport.request.assert_called_once()
