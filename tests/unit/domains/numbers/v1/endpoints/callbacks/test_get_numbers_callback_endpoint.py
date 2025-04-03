import pytest
from sinch.core.models.http_response import HTTPResponse
from sinch.domains.numbers.api.v1.internal import GetCallbackConfigurationEndpoint
from sinch.domains.numbers.models.v1.internal.base import BaseModelConfigurationRequest
from sinch.domains.numbers.models.v1.response import CallbackConfigurationResponse


@pytest.fixture
def mock_response():
    return HTTPResponse(
        status_code=200,
        body={
            "projectId": "j55aa9aa-b888-777c-dd6d-ee55e1010101010",
            "hmacSecret": "your_hmac_secret"
        },
        headers={"Content-Type": "application/json"}
    )


@pytest.fixture
def endpoint_empty_request_data():
    return GetCallbackConfigurationEndpoint("test_project_id", request_data=None)


@pytest.fixture
def endpoint_extra_request_data():
    data = {
        "key": "value",
        "extra_field": "extra value"
    }
    request_model = BaseModelConfigurationRequest(**data)
    return GetCallbackConfigurationEndpoint("test_project_id", request_data=request_model)


endpoint_fixtures = pytest.mark.parametrize("endpoint_fixture", [
    "endpoint_empty_request_data",
    "endpoint_extra_request_data"
])


@endpoint_fixtures
def test_build_url(endpoint_fixture, mock_sinch_client_numbers, request):
    """
    Check if endpoint URL is constructed correctly based on input data.
    """
    endpoint = request.getfixturevalue(endpoint_fixture)
    expected_url = "https://mock-numbers-api.sinch.com/v1/projects/test_project_id/callbackConfiguration"
    assert endpoint.build_url(mock_sinch_client_numbers) == expected_url


def test_build_empty_query_params_expects_correct_mapping(endpoint_empty_request_data):
    """
    Check if empty Query params is handled and mapped to the appropriate fields correctly.
    """
    assert endpoint_empty_request_data.build_query_params() == {}


def test_build_query_params_expects_correct_mapping(endpoint_extra_request_data):
    """
    Check if Query params is handled and mapped to the appropriate fields correctly.
    """
    expected_params = {
        "key": "value",
        "extraField": "extra value"
    }
    assert endpoint_extra_request_data.build_query_params() == expected_params


@endpoint_fixtures
def test_handle_response_expects_correct_mapping(endpoint_fixture, mock_response, request):
    """
    Check if response is handled and mapped to the appropriate fields correctly.
    """
    endpoint = request.getfixturevalue(endpoint_fixture)
    parsed_response = endpoint.handle_response(mock_response)
    assert isinstance(parsed_response, CallbackConfigurationResponse)
    assert parsed_response.project_id == "j55aa9aa-b888-777c-dd6d-ee55e1010101010"
    assert parsed_response.hmac_secret == "your_hmac_secret"
