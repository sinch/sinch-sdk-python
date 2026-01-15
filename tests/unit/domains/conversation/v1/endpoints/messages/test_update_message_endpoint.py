import json
import pytest
from datetime import datetime, timezone
from sinch.core.models.http_response import HTTPResponse
from sinch.domains.conversation.api.v1.internal import UpdateMessageMetadataEndpoint
from sinch.domains.conversation.models.v1.messages.internal.request import UpdateMessageMetadataRequest
from sinch.domains.conversation.models.v1.messages.response.message_response import (
    AppMessageResponse,
    ContactMessageResponse,
)


@pytest.fixture
def request_data():
    return UpdateMessageMetadataRequest(
        message_id="UPDATE123456789ABCDEFGHIJKLMNOP",
        metadata="updated_metadata_value",
    )


@pytest.fixture
def mock_contact_message_response():
    """Mock response for ContactMessageResponse (Union type test)."""
    return HTTPResponse(
        status_code=200,
        body={
            "id": "UPDATE123456789ABCDEFGHIJKLMNOP",
            "conversation_id": "UPDATE_CONV987654321ZYXWVUTSRQP",
            "contact_id": "UPDATE_CONTACT456789ABCDEFGHIJK",
            "direction": "TO_CONTACT",
            "channel_identity": {
                "app_id": "APP123456789ABCDEFGHIJK",
                "channel": "WHATSAPP",
                "identity": "+46701234567"
            },
            "metadata": "updated_metadata_value",
            "accept_time": "2026-01-15T17:19:12.000Z",
            "injected": True,
            "sender_id": "SENDER123456789ABCDEFGHIJK",
            "processing_mode": "CONVERSATION",
            "contact_message": {
                "channel_specific_message": {
                    "message_type": "nfm_reply",
                    "message": {
                        "type": "nfm_reply",
                        "nfm_reply": {
                            "name": "flow",
                            "response_json": "{\"key\": \"value\"}",
                            "body": "Updated message content"
                        }
                    }
                },
                "reply_to": {
                    "message_id": "REPLY_TO_MSG123456789ABCDEF"
                }
            }
        },
        headers={"Content-Type": "application/json"},
    )


@pytest.fixture
def mock_app_message_response():
    """Mock response for AppMessageResponse (Union type test)."""
    return HTTPResponse(
        status_code=200,
        body={
            "id": "UPDATE_APP123456789ABCDEFGHIJK",
            "conversation_id": "UPDATE_CONV987654321ZYXWVUTSRQP",
            "contact_id": "UPDATE_CONTACT456789ABCDEFGHIJK",
            "direction": "TO_CONTACT",
            "channel_identity": {
                "app_id": "APP123456789ABCDEFGHIJK",
                "channel": "WHATSAPP",
                "identity": "+46701234567"
            },
            "metadata": "updated_metadata_value",
            "accept_time": "2026-01-15T17:19:12.000Z",
            "injected": True,
            "sender_id": "SENDER123456789ABCDEFGHIJK",
            "processing_mode": "CONVERSATION",
            "app_message": {
                "card_message": {
                    "choices": [
                        {
                            "call_message": {
                                "phone_number": "+15551231234",
                                "title": "Message text"
                            },
                            "postback_data": None
                        }
                    ],
                    "description": "Card description text",
                    "height": "UNSPECIFIED_HEIGHT",
                    "title": "Card title",
                    "media_message": {
                        "thumbnail_url": "https://update.example.com/thumb.jpg",
                        "url": "https://update.example.com/image.jpg",
                        "filename_override": "updated_image.jpg"
                    },
                    "message_properties": {
                        "whatsapp_header": "WhatsApp header text"
                    }
                },
                "explicit_channel_message": {
                    "property1": "string",
                    "property2": "string"
                },
                "explicit_channel_omni_message": {
                    "property1": {
                        "text_message": {
                            "text": "string"
                        }
                    },
                    "property2": {
                        "text_message": {
                            "text": "string"
                        }
                    }
                },
                "channel_specific_message": {
                    "property1": {
                        "message_type": "FLOWS",
                        "message": {
                            "header": {
                                "type": "text",
                                "text": "string"
                            },
                            "body": {
                                "text": "string"
                            },
                            "footer": {
                                "text": "string"
                            },
                            "flow_id": "string",
                            "flow_token": "string",
                            "flow_mode": "draft",
                            "flow_cta": "string",
                            "flow_action": "navigate",
                            "flow_action_payload": {
                                "screen": "string",
                                "data": {}
                            }
                        }
                    }
                },
                "agent": {
                    "display_name": "Updated Agent",
                    "type": "HUMAN_AGENT",
                    "picture_url": "https://update.example.com/agent_photo.jpg"
                }
            }
        },
        headers={"Content-Type": "application/json"},
    )


@pytest.fixture
def endpoint(request_data):
    return UpdateMessageMetadataEndpoint("test_project_id", request_data)


def test_build_url_expects_correct_url(endpoint, mock_sinch_client_conversation):
    """Test that the URL is built correctly."""
    assert (
        endpoint.build_url(mock_sinch_client_conversation)
        == "https://us.conversation.api.sinch.com//v1/projects/test_project_id/messages/UPDATE123456789ABCDEFGHIJKLMNOP"
    )


def test_messages_source_query_param_expects_parsed_params():
    """
    Test that the URL is built correctly with messages_source query parameter.
    metadata is from body application/json, so it should not be in query params.
    """
    request_data = UpdateMessageMetadataRequest(
        message_id="UPDATE123456789ABCDEFGHIJKLMNOP",
        metadata="updated_metadata_value",
        messages_source="CONVERSATION_SOURCE"
    )
    endpoint = UpdateMessageMetadataEndpoint("test_project_id", request_data)
    
    query_params = endpoint.build_query_params()
    assert "metadata" not in query_params
    assert query_params["messages_source"] == "CONVERSATION_SOURCE"


def test_request_body_expects_excludes_message_id(request_data):
    """
    Test that message_id is excluded from request body.
    """
    endpoint = UpdateMessageMetadataEndpoint("test_project_id", request_data)
    body = json.loads(endpoint.request_body())

    assert "message_id" not in body
    assert "metadata" in body
    assert body["metadata"] == "updated_metadata_value"


def test_request_body_expects_excludes_query_params(request_data):
    """
    Test that messages_source is excluded from request body (it's a query param).
    """
    request_data.messages_source = "CONVERSATION_SOURCE"
    
    endpoint = UpdateMessageMetadataEndpoint("test_project_id", request_data)
    body = json.loads(endpoint.request_body())

    assert "message_id" not in body
    assert "messages_source" not in body
    assert "metadata" in body
    assert body["metadata"] == "updated_metadata_value"


def test_handle_response_expects_contact_message_mapping(endpoint, mock_contact_message_response):
    """
    Test that the response handles ContactMessageResponse correctly (Union type test).
    """
    parsed_response = endpoint.handle_response(mock_contact_message_response)

    assert isinstance(parsed_response, ContactMessageResponse)
    assert not isinstance(parsed_response, AppMessageResponse)
    
    assert parsed_response.id == "UPDATE123456789ABCDEFGHIJKLMNOP"
    assert parsed_response.conversation_id == "UPDATE_CONV987654321ZYXWVUTSRQP"
    assert parsed_response.contact_id == "UPDATE_CONTACT456789ABCDEFGHIJK"
    assert parsed_response.direction == "TO_CONTACT"
    assert parsed_response.metadata == "updated_metadata_value"
    assert parsed_response.contact_message is not None
    assert parsed_response.contact_message.channel_specific_message is not None
    assert parsed_response.contact_message.channel_specific_message.message_type == "nfm_reply"
    assert parsed_response.contact_message.channel_specific_message.message.type == "nfm_reply"
    assert parsed_response.contact_message.channel_specific_message.message.nfm_reply.name == "flow"
    assert parsed_response.contact_message.channel_specific_message.message.nfm_reply.response_json == "{\"key\": \"value\"}"
    assert parsed_response.contact_message.channel_specific_message.message.nfm_reply.body == "Updated message content"
    assert parsed_response.contact_message.reply_to is not None
    assert parsed_response.contact_message.reply_to.message_id == "REPLY_TO_MSG123456789ABCDEF"
    assert parsed_response.channel_identity is not None
    assert parsed_response.channel_identity.app_id == "APP123456789ABCDEFGHIJK"
    assert parsed_response.channel_identity.channel == "WHATSAPP"
    assert parsed_response.channel_identity.identity == "+46701234567"
    assert parsed_response.injected is True
    assert parsed_response.sender_id == "SENDER123456789ABCDEFGHIJK"
    assert parsed_response.processing_mode == "CONVERSATION"

    assert parsed_response.accept_time == datetime(
        2026, 1, 15, 17, 19, 12, 0, tzinfo=timezone.utc
    )


def test_handle_response_expects_app_message_mapping(mock_app_message_response):
    """
    Test that the response handles AppMessageResponse correctly (Union type test).
    """
    request_data = UpdateMessageMetadataRequest(
        message_id="UPDATE_APP123456789ABCDEFGHIJK",
        metadata="updated_metadata_value",
    )
    endpoint = UpdateMessageMetadataEndpoint("test_project_id", request_data)
    
    parsed_response = endpoint.handle_response(mock_app_message_response)

    assert isinstance(parsed_response, AppMessageResponse)
    assert not isinstance(parsed_response, ContactMessageResponse)
    
    assert parsed_response.id == "UPDATE_APP123456789ABCDEFGHIJK"
    assert parsed_response.conversation_id == "UPDATE_CONV987654321ZYXWVUTSRQP"
    assert parsed_response.contact_id == "UPDATE_CONTACT456789ABCDEFGHIJK"
    assert parsed_response.direction == "TO_CONTACT"
    assert parsed_response.metadata == "updated_metadata_value"
    assert parsed_response.app_message is not None
    assert parsed_response.app_message.card_message is not None
    assert parsed_response.app_message.card_message.title == "Card title"
    assert parsed_response.app_message.card_message.description == "Card description text"
    assert parsed_response.app_message.card_message.height == "UNSPECIFIED_HEIGHT"
    assert parsed_response.app_message.card_message.choices is not None
    assert len(parsed_response.app_message.card_message.choices) == 1
    assert parsed_response.app_message.card_message.choices[0].call_message is not None
    assert parsed_response.app_message.card_message.choices[0].call_message.phone_number == "+15551231234"
    assert parsed_response.app_message.card_message.choices[0].call_message.title == "Message text"
    assert parsed_response.app_message.card_message.media_message is not None
    assert parsed_response.app_message.card_message.media_message.url == "https://update.example.com/image.jpg"
    assert parsed_response.app_message.card_message.media_message.thumbnail_url == "https://update.example.com/thumb.jpg"
    assert parsed_response.app_message.card_message.media_message.filename_override == "updated_image.jpg"
    assert parsed_response.app_message.card_message.message_properties is not None
    assert parsed_response.app_message.card_message.message_properties.whatsapp_header == "WhatsApp header text"
    assert parsed_response.app_message.agent is not None
    assert parsed_response.app_message.agent.display_name == "Updated Agent"
    assert parsed_response.app_message.agent.type == "HUMAN_AGENT"
    assert parsed_response.app_message.agent.picture_url == "https://update.example.com/agent_photo.jpg"
    assert parsed_response.channel_identity is not None
    assert parsed_response.channel_identity.app_id == "APP123456789ABCDEFGHIJK"
    assert parsed_response.channel_identity.channel == "WHATSAPP"
    assert parsed_response.channel_identity.identity == "+46701234567"
    assert parsed_response.injected is True
    assert parsed_response.sender_id == "SENDER123456789ABCDEFGHIJK"
    assert parsed_response.processing_mode == "CONVERSATION"

    assert parsed_response.accept_time == datetime(
        2026, 1, 15, 17, 19, 12, 0, tzinfo=timezone.utc
    )
