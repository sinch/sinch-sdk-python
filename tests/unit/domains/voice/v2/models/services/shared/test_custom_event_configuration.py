from sinch.domains.voice.models.v2.services.shared.event_destination_configuration import (
    EventDestinationConfiguration,
)


def test_custom_event_configuration_expects_parsed_input():
    """Test that the model correctly parses a full valid input."""
    model = EventDestinationConfiguration(
        url="https://example.com/event_destination",
        fallback_url="https://example.com/fallback",
    )

    assert model.url == "https://example.com/event_destination"
    assert model.fallback_url == "https://example.com/fallback"

    # Asserting aliases on dump by alias
    alias_dump = model.model_dump(by_alias=True, exclude_none=True)
    assert alias_dump["url"] == "https://example.com/event_destination"
    assert alias_dump["fallbackUrl"] == "https://example.com/fallback"


def test_custom_event_configuration_expects_all_optionals_default_to_none():
    """Test that all optional fields default to None."""
    model = EventDestinationConfiguration(url="https://example.com/event_destination")

    assert model.fallback_url is None
