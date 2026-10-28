from sinch.domains.conversation.models.v1.project_settings.shared.contact_settings import (
    ContactSettings,
)
from sinch.domains.conversation.models.v1.project_settings.shared.project_settings import (
    ProjectSettings,
)


def test_project_settings_expects_parsed_input():
    """Test that the model correctly parses a full valid input."""
    model = ProjectSettings(
        contact_settings={"unified_contact_id_enabled": False}
    )

    assert isinstance(model.contact_settings, ContactSettings)
    assert model.contact_settings.unified_contact_id_enabled is False

    # Asserting aliases on dump by alias
    alias_dump = model.model_dump(by_alias=True, exclude_none=True)
    assert alias_dump == {
        "contact_settings": {"unified_contact_id_enabled": False}
    }


def test_project_settings_expects_all_optionals_default_to_none():
    """Test that omitted optional fields default to None."""
    model = ProjectSettings()

    assert model.contact_settings is None
