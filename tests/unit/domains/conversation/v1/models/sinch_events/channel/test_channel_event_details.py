from sinch.domains.conversation.models.v1.sinch_events.channel.channel_event_details import (
    ChannelEventDetails,
)


def test_channel_event_details_expects_parsed_input():
    """Test that the model correctly parses a full valid input."""
    model = ChannelEventDetails(
        channel="WHATSAPP",
        event_type="QUALITY_RATING_UPDATE",
        additional_data={"current_limit": "TIER_1K", "quality_rating": "GREEN"},
    )

    assert model.channel == "WHATSAPP"
    assert model.event_type == "QUALITY_RATING_UPDATE"
    assert model.additional_data == {
        "current_limit": "TIER_1K",
        "quality_rating": "GREEN",
    }

    # Asserting aliases on dump by alias
    alias_dump = model.model_dump(mode="json", by_alias=True, exclude_none=True)
    assert alias_dump["channel"] == "WHATSAPP"
    assert alias_dump["event_type"] == "QUALITY_RATING_UPDATE"
    assert alias_dump["additional_data"] == {
        "current_limit": "TIER_1K",
        "quality_rating": "GREEN",
    }


def test_channel_event_details_expects_all_optionals_default_to_none():
    """Test that all optional fields default to None."""
    model = ChannelEventDetails()

    assert model.channel is None
    assert model.event_type is None
    assert model.additional_data is None
