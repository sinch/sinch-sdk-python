import json
import pytest
from sinch.core.models.http_response import HTTPResponse
from sinch.domains.conversation.api.v1.internal import UpdateMessageMetadataEndpoint
from sinch.domains.conversation.models.v1.messages.internal.request import UpdateMessageMetadataRequest
from sinch.domains.conversation.models.v1.messages.response.message_response import (
    AppMessageResponse,
    ContactMessageResponse,
)
from tests.unit.domains.conversation.v1.models.response.test_conversation_message_response_model import (
    contact_message_response_data,
    app_message_response_data,
)


@pytest.fixture
def request_data():
    return UpdateMessageMetadataRequest(
        message_id="CAPY123456789ABCDEFGHIJKLMNOP",
        metadata="test_metadata",
    )


@pytest.fixture
def mock_contact_message_response(contact_message_response_data):
    """Mock response for ContactMessageResponse (Union type test)."""
    return HTTPResponse(
        status_code=200,
        body=contact_message_response_data,
        headers={"Content-Type": "application/json"},
    )


@pytest.fixture
def mock_app_message_response(app_message_response_data):
    """Mock response for AppMessageResponse (Union type test)."""
    return HTTPResponse(
        status_code=200,
        body=app_message_response_data,
        headers={"Content-Type": "application/json"},
    )


@pytest.fixture
def endpoint(request_data):
    return UpdateMessageMetadataEndpoint("test_project_id", request_data)


def test_build_url_expects_correct_url(endpoint, mock_sinch_client_conversation):
    """Test that the URL is built correctly."""
    assert (
        endpoint.build_url(mock_sinch_client_conversation)
        == "https://us.conversation.api.sinch.com/v1/projects/test_project_id/messages/CAPY123456789ABCDEFGHIJKLMNOP"
    )


def test_messages_source_query_param_expects_parsed_params(request_data):
    """
    Test that the URL is built correctly with messages_source query parameter.
    metadata is from body application/json, so it should not be in query params.
    """
    request_data.messages_source = "DISPATCH_SOURCE"
    endpoint = UpdateMessageMetadataEndpoint("test_project_id", request_data)
    
    query_params = endpoint.build_query_params()
    assert "metadata" not in query_params
    assert query_params["messages_source"] == "DISPATCH_SOURCE"


def test_request_body_expects_excludes_message_id_and_query_params(request_data):
    """
    Test that message_id and messages_source are excluded from request body.
    metadata should always be included in the request body.
    """
    request_data.messages_source = "CONVERSATION_SOURCE"
    endpoint = UpdateMessageMetadataEndpoint("test_project_id", request_data)
    body = json.loads(endpoint.request_body())

    assert "messages_source" not in body
    assert "message_id" not in body
    assert "metadata" in body
    assert body["metadata"] == "test_metadata"


def test_handle_response_expects_contact_message_mapping(endpoint, mock_contact_message_response):
    """
    Test that the response handles ContactMessageResponse correctly (Union type test).
    """
    parsed_response = endpoint.handle_response(mock_contact_message_response)

    assert isinstance(parsed_response, ContactMessageResponse)
    assert not isinstance(parsed_response, AppMessageResponse)

    assert parsed_response.id == "CAPY123456789ABCDEFGHIJKLMNOP"
    assert parsed_response.metadata == "test_metadata"


def test_handle_response_expects_app_message_mapping(mock_app_message_response):
    """
    Test that the response handles AppMessageResponse correctly (Union type test).
    """
    request_data = UpdateMessageMetadataRequest(
        message_id="APP123456789ABCDEFGHIJKLMNOP",
        metadata="test_metadata",
    )
    endpoint = UpdateMessageMetadataEndpoint("test_project_id", request_data)
    
    parsed_response = endpoint.handle_response(mock_app_message_response)

    assert isinstance(parsed_response, AppMessageResponse)
    assert not isinstance(parsed_response, ContactMessageResponse)

    assert parsed_response.id == "APP123456789ABCDEFGHIJKLMNOP"
    assert parsed_response.metadata == "test_metadata"
