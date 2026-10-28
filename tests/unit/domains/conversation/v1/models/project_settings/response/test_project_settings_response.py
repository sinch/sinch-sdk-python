from sinch.domains.conversation.models.v1.project_settings.response.project_settings_response import (
    ProjectSettingsResponse,
)
from sinch.domains.conversation.models.v1.project_settings.shared.project_settings import (
    ProjectSettings,
)


def test_project_settings_response_expects_parsed_input():
    """Test that the model correctly parses a full valid input."""
    model = ProjectSettingsResponse(
        project_id="123coffee-dada-beef-cafe-baadc0de5678",
        settings={"contact_settings": {"unified_contact_id_enabled": True}},
    )

    assert model.project_id == "123coffee-dada-beef-cafe-baadc0de5678"
    assert isinstance(model.settings, ProjectSettings)
    assert model.settings.contact_settings.unified_contact_id_enabled is True

    # Asserting aliases on dump by alias
    alias_dump = model.model_dump(by_alias=True, exclude_none=True)
    assert alias_dump == {
        "project_id": "123coffee-dada-beef-cafe-baadc0de5678",
        "settings": {"contact_settings": {"unified_contact_id_enabled": True}},
    }


def test_project_settings_response_expects_all_optionals_default_to_none():
    """Test that omitted optional fields default to None."""
    model = ProjectSettingsResponse()

    assert model.project_id is None
    assert model.settings is None
