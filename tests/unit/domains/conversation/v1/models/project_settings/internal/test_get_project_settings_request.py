from sinch.domains.conversation.models.v1.project_settings.internal.get_project_settings_request import (
    GetProjectSettingsRequest,
)


def test_get_project_settings_request_expects_parsed_input():
    """Test that the model carries no fields."""
    model = GetProjectSettingsRequest()

    assert model.model_dump(by_alias=True, exclude_none=True) == {}
