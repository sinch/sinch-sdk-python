from sinch.domains.voice.helpers.v2.svaml import CustomEvents


def test_trigger_expects_all_fields():
    """Test that trigger builds the command with all its fields."""
    command = CustomEvents.trigger(
        "menu.selection",
        "https://example.com/events",
        fallback_url="https://example.com/fallback",
    )

    assert command == {
        "command": "customEvent",
        "custom_event_name": "menu.selection",
        "url": "https://example.com/events",
        "fallback_url": "https://example.com/fallback",
    }


def test_trigger_expects_optionals_omitted_when_not_provided():
    """Test that omitted optionals are not included."""
    assert CustomEvents.trigger("done", "https://example.com/events") == {
        "command": "customEvent",
        "custom_event_name": "done",
        "url": "https://example.com/events",
    }
