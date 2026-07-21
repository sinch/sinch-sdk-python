from datetime import datetime, timezone

from sinch.domains.conversation.models.v1.messages.internal.request import (
    ListMessagesRequest,
)


def test_list_messages_request_expects_parsed_input():
    """Test that the model correctly parses input with all parameters."""
    start = datetime(2025, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
    end = datetime(2025, 1, 8, 12, 0, 0, tzinfo=timezone.utc)

    request = ListMessagesRequest(
        conversation_id="CONV123456789ABCDEFGHIJKLM",
        contact_id="CONTACT456789ABCDEFGHIJKLMNOP",
        app_id="APP123456789ABCDEFGHIJK",
        channel_identity="+46701234567",
        start_time=start,
        end_time=end,
        page_size=50,
        page_token="next_page_token_abc",
        view="WITH_METADATA",
        messages_source="CONVERSATION_SOURCE",
        only_recipient_originated=True,
        channel="WHATSAPP",
        direction="TO_CONTACT",
    )

    assert request.conversation_id == "CONV123456789ABCDEFGHIJKLM"
    assert request.contact_id == "CONTACT456789ABCDEFGHIJKLMNOP"
    assert request.app_id == "APP123456789ABCDEFGHIJK"
    assert request.channel_identity == "+46701234567"
    assert request.start_time == start
    assert request.end_time == end
    assert request.page_size == 50
    assert request.page_token == "next_page_token_abc"
    assert request.view == "WITH_METADATA"
    assert request.messages_source == "CONVERSATION_SOURCE"
    assert request.only_recipient_originated is True
    assert request.channel == "WHATSAPP"
    assert request.direction == "TO_CONTACT"
