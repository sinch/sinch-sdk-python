from datetime import datetime, timezone
import pytest
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


@pytest.mark.parametrize(
    "messages_source",
    ["CONVERSATION_SOURCE", "DISPATCH_SOURCE"],
)
def test_list_messages_request_expects_accepts_messages_source(messages_source):
    """Test that the model accepts messages_source with different values."""
    request = ListMessagesRequest(
        page_size=10,
        messages_source=messages_source,
    )

    assert request.page_size == 10
    assert request.messages_source == messages_source


@pytest.mark.parametrize(
    "view",
    ["WITH_METADATA", "WITHOUT_METADATA"],
)
def test_list_messages_request_expects_accepts_view(view):
    """Test that the model accepts view with different values."""
    request = ListMessagesRequest(page_size=10, view=view)

    assert request.view == view


@pytest.mark.parametrize(
    "channel",
    ["WHATSAPP", "RCS", "SMS", "MESSENGER"],
)
def test_list_messages_request_expects_accepts_channel(channel):
    """Test that the model accepts channel with different values."""
    request = ListMessagesRequest(page_size=10, channel=channel)

    assert request.channel == channel


@pytest.mark.parametrize(
    "direction",
    ["TO_APP", "TO_CONTACT"],
)
def test_list_messages_request_expects_accepts_direction(direction):
    """Test that the model accepts direction with different values."""
    request = ListMessagesRequest(page_size=10, direction=direction)

    assert request.direction == direction


def test_list_messages_request_expects_model_dump_excludes_none():
    """Test that model_dump with exclude_none=True omits None values."""
    request = ListMessagesRequest(page_size=10)
    dumped = request.model_dump(exclude_none=True, by_alias=True)

    assert "page_size" in dumped
    assert dumped["page_size"] == 10
