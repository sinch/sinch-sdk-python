from datetime import datetime, timezone

from sinch.domains.conversation.models.v1.events.internal.list_events_response import (
    ListEventsResponse,
)
from sinch.domains.conversation.models.v1.events.response.conversation_event_response import (
    ConversationEventResponse,
)


def test_list_events_response_expects_parsed_input():
    """Test that the model correctly parses a full valid input."""
    model = ListEventsResponse(
        events=[
            {
                "id": "01W4FFL35P4NC4K35EVENT0001",
                "direction": "TO_CONTACT",
                "app_event": {"composing_event": {}},
                "conversation_id": "01W4FFL35P4NC4K35CONVERS001",
                "contact_id": "01W4FFL35P4NC4K35CONTACT001",
                "channel_identity": {
                    "channel": "SMS",
                    "identity": "46700000000",
                },
                "accept_time": "2026-10-09T10:00:00Z",
                "processing_mode": "CONVERSATION",
            }
        ],
        next_page_token="token",
    )

    assert len(model.events) == 1
    event = model.events[0]
    assert isinstance(event, ConversationEventResponse)
    assert event.id == "01W4FFL35P4NC4K35EVENT0001"
    assert event.direction == "TO_CONTACT"
    assert event.app_event.composing_event == {}
    assert event.conversation_id == "01W4FFL35P4NC4K35CONVERS001"
    assert event.contact_id == "01W4FFL35P4NC4K35CONTACT001"
    assert event.channel_identity.channel == "SMS"
    assert event.channel_identity.identity == "46700000000"
    assert event.accept_time == datetime(
        2026, 10, 9, 10, 0, 0, tzinfo=timezone.utc
    )
    assert event.processing_mode == "CONVERSATION"
    assert model.next_page_token == "token"
    assert model.content == model.events

    # Asserting aliases on dump by alias
    alias_dump = model.model_dump(
        mode="json", by_alias=True, exclude_none=True
    )
    assert alias_dump["events"] == [
        {
            "id": "01W4FFL35P4NC4K35EVENT0001",
            "direction": "TO_CONTACT",
            "app_event": {"composing_event": {}},
            "conversation_id": "01W4FFL35P4NC4K35CONVERS001",
            "contact_id": "01W4FFL35P4NC4K35CONTACT001",
            "channel_identity": {"channel": "SMS", "identity": "46700000000"},
            "accept_time": "2026-10-09T10:00:00Z",
            "processing_mode": "CONVERSATION",
        }
    ]
    assert alias_dump["next_page_token"] == "token"


def test_list_events_response_expects_all_optionals_default_to_none():
    """Test that all optional fields default to None."""
    model = ListEventsResponse()

    assert model.events is None
    assert model.next_page_token is None


def test_list_events_response_expects_content_empty_when_events_is_none():
    """Test that content returns an empty list when events is None."""
    assert ListEventsResponse().content == []
