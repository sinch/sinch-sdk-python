from sinch.domains.conversation.models.v1.apps.internal.list_apps_response import (
    ListAppsResponse,
)
from sinch.domains.conversation.models.v1.apps.response.app_response import (
    AppResponse,
)


def test_list_apps_response_expects_apps_defaults_to_none():
    """Test that the apps field defaults to None."""
    model = ListAppsResponse()

    assert model.apps is None


def test_list_apps_response_expects_content_returns_empty_list_when_none():
    """Test that the content property returns an empty list when apps is None."""
    model = ListAppsResponse()

    assert model.content == []


def test_list_apps_response_expects_content_returns_apps_when_populated():
    """Test that the content property returns the parsed apps when populated."""
    model = ListAppsResponse(
        apps=[
            {"id": "app-1", "display_name": "First"},
            {"id": "app-2", "display_name": "Second"},
        ]
    )

    assert len(model.content) == 2
    assert all(isinstance(app, AppResponse) for app in model.content)
    assert model.content[0].id == "app-1"
    assert model.content[1].display_name == "Second"
