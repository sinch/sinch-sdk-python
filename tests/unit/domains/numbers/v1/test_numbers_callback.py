import pytest
from sinch.domains.numbers.api.v1 import CallbackConfiguration
from sinch.domains.numbers.api.v1.internal import (
    GetCallbackConfigurationEndpoint, UpdateCallbackConfigurationEndpoint
)
from sinch.domains.numbers.models.v1.internal import UpdateCallbackConfigurationRequest
from sinch.domains.numbers.models.v1.internal.base import BaseModelConfigurationRequest
from sinch.domains.numbers.models.v1.response import CallbackConfigurationResponse


@pytest.mark.parametrize(
    "test_name,config_kwargs,expected_request_data",
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
    mock_response = CallbackConfigurationResponse(project_id="test_project_id", hmac_secret="test_secret")
    mock_sinch_client_numbers.configuration.transport.request.return_value = mock_response
    spy_endpoint = mocker.spy(GetCallbackConfigurationEndpoint, "__init__")

    callback_configuration = CallbackConfiguration(mock_sinch_client_numbers)
    response = callback_configuration.get(**config_kwargs)

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
    mock_response = CallbackConfigurationResponse(project_id="test_project_id", hmac_secret="new_secret")
    mock_sinch_client_numbers.configuration.transport.request.return_value = mock_response

    spy_endpoint = mocker.spy(UpdateCallbackConfigurationEndpoint, "__init__")

    callback_configuration = CallbackConfiguration(mock_sinch_client_numbers)
    response = callback_configuration.update(hmac_secret="new_secret")

    spy_endpoint.assert_called_once()
    _, kwargs = spy_endpoint.call_args

    assert kwargs["project_id"] == "test_project_id"
    assert kwargs["request_data"] == UpdateCallbackConfigurationRequest(hmac_secret="new_secret")

    assert response == mock_response
    mock_sinch_client_numbers.configuration.transport.request.assert_called_once()
