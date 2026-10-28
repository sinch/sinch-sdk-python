from sinch.domains.conversation.models.v1.sinch_events.channel.channel_event_details import (
    ChannelEventDetails,
)
from sinch.domains.conversation.models.v1.sinch_events.channel.channel_event_notification import (
    ChannelEventNotification,
)


def test_channel_event_notification_expects_parsed_input():
    """Test that the model correctly parses a full valid input."""
    model = ChannelEventNotification(
        channel_event={"channel": "WHATSAPP", "event_type": "QUALITY_RATING_UPDATE"}
    )

    assert isinstance(model.channel_event, ChannelEventDetails)
    assert model.channel_event.channel == "WHATSAPP"
    assert model.channel_event.event_type == "QUALITY_RATING_UPDATE"

    # Asserting aliases on dump by alias
    alias_dump = model.model_dump(mode="json", by_alias=True, exclude_none=True)
    assert alias_dump["channel_event"] == {
        "channel": "WHATSAPP",
        "event_type": "QUALITY_RATING_UPDATE",
    }


def test_channel_event_notification_expects_all_optionals_default_to_none():
    """Test that all optional fields default to None."""
    model = ChannelEventNotification()

    assert model.channel_event is None
