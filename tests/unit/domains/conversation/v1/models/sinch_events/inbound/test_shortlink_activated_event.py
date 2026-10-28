from sinch.domains.conversation.models.v1.sinch_events.inbound.shortlink_activated_event import (
    ShortLinkActivatedEvent,
)


def test_shortlink_activated_event_expects_parsed_input():
    """Test that the model correctly parses a full valid input."""
    model = ShortLinkActivatedEvent(
        payload="postback-1",
        title="Open",
        ref="campaign",
        source="SHORTLINK",
        type="OPEN_THREAD",
        existing_thread=True,
    )

    assert model.payload == "postback-1"
    assert model.title == "Open"
    assert model.ref == "campaign"
    assert model.source == "SHORTLINK"
    assert model.type == "OPEN_THREAD"
    assert model.existing_thread is True

    # Asserting aliases on dump by alias
    alias_dump = model.model_dump(mode="json", by_alias=True, exclude_none=True)
    assert alias_dump["payload"] == "postback-1"
    assert alias_dump["title"] == "Open"
    assert alias_dump["ref"] == "campaign"
    assert alias_dump["source"] == "SHORTLINK"
    assert alias_dump["type"] == "OPEN_THREAD"
    assert alias_dump["existing_thread"] is True


def test_shortlink_activated_event_expects_all_optionals_default_to_none():
    """Test that all optional fields default to None."""
    model = ShortLinkActivatedEvent()

    assert model.payload is None
    assert model.title is None
    assert model.ref is None
    assert model.source is None
    assert model.type is None
    assert model.existing_thread is None
