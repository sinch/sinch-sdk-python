from sinch.domains.conversation.models.v1.apps.shared.event_destination_settings import (
    EventDestinationSettings,
)


def test_event_destination_settings_expects_parsed_input():
    """Test that the model correctly parses a full valid input."""
    model = EventDestinationSettings(secret_for_overridden_target="secret")

    assert model.secret_for_overridden_target == "secret"


def test_event_destination_settings_expects_defaults_to_none():
    """Test that the optional field defaults to None."""
    model = EventDestinationSettings()

    assert model.secret_for_overridden_target is None


def test_event_destination_settings_expects_accepts_alias():
    """Test that the field can be populated by its secret_for_overridden_callback_urls alias."""
    model = EventDestinationSettings(
        secret_for_overridden_callback_urls="secret-via-alias"
    )

    assert model.secret_for_overridden_target == "secret-via-alias"


def test_event_destination_settings_expects_dump_uses_alias():
    """Test that model_dump(by_alias=True) emits the wire alias."""
    model = EventDestinationSettings(secret_for_overridden_target="secret")

    dumped = model.model_dump(by_alias=True, exclude_none=True)

    assert dumped == {"secret_for_overridden_callback_urls": "secret"}
