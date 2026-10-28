import json

import pytest

from sinch.core.models.http_response import HTTPResponse
from sinch.domains.conversation.api.v1.exceptions import ConversationException
from sinch.domains.conversation.api.v1.internal.event_destinations_endpoints import (
    UpdateEventDestinationEndpoint,
)
from sinch.domains.conversation.models.v1.event_destinations.request.update_event_destination_request import (
    UpdateEventDestinationRequest,
)
from sinch.domains.conversation.models.v1.event_destinations.response.event_destination_response import (
    EventDestinationResponse,
)
from sinch.domains.conversation.models.v1.event_destinations.shared.client_credentials import (
    ClientCredentials,
)


@pytest.fixture
def request_data():
    return UpdateEventDestinationRequest(
        event_destination_id="01W4FFL35P4NC4K35WEBHOOK001",
        app_id="01W4FFL35P4NC4K35CONVAPP001",
        target="https://my-server.com/events",
        target_type="HTTP",
        secret="my-secret",
        triggers=["CAPABILITY", "OPT_IN"],
        client_credentials={
            "endpoint": "https://my-auth-server.com/oauth2/token",
            "client_id": "my-client-id",
            "client_secret": "my-client-secret",
        },
    )


@pytest.fixture
def mock_response():
    return HTTPResponse(
        status_code=200,
        body={
            "id": "01W4FFL35P4NC4K35WEBHOOK001",
            "app_id": "01W4FFL35P4NC4K35CONVAPP001",
            "target": "https://my-server.com/events",
            "target_type": "HTTP",
            "secret": "my-secret",
            "triggers": ["CAPABILITY", "OPT_IN"],
            "client_credentials": {
                "endpoint": "https://my-auth-server.com/oauth2/token",
                "client_id": "my-client-id",
                "client_secret": "my-client-secret",
                "scope": "read",
                "response_type": "token",
                "token_request_type": "FORM",
            },
            "extra_field": "extra",
        },
        headers={"Content-Type": "application/json"},
    )


@pytest.fixture
def mock_error_response():
    return HTTPResponse(
        status_code=400,
        body={
            "error": {
                "code": 400,
                "message": "Invalid argument",
                "status": "INVALID_ARGUMENT",
            }
        },
        headers={"Content-Type": "application/json"},
    )


@pytest.fixture
def endpoint(request_data):
    return UpdateEventDestinationEndpoint("test_project_id", request_data)


def test_build_url_expects_correct_url(
    endpoint, mock_sinch_client_conversation
):
    """Test that the URL is built correctly with the event destination ID path param."""
    assert (
        endpoint.build_url(mock_sinch_client_conversation)
        == "https://us.conversation.api.sinch.com/v1/projects/test_project_id/webhooks/01W4FFL35P4NC4K35WEBHOOK001"
    )


def test_build_query_params_expects_update_mask_from_body_fields(endpoint):
    """Test that update_mask is a comma-joined list of the set body fields."""
    mask = endpoint.build_query_params()["update_mask"].split(",")

    assert set(mask) == {
        "app_id",
        "target",
        "target_type",
        "secret",
        "triggers",
        "client_credentials",
    }
    assert "event_destination_id" not in mask


def test_build_query_params_expects_empty_when_no_body_fields():
    """Test that update_mask is omitted when no field is set."""
    endpoint = UpdateEventDestinationEndpoint(
        "test_project_id",
        UpdateEventDestinationRequest(
            event_destination_id="01W4FFL35P4NC4K35WEBHOOK001"
        ),
    )

    assert endpoint.build_query_params() == {}


def test_build_query_params_accepts_none_fields():
    """Test that an explicit None is listed in update_mask."""
    endpoint = UpdateEventDestinationEndpoint(
        "test_project_id",
        UpdateEventDestinationRequest(
            event_destination_id="01W4FFL35P4NC4K35WEBHOOK001",
            target="https://my-server.com/events",
            secret=None,
        ),
    )

    mask = endpoint.build_query_params()["update_mask"].split(",")
    assert set(mask) == {"target", "secret"}


def test_request_body_expects_correct_serialization(endpoint):
    """Test that the body carries the fields and no path or query params."""
    body = json.loads(endpoint.request_body())

    assert body["app_id"] == "01W4FFL35P4NC4K35CONVAPP001"
    assert body["target"] == "https://my-server.com/events"
    assert body["target_type"] == "HTTP"
    assert body["secret"] == "my-secret"
    assert body["triggers"] == ["CAPABILITY", "OPT_IN"]
    assert body["client_credentials"]["client_id"] == "my-client-id"
    assert "event_destination_id" not in body
    assert "update_mask" not in body
    assert "project_id" not in body


def test_request_body_accepts_none_fields_and_exclude_unset_fields():
    """Test that an explicit None is sent as null and unset fields are omitted."""
    endpoint = UpdateEventDestinationEndpoint(
        "test_project_id",
        UpdateEventDestinationRequest(
            event_destination_id="01W4FFL35P4NC4K35WEBHOOK001",
            target="https://my-server.com/events",
            secret=None,
        ),
    )
    body = json.loads(endpoint.request_body())

    assert body["target"] == "https://my-server.com/events"
    assert body["secret"] is None
    assert "triggers" not in body


def test_handle_response_expects_correct_mapping(endpoint, mock_response):
    """Test that the response is mapped into an EventDestinationResponse."""
    parsed_response = endpoint.handle_response(mock_response)

    assert isinstance(parsed_response, EventDestinationResponse)
    assert parsed_response.id == "01W4FFL35P4NC4K35WEBHOOK001"
    assert parsed_response.app_id == "01W4FFL35P4NC4K35CONVAPP001"
    assert parsed_response.target == "https://my-server.com/events"
    assert parsed_response.target_type == "HTTP"
    assert parsed_response.secret == "my-secret"
    assert parsed_response.triggers == ["CAPABILITY", "OPT_IN"]
    assert isinstance(parsed_response.client_credentials, ClientCredentials)
    assert parsed_response.client_credentials.client_id == "my-client-id"
    assert parsed_response.client_credentials.token_request_type == "FORM"


def test_handle_response_expects_conversation_exception_on_error(
    endpoint, mock_error_response
):
    """Test that ConversationException is raised with the server error message."""
    with pytest.raises(ConversationException) as exc_info:
        endpoint.handle_response(mock_error_response)

    assert str(exc_info.value) == "Invalid argument  INVALID_ARGUMENT"
    assert exc_info.value.is_from_server is True
    assert exc_info.value.http_response.status_code == 400
