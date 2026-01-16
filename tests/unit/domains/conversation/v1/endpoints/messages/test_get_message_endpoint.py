import pytest
from datetime import datetime, timezone
from sinch.core.models.http_response import HTTPResponse
from sinch.domains.conversation.api.v1.internal import GetMessageEndpoint
from sinch.domains.conversation.models.v1.messages.internal.request import MessageIdRequest
from sinch.domains.conversation.models.v1.messages.response.message_response import (
    AppMessageResponse,
    ContactMessageResponse,
)


@pytest.fixture
def request_data():
    return MessageIdRequest(message_id="CAPY123456789ABCDEFGHIJKLMNOP")


@pytest.fixture
def mock_contact_message_response():
    """Mock response for ContactMessageResponse (Union type test)."""
    return HTTPResponse(
        status_code=200,
        body={
            "id": "CAPY123456789ABCDEFGHIJKLMNOP",
            "conversation_id": "CONV987654321ZYXWVUTSRQPONMLK",
            "contact_id": "CONTACT456789ABCDEFGHIJKLMNOPQR",
            "direction": "UNDEFINED_DIRECTION",
            "channel_identity": {
                "app_id": "APP123456789ABCDEFGHIJK",
                "channel": "WHATSAPP",
                "identity": "+46701234567"
            },
            "metadata": "test_metadata",
            "accept_time": "2026-01-14T20:32:31.147Z",
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
                            "body": "Message body text"
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
            "id": "APP123456789ABCDEFGHIJKLMNOP",
            "conversation_id": "CONV987654321ZYXWVUTSRQPONMLK",
            "contact_id": "CONTACT456789ABCDEFGHIJKLMNOPQR",
            "direction": "UNDEFINED_DIRECTION",
            "channel_identity": {
                "app_id": "APP123456789ABCDEFGHIJK",
                "channel": "WHATSAPP",
                "identity": "+46701234567"
            },
            "metadata": "test_metadata",
            "accept_time": "2026-01-14T20:32:31.147Z",
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
                        "thumbnail_url": "https://example.com/thumbnail.jpg",
                        "url": "https://example.com/media.jpg",
                        "filename_override": "custom_filename.jpg"
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
                    "display_name": "Agent Name",
                    "type": "UNKNOWN_AGENT_TYPE",
                    "picture_url": "https://example.com/agent.jpg"
                }
            }
        },
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

    assert parsed_response.id == "CAPY123456789ABCDEFGHIJKLMNOP"
    assert parsed_response.conversation_id == "CONV987654321ZYXWVUTSRQPONMLK"
    assert parsed_response.contact_id == "CONTACT456789ABCDEFGHIJKLMNOPQR"
    assert parsed_response.direction == "UNDEFINED_DIRECTION"
    assert parsed_response.metadata == "test_metadata"
    assert parsed_response.contact_message is not None
    assert parsed_response.contact_message.channel_specific_message is not None
    assert parsed_response.contact_message.channel_specific_message.message_type == "nfm_reply"
    assert parsed_response.contact_message.channel_specific_message.message.type == "nfm_reply"
    assert parsed_response.contact_message.channel_specific_message.message.nfm_reply.name == "flow"
    assert parsed_response.contact_message.channel_specific_message.message.nfm_reply.response_json == "{\"key\": \"value\"}"
    assert parsed_response.contact_message.channel_specific_message.message.nfm_reply.body == "Message body text"
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
        2026, 1, 14, 20, 32, 31, 147000, tzinfo=timezone.utc
    )


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
    
    assert parsed_response.id == "APP123456789ABCDEFGHIJKLMNOP"
    assert parsed_response.conversation_id == "CONV987654321ZYXWVUTSRQPONMLK"
    assert parsed_response.contact_id == "CONTACT456789ABCDEFGHIJKLMNOPQR"
    assert parsed_response.direction == "UNDEFINED_DIRECTION"
    assert parsed_response.metadata == "test_metadata"
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
    assert parsed_response.app_message.card_message.media_message.url == "https://example.com/media.jpg"
    assert parsed_response.app_message.card_message.media_message.thumbnail_url == "https://example.com/thumbnail.jpg"
    assert parsed_response.app_message.card_message.media_message.filename_override == "custom_filename.jpg"
    assert parsed_response.app_message.card_message.message_properties is not None
    assert parsed_response.app_message.card_message.message_properties.whatsapp_header == "WhatsApp header text"
    assert parsed_response.app_message.agent is not None
    assert parsed_response.app_message.agent.display_name == "Agent Name"
    assert parsed_response.app_message.agent.type == "UNKNOWN_AGENT_TYPE"
    assert parsed_response.app_message.agent.picture_url == "https://example.com/agent.jpg"
    assert parsed_response.channel_identity is not None
    assert parsed_response.channel_identity.app_id == "APP123456789ABCDEFGHIJK"
    assert parsed_response.channel_identity.channel == "WHATSAPP"
    assert parsed_response.channel_identity.identity == "+46701234567"
    assert parsed_response.injected is True
    assert parsed_response.sender_id == "SENDER123456789ABCDEFGHIJK"
    assert parsed_response.processing_mode == "CONVERSATION"

    assert parsed_response.accept_time == datetime(
        2026, 1, 14, 20, 32, 31, 147000, tzinfo=timezone.utc
    )
