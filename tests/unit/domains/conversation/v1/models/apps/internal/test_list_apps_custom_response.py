"""Unit tests for ListAppsCustomResponse."""
from sinch.domains.conversation.models.v1.apps.internal.list_apps_custom_response import (
    ListAppsCustomResponse,
)
from sinch.domains.conversation.models.v1.apps.response.app_custom_response import (
    AppCustomResponse,
)


def test_list_apps_custom_response_expects_apps_default_none():
    """When apps is absent, the field is None and content is an empty list."""
    model = ListAppsCustomResponse.model_validate({})

    assert model.apps is None
    assert model.content == []


def test_list_apps_custom_response_expects_multiple_apps_mapped():
    """Each app entry is validated as AppCustomResponse with channel_credentials mapped."""
    model = ListAppsCustomResponse.model_validate(
        {
            "apps": [
                {
                    "id": "app-1",
                    "display_name": "First",
                    "channel_credentials": [
                        {
                            "channel": "SMS",
                            "static_bearer": {
                                "claimed_identity": "sp-id",
                                "token": "tok-1",
                            },
                        }
                    ],
                },
                {
                    "id": "app-2",
                    "display_name": "Second",
                    "channel_credentials": [
                        {
                            "channel": "MESSENGER",
                            "static_token": {"token": "tok-2"},
                        }
                    ],
                },
            ]
        }
    )

    assert len(model.content) == 2
    first, second = model.content
    assert isinstance(first, AppCustomResponse)
    assert isinstance(second, AppCustomResponse)
    assert first.id == "app-1"
    assert first.channel_credentials.sms.token == "tok-1"
    assert second.channel_credentials.messenger.token == "tok-2"


def test_list_apps_custom_response_content_returns_apps():
    """content returns the underlying apps list unchanged."""
    model = ListAppsCustomResponse.model_validate(
        {"apps": [{"id": "app-1", "display_name": "First"}]}
    )

    assert model.content is model.apps
