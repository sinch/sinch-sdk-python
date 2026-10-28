from sinch.domains.conversation.models.v1.project_settings.shared.contact_settings import (
    ContactSettings,
)


def test_contact_settings_expects_parsed_input():
    """Test that the model correctly parses a full valid input."""
    model = ContactSettings(unified_contact_id_enabled=True)

    assert model.unified_contact_id_enabled is True

    # Asserting aliases on dump by alias
    alias_dump = model.model_dump(by_alias=True, exclude_none=True)
    assert alias_dump == {"unified_contact_id_enabled": True}


def test_contact_settings_expects_all_optionals_default_to_none():
    """Test that omitted optional fields default to None."""
    model = ContactSettings()

    assert model.unified_contact_id_enabled is None
