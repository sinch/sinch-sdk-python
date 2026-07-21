from datetime import datetime, timezone
from sinch.domains.conversation.models.v1.messages.internal.request import (
    ListLastMessagesByChannelIdentityRequest,
)


def test_list_last_messages_by_channel_identity_request_expects_parsed_input():
    """Test that the model correctly parses input with all parameters."""
    start = datetime(2025, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
    end = datetime(2025, 1, 8, 12, 0, 0, tzinfo=timezone.utc)

    request = ListLastMessagesByChannelIdentityRequest(
        channel_identities=["+46701234567", "+46709876543"],
        contact_ids=["CONTACT456789ABCDEFGHIJKLMNOP"],
        app_id="APP123456789ABCDEFGHIJK",
        messages_source="DISPATCH_SOURCE",
        page_size=50,
        page_token="next_page_token_abc",
        view="WITH_METADATA",
        start_time=start,
        end_time=end,
        channel="WHATSAPP",
        direction="TO_CONTACT",
    )

    assert request.channel_identities == ["+46701234567", "+46709876543"]
    assert request.contact_ids == ["CONTACT456789ABCDEFGHIJKLMNOP"]
    assert request.app_id == "APP123456789ABCDEFGHIJK"
    assert request.messages_source == "DISPATCH_SOURCE"
    assert request.page_size == 50
    assert request.page_token == "next_page_token_abc"
    assert request.view == "WITH_METADATA"
    assert request.start_time == start
    assert request.end_time == end
    assert request.channel == "WHATSAPP"
    assert request.direction == "TO_CONTACT"
