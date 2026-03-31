import pytest
from sinch.core.models.http_response import HTTPResponse
from sinch.domains.conversation.api.v1.internal import GetMessageEndpoint
from sinch.domains.conversation.models.v1.messages.internal.request import MessageIdRequest
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
    return MessageIdRequest(message_id="CAPY123456789ABCDEFGHIJKLMNOP")


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
    return GetMessageEndpoint("test_project_id", request_data)


def test_build_url_expects_correct_url(endpoint, mock_sinch_client_conversation):
    """"
    Test that the URL is built correctly.
    """
    assert (
        endpoint.build_url(mock_sinch_client_conversation)
        == "https://us.conversation.api.sinch.com/v1/projects/test_project_id/messages/CAPY123456789ABCDEFGHIJKLMNOP"
    )


def test_messages_source_query_param_expects_parsed_params():
    """
    Test that the messages_source query parameter is parsed correctly.
    """
    request_data = MessageIdRequest(
        message_id="CAPY123456789ABCDEFGHIJKLMNOP",
        messages_source="CONVERSATION_SOURCE"
    )
    endpoint = GetMessageEndpoint("test_project_id", request_data)
    
    query_params = endpoint.build_query_params()
    assert query_params["messages_source"] == "CONVERSATION_SOURCE"


def test_handle_response_expects_contact_message_response(endpoint, mock_contact_message_response):
    """
    Test that contact message response is handled correctly and mapped to the appropriate fields.
    """
    parsed_response = endpoint.handle_response(mock_contact_message_response)

    # ConversationMessageResponse is a Union of AppMessageResponse and ContactMessageResponse
    # In this test case, we expect a ContactMessageResponse
    assert isinstance(parsed_response, ContactMessageResponse)
    assert not isinstance(parsed_response, AppMessageResponse)


def test_handle_response_expects_app_message_response(mock_app_message_response):
    """
    Test that the app message response is handled correctly and mapped to the appropriate fields.
    """
    request_data = MessageIdRequest(message_id="APP123456789ABCDEFGHIJKLMNOP")
    endpoint = GetMessageEndpoint("test_project_id", request_data)
    
    parsed_response = endpoint.handle_response(mock_app_message_response)

    # ConversationMessageResponse is a Union of AppMessageResponse and ContactMessageResponse
    # In this test case, we expect an AppMessageResponse
    assert isinstance(parsed_response, AppMessageResponse)
    assert not isinstance(parsed_response, ContactMessageResponse)
