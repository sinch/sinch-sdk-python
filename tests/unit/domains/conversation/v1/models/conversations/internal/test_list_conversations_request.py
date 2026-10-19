from sinch.domains.conversation.models.v1.conversations.internal.list_conversations_request import (
    ListConversationsRequest,
)


def test_list_conversations_request_expects_parsed_input():
    """Test that the model correctly parses a full valid input."""
    model = ListConversationsRequest(
        app_id="01W4FFL35P4NC4K35CONVAPP001",
        contact_id="01W4FFL35P4NC4K35CONTACT001",
        only_active=True,
        page_size=5,
        page_token="token_abc",
        active_channel="WHATSAPP",
    )

    assert model.app_id == "01W4FFL35P4NC4K35CONVAPP001"
    assert model.contact_id == "01W4FFL35P4NC4K35CONTACT001"
    assert model.only_active is True
    assert model.page_size == 5
    assert model.page_token == "token_abc"
    assert model.active_channel == "WHATSAPP"

    # Asserting aliases on dump by alias
    alias_dump = model.model_dump(by_alias=True, exclude_none=True)
    assert alias_dump == {
        "app_id": "01W4FFL35P4NC4K35CONVAPP001",
        "contact_id": "01W4FFL35P4NC4K35CONTACT001",
        "only_active": True,
        "page_size": 5,
        "page_token": "token_abc",
        "active_channel": "WHATSAPP",
    }


def test_list_conversations_request_expects_all_optionals_default_to_none():
    """Test that all optional fields default to None."""
    model = ListConversationsRequest()

    assert model.app_id is None
    assert model.contact_id is None
    assert model.only_active is None
    assert model.page_size is None
    assert model.page_token is None
    assert model.active_channel is None
