from sinch.domains.conversation.models.app.responses import UpdateConversationAppResponse


def test_update_conversation_app(sinch_client_sync):
    list_apps_response = sinch_client_sync.conversation.app.list()

    update_app_response = sinch_client_sync.conversation.app.update(
        app_id=list_apps_response.apps[0].id,
        display_name="Test2222"
    )
    assert isinstance(update_app_response, UpdateConversationAppResponse)


async def test_update_conversation_app_async(sinch_client_sync, sinch_client_async):
    list_apps_response = sinch_client_sync.conversation.app.list()

    update_app_response = await sinch_client_async.conversation.app.update(
        app_id=list_apps_response.apps[0].id,
        display_name="Test2222"
    )
    assert isinstance(update_app_response, UpdateConversationAppResponse)
