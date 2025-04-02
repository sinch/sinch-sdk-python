import json
import pytest
from sinch.core.models.http_response import HTTPResponse
from sinch.domains.numbers.api.v1.internal import UpdateCallbackConfigurationEndpoint
from sinch.domains.numbers.models.v1.internal import UpdateCallbackConfigurationRequest
from sinch.domains.numbers.models.v1.response import CallbackConfigurationResponse


@pytest.fixture
def mock_request_data():
    return UpdateCallbackConfigurationRequest(
        hmac_secret="your_hmac_secret"
    )


@pytest.fixture
def mock_response():
    return HTTPResponse(
        status_code=200,
        body={
          "projectId": "a99aa9aa-b888-777c-dd6d-ee55e5555555",
          "hmacSecret": "your_hmac_secret"
        },
        headers={"Content-Type": "application/json"}
    )


@pytest.fixture
def mock_response_body():
    expected_body = {
        "hmacSecret": "your_hmac_secret"
    }
    return json.dumps(expected_body)


@pytest.fixture
def endpoint(mock_request_data):
    return UpdateCallbackConfigurationEndpoint("test_project_id", mock_request_data)


def test_build_url(endpoint, mock_sinch_client_numbers):
    """
    Check if endpoint URL is constructed correctly based on input data.
    """
    expected_url = "https://mock-numbers-api.sinch.com/v1/projects/test_project_id/callbackConfiguration"
    assert endpoint.build_url(mock_sinch_client_numbers) == expected_url


def test_request_body_expects_correct_mapping(endpoint, mock_response_body):
    """
    Check if request body is properly formatted as JSON.
    """
    request_body = endpoint.request_body()
    assert request_body == mock_response_body


def test_handle_response_expects_correct_mapping(endpoint, mock_response):
    """
    Check if response is handled and mapped to the appropriate fields correctly.
    """
    parsed_response = endpoint.handle_response(mock_response)
    assert isinstance(parsed_response, CallbackConfigurationResponse)
    assert parsed_response.project_id == "a99aa9aa-b888-777c-dd6d-ee55e5555555"
    assert parsed_response.hmac_secret == "your_hmac_secret"
