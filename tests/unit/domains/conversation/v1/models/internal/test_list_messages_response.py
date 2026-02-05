from sinch.domains.conversation.models.v1.messages.internal import (
    ListMessagesResponse,
)
from tests.unit.domains.conversation.v1.models.response.test_conversation_message_response_model import (
    contact_message_response_data,
    app_message_response_data,
)


def test_list_messages_response_expects_correct_mapping(
    contact_message_response_data,
    app_message_response_data,
):
    """
    Test that response is correctly parsed from dict and 
    content property returns messages.
    """
    data = {
        "messages": [contact_message_response_data, app_message_response_data],
        "next_page_token": "token_abc",
    }
    response = ListMessagesResponse.model_validate(data)

    assert response.next_page_token == "token_abc"
    assert response.messages is not None
    assert len(response.messages) == 2
    assert response.messages[0].id == contact_message_response_data["id"]
    assert response.messages[1].id == app_message_response_data["id"]
    assert response.content == response.messages
    assert len(response.content) == 2


def test_list_messages_response_expects_empty_messages_list():
    """Test that response with empty messages list has content as empty list."""
    response = ListMessagesResponse(messages=[], next_page_token=None)

    assert response.messages == []
    assert response.content == []
    assert response.next_page_token is None
