from sinch.domains.conversation.models.v1.project_settings.internal.delete_project_settings_request import (
    DeleteProjectSettingsRequest,
)


def test_delete_project_settings_request_expects_parsed_input():
    """Test that the model carries no fields."""
    model = DeleteProjectSettingsRequest()

    assert model.model_dump(by_alias=True, exclude_none=True) == {}
